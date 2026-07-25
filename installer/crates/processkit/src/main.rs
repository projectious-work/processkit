use clap::{ArgAction, Parser, Subcommand, ValueEnum};
use ed25519_dalek::pkcs8::{DecodePublicKey, EncodePublicKey};
use ed25519_dalek::{Signature, Verifier, VerifyingKey};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::{BTreeSet, HashSet};
use std::fs;
use std::fs::OpenOptions;
use std::io::Write;
#[cfg(unix)]
use std::os::unix::fs::{OpenOptionsExt, PermissionsExt};
use std::path::{Component, Path, PathBuf};

const API_VERSION: &str = "processkit.projectious.work/installer/v1alpha1";

#[derive(Parser)]
#[command(name = "processkit", about = "Manifest-driven processkit installer")]
struct Cli {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand)]
enum Command {
    /// Produce a deterministic, non-mutating installation plan.
    Plan {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long)]
        distribution: PathBuf,
        #[arg(long, default_value = "managed")]
        profile: Vec<String>,
        #[arg(long)]
        harness: Vec<String>,
        /// Assert the non-mutating planner mode (the default for Phase 1).
        #[arg(long, action = ArgAction::SetTrue)]
        dry_run: bool,
        /// Emit the stable JSON plan schema.
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
        #[arg(long, value_enum, default_value_t = OutputFormat::Json)]
        format: OutputFormat,
    },
    /// Install a verified release into a new or empty target project.
    Install {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long)]
        distribution: PathBuf,
        #[arg(long, default_value = "managed")]
        profile: Vec<String>,
        #[arg(long)]
        harness: Vec<String>,
        /// Required acknowledgement for filesystem mutation.
        #[arg(long)]
        yes: bool,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Roll back or finalize incomplete installer transactions.
    Recover {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long)]
        yes: bool,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Remove unchanged files owned by a prior installation.
    Uninstall {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long)]
        yes: bool,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Update unchanged managed files from a verified release.
    Update {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long)]
        distribution: PathBuf,
        #[arg(long)]
        yes: bool,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Verify a signed local release against an explicit local trust store.
    VerifyRelease {
        #[arg(long)]
        envelope: PathBuf,
        #[arg(long)]
        signature: PathBuf,
        #[arg(long)]
        trust_store: PathBuf,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Execute one versioned installer request and emit one result envelope.
    Execute {
        #[arg(long)]
        request: PathBuf,
    },
}

#[derive(Clone, Copy, ValueEnum)]
enum OutputFormat {
    Json,
    Human,
}

#[derive(Deserialize)]
struct Distribution {
    #[serde(rename = "apiVersion")]
    api_version: String,
    kind: String,
    metadata: Metadata,
    spec: Spec,
}
#[derive(serde::Deserialize)]
struct Metadata {
    name: String,
    version: String,
}
#[derive(serde::Deserialize)]
struct Spec {
    installer: InstallerSpec,
    components: Vec<ComponentSpec>,
    profiles: std::collections::BTreeMap<String, Profile>,
    #[serde(default, rename = "catalogs")]
    catalogs: std::collections::BTreeMap<String, String>,
    #[serde(default, rename = "harnessAdapters")]
    harness_adapters: std::collections::BTreeMap<String, String>,
}
#[derive(Deserialize)]
struct InstallerSpec {
    protocol: String,
}
#[derive(Deserialize)]
struct HarnessAdapter {
    #[serde(rename = "apiVersion")]
    api_version: String,
    kind: String,
    id: String,
    format: String,
    destination: String,
    ownership: String,
    catalog: String,
}
#[derive(Deserialize)]
struct McpCatalog {
    #[serde(rename = "apiVersion")]
    api_version: String,
    kind: String,
    servers: Vec<McpServer>,
}
#[derive(Deserialize, Serialize)]
struct McpServer {
    id: String,
    command: String,
    args: Vec<String>,
    #[serde(default)]
    env: std::collections::BTreeMap<String, String>,
}
#[derive(serde::Deserialize)]
struct Profile {
    include: Vec<String>,
}
#[derive(serde::Deserialize)]
struct ComponentSpec {
    id: String,
    source: Source,
    destination: String,
    operation: String,
    ownership: String,
}
#[derive(serde::Deserialize)]
struct Source {
    file: Option<String>,
    include: Option<Vec<String>>,
}

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

struct VerifiedRelease {
    root: PathBuf,
    distribution: Distribution,
    manifest: PathBuf,
    manifest_sha256: String,
}

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct Plan {
    api_version: &'static str,
    status: String,
    distribution: DistributionInfo,
    selected_profiles: Vec<String>,
    harnesses: Vec<String>,
    changes: Vec<Change>,
    conflicts: Vec<Problem>,
    warnings: Vec<Problem>,
    errors: Vec<Problem>,
}
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct DistributionInfo {
    name: String,
    version: String,
    manifest_sha256: String,
}
#[derive(Serialize, Ord, PartialOrd, Eq, PartialEq)]
struct Change {
    destination: String,
    component: String,
    operation: String,
    ownership: String,
    kind: String,
    source_sha256: String,
    #[serde(skip)]
    source: PathBuf,
}
#[derive(Serialize, Ord, PartialOrd, Eq, PartialEq)]
struct Problem {
    code: String,
    path: String,
    message: String,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct LocalReleaseEnvelope {
    api_version: String,
    kind: String,
    release: LocalReleaseIdentity,
    archive: LocalReleaseArchive,
    signing: LocalReleaseSigning,
}
#[derive(Deserialize)]
struct LocalReleaseIdentity {
    name: String,
    version: String,
}
#[derive(Deserialize)]
struct LocalReleaseArchive {
    file: String,
    sha256: String,
}
#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct LocalReleaseSigning {
    algorithm: String,
    key_id: String,
}
#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct LocalTrustStore {
    api_version: String,
    kind: String,
    keys: Vec<LocalTrustKey>,
}
#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct LocalTrustKey {
    key_id: String,
    algorithm: String,
    public_key_file: String,
    status: String,
}
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct VerifiedReleaseEvidence {
    api_version: &'static str,
    status: &'static str,
    version: String,
    archive: String,
    archive_sha256: String,
    key_id: String,
}
#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct InstallerRequest {
    api_version: String,
    operation: String,
    root: PathBuf,
    distribution_path: Option<PathBuf>,
    #[serde(default)]
    profiles: Vec<String>,
    #[serde(default)]
    harnesses: Vec<String>,
    #[serde(default)]
    yes: bool,
}

