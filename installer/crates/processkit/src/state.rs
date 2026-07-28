//! Persistent installer state models and validation.

use crate::contract::API_VERSION;
use crate::filesystem::{safe_relative, valid_sha256};
use serde::{Deserialize, Serialize};
use std::collections::{BTreeMap, HashSet};

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
pub(super) struct InstallationState {
    pub(super) api_version: String,
    pub(super) release: StateRelease,
    pub(super) profiles: Vec<String>,
    pub(super) harnesses: Vec<String>,
    pub(super) owned_paths: Vec<OwnedPath>,
    #[serde(default)]
    pub(super) managed_adapters: Vec<ManagedAdapterState>,
}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
pub(super) struct StateRelease {
    pub(super) name: String,
    pub(super) version: String,
    pub(super) manifest_sha256: String,
}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
pub(super) struct OwnedPath {
    pub(super) path: String,
    pub(super) component: String,
    pub(super) operation: String,
    pub(super) ownership: String,
    pub(super) installed_sha256: String,
}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
pub(super) struct ManagedAdapterState {
    pub(super) adapter: String,
    pub(super) path: String,
    pub(super) format: String,
    pub(super) catalog_sha256: String,
    pub(super) managed_keys: BTreeMap<String, String>,
    #[serde(default)]
    pub(super) created_file: bool,
    #[serde(default)]
    pub(super) created_mcp_servers: bool,
}

pub(super) fn validate_installation_state(state: &InstallationState) -> Result<(), String> {
    if state.api_version != API_VERSION {
        return Err("unsupported installer state version".into());
    }
    if state.release.name.trim().is_empty()
        || semver::Version::parse(state.release.version.trim_start_matches('v')).is_err()
        || !valid_sha256(&state.release.manifest_sha256)
    {
        return Err("installer state has invalid release provenance".into());
    }
    let mut paths = HashSet::new();
    for owned in &state.owned_paths {
        if !safe_relative(&owned.path)
            || !paths.insert(owned.path.as_str())
            || !valid_sha256(&owned.installed_sha256)
            || !matches!(
                owned.ownership.as_str(),
                "managed-three-way" | "managed-keys" | "shared"
            )
        {
            return Err("installer state contains an invalid owned path".into());
        }
    }
    let mut adapter_paths = HashSet::new();
    for adapter in &state.managed_adapters {
        if adapter.adapter.trim().is_empty()
            || adapter.format != "json"
            || !safe_relative(&adapter.path)
            || !adapter_paths.insert(adapter.path.as_str())
            || !valid_sha256(&adapter.catalog_sha256)
            || adapter.managed_keys.iter().any(|(key, digest)| {
                key.is_empty() || key.chars().any(char::is_control) || !valid_sha256(digest)
            })
        {
            return Err("installer state contains an invalid managed adapter".into());
        }
    }
    Ok(())
}
