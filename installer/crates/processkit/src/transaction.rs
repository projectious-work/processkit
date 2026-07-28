//! Transaction staging, journaling, execution, and rollback.

use super::{create_private_dir, has_symlink_ancestor, write_json_atomic};
use crate::contract::API_VERSION;
use crate::filesystem::{digest, ensure_non_symlink_directory, safe_relative, valid_sha256};
use crate::state::InstallationState;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
pub(super) struct Journal {
    pub(super) api_version: String,
    pub(super) transaction_id: String,
    pub(super) operation: String,
    pub(super) phase: String,
    pub(super) old_state_sha256: Option<String>,
    pub(super) new_state_sha256: Option<String>,
    pub(super) actions: Vec<TransactionAction>,
}
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
pub(super) struct TransactionAction {
    pub(super) kind: String,
    #[serde(rename = "path")]
    pub(super) target: String,
    pub(super) old_sha256: Option<String>,
    pub(super) new_sha256: Option<String>,
    pub(super) staged_path: Option<String>,
    pub(super) backup_path: Option<String>,
    pub(super) created_parents: Vec<String>,
    pub(super) ownership: String,
    pub(super) applied: bool,
}

pub(super) struct PendingAction {
    pub(super) action: TransactionAction,
    pub(super) source: Option<PathBuf>,
    pub(super) content: Option<Vec<u8>>,
}

fn transaction_id(operation: &str) -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    let nanos = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_nanos();
    format!("{operation}-{}-{nanos}", std::process::id())
}

pub(super) fn execute_transaction(
    root: &Path,
    operation: &str,
    mut pending: Vec<PendingAction>,
    new_state: Option<&InstallationState>,
) -> Result<(), String> {
    let state_dir = root.join(".processkit");
    let transaction = transaction_id(operation);
    let transactions = state_dir.join("transactions");
    if transactions.exists() {
        ensure_non_symlink_directory(&transactions, "transaction journal directory")?;
    } else {
        create_private_dir(&transactions)?;
    }
    let staging_root = state_dir.join(".staging");
    if staging_root.exists() {
        ensure_non_symlink_directory(&staging_root, "transaction staging directory")?;
    } else {
        create_private_dir(&staging_root)?;
    }
    let staging = staging_root.join(&transaction);
    let new_dir = staging.join("new");
    let backup_dir = staging.join("backup");
    create_private_dir(&new_dir)?;
    create_private_dir(&backup_dir)?;

    let state_path = state_dir.join("state.json");
    let old_state_sha256 = state_path
        .is_file()
        .then(|| digest(&state_path))
        .transpose()?;
    let staged_state = staging.join("state.json");
    let new_state_sha256 = if let Some(state) = new_state {
        write_json_atomic(&staged_state, state)?;
        Some(digest(&staged_state)?)
    } else {
        None
    };

    for item in &mut pending {
        if !safe_relative(&item.action.target) || has_symlink_ancestor(root, &item.action.target)? {
            return Err(format!("unsafe transaction target: {}", item.action.target));
        }
        if item.source.is_some() || item.content.is_some() {
            let staged = new_dir.join(&item.action.target);
            if let Some(parent) = staged.parent() {
                fs::create_dir_all(parent).map_err(|error| error.to_string())?;
            }
            if let Some(source) = &item.source {
                fs::copy(source, &staged).map_err(|error| error.to_string())?;
            } else {
                fs::write(
                    &staged,
                    item.content
                        .as_ref()
                        .ok_or("transaction content is missing")?,
                )
                .map_err(|error| error.to_string())?;
            }
            let expected = item
                .action
                .new_sha256
                .as_ref()
                .ok_or("transaction write action lacks a new digest")?;
            if digest(&staged)? != *expected {
                return Err(format!("staged digest mismatch: {}", item.action.target));
            }
            item.action.staged_path = Some(
                staged
                    .strip_prefix(root)
                    .map_err(|_| "staged path escaped target root")?
                    .to_string_lossy()
                    .replace('\\', "/"),
            );
        }
        if item.action.old_sha256.is_some() {
            let backup = backup_dir.join(&item.action.target);
            item.action.backup_path = Some(
                backup
                    .strip_prefix(root)
                    .map_err(|_| "backup path escaped target root")?
                    .to_string_lossy()
                    .replace('\\', "/"),
            );
        }
    }

    let journal_path = state_dir
        .join("transactions")
        .join(format!("{transaction}.json"));
    let mut journal = Journal {
        api_version: API_VERSION.into(),
        transaction_id: transaction.clone(),
        operation: operation.into(),
        phase: "prepared".into(),
        old_state_sha256,
        new_state_sha256,
        actions: pending.into_iter().map(|item| item.action).collect(),
    };
    write_json_atomic(&journal_path, &journal)?;

    let apply_result = (|| -> Result<(), String> {
        journal.phase = "applying".into();
        write_json_atomic(&journal_path, &journal)?;
        for index in 0..journal.actions.len() {
            let action = &journal.actions[index];
            let target = root.join(&action.target);
            if let Some(expected) = &action.old_sha256 {
                if !target.is_file() || digest(&target)? != *expected {
                    return Err(format!(
                        "transaction target changed before apply: {}",
                        action.target
                    ));
                }
                let backup = root.join(
                    action
                        .backup_path
                        .as_ref()
                        .ok_or("transaction backup path is missing")?,
                );
                if let Some(parent) = backup.parent() {
                    fs::create_dir_all(parent).map_err(|error| error.to_string())?;
                }
                fs::rename(&target, backup).map_err(|error| error.to_string())?;
            } else if target.exists() {
                return Err(format!(
                    "transaction create target appeared: {}",
                    action.target
                ));
            }
            if action.kind != "remove" {
                let staged = root.join(
                    action
                        .staged_path
                        .as_ref()
                        .ok_or("transaction staged path is missing")?,
                );
                if let Some(parent) = target.parent() {
                    fs::create_dir_all(parent).map_err(|error| error.to_string())?;
                }
                fs::rename(staged, &target).map_err(|error| error.to_string())?;
            }
            if std::env::var("PROCESSKIT_INSTALLER_FAIL_AFTER_ACTION")
                .ok()
                .and_then(|value| value.parse::<usize>().ok())
                == Some(index)
            {
                std::process::exit(75);
            }
            journal.actions[index].applied = true;
            write_json_atomic(&journal_path, &journal)?;
        }
        journal.phase = "state-written".into();
        if new_state.is_some() {
            fs::rename(&staged_state, &state_path).map_err(|error| error.to_string())?;
        } else if state_path.exists() {
            fs::remove_file(&state_path).map_err(|error| error.to_string())?;
        }
        write_json_atomic(&journal_path, &journal)?;
        journal.phase = "committed".into();
        write_json_atomic(&journal_path, &journal)
    })();

    if let Err(error) = apply_result {
        rollback_journal(root, &journal)?;
        let _ = fs::remove_file(&journal_path);
        let _ = fs::remove_dir_all(&staging);
        return Err(error);
    }
    fs::remove_file(&journal_path).map_err(|error| error.to_string())?;
    fs::remove_dir_all(&staging).map_err(|error| error.to_string())?;
    Ok(())
}

