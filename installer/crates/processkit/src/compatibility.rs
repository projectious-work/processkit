//! Compatibility evidence inspection for legacy projects.

use crate::contract::API_VERSION;
use crate::filesystem::{digest, ensure_regular_file, safe_relative, valid_sha256};
use crate::release::verified_release;
use serde::{Deserialize, Serialize};
use std::collections::HashSet;
use std::fs;
use std::path::Path;

#[derive(Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
struct CompatibilityManifest {
    api_version: String,
    kind: String,
    id: String,
    source: CompatibilitySource,
    detection: CompatibilityDetection,
    migration: CompatibilityMigration,
    ownership_baseline: String,
}
#[derive(Deserialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
struct CompatibilitySource {
    project: String,
    release_version: String,
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct CompatibilityDetection {
    mode: String,
    anchors: Vec<CompatibilityAnchor>,
}
#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct CompatibilityAnchor {
    path: String,
    sha256: String,
}
#[derive(Deserialize, Serialize)]
#[serde(deny_unknown_fields)]
struct CompatibilityMigration {
    disposition: String,
    reason: String,
}

pub(super) fn inspect_compatibility(
    root: &Path,
    distribution_root: &Path,
) -> Result<serde_json::Value, String> {
    let metadata = root
        .symlink_metadata()
        .map_err(|error| format!("compatibility root: {error}"))?;
    if metadata.file_type().is_symlink() || !metadata.is_dir() {
        return Err("compatibility root must be a non-symlink directory".into());
    }
    let release = verified_release(distribution_root)?;
    let mut matches = Vec::new();
    let mut evidence = Vec::new();
    for relative in &release.distribution.spec.compatibility {
        if !safe_relative(relative) {
            return Err("compatibility manifest path is unsafe".into());
        }
        let path = distribution_root.join(relative);
        ensure_regular_file(distribution_root, &path, "compatibility manifest")?;
        let manifest: CompatibilityManifest = serde_yaml::from_slice(
            &fs::read(&path).map_err(|error| format!("compatibility manifest: {error}"))?,
        )
        .map_err(|error| format!("compatibility manifest YAML: {error}"))?;
        if manifest.api_version != API_VERSION
            || manifest.kind != "CompatibilityManifest"
            || manifest.source.project != "processkit"
            || manifest.detection.mode != "exact-release"
            || manifest.detection.anchors.len() < 3
            || !matches!(
                manifest.migration.disposition.as_str(),
                "evidence-only" | "unsupported"
            )
            || !safe_relative(&manifest.ownership_baseline)
        {
            return Err(format!(
                "unsupported compatibility manifest: {}",
                manifest.id
            ));
        }
        let mut matched = Vec::new();
        let mut missing = Vec::new();
        let mut mismatched = Vec::new();
        let mut seen = HashSet::new();
        for anchor in &manifest.detection.anchors {
            if !safe_relative(&anchor.path)
                || !valid_sha256(&anchor.sha256)
                || !seen.insert(anchor.path.as_str())
            {
                return Err(format!("invalid compatibility anchor in {}", manifest.id));
            }
            let candidate = root.join(&anchor.path);
            match candidate.symlink_metadata() {
                Ok(meta) if meta.is_file() && !meta.file_type().is_symlink() => {
                    if digest(&candidate)? == anchor.sha256 {
                        matched.push(anchor.path.clone());
                    } else {
                        mismatched.push(anchor.path.clone());
                    }
                }
                Ok(_) => mismatched.push(anchor.path.clone()),
                Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
                    missing.push(anchor.path.clone());
                }
                Err(error) => return Err(format!("compatibility anchor: {error}")),
            }
        }
        if missing.is_empty() && mismatched.is_empty() {
            matches.push(serde_json::json!({
                "manifestId": manifest.id,
                "releaseVersion": manifest.source.release_version,
                "migration": manifest.migration,
                "ownershipBaseline": manifest.ownership_baseline,
            }));
        }
        evidence.push(serde_json::json!({
            "manifestId": manifest.id,
            "matchedAnchors": matched,
            "missingAnchors": missing,
            "mismatchedAnchors": mismatched,
        }));
    }
    if matches.len() > 1 {
        return Err("ambiguous compatibility evidence matched multiple releases".into());
    }
    let candidate = legacy_project_candidate(root)?;
    let status = if matches.len() == 1 {
        "exact-release"
    } else if candidate {
        "legacy-project-candidate"
    } else {
        "not-detected"
    };
    Ok(serde_json::json!({
        "apiVersion": API_VERSION,
        "status": status,
        "root": root,
        "matches": matches,
        "evidence": evidence,
        "migration": if status == "exact-release" {
            serde_json::json!({
                "disposition": "evidence-only",
                "reason": "inspect and plan corpus migration before a fresh v1 install"
            })
        } else {
            serde_json::json!({"disposition": "none"})
        }
    }))
}

fn legacy_project_candidate(root: &Path) -> Result<bool, String> {
    let manifest = root.join("context/.processkit-mcp-manifest.json");
    if !manifest.is_file()
        || manifest
            .symlink_metadata()
            .map_err(|error| error.to_string())?
            .file_type()
            .is_symlink()
    {
        return Ok(false);
    }
    let schemas = root.join("context/schemas");
    let entries = match fs::read_dir(schemas) {
        Ok(entries) => entries,
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => return Ok(false),
        Err(error) => return Err(error.to_string()),
    };
    for entry in entries {
        let path = entry.map_err(|error| error.to_string())?.path();
        if path.extension().and_then(|value| value.to_str()) != Some("yaml") || !path.is_file() {
            continue;
        }
        let value: serde_yaml::Value =
            match serde_yaml::from_slice(&fs::read(&path).map_err(|error| error.to_string())?) {
                Ok(value) => value,
                Err(_) => continue,
            };
        if value["apiVersion"].as_str() == Some("processkit.projectious.work/v2")
            && value["kind"].as_str() == Some("Schema")
        {
            return Ok(true);
        }
    }
    Ok(false)
}
