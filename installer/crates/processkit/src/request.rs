//! Versioned machine request parsing and lifecycle dispatch.

use super::{install, recover, uninstall, update, verify_installation};
use crate::contract::API_VERSION;
use crate::error::InstallerError;
use crate::planner::plan;
use crate::signed_release::extract_verified_release;
use serde::Deserialize;
use std::fs;
use std::path::{Path, PathBuf};

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
#[serde(deny_unknown_fields)]
struct InstallerRequest {
    api_version: String,
    operation: String,
    root: PathBuf,
    distribution_path: Option<PathBuf>,
    envelope_path: Option<PathBuf>,
    signature_path: Option<PathBuf>,
    trust_store_path: Option<PathBuf>,
    #[serde(default)]
    profiles: Vec<String>,
    #[serde(default)]
    harnesses: Vec<String>,
    #[serde(default)]
    yes: bool,
}

pub(super) fn execute_request(path: &Path) -> Result<serde_json::Value, InstallerError> {
    let bytes = fs::read(path)
        .map_err(|error| InstallerError::request_read(format!("installer request: {error}")))?;
    let request: InstallerRequest = serde_json::from_slice(&bytes).map_err(|error| {
        InstallerError::request_decode(format!("installer request JSON: {error}"))
    })?;
    if request.api_version != API_VERSION {
        return Err(InstallerError::request_validation(
            "unsupported installer request API version".into(),
        ));
    }
    let signed_input_count = [
        request.envelope_path.is_some(),
        request.signature_path.is_some(),
        request.trust_store_path.is_some(),
    ]
    .into_iter()
    .filter(|present| *present)
    .count();
    if !matches!(signed_input_count, 0 | 3) {
        return Err(InstallerError::request_validation(
            "signed release input requires envelope, signature, and trust store".into(),
        ));
    }
    if signed_input_count == 3 && request.distribution_path.is_some() {
        return Err(InstallerError::request_validation(
            "signed and unsigned release inputs are mutually exclusive".into(),
        ));
    }
    let needs_release = matches!(request.operation.as_str(), "plan" | "install" | "update");
    if !needs_release && (signed_input_count != 0 || request.distribution_path.is_some()) {
        return Err(InstallerError::request_validation(
            "operation does not accept a release input".into(),
        ));
    }
    let extracted = if let (Some(envelope), Some(signature), Some(trust_store)) = (
        request.envelope_path.as_deref(),
        request.signature_path.as_deref(),
        request.trust_store_path.as_deref(),
    ) {
        Some(
            extract_verified_release(envelope, signature, trust_store)
                .map_err(InstallerError::release_verification)?,
        )
    } else {
        None
    };
    let distribution_path = extracted
        .as_ref()
        .map(|release| release.1.as_path())
        .or(request.distribution_path.as_deref());
    let distribution = || {
        distribution_path.ok_or_else(|| {
            InstallerError::request_validation("operation requires release input".into())
        })
    };
    match request.operation.as_str() {
        "plan" => {
            let result = plan(
                &request.root,
                distribution()?,
                request.profiles,
                request.harnesses,
            )
            .map_err(InstallerError::operation)?;
            serde_json::to_value(result)
                .map_err(|error| InstallerError::serialization(error.to_string()))
        }
        "install" => {
            let state = install(
                &request.root,
                distribution()?,
                request.profiles,
                request.harnesses,
                request.yes,
            )
            .map_err(InstallerError::operation)?;
            Ok(serde_json::json!({
                "apiVersion": API_VERSION,
                "status": "installed",
                "changes": [{"count": state.owned_paths.len()}],
                "conflicts": [],
                "warnings": [],
                "errors": [],
                "state": state,
            }))
        }
        "update" => {
            let changed = update(&request.root, distribution()?, request.yes)
                .map_err(InstallerError::operation)?;
            Ok(success_result("updated", changed))
        }
        "uninstall" => {
            let changed =
                uninstall(&request.root, request.yes).map_err(InstallerError::operation)?;
            Ok(success_result("uninstalled", changed))
        }
        "recover" => {
            let changed = recover(&request.root, request.yes).map_err(InstallerError::operation)?;
            Ok(success_result("recovered", changed))
        }
        "verify" => verify_installation(&request.root).map_err(InstallerError::operation),
        _ => Err(InstallerError::request_validation(format!(
            "unsupported installer request operation: {}",
            request.operation
        ))),
    }
}

fn success_result(status: &str, changes: usize) -> serde_json::Value {
    serde_json::json!({
        "apiVersion": API_VERSION,
        "status": status,
        "changes": [{"count": changes}],
        "conflicts": [],
        "warnings": [],
        "errors": [],
    })
}

#[cfg(test)]
mod tests {
    use super::InstallerRequest;

    #[test]
    fn rejects_unmodelled_secret_inputs() {
        let request = br#"{
          "apiVersion":"processkit.projectious.work/installer/v1alpha1",
          "operation":"plan",
          "root":".",
          "secret":"must-not-enter-results-or-state"
        }"#;
        let error = match serde_json::from_slice::<InstallerRequest>(request) {
            Ok(_) => panic!("unknown secret-bearing fields must be rejected"),
            Err(error) => error,
        };
        assert!(error.to_string().contains("unknown field"));
    }
}