pub(super) fn rollback_journal(root: &Path, journal: &Journal) -> Result<(), String> {
    for action in journal.actions.iter().rev() {
        let target = root.join(&action.target);
        let backup = action.backup_path.as_ref().map(|path| root.join(path));
        let was_applied = action.applied
            || backup.as_ref().is_some_and(|path| path.exists())
            || action.new_sha256.as_ref().is_some_and(|expected| {
                target.is_file() && digest(&target).ok().as_ref() == Some(expected)
            });
        if !was_applied {
            continue;
        }
        if target.exists() {
            if action.kind == "remove" {
                return Err(format!(
                    "manual recovery required: removed target reappeared: {}",
                    action.target
                ));
            }
            let expected = action
                .new_sha256
                .as_ref()
                .ok_or("manual recovery required: missing new digest")?;
            if !target.is_file() || digest(&target)? != *expected {
                return Err(format!(
                    "manual recovery required: applied target changed: {}",
                    action.target
                ));
            }
            fs::remove_file(&target).map_err(|error| error.to_string())?;
        }
        if let Some(backup) = backup {
            if backup.exists() {
                if let Some(parent) = target.parent() {
                    fs::create_dir_all(parent).map_err(|error| error.to_string())?;
                }
                fs::rename(backup, target).map_err(|error| error.to_string())?;
            }
        }
    }
    Ok(())
}

