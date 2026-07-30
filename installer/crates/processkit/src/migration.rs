//! Evidence-driven planning for legacy project corpus migration.

use crate::filesystem::{digest, safe_relative};
use serde::Serialize;
use std::fs;
use std::path::Path;

const ENTITY_ROOTS: &[(&str, &str)] = &[
    ("context/actors", "Actor"),
    ("context/decisions", "DecisionRecord"),
    ("context/discussions", "Discussion"),
    ("context/gates", "Gate"),
    ("context/logs", "LogEntry"),
    ("context/migrations", "Migration"),
    ("context/notes", "Note"),
    ("context/scopes", "Scope"),
    ("context/workitems", "WorkItem"),
];

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub(super) struct CorpusPlan {
    pub(super) status: String,
    entries: Vec<CorpusEntry>,
    excluded_roots: Vec<&'static str>,
    errors: Vec<CorpusFinding>,
    summary: CorpusSummary,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct CorpusEntry {
    path: String,
    kind: String,
    id: String,
    sha256: String,
    disposition: String,
    field_loss: Vec<String>,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct CorpusFinding {
    path: String,
    code: String,
    message: String,
}

#[derive(Default, Serialize)]
#[serde(rename_all = "camelCase")]
struct CorpusSummary {
    copy_compatible: usize,
    preserve_immutable: usize,
    blocked: usize,
}

pub(super) fn plan_v0_corpus(source: &Path) -> Result<CorpusPlan, String> {
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
        walk_entity_root(source, &root, expected_kind, &mut entries, &mut errors)?;
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
        excluded_roots: vec![
            "context/artifacts",
            "context/bindings",
            "context/roles",
            "context/team-members",
        ],
        errors,
        summary,
    })
}

fn walk_entity_root(
    source: &Path,
    directory: &Path,
    expected_kind: &str,
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
            walk_entity_root(source, &path, expected_kind, entries, errors)?;
        } else if metadata.is_file()
            && path.extension().and_then(|extension| extension.to_str()) == Some("md")
            && (expected_kind != "TeamMember"
                || path.file_name().and_then(|name| name.to_str()) == Some("team-member.md"))
        {
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
    }
}