#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct InstallationState {
    api_version: String,
    release: StateRelease,
    profiles: Vec<String>,
    harnesses: Vec<String>,
    owned_paths: Vec<OwnedPath>,
}
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct StateRelease {
    name: String,
    version: String,
    manifest_sha256: String,
}
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct OwnedPath {
    path: String,
    component: String,
    operation: String,
    ownership: String,
    installed_sha256: String,
}
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct Journal {
    api_version: String,
    transaction_id: String,
    operation: String,
    phase: String,
    old_state_sha256: Option<String>,
    new_state_sha256: Option<String>,
    actions: Vec<TransactionAction>,
}
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct TransactionAction {
    kind: String,
    #[serde(rename = "path")]
    target: String,
    old_sha256: Option<String>,
    new_sha256: Option<String>,
    staged_path: Option<String>,
    backup_path: Option<String>,
    created_parents: Vec<String>,
    ownership: String,
    applied: bool,
}
struct OperationLock {
    path: PathBuf,
}
impl Drop for OperationLock {
    fn drop(&mut self) {
        let _ = fs::remove_file(&self.path);
    }
}

fn safe_relative(value: &str) -> bool {
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
fn digest(path: &Path) -> Result<String, String> {
    let bytes = fs::read(path).map_err(|e| format!("{}: {e}", path.display()))?;
    Ok(format!("{:x}", Sha256::digest(bytes)))
}

fn verified_release(distribution_root: &Path) -> Result<VerifiedRelease, String> {
    let root_metadata = distribution_root
        .symlink_metadata()
        .map_err(|error| format!("release root: {error}"))?;
    if root_metadata.file_type().is_symlink() || !root_metadata.is_dir() {
        return Err("release root must be a non-symlink directory".into());
    }
    let descriptor_path = distribution_root.join(".processkit/installer/release-descriptor.json");
    ensure_regular_file(distribution_root, &descriptor_path, "release descriptor")?;
    let descriptor_bytes =
        fs::read(&descriptor_path).map_err(|error| format!("release descriptor: {error}"))?;
    let descriptor: ReleaseDescriptor = serde_json::from_slice(&descriptor_bytes)
        .map_err(|error| format!("release descriptor JSON: {error}"))?;
    if descriptor.api_version != API_VERSION || descriptor.kind != "ReleaseDescriptor" {
        return Err("unsupported release descriptor API or kind".into());
    }
    if descriptor.distribution.protocol != API_VERSION {
        return Err("release descriptor has unsupported installer protocol".into());
    }
    if descriptor.installer.requires.trim().is_empty()
        || descriptor.asset.layout != "single-top-level-directory"
    {
        return Err("release descriptor has invalid installer or asset contract".into());
    }
    if !safe_relative(&descriptor.distribution.manifest) {
        return Err("release descriptor manifest must be a safe relative path".into());
    }
    let manifest = distribution_root.join(&descriptor.distribution.manifest);
    ensure_regular_file(distribution_root, &manifest, "distribution manifest")?;
    let manifest_sha256 = digest(&manifest)?;
    if manifest_sha256 != descriptor.distribution.manifest_sha256 {
        return Err("release descriptor manifest SHA-256 mismatch".into());
    }
    let text = fs::read_to_string(&manifest).map_err(|error| format!("manifest: {error}"))?;
    let distribution: Distribution =
        serde_yaml::from_str(&text).map_err(|error| format!("manifest YAML: {error}"))?;
    if distribution.api_version != "processkit.projectious.work/distribution/v1alpha1"
        || distribution.kind != "Distribution"
        || distribution.spec.installer.protocol != descriptor.distribution.protocol
    {
        return Err("release descriptor and distribution manifest disagree".into());
    }
    for path in distribution
        .spec
        .catalogs
        .values()
        .chain(distribution.spec.harness_adapters.values())
    {
        if !safe_relative(path) {
            return Err("distribution references an unsafe catalog or adapter path".into());
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

fn ensure_regular_file(root: &Path, path: &Path, label: &str) -> Result<(), String> {
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
fn main() {
    let cli = Cli::parse();
    match cli.command {
        Command::Plan {
            root,
            distribution,
            profile,
            harness,
            dry_run,
            json,
            format,
        } => {
            let _ = dry_run;
            match plan(&root, &distribution, profile, harness) {
                Ok(plan) if json || matches!(format, OutputFormat::Json) => {
                    println!("{}", serde_json::to_string_pretty(&plan).unwrap())
                }
                Ok(plan) => {
                    println!(
                        "{} {}: {} change(s), {} conflict(s)",
                        plan.distribution.name,
                        plan.distribution.version,
                        plan.changes.len(),
                        plan.conflicts.len()
                    );
                    for change in plan.changes {
                        println!("{} {}", change.kind, change.destination);
                    }
                }
                Err(error) => {
                    eprintln!("processkit: {error}");
                    std::process::exit(3);
                }
            }
        }
        Command::Install {
            root,
            distribution,
            profile,
            harness,
            yes,
            json,
        } => match install(&root, &distribution, profile, harness, yes) {
            Ok(state) if json => println!("{}", serde_json::to_string_pretty(&state).unwrap()),
            Ok(state) => println!("installed {} {}", state.release.name, state.release.version),
            Err(error) => {
                eprintln!("processkit: {error}");
                std::process::exit(3);
            }
        },
        Command::Recover { root, yes, json } => match recover(&root, yes) {
            Ok(recovered) if json => println!("{{\"recovered\":{recovered}}}"),
            Ok(recovered) => println!("recovered {recovered} transaction(s)"),
            Err(error) => {
                eprintln!("processkit: {error}");
                std::process::exit(3);
            }
        },
        Command::Uninstall { root, yes, json } => match uninstall(&root, yes) {
            Ok(removed) if json => println!("{{\"removed\":{removed}}}"),
            Ok(removed) => println!("removed {removed} owned file(s)"),
            Err(error) => {
                eprintln!("processkit: {error}");
                std::process::exit(3);
            }
        },
        Command::Update {
            root,
            distribution,
            yes,
            json,
        } => match update(&root, &distribution, yes) {
            Ok(updated) if json => println!("{{\"updated\":{updated}}}"),
            Ok(updated) => println!("updated {updated} managed file(s)"),
            Err(error) => {
                eprintln!("processkit: {error}");
                std::process::exit(3);
            }
        },
        Command::VerifyRelease {
            envelope,
            signature,
            trust_store,
            json,
        } => match verify_local_release(&envelope, &signature, &trust_store) {
            Ok(evidence) if json => {
                println!("{}", serde_json::to_string_pretty(&evidence).unwrap())
            }
            Ok(evidence) => println!(
                "verified local release {} with key {}",
                evidence.version, evidence.key_id
            ),
            Err(error) => {
                eprintln!("processkit: {error}");
                std::process::exit(3);
            }
        },
        Command::Execute { request } => match execute_request(&request) {
            Ok(result) => println!("{}", serde_json::to_string_pretty(&result).unwrap()),
            Err(error) => {
                println!(
                    "{}",
                    serde_json::json!({
                        "apiVersion": API_VERSION,
                        "status": "invalid",
                        "changes": [],
                        "conflicts": [],
                        "warnings": [],
                        "errors": [{
                            "code": "request-failed",
                            "path": "",
                            "message": error,
                        }],
                    })
                );
                std::process::exit(3);
            }
        },
    }
}

fn execute_request(path: &Path) -> Result<serde_json::Value, String> {
    let bytes = fs::read(path).map_err(|error| format!("installer request: {error}"))?;
    let request: InstallerRequest = serde_json::from_slice(&bytes)
        .map_err(|error| format!("installer request JSON: {error}"))?;
    if request.api_version != API_VERSION {
        return Err("unsupported installer request API version".into());
    }
    let distribution = || {
        request
            .distribution_path
            .as_deref()
            .ok_or("operation requires distributionPath")
    };
    match request.operation.as_str() {
        "plan" => serde_json::to_value(plan(
            &request.root,
            distribution()?,
            request.profiles,
            request.harnesses,
        ))
        .map_err(|error| error.to_string()),
        "install" => {
            let state = install(
                &request.root,
                distribution()?,
                request.profiles,
                request.harnesses,
                request.yes,
            )?;
            Ok(serde_json::json!({
                "apiVersion": API_VERSION,
                "status": "installed",
                "changes": state.owned_paths.len(),
                "conflicts": [],
                "warnings": [],
                "errors": [],
                "state": state,
            }))
        }
        "update" => {
            let changed = update(&request.root, distribution()?, request.yes)?;
            Ok(success_result("updated", changed))
        }
        "uninstall" => {
            let changed = uninstall(&request.root, request.yes)?;
            Ok(success_result("uninstalled", changed))
        }
        "recover" => {
            let changed = recover(&request.root, request.yes)?;
            Ok(success_result("recovered", changed))
        }
        _ => Err(format!(
            "unsupported installer request operation: {}",
            request.operation
        )),
    }
}

fn success_result(status: &str, changes: usize) -> serde_json::Value {
    serde_json::json!({
        "apiVersion": API_VERSION,
        "status": status,
        "changes": changes,
        "conflicts": [],
        "warnings": [],
        "errors": [],
    })
}

fn verify_local_release(
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
        || !valid_sha256(&envelope.signing.key_id)
    {
        return Err("local release envelope contains an unsafe field".into());
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
    if digest(&archive_path)? != envelope.archive.sha256 {
        return Err("release archive digest mismatch".into());
    }
    Ok(VerifiedReleaseEvidence {
        api_version: API_VERSION,
        status: "verified",
        version: envelope.release.version,
        archive: envelope.archive.file,
        archive_sha256: envelope.archive.sha256,
        key_id: envelope.signing.key_id,
    })
}

fn valid_sha256(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|byte| byte.is_ascii_digit() || (b'a'..=b'f').contains(&byte))
}

fn plan(
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

struct PendingAction {
    action: TransactionAction,
    source: Option<PathBuf>,
    content: Option<Vec<u8>>,
}

fn transaction_id(operation: &str) -> String {
    use std::time::{SystemTime, UNIX_EPOCH};
    let nanos = SystemTime::now()
        .duration_since(UNIX_EPOCH)
        .unwrap_or_default()
        .as_nanos();
    format!("{operation}-{}-{nanos}", std::process::id())
}

fn execute_transaction(
    root: &Path,
    operation: &str,
    mut pending: Vec<PendingAction>,
    new_state: Option<&InstallationState>,
) -> Result<(), String> {
    let state_dir = root.join(".processkit");
    let transaction = transaction_id(operation);
    let staging = state_dir.join(".staging").join(&transaction);
    let new_dir = staging.join("new");
    let backup_dir = staging.join("backup");
    create_private_dir(&new_dir)?;
    create_private_dir(&backup_dir)?;

    let state_path = state_dir.join("state.json");
    let old_state_sha256 = state_path
        .is_file()
        .then(|| digest(&state_path))
        .transpose()?;
    let staged_state = staging.join("state.json");
    let new_state_sha256 = if let Some(state) = new_state {
        write_json_atomic(&staged_state, state)?;
        Some(digest(&staged_state)?)
    } else {
        None
    };

    for item in &mut pending {
        if !safe_relative(&item.action.target) || has_symlink_ancestor(root, &item.action.target)? {
            return Err(format!("unsafe transaction target: {}", item.action.target));
        }
        if item.source.is_some() || item.content.is_some() {
            let staged = new_dir.join(&item.action.target);
            if let Some(parent) = staged.parent() {
                fs::create_dir_all(parent).map_err(|error| error.to_string())?;
            }
            if let Some(source) = &item.source {
                fs::copy(source, &staged).map_err(|error| error.to_string())?;
            } else {
                fs::write(
                    &staged,
                    item.content
                        .as_ref()
                        .ok_or("transaction content is missing")?,
                )
                .map_err(|error| error.to_string())?;
            }
            let expected = item
                .action
                .new_sha256
                .as_ref()
                .ok_or("transaction write action lacks a new digest")?;
            if digest(&staged)? != *expected {
                return Err(format!("staged digest mismatch: {}", item.action.target));
            }
            item.action.staged_path = Some(
                staged
                    .strip_prefix(root)
                    .map_err(|_| "staged path escaped target root")?
                    .to_string_lossy()
                    .replace('\\', "/"),
            );
        }
        if item.action.old_sha256.is_some() {
            let backup = backup_dir.join(&item.action.target);
            item.action.backup_path = Some(
                backup
                    .strip_prefix(root)
                    .map_err(|_| "backup path escaped target root")?
                    .to_string_lossy()
                    .replace('\\', "/"),
            );
        }
    }

    let journal_path = state_dir
        .join("transactions")
        .join(format!("{transaction}.json"));
    let mut journal = Journal {
        api_version: API_VERSION.into(),
        transaction_id: transaction.clone(),
        operation: operation.into(),
        phase: "prepared".into(),
        old_state_sha256,
        new_state_sha256,
        actions: pending.into_iter().map(|item| item.action).collect(),
    };
    write_json_atomic(&journal_path, &journal)?;

    let apply_result = (|| -> Result<(), String> {
        journal.phase = "applying".into();
        write_json_atomic(&journal_path, &journal)?;
        for index in 0..journal.actions.len() {
            let action = &journal.actions[index];
            let target = root.join(&action.target);
            if let Some(expected) = &action.old_sha256 {
                if !target.is_file() || digest(&target)? != *expected {
                    return Err(format!(
                        "transaction target changed before apply: {}",
                        action.target
                    ));
                }
                let backup = root.join(
                    action
                        .backup_path
                        .as_ref()
                        .ok_or("transaction backup path is missing")?,
                );
                if let Some(parent) = backup.parent() {
                    fs::create_dir_all(parent).map_err(|error| error.to_string())?;
                }
                fs::rename(&target, backup).map_err(|error| error.to_string())?;
            } else if target.exists() {
                return Err(format!(
                    "transaction create target appeared: {}",
                    action.target
                ));
            }
            if action.kind != "remove" {
                let staged = root.join(
                    action
                        .staged_path
                        .as_ref()
                        .ok_or("transaction staged path is missing")?,
                );
                if let Some(parent) = target.parent() {
                    fs::create_dir_all(parent).map_err(|error| error.to_string())?;
                }
                fs::rename(staged, &target).map_err(|error| error.to_string())?;
            }
            if std::env::var("PROCESSKIT_INSTALLER_FAIL_AFTER_ACTION")
                .ok()
                .and_then(|value| value.parse::<usize>().ok())
                == Some(index)
            {
                std::process::exit(75);
            }
            journal.actions[index].applied = true;
            write_json_atomic(&journal_path, &journal)?;
        }
        journal.phase = "state-written".into();
        if new_state.is_some() {
            fs::rename(&staged_state, &state_path).map_err(|error| error.to_string())?;
        } else if state_path.exists() {
            fs::remove_file(&state_path).map_err(|error| error.to_string())?;
        }
        write_json_atomic(&journal_path, &journal)?;
        journal.phase = "committed".into();
        write_json_atomic(&journal_path, &journal)
    })();

    if let Err(error) = apply_result {
        rollback_journal(root, &journal)?;
        let _ = fs::remove_file(&journal_path);
        let _ = fs::remove_dir_all(&staging);
        return Err(error);
    }
    fs::remove_file(&journal_path).map_err(|error| error.to_string())?;
    fs::remove_dir_all(&staging).map_err(|error| error.to_string())?;
    Ok(())
}

fn rollback_journal(root: &Path, journal: &Journal) -> Result<(), String> {
    for action in journal.actions.iter().rev() {
        let target = root.join(&action.target);
        let backup = action.backup_path.as_ref().map(|path| root.join(path));
        let was_applied = action.applied
            || backup.as_ref().is_some_and(|path| path.exists())
            || action.new_sha256.as_ref().is_some_and(|expected| {
                target.is_file() && digest(&target).ok().as_ref() == Some(expected)
            });
        if !was_applied {
            continue;
        }
        if target.exists() {
            if action.kind == "remove" {
                return Err(format!(
                    "manual recovery required: removed target reappeared: {}",
                    action.target
                ));
            }
            let expected = action
                .new_sha256
                .as_ref()
                .ok_or("manual recovery required: missing new digest")?;
            if !target.is_file() || digest(&target)? != *expected {
                return Err(format!(
                    "manual recovery required: applied target changed: {}",
                    action.target
                ));
            }
            fs::remove_file(&target).map_err(|error| error.to_string())?;
        }
        if let Some(backup) = backup {
            if backup.exists() {
                if let Some(parent) = target.parent() {
                    fs::create_dir_all(parent).map_err(|error| error.to_string())?;
                }
                fs::rename(backup, target).map_err(|error| error.to_string())?;
            }
        }
    }
    Ok(())
}

fn install(
    root: &Path,
    distribution: &Path,
    profiles: Vec<String>,
    harnesses: Vec<String>,
    yes: bool,
) -> Result<InstallationState, String> {
    if !yes {
        return Err("install requires --yes after reviewing a plan".into());
    }
    if !root.exists() {
        fs::create_dir_all(root).map_err(|error| format!("create target root: {error}"))?;
    }
    if root
        .symlink_metadata()
        .map_err(|error| format!("target root: {error}"))?
        .file_type()
        .is_symlink()
    {
        return Err("target root must not be a symlink".into());
    }
    let plan = plan(root, distribution, profiles, harnesses)?;
    if plan.status != "planned" {
        return Err("install plan is not safe to apply; resolve conflicts first".into());
    }
    let state_dir = root.join(".processkit");
    if state_dir.exists()
        && state_dir
            .symlink_metadata()
            .map_err(|error| format!("installer state directory: {error}"))?
            .file_type()
            .is_symlink()
    {
        return Err("installer state directory must not be a symlink".into());
    }
    fs::create_dir_all(state_dir.join("transactions"))
        .map_err(|error| format!("create installer state directory: {error}"))?;
    let state_path = state_dir.join("state.json");
    if state_path.exists() {
        return Err("target already has processkit installation state; use update".into());
    }
    let _lock = acquire_lock(root, "install")?;
    let mut pending = Vec::new();
    let mut owned_paths = Vec::new();
    for change in &plan.changes {
        if change.kind == "create" {
            pending.push(PendingAction {
                action: TransactionAction {
                    kind: "create".into(),
                    target: change.destination.clone(),
                    old_sha256: None,
                    new_sha256: Some(change.source_sha256.clone()),
                    staged_path: None,
                    backup_path: None,
                    created_parents: Vec::new(),
                    ownership: change.ownership.clone(),
                    applied: false,
                },
                source: Some(change.source.clone()),
                content: None,
            });
            owned_paths.push(OwnedPath {
                path: change.destination.clone(),
                component: change.component.clone(),
                operation: change.operation.clone(),
                ownership: change.ownership.clone(),
                installed_sha256: change.source_sha256.clone(),
            });
        }
    }
    for (action, owned) in adapter_actions(root, distribution, &plan.harnesses, false)? {
        pending.push(action);
        owned_paths.push(owned);
    }
    let state = InstallationState {
        api_version: API_VERSION.into(),
        release: StateRelease {
            name: plan.distribution.name,
            version: plan.distribution.version,
            manifest_sha256: plan.distribution.manifest_sha256,
        },
        profiles: plan.selected_profiles,
        harnesses: plan.harnesses,
        owned_paths,
    };
    execute_transaction(root, "install", pending, Some(&state))?;
    Ok(state)
}

fn adapter_actions(
    root: &Path,
    distribution_root: &Path,
    harnesses: &[String],
    updating: bool,
) -> Result<Vec<(PendingAction, OwnedPath)>, String> {
    let verified = verified_release(distribution_root)?;
    let mut actions = Vec::new();
    for harness in harnesses {
        let adapter_relative = verified
            .distribution
            .spec
            .harness_adapters
            .get(harness)
            .ok_or_else(|| format!("unknown harness adapter: {harness}"))?;
        let adapter_path = distribution_root.join(adapter_relative);
        let adapter: HarnessAdapter = serde_yaml::from_slice(
            &fs::read(&adapter_path).map_err(|error| format!("harness adapter: {error}"))?,
        )
        .map_err(|error| format!("harness adapter YAML: {error}"))?;
        if adapter.api_version != API_VERSION
            || adapter.kind != "HarnessAdapter"
            || adapter.id != *harness
            || adapter.format != "json"
            || adapter.ownership != "managed-keys"
            || !safe_relative(&adapter.destination)
            || !safe_relative(&adapter.catalog)
        {
            return Err(format!("unsupported harness adapter contract: {harness}"));
        }
        let catalog_path = distribution_root.join(&adapter.catalog);
        ensure_regular_file(distribution_root, &catalog_path, "MCP catalog")?;
        let catalog: McpCatalog = serde_yaml::from_slice(
            &fs::read(&catalog_path).map_err(|error| format!("MCP catalog: {error}"))?,
        )
        .map_err(|error| format!("MCP catalog YAML: {error}"))?;
        if catalog.api_version != API_VERSION || catalog.kind != "McpCatalog" {
            return Err("unsupported MCP catalog contract".into());
        }
        let target = root.join(&adapter.destination);
        let old_sha256 = target.is_file().then(|| digest(&target)).transpose()?;
        let config_existed = old_sha256.is_some();
        let mut document = if target.exists() {
            if target
                .symlink_metadata()
                .map_err(|error| error.to_string())?
                .file_type()
                .is_symlink()
            {
                return Err(format!(
                    "harness config is a symlink: {}",
                    adapter.destination
                ));
            }
            serde_json::from_slice::<serde_json::Value>(
                &fs::read(&target).map_err(|error| error.to_string())?,
            )
            .map_err(|error| format!("harness config JSON: {error}"))?
        } else {
            serde_json::json!({})
        };
        let object = document
            .as_object_mut()
            .ok_or("harness config root must be a JSON object")?;
        let servers = object
            .entry("mcpServers")
            .or_insert_with(|| serde_json::json!({}))
            .as_object_mut()
            .ok_or("harness mcpServers must be a JSON object")?;
        for server in catalog.servers {
            let server_value = serde_json::json!({
                "command": server.command,
                "args": server.args,
                "env": server.env,
            });
            if let Some(existing) = servers.get(&server.id) {
                if existing != &server_value && !updating {
                    return Err(format!(
                        "harness config already defines managed server: {}",
                        server.id
                    ));
                }
            }
            servers.insert(server.id, server_value);
        }
        let mut content =
            serde_json::to_vec_pretty(&document).map_err(|error| error.to_string())?;
        content.push(b'\n');
        let new_sha256 = format!("{:x}", Sha256::digest(&content));
        actions.push((
            PendingAction {
                action: TransactionAction {
                    kind: if config_existed {
                        "replace".into()
                    } else {
                        "create".into()
                    },
                    target: adapter.destination.clone(),
                    old_sha256,
                    new_sha256: Some(new_sha256.clone()),
                    staged_path: None,
                    backup_path: None,
                    created_parents: Vec::new(),
                    ownership: "managed-keys".into(),
                    applied: false,
                },
                source: None,
                content: Some(content),
            },
            OwnedPath {
                path: adapter.destination,
                component: format!("harness-adapter:{harness}"),
                operation: if config_existed {
                    "managed-keys-merge/v1".into()
                } else {
                    "managed-keys-create/v1".into()
                },
                ownership: "managed-keys".into(),
                installed_sha256: new_sha256,
            },
        ));
    }
    Ok(actions)
}

fn recover(root: &Path, yes: bool) -> Result<usize, String> {
    if !yes {
        return Err("recovery requires --yes because it can remove staged files".into());
    }
    clear_stale_lock_for_recovery(root)?;
    let _lock = acquire_lock(root, "recover")?;
    let state_dir = root.join(".processkit");
    let transactions = state_dir.join("transactions");
    if !transactions.is_dir() {
        return Ok(0);
    }
    if state_dir
        .symlink_metadata()
        .map_err(|error| format!("installer state directory: {error}"))?
        .file_type()
        .is_symlink()
    {
        return Err("installer state directory must not be a symlink".into());
    }
    let mut recovered = 0;
    for entry in fs::read_dir(&transactions).map_err(|error| error.to_string())? {
        let entry = entry.map_err(|error| error.to_string())?;
        let journal_path = entry.path();
        if journal_path.extension().and_then(|value| value.to_str()) != Some("json") {
            continue;
        }
        let journal: Journal =
            serde_json::from_slice(&fs::read(&journal_path).map_err(|error| error.to_string())?)
                .map_err(|error| {
                    format!(
                        "invalid transaction journal {}: {error}",
                        journal_path.display()
                    )
                })?;
        if journal.api_version != API_VERSION {
            return Err(format!(
                "unsupported transaction journal: {}",
                journal_path.display()
            ));
        }
        let transaction = journal_path
            .file_stem()
            .and_then(|value| value.to_str())
            .ok_or("transaction journal has no safe name")?;
        if !safe_relative(transaction) {
            return Err("transaction journal has an unsafe name".into());
        }
        if journal.transaction_id != transaction || !safe_relative(&journal.transaction_id) {
            return Err("transaction journal identity does not match its filename".into());
        }
        let state_path = state_dir.join("state.json");
        let state_sha256 = state_path
            .is_file()
            .then(|| digest(&state_path))
            .transpose()?;
        let state_is_new = state_sha256 == journal.new_state_sha256;
        let state_is_old = state_sha256 == journal.old_state_sha256;
        if journal.phase == "committed" || state_is_new {
            fs::remove_file(&journal_path).map_err(|error| error.to_string())?;
            let _ = fs::remove_dir_all(state_dir.join(".staging").join(transaction));
            recovered += 1;
            continue;
        }
        if !state_is_old {
            return Err(
                "manual recovery required: installation state matches neither transaction side"
                    .into(),
            );
        }
        rollback_journal(root, &journal)?;
        fs::remove_file(&journal_path).map_err(|error| error.to_string())?;
        let _ = fs::remove_dir_all(state_dir.join(".staging").join(transaction));
        recovered += 1;
    }
    Ok(recovered)
}

fn uninstall(root: &Path, yes: bool) -> Result<usize, String> {
    if !yes {
        return Err("uninstall requires --yes because it removes owned files".into());
    }
    let _lock = acquire_lock(root, "uninstall")?;
    let state_path = root.join(".processkit/state.json");
    let mut state: InstallationState = serde_json::from_slice(
        &fs::read(&state_path).map_err(|error| format!("installer state: {error}"))?,
    )
    .map_err(|error| format!("invalid installer state: {error}"))?;
    if state.api_version != API_VERSION {
        return Err("unsupported installer state version".into());
    }
    let removable: Vec<&OwnedPath> = state
        .owned_paths
        .iter()
        .filter(|path| path.ownership == "managed-three-way")
        .collect();
    for path in &removable {
        if !safe_relative(&path.path) || has_symlink_ancestor(root, &path.path)? {
            return Err("uninstall refused an unsafe owned path".into());
        }
        let target = root.join(&path.path);
        if !target.is_file()
            || target
                .symlink_metadata()
                .map_err(|error| error.to_string())?
                .file_type()
                .is_symlink()
            || digest(&target)? != path.installed_sha256
        {
            return Err(format!(
                "uninstall conflict: owned file was changed or missing: {}",
                path.path
            ));
        }
    }
    let mut pending: Vec<PendingAction> = removable
        .iter()
        .map(|path| PendingAction {
            action: TransactionAction {
                kind: "remove".into(),
                target: path.path.clone(),
                old_sha256: Some(path.installed_sha256.clone()),
                new_sha256: None,
                staged_path: None,
                backup_path: None,
                created_parents: Vec::new(),
                ownership: path.ownership.clone(),
                applied: false,
            },
            source: None,
            content: None,
        })
        .collect();
    let adapters: Vec<&OwnedPath> = state
        .owned_paths
        .iter()
        .filter(|path| path.ownership == "managed-keys")
        .collect();
    for adapter in &adapters {
        if !safe_relative(&adapter.path) || has_symlink_ancestor(root, &adapter.path)? {
            return Err("uninstall refused an unsafe adapter path".into());
        }
        let target = root.join(&adapter.path);
        if !target.is_file() {
            return Err(format!("uninstall adapter is missing: {}", adapter.path));
        }
        let current_sha256 = digest(&target)?;
        if adapter.operation == "managed-keys-create/v1"
            && current_sha256 == adapter.installed_sha256
        {
            pending.push(PendingAction {
                action: TransactionAction {
                    kind: "remove".into(),
                    target: adapter.path.clone(),
                    old_sha256: Some(current_sha256),
                    new_sha256: None,
                    staged_path: None,
                    backup_path: None,
                    created_parents: Vec::new(),
                    ownership: adapter.ownership.clone(),
                    applied: false,
                },
                source: None,
                content: None,
            });
            continue;
        }
        let mut document: serde_json::Value =
            serde_json::from_slice(&fs::read(&target).map_err(|error| error.to_string())?)
                .map_err(|error| format!("harness config JSON: {error}"))?;
        let servers = document
            .get_mut("mcpServers")
            .and_then(serde_json::Value::as_object_mut)
            .ok_or("managed harness config no longer has mcpServers")?;
        let managed = servers
            .get("processkit-gateway")
            .ok_or("managed processkit gateway key is missing")?;
        if managed
            .get("env")
            .and_then(|env| env.get("PROCESSKIT_MCP_MODE"))
            .and_then(serde_json::Value::as_str)
            != Some("gateway")
        {
            return Err("managed processkit gateway key was changed".into());
        }
        servers.remove("processkit-gateway");
        if servers.is_empty() {
            document
                .as_object_mut()
                .ok_or("harness config root must be an object")?
                .remove("mcpServers");
        }
        let mut content =
            serde_json::to_vec_pretty(&document).map_err(|error| error.to_string())?;
        content.push(b'\n');
        let new_sha256 = format!("{:x}", Sha256::digest(&content));
        pending.push(PendingAction {
            action: TransactionAction {
                kind: "replace".into(),
                target: adapter.path.clone(),
                old_sha256: Some(current_sha256),
                new_sha256: Some(new_sha256),
                staged_path: None,
                backup_path: None,
                created_parents: Vec::new(),
                ownership: adapter.ownership.clone(),
                applied: false,
            },
            source: None,
            content: Some(content),
        });
    }
    let removed = removable.len() + adapters.len();
    state.owned_paths.retain(|path| {
        !matches!(
            path.ownership.as_str(),
            "managed-three-way" | "managed-keys"
        )
    });
    if state.owned_paths.is_empty() {
        execute_transaction(root, "uninstall", pending, None)?;
    } else {
        execute_transaction(root, "uninstall", pending, Some(&state))?;
    }
    Ok(removed)
}

fn update(root: &Path, distribution: &Path, yes: bool) -> Result<usize, String> {
    if !yes {
        return Err("update requires --yes after reviewing a plan".into());
    }
    let _lock = acquire_lock(root, "update")?;
    let state_path = root.join(".processkit/state.json");
    let mut old: InstallationState = serde_json::from_slice(
        &fs::read(&state_path).map_err(|error| format!("installer state: {error}"))?,
    )
    .map_err(|error| format!("invalid installer state: {error}"))?;
    if old.api_version != API_VERSION {
        return Err("unsupported installer state version".into());
    }
    let virtual_root = root
        .join(".processkit/.staging")
        .join(format!("update-plan-{}", std::process::id()));
    let desired = plan(
        &virtual_root,
        distribution,
        old.profiles.clone(),
        old.harnesses.clone(),
    )?;
    if desired.status != "planned" {
        return Err("new release cannot be planned safely".into());
    }
    let old_version = semver::Version::parse(old.release.version.trim_start_matches('v'))
        .map_err(|error| format!("installed release version is invalid: {error}"))?;
    let new_version = semver::Version::parse(desired.distribution.version.trim_start_matches('v'))
        .map_err(|error| format!("new release version is invalid: {error}"))?;
    if new_version < old_version {
        return Err("update refused a release downgrade".into());
    }
    if new_version == old_version
        && desired.distribution.manifest_sha256 != old.release.manifest_sha256
    {
        return Err("update refused same-version release equivocation".into());
    }
    let mut desired_by_path = std::collections::BTreeMap::new();
    for change in desired
        .changes
        .into_iter()
        .filter(|change| change.ownership == "managed-three-way")
    {
        desired_by_path.insert(change.destination.clone(), change);
    }
    let mut replacements = Vec::new();
    for owned in old
        .owned_paths
        .iter()
        .filter(|path| path.ownership == "managed-three-way")
    {
        let target = root.join(&owned.path);
        if !safe_relative(&owned.path)
            || has_symlink_ancestor(root, &owned.path)?
            || !target.is_file()
            || digest(&target)? != owned.installed_sha256
        {
            return Err(format!(
                "update conflict: managed file was changed or missing: {}",
                owned.path
            ));
        }
        match desired_by_path.remove(&owned.path) {
            Some(change) if change.source_sha256 != owned.installed_sha256 => {
                replacements.push(change)
            }
            Some(_) => {}
            None => {
                return Err(format!(
                    "update requires explicit removal policy: {}",
                    owned.path
                ))
            }
        }
    }
    let additions: Vec<Change> = desired_by_path.into_values().collect();
    for change in &additions {
        if root.join(&change.destination).exists()
            || has_symlink_ancestor(root, &change.destination)?
        {
            return Err(format!(
                "update conflict: target exists: {}",
                change.destination
            ));
        }
    }
    let changed = replacements.len() + additions.len();
    let mut pending = Vec::new();
    for change in replacements.iter().chain(additions.iter()) {
        if digest(&change.source)? != change.source_sha256 {
            return Err("release source changed during update".into());
        }
        let old_sha256 = old
            .owned_paths
            .iter()
            .find(|owned| owned.path == change.destination)
            .map(|owned| owned.installed_sha256.clone());
        pending.push(PendingAction {
            action: TransactionAction {
                kind: if old_sha256.is_some() {
                    "replace".into()
                } else {
                    "create".into()
                },
                target: change.destination.clone(),
                old_sha256,
                new_sha256: Some(change.source_sha256.clone()),
                staged_path: None,
                backup_path: None,
                created_parents: Vec::new(),
                ownership: change.ownership.clone(),
                applied: false,
            },
            source: Some(change.source.clone()),
            content: None,
        });
    }
    for owned in &mut old.owned_paths {
        if let Some(change) = replacements
            .iter()
            .find(|change| change.destination == owned.path)
        {
            owned.installed_sha256 = change.source_sha256.clone();
            owned.component = change.component.clone();
            owned.operation = change.operation.clone();
        }
    }
    for change in &additions {
        old.owned_paths.push(OwnedPath {
            path: change.destination.clone(),
            component: change.component.clone(),
            operation: change.operation.clone(),
            ownership: change.ownership.clone(),
            installed_sha256: change.source_sha256.clone(),
        });
    }
    for adapter in old
        .owned_paths
        .iter()
        .filter(|path| path.ownership == "managed-keys")
    {
        let target = root.join(&adapter.path);
        if !target.is_file() || digest(&target)? != adapter.installed_sha256 {
            return Err(format!(
                "update conflict: managed harness config changed: {}",
                adapter.path
            ));
        }
    }
    let adapter_changes = adapter_actions(root, distribution, &old.harnesses, true)?;
    old.owned_paths
        .retain(|path| path.ownership != "managed-keys");
    for (action, owned) in adapter_changes {
        pending.push(action);
        old.owned_paths.push(owned);
    }
    let new_state = InstallationState {
        api_version: API_VERSION.into(),
        release: StateRelease {
            name: desired.distribution.name,
            version: desired.distribution.version,
            manifest_sha256: desired.distribution.manifest_sha256,
        },
        profiles: old.profiles,
        harnesses: old.harnesses,
        owned_paths: old.owned_paths,
    };
    execute_transaction(root, "update", pending, Some(&new_state))?;
    Ok(changed)
}

fn acquire_lock(root: &Path, operation: &str) -> Result<OperationLock, String> {
    let state_dir = root.join(".processkit");
    create_private_dir(&state_dir)?;
    let lock_path = state_dir.join("lock");
    let mut options = OpenOptions::new();
    options.write(true).create_new(true);
    #[cfg(unix)]
    options.mode(0o600);
    let mut lock = options
        .open(&lock_path)
        .map_err(|_| "another processkit operation is already in progress")?;
    writeln!(lock, "{operation}:{}", std::process::id()).map_err(|error| error.to_string())?;
    lock.sync_all().map_err(|error| error.to_string())?;
    Ok(OperationLock { path: lock_path })
}

fn clear_stale_lock_for_recovery(root: &Path) -> Result<(), String> {
    let lock_path = root.join(".processkit/lock");
    if !lock_path.exists() {
        return Ok(());
    }
    let value = fs::read_to_string(&lock_path).map_err(|error| error.to_string())?;
    let pid = value
        .trim()
        .rsplit(':')
        .next()
        .and_then(|item| item.parse::<u32>().ok())
        .ok_or("manual recovery required: malformed operation lock")?;
    if Path::new("/proc").join(pid.to_string()).exists() {
        return Err("another processkit operation is still running".into());
    }
    fs::remove_file(lock_path).map_err(|error| error.to_string())
}

fn write_json_atomic<T: Serialize>(path: &Path, value: &T) -> Result<(), String> {
    let parent = path.parent().ok_or("state path has no parent")?;
    create_private_dir(parent)?;
    let temporary = parent.join(format!(
        ".{}.tmp-{}",
        path.file_name().unwrap().to_string_lossy(),
        std::process::id()
    ));
    let bytes = serde_json::to_vec_pretty(value).map_err(|error| error.to_string())?;
    let mut options = OpenOptions::new();
    options.write(true).create_new(true);
    #[cfg(unix)]
    options.mode(0o600);
    let mut file = options
        .open(&temporary)
        .map_err(|error| error.to_string())?;
    file.write_all(&bytes).map_err(|error| error.to_string())?;
    file.sync_all().map_err(|error| error.to_string())?;
    fs::rename(&temporary, path).map_err(|error| error.to_string())?;
    sync_directory(parent)
}

fn create_private_dir(path: &Path) -> Result<(), String> {
    fs::create_dir_all(path).map_err(|error| error.to_string())?;
    #[cfg(unix)]
    fs::set_permissions(path, fs::Permissions::from_mode(0o700))
        .map_err(|error| error.to_string())?;
    Ok(())
}

fn sync_directory(path: &Path) -> Result<(), String> {
    let directory = fs::File::open(path).map_err(|error| error.to_string())?;
    directory.sync_all().map_err(|error| error.to_string())
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

fn has_symlink_ancestor(root: &Path, destination: &str) -> Result<bool, String> {
    let mut current = root.to_path_buf();
    if current.exists()
        && current
            .symlink_metadata()
            .map_err(|error| error.to_string())?
            .file_type()
            .is_symlink()
    {
        return Ok(true);
    }
    for component in Path::new(destination).components() {
        if let Component::Normal(segment) = component {
            current.push(segment);
            if !current.exists() {
                break;
            }
            if current
                .symlink_metadata()
                .map_err(|error| error.to_string())?
                .file_type()
                .is_symlink()
            {
                return Ok(true);
            }
        }
    }
    Ok(false)
}

#[cfg(test)]
mod tests {
    use super::safe_relative;
    #[test]
    fn rejects_escaping_paths() {
        assert!(safe_relative("context/skills"));
        assert!(!safe_relative("../context"));
        assert!(!safe_relative("/context"));
        assert!(!safe_relative("context\\skills"));
        assert!(!safe_relative(""));
    }
}