pub(super) fn validate_recovery_journal(root: &Path, journal: &Journal) -> Result<(), String> {
    if !matches!(
        journal.operation.as_str(),
        "install" | "update" | "uninstall"
    ) || !matches!(
        journal.phase.as_str(),
        "prepared" | "applying" | "state-written" | "committed"
    ) {
        return Err("transaction journal has invalid lifecycle metadata".into());
    }
    for digest_value in [
        journal.old_state_sha256.as_deref(),
        journal.new_state_sha256.as_deref(),
    ]
    .into_iter()
    .flatten()
    {
        if !valid_sha256(digest_value) {
            return Err("transaction journal has an invalid state digest".into());
        }
    }
    let staging_prefix = format!(".processkit/.staging/{}", journal.transaction_id);
    for action in &journal.actions {
        if !safe_relative(&action.target)
            || has_symlink_ancestor(root, &action.target)?
            || !action.created_parents.is_empty()
            || !matches!(
                action.ownership.as_str(),
                "managed-three-way" | "managed-keys" | "shared"
            )
        {
            return Err("transaction journal has an unsafe action".into());
        }
        for digest_value in [action.old_sha256.as_deref(), action.new_sha256.as_deref()]
            .into_iter()
            .flatten()
        {
            if !valid_sha256(digest_value) {
                return Err("transaction journal has an invalid action digest".into());
            }
        }
        let staged = format!("{staging_prefix}/new/{}", action.target);
        let backup = format!("{staging_prefix}/backup/{}", action.target);
        let shape_is_valid = match action.kind.as_str() {
            "create" => {
                action.old_sha256.is_none()
                    && action.new_sha256.is_some()
                    && (action.staged_path.as_deref() == Some(staged.as_str())
                        || (action.applied && action.staged_path.is_none()))
                    && action.backup_path.is_none()
            }
            "replace" => {
                action.old_sha256.is_some()
                    && action.new_sha256.is_some()
                    && action.staged_path.as_deref() == Some(staged.as_str())
                    && action.backup_path.as_deref() == Some(backup.as_str())
            }
            "remove" => {
                action.old_sha256.is_some()
                    && action.new_sha256.is_none()
                    && action.staged_path.is_none()
                    && action.backup_path.as_deref() == Some(backup.as_str())
            }
            _ => false,
        };
        if !shape_is_valid {
            return Err("transaction journal has an invalid action shape".into());
        }
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn journal_with(action: TransactionAction) -> Journal {
        let digest = "a".repeat(64);
        Journal {
            api_version: API_VERSION.into(),
            transaction_id: "update-1".into(),
            operation: "update".into(),
            phase: "applying".into(),
            old_state_sha256: Some(digest.clone()),
            new_state_sha256: Some(digest),
            actions: vec![action],
        }
    }

    #[test]
    fn recovery_rejects_journal_path_traversal() {
        let root = tempfile::tempdir().unwrap();
        let digest = "a".repeat(64);
        let journal = journal_with(TransactionAction {
            kind: "replace".into(),
            target: "../outside".into(),
            old_sha256: Some(digest.clone()),
            new_sha256: Some(digest),
            staged_path: Some(".processkit/.staging/update-1/new/../outside".into()),
            backup_path: Some(".processkit/.staging/update-1/backup/../outside".into()),
            created_parents: Vec::new(),
            ownership: "managed-three-way".into(),
            applied: true,
        });
        assert_eq!(
            validate_recovery_journal(root.path(), &journal),
            Err("transaction journal has an unsafe action".into())
        );
    }

    #[test]
    fn recovery_rejects_forged_staging_paths() {
        let root = tempfile::tempdir().unwrap();
        let digest = "a".repeat(64);
        let journal = journal_with(TransactionAction {
            kind: "replace".into(),
            target: "payload/file".into(),
            old_sha256: Some(digest.clone()),
            new_sha256: Some(digest),
            staged_path: Some(".processkit/.staging/update-1/new/../outside".into()),
            backup_path: Some(".processkit/.staging/update-1/backup/payload/file".into()),
            created_parents: Vec::new(),
            ownership: "managed-three-way".into(),
            applied: true,
        });
        assert_eq!(
            validate_recovery_journal(root.path(), &journal),
            Err("transaction journal has an invalid action shape".into())
        );
    }

    #[cfg(unix)]
    #[test]
    fn execution_rejects_symlinked_staging_directory() {
        use std::os::unix::fs::symlink;

        let root = tempfile::tempdir().unwrap();
        let outside = tempfile::tempdir().unwrap();
        let state_dir = root.path().join(".processkit");
        fs::create_dir_all(state_dir.join("transactions")).unwrap();
        symlink(outside.path(), state_dir.join(".staging")).unwrap();

        assert_eq!(
            execute_transaction(root.path(), "update", Vec::new(), None),
            Err("transaction staging directory must be a non-symlink directory".into())
        );
    }
}
