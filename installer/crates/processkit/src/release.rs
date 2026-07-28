//! Validation of an extracted, unsigned processkit distribution.

use super::Distribution;
use crate::contract::API_VERSION;
use crate::filesystem::{digest, ensure_regular_file, safe_relative};
use serde::Deserialize;
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct ReleaseDescriptor {
    #[serde(rename = "$schema")]
    _schema: Option<String>,
    #[serde(rename = "apiVersion")]
    api_version: String,
    kind: String,
    distribution: DescriptorDistribution,
    installer: DescriptorInstaller,
    asset: DescriptorAsset,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct DescriptorDistribution {
    manifest: String,
    #[serde(rename = "manifestSha256")]
    manifest_sha256: String,
    protocol: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct DescriptorInstaller {
    requires: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct DescriptorAsset {
    layout: String,
}

pub(super) struct VerifiedRelease {
    pub(super) root: PathBuf,
    pub(super) distribution: Distribution,
    pub(super) manifest: PathBuf,
    pub(super) manifest_sha256: String,
}

pub(super) fn verified_release(
    distribution_root: &Path,
) -> Result<VerifiedRelease, String> {
    let root_metadata = distribution_root
        .symlink_metadata()
        .map_err(|error| format!("release root: {error}"))?;
    if root_metadata.file_type().is_symlink() || !root_metadata.is_dir() {
        return Err("release root must be a non-symlink directory".into());
    }
    let descriptor_path = distribution_root.join(
        ".processkit/installer/release-descriptor.json",
    );
    ensure_regular_file(
        distribution_root,
        &descriptor_path,
        "release descriptor",
    )?;
    let descriptor_bytes = fs::read(&descriptor_path)
        .map_err(|error| format!("release descriptor: {error}"))?;
    let descriptor: ReleaseDescriptor =
        serde_json::from_slice(&descriptor_bytes)
            .map_err(|error| format!("release descriptor JSON: {error}"))?;
    if descriptor.api_version != API_VERSION
        || descriptor.kind != "ReleaseDescriptor"
    {
        return Err("unsupported release descriptor API or kind".into());
    }
    if descriptor.distribution.protocol != API_VERSION {
        return Err(
            "release descriptor has unsupported installer protocol".into(),
        );
    }
    if descriptor.installer.requires.trim().is_empty()
        || descriptor.asset.layout != "single-top-level-directory"
    {
        return Err(
            "release descriptor has invalid installer or asset contract"
                .into(),
        );
    }
    if !safe_relative(&descriptor.distribution.manifest) {
        return Err(
            "release descriptor manifest must be a safe relative path".into(),
        );
    }
    let manifest = distribution_root.join(&descriptor.distribution.manifest);
    ensure_regular_file(
        distribution_root,
        &manifest,
        "distribution manifest",
    )?;
    let manifest_sha256 = digest(&manifest)?;
    if manifest_sha256 != descriptor.distribution.manifest_sha256 {
        return Err("release descriptor manifest SHA-256 mismatch".into());
    }
    let text = fs::read_to_string(&manifest)
        .map_err(|error| format!("manifest: {error}"))?;
    let distribution: Distribution = serde_yaml::from_str(&text)
        .map_err(|error| format!("manifest YAML: {error}"))?;
    if distribution.api_version
        != "processkit.projectious.work/distribution/v1alpha1"
        || distribution.kind != "Distribution"
        || distribution.spec.installer.protocol
            != descriptor.distribution.protocol
    {
        return Err(
            "release descriptor and distribution manifest disagree".into(),
        );
    }
    for path in distribution
        .spec
        .catalogs
        .values()
        .chain(distribution.spec.harness_adapters.values())
    {
        if !safe_relative(path) {
            return Err(
                "distribution references an unsafe catalog or adapter path"
                    .into(),
            );
        }
        ensure_regular_file(
            distribution_root,
            &distribution_root.join(path),
            "release reference",
        )?;
    }
    Ok(VerifiedRelease {
        root: distribution_root.to_path_buf(),
        distribution,
        manifest,
        manifest_sha256,
    })
}
