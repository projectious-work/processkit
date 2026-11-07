//! Deterministic, non-mutating installation planning.

use super::{adapter_actions, has_symlink_ancestor, Source};
use crate::contract::API_VERSION;
use crate::filesystem::{digest, safe_relative};
use crate::release::{verified_release, VerifiedRelease};
use serde::Serialize;
use std::collections::{BTreeSet, HashSet};
use std::path::{Path, PathBuf};

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub(super) struct Plan {
    pub(super) api_version: &'static str,
    pub(super) status: String,
    pub(super) distribution: DistributionInfo,
    pub(super) selected_profiles: Vec<String>,
    pub(super) harnesses: Vec<String>,
    pub(super) changes: Vec<Change>,
    pub(super) conflicts: Vec<Problem>,
    pub(super) warnings: Vec<Problem>,
    pub(super) errors: Vec<Problem>,
}
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub(super) struct DistributionInfo {
    pub(super) name: String,
    pub(super) version: String,
    pub(super) manifest_sha256: String,
}
#[derive(Serialize, Ord, PartialOrd, Eq, PartialEq)]
#[serde(rename_all = "camelCase")]
pub(super) struct Change {
    pub(super) destination: String,
    pub(super) component: String,
    pub(super) operation: String,
    pub(super) ownership: String,
    pub(super) kind: String,
    pub(super) source_sha256: String,
    #[serde(skip)]
    pub(super) source: PathBuf,
}
#[derive(Serialize, Ord, PartialOrd, Eq, PartialEq)]
pub(super) struct Problem {
    code: String,
    path: String,
    message: String,
}

pub(super) fn plan(
    root: &Path,
    distribution_root: &Path,
    mut profiles: Vec<String>,
    mut harnesses: Vec<String>,
) -> Result<Plan, String> {
    if profiles.is_empty() {
        profiles.push("managed".into());
    }
    profiles.sort();
    profiles.dedup();
    harnesses.sort();
    harnesses.dedup();
    let VerifiedRelease {
        root: release_root,
        distribution,
        manifest: _manifest,
        manifest_sha256,
    } = verified_release(distribution_root)?;
    for harness in &harnesses {
        if !distribution.spec.harness_adapters.contains_key(harness) {
            return Err(format!("unknown harness adapter: {harness}"));
        }
    }
    let mut selected = BTreeSet::new();
    for profile in &profiles {
        let item = distribution
            .spec
            .profiles
            .get(profile)
            .ok_or_else(|| format!("unknown profile: {profile}"))?;
        selected.extend(item.include.iter().cloned());
    }
    let mut changes = Vec::new();
    let mut conflicts = Vec::new();
    let mut errors = Vec::new();
    let mut component_ids = HashSet::new();
    for component in &distribution.spec.components {
        if !component_ids.insert(component.id.as_str()) {
            errors.push(Problem {
                code: "duplicate-component".into(),
                path: component.id.clone(),
                message: "component IDs must be unique".into(),
            });
        }
    }
    for component in &selected {
        if !component_ids.contains(component.as_str()) {
            errors.push(Problem {
                code: "unknown-component".into(),
                path: component.clone(),
                message: "profile references a missing component".into(),
            });
        }
    }
    for component in distribution
        .spec
        .components
        .into_iter()
        .filter(|c| selected.contains(&c.id))
    {
        if !matches!(component.operation.as_str(), "copy/v1" | "preserve-user/v1") {
            errors.push(Problem {
                code: "unsupported-operation".into(),
                path: component.id.clone(),
                message: component.operation.clone(),
            });
            continue;
        }
        if !safe_relative(&component.destination) {
            errors.push(Problem {
                code: "unsafe-destination".into(),
                path: component.destination.clone(),
                message: "destination must be relative".into(),
            });
            continue;
        }
        let sources = match source_paths(&release_root, &component.source) {
            Ok(items) => items,
            Err(message) => {
                errors.push(Problem {
                    code: "invalid-source".into(),
                    path: component.id.clone(),
                    message,
                });
                continue;
            }
        };
        let file_source = component.source.file.is_some();
        for (source_path, relative) in sources {
            let destination = if file_source {
                component.destination.clone()
            } else if component.destination == "." {
                relative
            } else {
                format!(
                    "{}/{}",
                    component.destination.trim_end_matches('/'),
                    relative
                )
            };
            let target = root.join(&destination);
            if has_symlink_ancestor(root, &destination)? {
                conflicts.push(Problem {
                    code: "symlink-target".into(),
                    path: destination,
                    message: "refusing symlink target or ancestor".into(),
                });
                continue;
            }
            if target
                .symlink_metadata()
                .map(|m| m.file_type().is_symlink())
                .unwrap_or(false)
            {
                conflicts.push(Problem {
                    code: "symlink-target".into(),
                    path: destination,
                    message: "refusing symlink target".into(),
                });
                continue;
            }
            if target.exists() && component.operation == "preserve-user/v1" {
                changes.push(Change {
                    destination,
                    component: component.id.clone(),
                    operation: component.operation.clone(),
                    ownership: component.ownership.clone(),
                    kind: "preserve".into(),
                    source_sha256: digest(&source_path)?,
                    source: source_path,
                });
            } else if target.exists() {
                conflicts.push(Problem {
                    code: "existing-target".into(),
                    path: destination,
                    message: "managed replacement requires an explicit update policy".into(),
                });
            } else {
                changes.push(Change {
                    destination,
                    component: component.id.clone(),
                    operation: component.operation.clone(),
                    ownership: component.ownership.clone(),
                    kind: "create".into(),
                    source_sha256: digest(&source_path)?,
                    source: source_path,
                });
            }
        }
    }
    // Harness projections are mutations too. Include their exact target,
    // ownership, operation, and resulting digest in the non-mutating plan
    // instead of discovering them only during install.
    for (pending, owned, _) in adapter_actions(root, &release_root, &harnesses, false)? {
        changes.push(Change {
            destination: owned.path,
            component: owned.component,
            operation: owned.operation,
            ownership: owned.ownership,
            kind: pending.action.kind,
            source_sha256: owned.installed_sha256,
            source: PathBuf::new(),
        });
    }
    let mut destinations = HashSet::new();
    for change in &changes {
        if !destinations.insert(change.destination.as_str()) {
            errors.push(Problem {
                code: "destination-collision".into(),
                path: change.destination.clone(),
                message: "multiple components resolve to the same destination".into(),
            });
        }
    }
    changes.sort();
    conflicts.sort();
    errors.sort();
    let status = if !errors.is_empty() {
        "invalid"
    } else if !conflicts.is_empty() {
        "conflict"
    } else {
        "planned"
    }
    .into();
    Ok(Plan {
        api_version: API_VERSION,
        status,
        distribution: DistributionInfo {
            name: distribution.metadata.name,
            version: distribution.metadata.version,
            manifest_sha256,
        },
        selected_profiles: profiles,
        harnesses,
        changes,
        conflicts,
        warnings: vec![],
        errors,
    })
}

