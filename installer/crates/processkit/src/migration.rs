//! Evidence-driven planning for legacy project corpus migration.

use crate::filesystem::{digest, safe_relative};
use crate::transaction::{PendingAction, TransactionAction};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::BTreeMap;
use std::fs;
use std::path::Path;

const ENTITY_ROOTS: &[(&str, &str)] = &[
    ("context/actors", "Actor"),
    ("context/artifacts", "Artifact"),
    ("context/bindings", "Binding"),
    ("context/decisions", "DecisionRecord"),
    ("context/discussions", "Discussion"),
    ("context/gates", "Gate"),
    ("context/logs", "LogEntry"),
    ("context/migrations", "Migration"),
    ("context/notes", "Note"),
    ("context/roles", "Role"),
    ("context/scopes", "Scope"),
    ("context/team-members", "TeamMember"),
    ("context/workitems", "WorkItem"),
];

#[derive(Clone, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
pub(super) struct CorpusPlan {
    pub(super) status: String,
    pub(super) entries: Vec<CorpusEntry>,
    excluded_roots: Vec<String>,
    errors: Vec<CorpusFinding>,
    summary: CorpusSummary,
}

#[derive(Clone, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
pub(super) struct CorpusEntry {
    path: String,
    kind: String,
    id: String,
    sha256: String,
    disposition: String,
    field_loss: Vec<String>,
}

#[derive(Clone, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
struct CorpusFinding {
    path: String,
    code: String,
    message: String,
    remediation: String,
}

#[derive(Clone, Default, Deserialize, Serialize)]
#[serde(rename_all = "camelCase")]
struct CorpusSummary {
    copy_compatible: usize,
    preserve_immutable: usize,
    blocked: usize,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
struct OwnershipBaseline {
    release_version: String,
    files: BTreeMap<String, String>,
}

pub(super) fn plan_v0_corpus(source: &Path, baseline_path: &Path) -> Result<CorpusPlan, String> {
    let baseline: OwnershipBaseline = serde_json::from_slice(
        &fs::read(baseline_path).map_err(|error| format!("ownership baseline: {error}"))?,
    )
    .map_err(|error| format!("ownership baseline JSON: {error}"))?;
    if baseline.release_version.is_empty()
        || baseline
            .files
            .iter()
            .any(|(path, digest)| !safe_relative(path) || digest.len() != 64)
    {
        return Err("ownership baseline is invalid".into());
    }
    let mut entries = Vec::new();
    let mut errors = Vec::new();
    for (relative_root, expected_kind) in ENTITY_ROOTS {
        let root = source.join(relative_root);
        if !root.exists() {
            continue;
        }
        let root_metadata = root
            .symlink_metadata()
            .map_err(|error| format!("legacy corpus root metadata: {error}"))?;
        if root_metadata.file_type().is_symlink() {
            errors.push(finding(
                relative_root,
                "unsafe-symlink",
                "entity roots must not be symlinks",
            ));
            continue;
        }
        walk_entity_root(
            source,
            &root,
            expected_kind,
            &baseline.files,
            &mut entries,
            &mut errors,
        )?;
    }
    entries.sort_by(|left, right| left.path.cmp(&right.path));
    errors.sort_by(|left, right| left.path.cmp(&right.path));
    let summary = CorpusSummary {
        copy_compatible: entries
            .iter()
            .filter(|entry| entry.disposition == "copy-compatible")
            .count(),
        preserve_immutable: entries
            .iter()
            .filter(|entry| entry.disposition == "preserve-immutable")
            .count(),
        blocked: errors.len(),
    };
    Ok(CorpusPlan {
        status: if errors.is_empty() {
            "planned".into()
        } else {
            "blocked".into()
        },
        entries,
        excluded_roots: Vec::new(),
        errors,
        summary,
    })
}

impl CorpusPlan {
    pub(super) fn sha256(&self) -> Result<String, String> {
        let bytes = serde_json::to_vec(self)
            .map_err(|error| format!("serialize legacy corpus plan: {error}"))?;
        Ok(format!("{:x}", Sha256::digest(bytes)))
    }

