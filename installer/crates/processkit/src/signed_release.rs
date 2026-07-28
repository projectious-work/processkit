//! Verification of signed local release metadata and bound assets.

use crate::contract::API_VERSION;
use crate::filesystem::{digest, ensure_regular_file, safe_relative, valid_sha256};
use crate::release::verified_release;
use ed25519_dalek::pkcs8::{DecodePublicKey, EncodePublicKey};
use ed25519_dalek::{Signature, Verifier, VerifyingKey};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::BTreeSet;
use std::fs;
use std::path::{Component, Path, PathBuf};

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
struct LocalReleaseEnvelope {
    api_version: String,
    kind: String,
    release: LocalReleaseIdentity,
    archive: LocalReleaseArchive,
    descriptor: LocalReleaseBoundFile,
    provenance: LocalReleaseProvenance,
    signing: LocalReleaseSigning,
    installer_assets: Vec<LocalReleaseInstallerAsset>,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct LocalReleaseIdentity {
    name: String,
    version: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct LocalReleaseArchive {
    file: String,
    sha256: String,
    size: u64,
    #[serde(rename = "topLevelDirectory")]
    top_level_directory: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct LocalReleaseBoundFile {
    file: String,
    sha256: String,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
struct LocalReleaseProvenance {
    file: String,
    sha256: String,
    generated_for_tag: String,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
struct LocalReleaseSigning {
    algorithm: String,
    key_id: String,
}

#[derive(Deserialize)]
#[serde(deny_unknown_fields)]
struct LocalReleaseInstallerAsset {
    file: String,
    sha256: String,
    target: String,
    size: u64,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
struct LocalTrustStore {
    api_version: String,
    kind: String,
    keys: Vec<LocalTrustKey>,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
struct LocalTrustKey {
    key_id: String,
    algorithm: String,
    public_key_file: String,
    status: String,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
pub(super) struct VerifiedReleaseEvidence {
    pub(super) api_version: &'static str,
    pub(super) status: &'static str,
    pub(super) version: String,
    pub(super) archive: String,
    pub(super) archive_sha256: String,
    pub(super) archive_top_level_directory: String,
    pub(super) descriptor_file: String,
    pub(super) descriptor_sha256: String,
    pub(super) provenance_file: String,
    pub(super) provenance_sha256: String,
    pub(super) provenance_generated_for_tag: String,
    pub(super) installer_asset_count: usize,
    pub(super) key_id: String,
}

pub(super) fn extract_verified_release(
    envelope_path: &Path,
    signature_path: &Path,
    trust_store_path: &Path,
) -> Result<(tempfile::TempDir, PathBuf), String> {
    let evidence = verify_local_release(envelope_path, signature_path, trust_store_path)?;
    let archive_path = envelope_path
        .parent()
        .ok_or("release envelope has no parent directory")?
        .join(evidence.archive);
    let file =
        fs::File::open(&archive_path).map_err(|error| format!("release archive: {error}"))?;
    let decoder = flate2::read::GzDecoder::new(file);
    let mut archive = tar::Archive::new(decoder);
    let temporary =
        tempfile::tempdir().map_err(|error| format!("release extraction directory: {error}"))?;
    let mut top_level = None;
    let mut seen = BTreeSet::new();
    let mut total_size = 0_u64;
    let entries = archive
        .entries()
        .map_err(|error| format!("release archive entries: {error}"))?;
    for (index, entry) in entries.enumerate() {
        if index >= 100_000 {
            return Err("release archive contains too many entries".into());
        }
        let mut entry = entry.map_err(|error| format!("release archive entry: {error}"))?;
        let entry_type = entry.header().entry_type();
        if !entry_type.is_file() && !entry_type.is_dir() {
            return Err("release archive contains a link or special file".into());
        }
        total_size = total_size
            .checked_add(entry.size())
            .ok_or("release archive size overflow")?;
        if total_size > 1024 * 1024 * 1024 {
            return Err("release archive expands beyond the 1 GiB safety limit".into());
        }
        let path = entry
            .path()
            .map_err(|error| format!("release archive path: {error}"))?
            .into_owned();
        if path.is_absolute()
            || path
                .components()
                .any(|component| !matches!(component, Component::Normal(_)))
        {
            return Err("release archive contains an unsafe path".into());
        }
        let first = path
            .components()
            .next()
            .and_then(|component| match component {
                Component::Normal(value) => Some(value.to_owned()),
                _ => None,
            })
            .ok_or("release archive entry has no top-level directory")?;
        if let Some(expected) = &top_level {
            if expected != &first {
                return Err("release archive has multiple top-level directories".into());
            }
        } else {
            top_level = Some(first);
        }
        if !seen.insert(path.clone()) {
            return Err("release archive contains a duplicate path".into());
        }
        entry
            .unpack_in(temporary.path())
            .map_err(|error| format!("release archive extraction: {error}"))?;
    }
    let root = temporary
        .path()
        .join(top_level.ok_or("release archive contains no entries")?);
    if root.file_name().and_then(|value| value.to_str())
        != Some(evidence.archive_top_level_directory.as_str())
    {
        return Err("release archive top-level directory mismatch".into());
    }
    let descriptor_path = root.join(&evidence.descriptor_file);
    ensure_regular_file(&root, &descriptor_path, "bound release descriptor")?;
    if digest(&descriptor_path)? != evidence.descriptor_sha256 {
        return Err("bound release descriptor digest mismatch".into());
    }
    let provenance_path = root.join(&evidence.provenance_file);
    ensure_regular_file(&root, &provenance_path, "bound release provenance")?;
    if digest(&provenance_path)? != evidence.provenance_sha256 {
        return Err("bound release provenance digest mismatch".into());
    }
    let provenance = fs::read_to_string(&provenance_path)
        .map_err(|error| format!("bound release provenance: {error}"))?;
    let expected_tag = format!(
        "generated_for_tag = \"{}\"",
        evidence.provenance_generated_for_tag
    );
    if !provenance.lines().any(|line| line.trim() == expected_tag) {
        return Err("bound release provenance tag mismatch".into());
    }
    verified_release(&root)?;
    Ok((temporary, root))
}

pub(super) fn verify_local_release(
    envelope_path: &Path,
    signature_path: &Path,
    trust_store_path: &Path,
) -> Result<VerifiedReleaseEvidence, String> {
    let envelope_bytes =
        fs::read(envelope_path).map_err(|error| format!("release envelope: {error}"))?;
    let envelope: LocalReleaseEnvelope = serde_json::from_slice(&envelope_bytes)
        .map_err(|error| format!("release envelope JSON: {error}"))?;
    if envelope.api_version != "processkit.projectious.work/local-release/v1alpha1"
        || envelope.kind != "LocalRelease"
        || envelope.release.name != "processkit"
        || envelope.signing.algorithm != "Ed25519"
    {
        return Err("unsupported local release envelope".into());
    }
    semver::Version::parse(envelope.release.version.trim_start_matches('v'))
        .map_err(|error| format!("release version is not semantic: {error}"))?;
    if !safe_relative(&envelope.archive.file)
        || envelope.archive.file.contains('/')
        || envelope.archive.file != format!("processkit-{}.tar.gz", envelope.release.version)
        || !valid_sha256(&envelope.archive.sha256)
        || envelope.archive.size == 0
        || envelope.archive.top_level_directory
            != format!("processkit-{}", envelope.release.version)
        || !safe_relative(&envelope.archive.top_level_directory)
        || envelope.archive.top_level_directory.contains('/')
        || !safe_relative(&envelope.descriptor.file)
        || !safe_relative(&envelope.provenance.file)
        || !valid_sha256(&envelope.descriptor.sha256)
        || !valid_sha256(&envelope.provenance.sha256)
        || envelope.provenance.generated_for_tag != envelope.release.version
        || !valid_sha256(&envelope.signing.key_id)
    {
        return Err("local release envelope contains an unsafe field".into());
    }
    if envelope.descriptor.file != ".processkit/installer/release-descriptor.json"
        || envelope.provenance.file != "PROVENANCE.toml"
        || envelope.installer_assets.is_empty()
    {
        return Err("local release envelope has an incomplete release identity".into());
    }

    let trust_bytes =
        fs::read(trust_store_path).map_err(|error| format!("local trust store: {error}"))?;
    let trust: LocalTrustStore = serde_json::from_slice(&trust_bytes)
        .map_err(|error| format!("local trust store JSON: {error}"))?;
    if trust.api_version != "processkit.projectious.work/local-trust/v1alpha1"
        || trust.kind != "TrustStore"
    {
        return Err("unsupported local trust store".into());
    }
    let trusted = trust
        .keys
        .iter()
        .find(|key| {
            key.key_id == envelope.signing.key_id
                && key.algorithm == "Ed25519"
                && key.status == "active"
        })
        .ok_or("release signing key is not active in the local trust store")?;
    if !safe_relative(&trusted.public_key_file) {
        return Err("local trust store contains an unsafe key path".into());
    }
    let trust_root = trust_store_path
        .parent()
        .ok_or("local trust store has no parent directory")?;
    let key_path = trust_root.join(&trusted.public_key_file);
    ensure_regular_file(trust_root, &key_path, "trusted public key")?;
    let key_pem =
        fs::read_to_string(&key_path).map_err(|error| format!("trusted public key: {error}"))?;
    let key = VerifyingKey::from_public_key_pem(&key_pem)
        .map_err(|error| format!("trusted public key: {error}"))?;
    let der = key
        .to_public_key_der()
        .map_err(|error| format!("trusted public key DER: {error}"))?;
    let actual_key_id = format!("{:x}", Sha256::digest(der.as_bytes()));
    if actual_key_id != envelope.signing.key_id {
        return Err("trusted public key ID does not match the release envelope".into());
    }
    let signature_bytes =
        fs::read(signature_path).map_err(|error| format!("release signature: {error}"))?;
    let signature = Signature::from_slice(&signature_bytes)
        .map_err(|error| format!("release signature: {error}"))?;
    key.verify(&envelope_bytes, &signature)
        .map_err(|_| "release signature verification failed")?;

    let envelope_root = envelope_path
        .parent()
        .ok_or("release envelope has no parent directory")?;
    let archive_path = envelope_root.join(&envelope.archive.file);
    ensure_regular_file(envelope_root, &archive_path, "release archive")?;
    if fs::metadata(&archive_path)
        .map_err(|error| format!("release archive metadata: {error}"))?
        .len()
        != envelope.archive.size
    {
        return Err("release archive size mismatch".into());
    }
    if digest(&archive_path)? != envelope.archive.sha256 {
        return Err("release archive digest mismatch".into());
    }
    let mut targets = BTreeSet::new();
    let mut files = BTreeSet::new();
    for installer in &envelope.installer_assets {
        if !safe_relative(&installer.file)
            || installer.file.contains('/')
            || !valid_sha256(&installer.sha256)
            || installer.size == 0
            || installer.target.is_empty()
            || !installer
                .target
                .bytes()
                .all(|byte| byte.is_ascii_alphanumeric() || matches!(byte, b'-' | b'_' | b'.'))
            || installer.file
                != format!(
                    "processkit-{}-{}",
                    envelope.release.version, installer.target
                )
            || !targets.insert(installer.target.as_str())
            || !files.insert(installer.file.as_str())
        {
            return Err("local release envelope contains unsafe installer evidence".into());
        }
        let installer_path = envelope_root.join(&installer.file);
        ensure_regular_file(envelope_root, &installer_path, "installer executable")?;
        if fs::metadata(&installer_path)
            .map_err(|error| format!("installer executable metadata: {error}"))?
            .len()
            != installer.size
        {
            return Err("installer executable size mismatch".into());
        }
        if digest(&installer_path)? != installer.sha256 {
            return Err("installer executable digest mismatch".into());
        }
    }
    Ok(VerifiedReleaseEvidence {
        api_version: API_VERSION,
        status: "verified",
        version: envelope.release.version,
        archive: envelope.archive.file,
        archive_sha256: envelope.archive.sha256,
        archive_top_level_directory: envelope.archive.top_level_directory,
        descriptor_file: envelope.descriptor.file,
        descriptor_sha256: envelope.descriptor.sha256,
        provenance_file: envelope.provenance.file,
        provenance_sha256: envelope.provenance.sha256,
        provenance_generated_for_tag: envelope.provenance.generated_for_tag,
        installer_asset_count: envelope.installer_assets.len(),
        key_id: envelope.signing.key_id,
    })
}