fn source_paths(root: &Path, source: &Source) -> Result<Vec<(PathBuf, String)>, String> {
    if source.file.is_some() && source.include.is_some() {
        return Err("source must specify exactly one of file or include".into());
    }
    if let Some(file) = &source.file {
        if !safe_relative(file) {
            return Err("file source must be relative".into());
        }
        let path = root.join(file);
        if path
            .symlink_metadata()
            .map_err(|error| error.to_string())?
            .file_type()
            .is_symlink()
        {
            return Err(format!("source symlink is not allowed: {file}"));
        }
        if !path.is_file() {
            return Err(format!("source file is missing: {file}"));
        }
        return Ok(vec![(path, file.clone())]);
    }
    let includes = source
        .include
        .as_ref()
        .ok_or("source requires file or include")?;
    if includes.len() != 1 || !includes[0].ends_with("/**") {
        return Err("Phase 1 accepts one recursive include pattern".into());
    }
    let prefix = includes[0].trim_end_matches("/**");
    if !safe_relative(prefix) {
        return Err("include source must be relative".into());
    }
    let base = root.join(prefix);
    if base
        .symlink_metadata()
        .map_err(|error| error.to_string())?
        .file_type()
        .is_symlink()
    {
        return Err(format!("source symlink is not allowed: {}", includes[0]));
    }
    if !base.is_dir() {
        return Err(format!("include source is missing: {}", includes[0]));
    }
    let mut paths = Vec::new();
    for entry in walkdir::WalkDir::new(&base).follow_links(false) {
        let entry = entry.map_err(|error| error.to_string())?;
        if entry.file_type().is_symlink() {
            return Err(format!(
                "source symlink is not allowed: {}",
                entry.path().display()
            ));
        }
        if entry.file_type().is_file() {
            let relative = entry
                .path()
                .strip_prefix(root)
                .map_err(|_| "source escaped distribution root")?;
            paths.push((
                entry.path().to_path_buf(),
                relative.to_string_lossy().replace('\\', "/"),
            ));
        }
    }
    paths.sort_by(|a, b| a.1.cmp(&b.1));
    Ok(paths)
}