    pub(super) fn entry_count(&self) -> usize {
        self.entries.len()
    }

    pub(super) fn pending_actions(
        &self,
        source: &Path,
        target: &Path,
    ) -> Result<Vec<PendingAction>, String> {
        let mut pending = Vec::with_capacity(self.entries.len());
        for entry in &self.entries {
            let destination = target.join(&entry.path);
            if destination.exists() {
                return Err(format!(
                    "migration target collides with installed content: {}",
                    entry.path
                ));
            }
            pending.push(PendingAction {
                action: TransactionAction {
                    kind: "create".into(),
                    target: entry.path.clone(),
                    old_sha256: None,
                    new_sha256: Some(entry.sha256.clone()),
                    staged_path: None,
                    backup_path: None,
                    created_parents: Vec::new(),
                    ownership: "shared".into(),
                    applied: false,
                },
                source: Some(source.join(&entry.path)),
                content: None,
            });
        }
        Ok(pending)
    }

    pub(super) fn verify_applied(&self, root: &Path) -> Result<Vec<serde_json::Value>, String> {
        let mut findings = Vec::new();
        for entry in &self.entries {
            if !safe_relative(&entry.path) {
                return Err("migration evidence contains an unsafe path".into());
            }
            let target = root.join(&entry.path);
            let metadata = match target.symlink_metadata() {
                Ok(metadata) => metadata,
                Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
                    findings.push(serde_json::json!({
                        "code": "missing-migrated-path",
                        "path": entry.path,
                        "message": "migrated entity is missing",
                    }));
                    continue;
                }
                Err(error) => return Err(format!("migrated path metadata: {error}")),
            };
            if metadata.file_type().is_symlink()
                || !metadata.is_file()
                || crate::has_symlink_ancestor(root, &entry.path)?
            {
                findings.push(serde_json::json!({
                    "code": "unsafe-migrated-path",
                    "path": entry.path,
                    "message": "migrated entity or ancestor is not a regular path",
                }));
                continue;
            }
            let actual = digest(&target)?;
            if actual != entry.sha256 {
                findings.push(serde_json::json!({
                    "code": "migrated-path-drift",
                    "path": entry.path,
                    "message": "migrated entity digest differs from migration evidence",
                    "expectedSha256": entry.sha256,
                    "actualSha256": actual,
                }));
            }
        }
        Ok(findings)
    }
}

fn walk_entity_root(
    source: &Path,
    directory: &Path,
    expected_kind: &str,
    baseline: &BTreeMap<String, String>,
    entries: &mut Vec<CorpusEntry>,
    errors: &mut Vec<CorpusFinding>,
) -> Result<(), String> {
    let mut children = fs::read_dir(directory)
        .map_err(|error| format!("read legacy corpus directory: {error}"))?
        .collect::<Result<Vec<_>, _>>()
        .map_err(|error| format!("read legacy corpus entry: {error}"))?;
    children.sort_by_key(|entry| entry.file_name());
    for child in children {
        let path = child.path();
        let relative = relative_path(source, &path)?;
        let file_type = child
            .file_type()
            .map_err(|error| format!("legacy corpus file type: {error}"))?;
        if file_type.is_symlink() {
            errors.push(finding(
                &relative,
                "unsafe-symlink",
                "entity paths must not be symlinks",
            ));
            continue;
        }
        let metadata = child
            .metadata()
            .map_err(|error| format!("legacy corpus metadata: {error}"))?;
        if metadata.is_dir() {
            walk_entity_root(source, &path, expected_kind, baseline, entries, errors)?;
        } else if metadata.is_file()
            && path.extension().and_then(|extension| extension.to_str()) == Some("md")
            && (expected_kind != "TeamMember"
                || path.file_name().and_then(|name| name.to_str()) == Some("team-member.md"))
        {
            let actual = digest(&path)?;
            if let Some(expected) = baseline.get(&relative) {
                if expected == &actual {
                    continue;
                }
                errors.push(finding(
                    &relative,
                    "modified-product-owned-path",
                    "path differs from the exact-release ownership baseline",
                ));
                continue;
            }
            inspect_entity(&path, &relative, expected_kind, entries, errors)?;
        }
    }
    Ok(())
}

