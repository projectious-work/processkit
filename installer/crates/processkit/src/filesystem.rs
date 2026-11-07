//! Filesystem validation helpers used at the release trust boundary.

use sha2::{Digest, Sha256};
use std::fs;
use std::path::{Component, Path};

pub(crate) fn safe_relative(value: &str) -> bool {
    let path = Path::new(value);
    !value.is_empty()
        && !value.contains('\\')
        && !value.contains('\0')
        && !path.is_absolute()
        && (value == "." || value.split('/').all(|part| !part.is_empty() && part != "."))
        && !path.components().any(|component| {
            matches!(
                component,
                Component::ParentDir | Component::RootDir | Component::Prefix(_)
            )
        })
}

pub(crate) fn digest(path: &Path) -> Result<String, String> {
    let bytes = fs::read(path).map_err(|error| format!("{}: {error}", path.display()))?;
    Ok(format!("{:x}", Sha256::digest(bytes)))
}

pub(crate) fn ensure_regular_file(root: &Path, path: &Path, label: &str) -> Result<(), String> {
    let relative = path
        .strip_prefix(root)
        .map_err(|_| format!("{label} escaped release root"))?;
    if !safe_relative(&relative.to_string_lossy()) {
        return Err(format!("{label} must be a safe relative path"));
    }
    let metadata = path
        .symlink_metadata()
        .map_err(|error| format!("{label}: {error}"))?;
    if metadata.file_type().is_symlink() || !metadata.is_file() {
        return Err(format!("{label} must be a regular non-symlink file"));
    }
    Ok(())
}

pub(crate) fn ensure_non_symlink_directory(path: &Path, label: &str) -> Result<(), String> {
    let metadata = path
        .symlink_metadata()
        .map_err(|error| format!("{label}: {error}"))?;
    if metadata.file_type().is_symlink() || !metadata.is_dir() {
        return Err(format!("{label} must be a non-symlink directory"));
    }
    Ok(())
}

pub(crate) fn valid_sha256(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
}
