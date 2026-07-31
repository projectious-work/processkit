//! Supported library surface for processkit lifecycle integrations.
//!
//! The command-line executable remains the primary interface. This crate
//! exposes the stable request envelope so integrators can construct typed
//! requests without duplicating protocol strings.

use serde::{Deserialize, Serialize};
use std::path::PathBuf;

/// Current machine-request protocol version.
pub const API_VERSION: &str = "processkit.projectious.work/installer/v1alpha1";

/// Supported lifecycle operation in a machine request.
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "kebab-case")]
pub enum Operation {
    Plan,
    Install,
    Update,
    Recover,
    Uninstall,
    Verify,
}

/// Typed request accepted by `processkit execute --request`.
///
/// ```
/// use processkit::{InstallerRequest, Operation, API_VERSION};
///
/// let request = InstallerRequest::new(Operation::Plan, ".")
///     .with_distribution("./processkit-v1.0.0");
/// assert_eq!(request.api_version, API_VERSION);
/// assert_eq!(request.profiles, vec!["managed"]);
/// ```
#[derive(Clone, Debug, Deserialize, Eq, PartialEq, Serialize)]
#[serde(rename_all = "camelCase", deny_unknown_fields)]
pub struct InstallerRequest {
    /// Protocol identity. Constructed requests use [`API_VERSION`].
    pub api_version: String,
    /// Requested lifecycle operation.
    pub operation: Operation,
    /// Target project root.
    pub root: PathBuf,
    /// Explicit extracted distribution path.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub distribution_path: Option<PathBuf>,
    /// Signed release envelope path.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub envelope_path: Option<PathBuf>,
    /// Detached release signature path.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub signature_path: Option<PathBuf>,
    /// Explicit trust-store path.
    #[serde(skip_serializing_if = "Option::is_none")]
    pub trust_store_path: Option<PathBuf>,
    /// Distribution profiles selected for planning or installation.
    pub profiles: Vec<String>,
    /// Harness adapters selected for installation.
    pub harnesses: Vec<String>,
    /// Explicit mutation acknowledgement.
    pub yes: bool,
}

impl InstallerRequest {
    /// Create a request with the managed profile and no release input.
    pub fn new(operation: Operation, root: impl Into<PathBuf>) -> Self {
        Self {
            api_version: API_VERSION.into(),
            operation,
            root: root.into(),
            distribution_path: None,
            envelope_path: None,
            signature_path: None,
            trust_store_path: None,
            profiles: vec!["managed".into()],
            harnesses: Vec::new(),
            yes: false,
        }
    }

    /// Select an explicit extracted distribution.
    pub fn with_distribution(mut self, path: impl Into<PathBuf>) -> Self {
        self.distribution_path = Some(path.into());
        self
    }

    /// Acknowledge mutation for install, update, recover, or uninstall.
    pub fn acknowledged(mut self) -> Self {
        self.yes = true;
        self
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn request_round_trip_preserves_supported_fields() {
        let request = InstallerRequest::new(Operation::Install, "/tmp/project")
            .with_distribution("/tmp/release")
            .acknowledged();
        let encoded = serde_json::to_vec(&request).expect("serialize request");
        let decoded: InstallerRequest =
            serde_json::from_slice(&encoded).expect("deserialize request");
        assert_eq!(decoded, request);
    }
}