fn inspect_entity(
    path: &Path,
    relative: &str,
    expected_kind: &str,
    entries: &mut Vec<CorpusEntry>,
    errors: &mut Vec<CorpusFinding>,
) -> Result<(), String> {
    let bytes = fs::read(path).map_err(|error| format!("read legacy entity: {error}"))?;
    let frontmatter = match yaml_frontmatter(&bytes) {
        Ok(frontmatter) => frontmatter,
        Err(message) => {
            errors.push(finding(relative, "invalid-frontmatter", &message));
            return Ok(());
        }
    };
    let value: serde_yaml::Value = match serde_yaml::from_slice(frontmatter) {
        Ok(value) => value,
        Err(error) => {
            errors.push(finding(
                relative,
                "invalid-yaml",
                &format!("entity frontmatter is invalid YAML: {error}"),
            ));
            return Ok(());
        }
    };
    if value["apiVersion"].as_str() != Some("processkit.projectious.work/v2") {
        errors.push(finding(
            relative,
            "unsupported-api-version",
            "entity must use processkit.projectious.work/v2",
        ));
        return Ok(());
    }
    if value["kind"].as_str() != Some(expected_kind) {
        errors.push(finding(
            relative,
            "kind-directory-mismatch",
            &format!("expected kind {expected_kind} in this entity root"),
        ));
        return Ok(());
    }
    let Some(id) = value["metadata"]["id"].as_str() else {
        errors.push(finding(
            relative,
            "missing-id",
            "entity metadata.id must be a string",
        ));
        return Ok(());
    };
    let immutable = expected_kind == "LogEntry"
        || (expected_kind == "Migration" && relative.contains("/applied/"));
    entries.push(CorpusEntry {
        path: relative.into(),
        kind: expected_kind.into(),
        id: id.into(),
        sha256: digest(path)?,
        disposition: if immutable {
            "preserve-immutable".into()
        } else {
            "copy-compatible".into()
        },
        field_loss: Vec::new(),
    });
    Ok(())
}

fn yaml_frontmatter(bytes: &[u8]) -> Result<&[u8], String> {
    let text = std::str::from_utf8(bytes).map_err(|_| "entity must be valid UTF-8".to_string())?;
    let Some(rest) = text.strip_prefix("---\n") else {
        return Err("entity must start with YAML frontmatter".into());
    };
    let Some(end) = rest.find("\n---") else {
        return Err("entity frontmatter closing delimiter is missing".into());
    };
    Ok(&rest.as_bytes()[..end])
}

fn relative_path(source: &Path, path: &Path) -> Result<String, String> {
    let relative = path
        .strip_prefix(source)
        .map_err(|_| "legacy corpus path escaped its source root")?;
    let rendered = relative
        .to_str()
        .ok_or("legacy corpus path must be valid UTF-8")?
        .replace('\\', "/");
    if !safe_relative(&rendered) {
        return Err("legacy corpus path is unsafe".into());
    }
    Ok(rendered)
}

fn finding(path: &str, code: &str, message: &str) -> CorpusFinding {
    CorpusFinding {
        path: path.into(),
        code: code.into(),
        message: message.into(),
        remediation: match code {
            "modified-product-owned-path" => {
                "restore this path from the exact v0 release or move the local changes to a new user-owned entity"
            }
            "unsafe-symlink" => "replace the symlink with a regular file or directory",
            "invalid-frontmatter" | "invalid-yaml" => {
                "repair the entity frontmatter before retrying migration"
            }
            "unsupported-api-version" => {
                "convert the entity to processkit.projectious.work/v2"
            }
            "kind-directory-mismatch" => {
                "move the entity to the root matching its declared kind"
            }
            "missing-id" => "add a string metadata.id before retrying migration",
            _ => "resolve the reported source-path problem before retrying migration",
        }
        .into(),
    }
}
