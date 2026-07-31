use clap::{ArgAction, Parser, Subcommand, ValueEnum};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::{BTreeMap, HashSet};
use std::fs;
use std::fs::OpenOptions;
use std::io::Write;
#[cfg(unix)]
use std::os::unix::fs::{OpenOptionsExt, PermissionsExt};
use std::path::{Component, Path, PathBuf};

mod compatibility;
mod contract;
mod error;
mod filesystem;
mod mcp_runtime;
mod migration;
mod output;
mod planner;
mod release;
mod request;
mod runtime;
mod signed_release;
mod state;
mod transaction;

use compatibility::inspect_compatibility;
use contract::API_VERSION;
use filesystem::{digest, ensure_non_symlink_directory, ensure_regular_file, safe_relative};
use mcp_runtime::{prepare_runtime, proxy_mcp, serve_mcp, verify_mcp, McpTransport};
use migration::plan_v0_corpus;
use output::pretty_json;
use planner::{plan, Change};
use release::verified_release;
use request::execute_request;
use runtime::run_doctor;
use signed_release::verify_local_release;
use state::{
    validate_installation_state, InstallationState, ManagedAdapterState, MigrationEvidence,
    OwnedPath, StateRelease,
};
use transaction::{
    execute_transaction, rollback_journal, validate_recovery_journal, Journal, PendingAction,
    TransactionAction,
};

#[derive(Parser)]
#[command(
    name = "processkit",
    version,
    about = "Native lifecycle CLI for processkit projects"
)]
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
    /// Verify installed provenance and report managed-path drift.
    Verify {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Inspect a legacy processkit tree without mutating it.
    InspectCompatibility {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long)]
        distribution: PathBuf,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Transition an exact v0 release into a fresh v1 target.
    MigrateV0 {
        #[arg(long)]
        source: PathBuf,
        #[arg(long)]
        root: PathBuf,
        #[arg(long)]
        distribution: PathBuf,
        #[arg(long, default_value = "managed")]
        profile: Vec<String>,
        #[arg(long)]
        harness: Vec<String>,
        /// Emit compatibility and corpus evidence without installing.
        #[arg(long, action = ArgAction::SetTrue)]
        plan_only: bool,
        /// Required acknowledgement for filesystem mutation.
        #[arg(long)]
        yes: bool,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Diagnose the installed project and Python MCP runtime without mutation.
    Doctor {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long)]
        category: Option<String>,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Verify or supervise the shipped Python MCP gateway.
    Mcp {
        #[command(subcommand)]
        command: McpCommand,
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

#[derive(Subcommand)]
enum McpCommand {
    /// Verify the gateway path and uv runtime without starting a server.
    Verify {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Resolve dependency profiles or verify an existing cache offline.
    Prepare {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long)]
        cache_dir: Option<PathBuf>,
        /// Prohibit network access and fail unless every profile is cached.
        #[arg(long, action = ArgAction::SetTrue)]
        offline: bool,
        #[arg(long, action = ArgAction::SetTrue)]
        json: bool,
    },
    /// Run the Python gateway under native process supervision.
    Serve {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long, value_enum, default_value_t = McpTransportArg::Stdio)]
        transport: McpTransportArg,
        #[arg(long, default_value = "127.0.0.1")]
        host: String,
        #[arg(long, default_value_t = 8000)]
        port: u16,
        #[arg(long, default_value = "/mcp")]
        path: String,
    },
    /// Bridge stdio to a loopback streamable-HTTP gateway.
    Proxy {
        #[arg(long, default_value = ".")]
        root: PathBuf,
        #[arg(long)]
        url: String,
    },
}

#[derive(Clone, Copy, ValueEnum)]
enum McpTransportArg {
    Stdio,
    StreamableHttp,
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
    #[serde(default)]
    compatibility: Vec<String>,
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

struct OperationLock {
    path: PathBuf,
}
impl Drop for OperationLock {
    fn drop(&mut self) {
        let _ = fs::remove_file(&self.path);
    }
}

fn print_json_or_exit<T: Serialize>(value: &T) {
    match pretty_json(value) {
        Ok(rendered) => println!("{rendered}"),
        Err(error) => {
            eprintln!("processkit: {error}");
            std::process::exit(error.exit_code());
        }
    }
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
                    print_json_or_exit(&plan)
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
            Ok(state) if json => print_json_or_exit(&state),
            Ok(state) => println!("installed {} {}", state.release.name, state.release.version),
            Err(error) => {
                eprintln!("processkit: {error}");
                std::process::exit(3);
            }
        },
        Command::Recover { root, yes, json } => match recover(&root, yes) {
            Ok(recovered) if json => println!(
                "{}",
                serde_json::json!({
                    "apiVersion": API_VERSION,
                    "status": if recovered == 0 { "clean" } else { "recovered" },
                    "recovered": recovered,
                    "errors": [],
                })
            ),
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
            Ok(evidence) if json => print_json_or_exit(&evidence),
            Ok(evidence) => println!(
                "verified local release {} with key {}",
                evidence.version, evidence.key_id
            ),
            Err(error) => {
                eprintln!("processkit: {error}");
                std::process::exit(3);
            }
        },
        Command::Verify { root, json } => match verify_installation(&root) {
            Ok(result) => {
                if json {
                    print_json_or_exit(&result);
                } else {
                    println!(
                        "{}: {} checked path(s), {} drift finding(s)",
                        result["status"].as_str().unwrap_or("invalid"),
                        result["checked"].as_u64().unwrap_or(0),
                        result["errors"].as_array().map_or(0, Vec::len)
                    );
                }
                if result["status"] != "verified" {
                    std::process::exit(4);
                }
            }
            Err(error) => {
                eprintln!("processkit: {error}");
                std::process::exit(3);
            }
        },
        Command::InspectCompatibility {
            root,
            distribution,
            json,
        } => match inspect_compatibility(&root, &distribution) {
            Ok(result) => {
                if json {
                    print_json_or_exit(&result);
                } else {
                    println!("{}", result["status"].as_str().unwrap_or("not-detected"));
                }
            }
            Err(error) => {
                eprintln!("processkit: {error}");
                std::process::exit(3);
            }
        },
        Command::MigrateV0 {
            source,
            root,
            distribution,
            profile,
            harness,
            plan_only,
            yes,
            json,
        } => match migrate_v0(
            &source,
            &root,
            &distribution,
            profile,
            harness,
            plan_only,
            yes,
        ) {
            Ok(result) if json => print_json_or_exit(&result),
            Ok(result) if result["status"] == "transitioned-to-fresh-target" => {
                println!(
                    "transitioned {} into fresh v1 target {}",
                    result["source"]["releaseVersion"]
                        .as_str()
                        .unwrap_or("unknown"),
                    result["target"]["root"].as_str().unwrap_or("unknown")
                )
            }
            Ok(result) => println!(
                "v0 migration plan: {}",
                result["status"].as_str().unwrap_or("blocked")
            ),
            Err(error) => {
                eprintln!("processkit: {error}");
                std::process::exit(3);
            }
        },
        Command::Doctor {
            root,
            category,
            json,
        } => match run_doctor(&root, category.as_deref()) {
            Ok(result) => {
                let has_errors = result.has_errors();
                if json {
                    print_json_or_exit(&result);
                } else {
                    println!("{}", result.summary());
                }
                if has_errors {
                    std::process::exit(1);
                }
            }
            Err(error) => {
                if json {
                    print_json_or_exit(&serde_json::json!({
                        "apiVersion": "processkit.projectious.work/runtime/v1alpha1",
                        "kind": "DoctorResult",
                        "status": "unavailable",
                        "errors": [{
                            "code": "runtime-unavailable",
                            "message": error,
                        }],
                    }));
                } else {
                    eprintln!("processkit: {error}");
                }
                std::process::exit(3);
            }
        },
        Command::Mcp { command } => match command {
            McpCommand::Verify { root, json } => match verify_mcp(&root) {
                Ok(result) if json => print_json_or_exit(&result),
                Ok(result) => println!("{}", result.summary()),
                Err(error) => {
                    eprintln!("processkit: {error}");
                    std::process::exit(3);
                }
            },
            McpCommand::Prepare {
                root,
                cache_dir,
                offline,
                json,
            } => match prepare_runtime(&root, cache_dir.as_deref(), offline) {
                Ok(result) if json => print_json_or_exit(&result),
                Ok(result) => println!("{}", result.summary()),
                Err(error) => {
                    eprintln!("processkit: {error}");
                    std::process::exit(3);
                }
            },
            McpCommand::Serve {
                root,
                transport,
                host,
                port,
                path,
            } => {
                let transport = match transport {
                    McpTransportArg::Stdio => McpTransport::Stdio,
                    McpTransportArg::StreamableHttp => McpTransport::StreamableHttp,
                };
                match serve_mcp(&root, transport, &host, port, &path) {
                    Ok(0) => {}
                    Ok(code) => std::process::exit(code),
                    Err(error) => {
                        eprintln!("processkit: {error}");
                        std::process::exit(3);
                    }
                }
            }
            McpCommand::Proxy { root, url } => match proxy_mcp(&root, &url) {
                Ok(0) => {}
                Ok(code) => std::process::exit(code),
                Err(error) => {
                    eprintln!("processkit: {error}");
                    std::process::exit(3);
                }
            },
        },
        Command::Execute { request } => match execute_request(&request) {
            Ok(result) => print_json_or_exit(&result),
            Err(error) => {
                println!(
                    "{}",
                    serde_json::json!({
                        "apiVersion": API_VERSION,
                        "status": "invalid",
                        "changes": [],
                        "conflicts": [],
                        "warnings": [],
                        "errors": [error.request_problem()],
                    })
                );
                std::process::exit(error.exit_code());
            }
        },
    }
}

fn verify_installation(root: &Path) -> Result<serde_json::Value, String> {
    let state_dir = root.join(".processkit");
    if state_dir
        .symlink_metadata()
        .map_err(|error| format!("installer state directory: {error}"))?
        .file_type()
        .is_symlink()
    {
        return Err("installer state directory must not be a symlink".into());
    }
    let state_path = state_dir.join("state.json");
    ensure_regular_file(root, &state_path, "installer state")?;
    let state: InstallationState = serde_json::from_slice(
        &fs::read(&state_path).map_err(|error| format!("installer state: {error}"))?,
    )
    .map_err(|error| format!("invalid installer state: {error}"))?;
    validate_installation_state(&state)?;

    let mut findings = Vec::new();
    let migrated_count: usize = state
        .migration_evidence
        .iter()
        .map(|evidence| evidence.entry_count)
        .sum();
    for evidence in &state.migration_evidence {
        findings.extend(evidence.plan.verify_applied(root)?);
    }
    for owned in &state.owned_paths {
        let target = root.join(&owned.path);
        if has_symlink_ancestor(root, &owned.path)? {
            findings.push(serde_json::json!({
                "code": "symlink-drift",
                "path": owned.path,
                "message": "managed path or ancestor is a symlink",
            }));
            continue;
        }
        let metadata = match target.symlink_metadata() {
            Ok(metadata) => metadata,
            Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
                findings.push(serde_json::json!({
                    "code": "missing-managed-path",
                    "path": owned.path,
                    "message": "managed path is missing",
                }));
                continue;
            }
            Err(error) => return Err(format!("managed path metadata: {error}")),
        };
        if metadata.file_type().is_symlink() || !metadata.is_file() {
            findings.push(serde_json::json!({
                "code": "non-regular-managed-path",
                "path": owned.path,
                "message": "managed path is not a regular file",
            }));
            continue;
        }
        let actual = digest(&target)?;
        if actual != owned.installed_sha256 {
            findings.push(serde_json::json!({
                "code": "managed-path-drift",
                "path": owned.path,
                "message": "managed path digest differs from installed provenance",
                "expectedSha256": owned.installed_sha256,
                "actualSha256": actual,
            }));
        }
    }
    let transaction_dir = state_dir.join("transactions");
    if transaction_dir.is_dir()
        && fs::read_dir(&transaction_dir)
            .map_err(|error| error.to_string())?
            .any(|entry| entry.is_ok())
    {
        findings.push(serde_json::json!({
            "code": "incomplete-transaction",
            "path": ".processkit/transactions",
            "message": "recovery is required before the installation is verified",
        }));
    }
    Ok(serde_json::json!({
        "apiVersion": API_VERSION,
        "status": if findings.is_empty() { "verified" } else { "drifted" },
        "checked": state.owned_paths.len() + migrated_count,
        "changes": [],
        "conflicts": [],
        "warnings": [],
        "errors": findings,
        "provenance": {
            "release": state.release,
            "profiles": state.profiles,
            "harnesses": state.harnesses,
            "stateSha256": digest(&state_path)?,
        }
    }))
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
        // Harness adapter changes are represented in the public plan, but
        // adapter_actions builds their in-memory content and ownership state.
        // Do not enqueue them a second time as file-backed distribution
        // components.
        if change.kind == "create" && change.ownership != "managed-keys" {
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
    let mut managed_adapters = Vec::new();
    for (action, _owned, managed) in adapter_actions(root, distribution, &plan.harnesses, false)? {
        pending.push(action);
        managed_adapters.push(managed);
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
        managed_adapters,
        migration_evidence: Vec::new(),
    };
    execute_transaction(root, "install", pending, Some(&state))?;
    Ok(state)
}

fn migrate_v0(
    source: &Path,
    root: &Path,
    distribution: &Path,
    profiles: Vec<String>,
    harnesses: Vec<String>,
    plan_only: bool,
    yes: bool,
) -> Result<serde_json::Value, String> {
    if !plan_only && !yes {
        return Err("v0 migration requires --yes after reviewing compatibility evidence".into());
    }
    let source = source
        .canonicalize()
        .map_err(|error| format!("legacy source root: {error}"))?;
    ensure_non_symlink_directory(&source, "legacy source root")?;

    let root = root
        .canonicalize()
        .map_err(|error| format!("fresh target root: {error}"))?;
    ensure_non_symlink_directory(&root, "fresh target root")?;
    if source == root || source.starts_with(&root) || root.starts_with(&source) {
        return Err("fresh target must be separate from and outside the legacy source".into());
    }
    let inspection = inspect_compatibility(&source, distribution)?;
    if inspection["status"] != "exact-release" {
        return Err("legacy source must exactly match a shipped compatibility manifest".into());
    }
    let exact_match = inspection["matches"]
        .as_array()
        .and_then(|matches| matches.first())
        .ok_or_else(|| "exact compatibility result is missing release evidence".to_string())?;
    let manifest_id = exact_match["manifestId"]
        .as_str()
        .ok_or_else(|| "compatibility evidence is missing manifestId".to_string())?;
    let release_version = exact_match["releaseVersion"]
        .as_str()
        .ok_or_else(|| "compatibility evidence is missing releaseVersion".to_string())?;
    let baseline_relative = exact_match["ownershipBaseline"]
        .as_str()
        .ok_or_else(|| "compatibility evidence is missing ownershipBaseline".to_string())?;
    let corpus_plan = plan_v0_corpus(&source, &distribution.join(baseline_relative))?;
    let plan_sha256 = corpus_plan.sha256()?;
    let entry_count = corpus_plan.entry_count();
    let target_nonempty = fs::read_dir(&root)
        .map_err(|error| format!("fresh target root: {error}"))?
        .next()
        .is_some();
    if target_nonempty {
        let state_path = root.join(".processkit/state.json");
        let state: InstallationState = serde_json::from_slice(
            &fs::read(&state_path)
                .map_err(|_| "non-empty migration target has no installer state".to_string())?,
        )
        .map_err(|error| format!("migration target state: {error}"))?;
        validate_installation_state(&state)?;
        let matching_evidence = state.migration_evidence.iter().any(|evidence| {
            evidence.source_release == release_version
                && evidence.manifest_id == manifest_id
                && evidence.plan_sha256 == plan_sha256
                && evidence.entry_count == entry_count
        });
        let drift = corpus_plan.verify_applied(&root)?;
        if !matching_evidence || !drift.is_empty() {
            return Err(
                "non-empty migration target does not match the completed migration; use a fresh target or restore migrated paths"
                    .into(),
            );
        }
        return Ok(serde_json::json!({
            "apiVersion": API_VERSION,
            "status": "already-transitioned",
            "source": {
                "root": source,
                "releaseVersion": release_version,
                "manifestId": manifest_id,
                "disposition": "preserved-read-only",
            },
            "target": {
                "root": root,
                "release": state.release,
                "profiles": state.profiles,
                "harnesses": state.harnesses,
                "disposition": "verified-existing-migration",
            },
            "corpus": {
                "status": "already-applied",
                "planSha256": plan_sha256,
                "entryCount": entry_count,
                "plan": corpus_plan,
            },
            "warnings": [],
            "errors": [],
        }));
    }
    if plan_only {
        return Ok(serde_json::json!({
            "apiVersion": API_VERSION,
            "status": corpus_plan.status,
            "source": {
                "root": source,
                "releaseVersion": release_version,
                "manifestId": manifest_id,
                "disposition": "preserved-read-only",
            },
            "target": {
                "root": root,
                "disposition": "not-modified",
            },
            "corpus": corpus_plan,
            "warnings": [
                "the migration plan is non-mutating",
                "producer-owned baseline files are excluded; modified baseline files block migration",
            ],
            "errors": [],
        }));
    }
    if corpus_plan.status != "planned" {
        return Err("legacy corpus plan is blocked; resolve every reported finding".into());
    }

    let mut state = install(&root, distribution, profiles, harnesses, true)?;
    let pending = corpus_plan.pending_actions(&source, &root)?;
    state.migration_evidence.push(MigrationEvidence {
        source_release: release_version.into(),
        manifest_id: manifest_id.into(),
        plan_sha256: plan_sha256.clone(),
        entry_count,
        plan: corpus_plan.clone(),
    });
    execute_transaction(&root, "migrate-v0-corpus", pending, Some(&state))?;
    Ok(serde_json::json!({
        "apiVersion": API_VERSION,
        "status": "transitioned-to-fresh-target",
        "source": {
            "root": source,
            "releaseVersion": release_version,
            "manifestId": manifest_id,
            "disposition": "preserved-read-only",
        },
        "target": {
            "root": root,
            "release": state.release,
            "profiles": state.profiles,
            "harnesses": state.harnesses,
        },
        "corpus": {
            "status": "applied",
            "planSha256": plan_sha256,
            "entryCount": entry_count,
            "plan": corpus_plan,
        },
        "warnings": [
            "the legacy source was inspected but not modified",
            "producer-owned baseline files were excluded from project corpus migration",
        ],
        "errors": [],
    }))
}

fn adapter_actions(
    root: &Path,
    distribution_root: &Path,
    harnesses: &[String],
    updating: bool,
) -> Result<Vec<(PendingAction, OwnedPath, ManagedAdapterState)>, String> {
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
        let mcp_servers_existed = object.contains_key("mcpServers");
        let servers = object
            .entry("mcpServers")
            .or_insert_with(|| serde_json::json!({}))
            .as_object_mut()
            .ok_or("harness mcpServers must be a JSON object")?;
        let mut managed_keys = BTreeMap::new();
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
            let server_digest = format!(
                "{:x}",
                Sha256::digest(
                    serde_json::to_vec(&server_value).map_err(|error| error.to_string())?
                )
            );
            managed_keys.insert(server.id.clone(), server_digest);
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
                path: adapter.destination.clone(),
                component: format!("harness-adapter:{harness}"),
                operation: if config_existed {
                    "managed-keys-merge/v1".into()
                } else {
                    "managed-keys-create/v1".into()
                },
                ownership: "managed-keys".into(),
                installed_sha256: new_sha256,
            },
            ManagedAdapterState {
                adapter: harness.clone(),
                path: adapter.destination,
                format: "json".into(),
                catalog_sha256: digest(&catalog_path)?,
                managed_keys,
                created_file: !config_existed,
                created_mcp_servers: !mcp_servers_existed,
            },
        ));
    }
    Ok(actions)
}

fn recover(root: &Path, yes: bool) -> Result<usize, String> {
    if !yes {
        return Err("recovery requires --yes because it can remove staged files".into());
    }
    validate_operation_root(root)?;
    clear_stale_lock_for_recovery(root)?;
    let _lock = acquire_lock(root, "recover")?;
    let state_dir = root.join(".processkit");
    let transactions = state_dir.join("transactions");
    match transactions.symlink_metadata() {
        Ok(_) => ensure_non_symlink_directory(&transactions, "transaction journal directory")?,
        Err(error) if error.kind() == std::io::ErrorKind::NotFound => {
            return Ok(0);
        }
        Err(error) => {
            return Err(format!("transaction journal directory: {error}"));
        }
    }
    let staging_root = state_dir.join(".staging");
    if staging_root.exists() {
        ensure_non_symlink_directory(&staging_root, "transaction staging directory")?;
    }
    let mut recovered = 0;
    for entry in fs::read_dir(&transactions).map_err(|error| error.to_string())? {
        let entry = entry.map_err(|error| error.to_string())?;
        let journal_path = entry.path();
        if journal_path.extension().and_then(|value| value.to_str()) != Some("json") {
            continue;
        }
        ensure_regular_file(root, &journal_path, "transaction journal")?;
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
        validate_recovery_journal(root, &journal)?;
        let state_path = state_dir.join("state.json");
        let state_sha256 = state_path
            .is_file()
            .then(|| digest(&state_path))
            .transpose()?;
        let state_is_new = state_sha256 == journal.new_state_sha256;
        let state_is_old = state_sha256 == journal.old_state_sha256;
        if journal.phase == "committed" || state_is_new {
            fs::remove_file(&journal_path).map_err(|error| error.to_string())?;
            let _ = fs::remove_dir_all(staging_root.join(transaction));
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
        let _ = fs::remove_dir_all(staging_root.join(transaction));
        recovered += 1;
    }
    Ok(recovered)
}

fn uninstall(root: &Path, yes: bool) -> Result<usize, String> {
    if !yes {
        return Err("uninstall requires --yes because it removes owned files".into());
    }
    validate_operation_root(root)?;
    let _lock = acquire_lock(root, "uninstall")?;
    let state_path = root.join(".processkit/state.json");
    if !state_path.exists() {
        return Ok(0);
    }
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
    for adapter in &state.managed_adapters {
        if !safe_relative(&adapter.path) || has_symlink_ancestor(root, &adapter.path)? {
            return Err("uninstall refused an unsafe managed adapter path".into());
        }
        let target = root.join(&adapter.path);
        let original = fs::read(&target)
            .map_err(|error| format!("managed adapter {}: {error}", adapter.path))?;
        let old_sha256 = format!("{:x}", Sha256::digest(&original));
        let mut document: serde_json::Value = serde_json::from_slice(&original)
            .map_err(|error| format!("harness config JSON: {error}"))?;
        let servers = document
            .get_mut("mcpServers")
            .and_then(serde_json::Value::as_object_mut)
            .ok_or("managed harness config no longer has mcpServers")?;
        for (key, baseline) in &adapter.managed_keys {
            let value = servers
                .get(key)
                .ok_or_else(|| format!("managed harness key is missing: {key}"))?;
            let actual = format!(
                "{:x}",
                Sha256::digest(serde_json::to_vec(value).map_err(|error| error.to_string())?)
            );
            if &actual != baseline {
                return Err(format!("managed harness key was changed: {key}"));
            }
        }
        for key in adapter.managed_keys.keys() {
            servers.remove(key);
        }
        if servers.is_empty() && adapter.created_mcp_servers {
            document
                .as_object_mut()
                .ok_or("harness config root must be an object")?
                .remove("mcpServers");
        }
        let remove_file =
            adapter.created_file && document.as_object().is_some_and(serde_json::Map::is_empty);
        let (kind, new_sha256, content) = if remove_file {
            ("remove".into(), None, None)
        } else {
            let mut bytes =
                serde_json::to_vec_pretty(&document).map_err(|error| error.to_string())?;
            bytes.push(b'\n');
            let digest = format!("{:x}", Sha256::digest(&bytes));
            ("replace".into(), Some(digest), Some(bytes))
        };
        pending.push(PendingAction {
            action: TransactionAction {
                kind,
                target: adapter.path.clone(),
                old_sha256: Some(old_sha256),
                new_sha256,
                staged_path: None,
                backup_path: None,
                created_parents: Vec::new(),
                ownership: "managed-keys".into(),
                applied: false,
            },
            source: None,
            content,
        });
    }
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
    let removed = removable.len() + adapters.len() + state.managed_adapters.len();
    state.owned_paths.retain(|path| {
        !matches!(
            path.ownership.as_str(),
            "managed-three-way" | "managed-keys"
        )
    });
    state.managed_adapters.clear();
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
    validate_operation_root(root)?;
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
    let mut removals = Vec::new();
    let mut preserved_stale = Vec::new();
    for owned in old
        .owned_paths
        .iter()
        .filter(|path| path.ownership == "managed-three-way")
    {
        let target = root.join(&owned.path);
        if !safe_relative(&owned.path)
            || has_symlink_ancestor(root, &owned.path)?
            || !target.is_file()
        {
            return Err(format!(
                "update conflict: managed file was changed or missing: {}",
                owned.path
            ));
        }
        let current_sha256 = digest(&target)?;
        let current_is_baseline = current_sha256 == owned.installed_sha256;
        match desired_by_path.remove(&owned.path) {
            Some(change) if current_is_baseline => {
                if change.source_sha256 != owned.installed_sha256 {
                    replacements.push(change);
                }
            }
            Some(change) if change.source_sha256 == owned.installed_sha256 => {
                // The user changed this path while upstream did not. Preserve
                // the user version and retain the baseline for future
                // three-way comparisons.
            }
            Some(_) => {
                return Err(format!(
                    "update conflict: user and release both changed managed file: {}",
                    owned.path
                ));
            }
            None if current_is_baseline => {
                removals.push(owned.path.clone());
            }
            None => {
                // Upstream removed the path, but the user changed it. Preserve
                // the file and relinquish installer ownership.
                preserved_stale.push(owned.path.clone());
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
    let changed = replacements.len() + additions.len() + removals.len();
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
    for path in &removals {
        let owned = old
            .owned_paths
            .iter()
            .find(|owned| owned.path == *path)
            .ok_or("removal path has no ownership state")?;
        pending.push(PendingAction {
            action: TransactionAction {
                kind: "remove".into(),
                target: owned.path.clone(),
                old_sha256: Some(owned.installed_sha256.clone()),
                new_sha256: None,
                staged_path: None,
                backup_path: None,
                created_parents: Vec::new(),
                ownership: owned.ownership.clone(),
                applied: false,
            },
            source: None,
            content: None,
        });
    }
    old.owned_paths
        .retain(|owned| !removals.contains(&owned.path) && !preserved_stale.contains(&owned.path));
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
    for adapter in &old.managed_adapters {
        let target = root.join(&adapter.path);
        if !target.is_file() || has_symlink_ancestor(root, &adapter.path)? {
            return Err(format!(
                "update conflict: managed harness config is missing or unsafe: {}",
                adapter.path
            ));
        }
        let document: serde_json::Value =
            serde_json::from_slice(&fs::read(&target).map_err(|error| error.to_string())?)
                .map_err(|error| format!("harness config JSON: {error}"))?;
        let servers = document
            .get("mcpServers")
            .and_then(serde_json::Value::as_object)
            .ok_or("managed harness config no longer has mcpServers")?;
        for (key, baseline) in &adapter.managed_keys {
            let value = servers
                .get(key)
                .ok_or_else(|| format!("managed harness key is missing: {key}"))?;
            let actual = format!(
                "{:x}",
                Sha256::digest(serde_json::to_vec(value).map_err(|error| error.to_string())?)
            );
            if &actual != baseline {
                return Err(format!("managed harness key was changed: {key}"));
            }
        }
    }
    let installer_created_adapters: HashSet<String> = old
        .owned_paths
        .iter()
        .filter(|path| {
            path.ownership == "managed-keys" && path.operation == "managed-keys-create/v1"
        })
        .map(|path| path.path.clone())
        .collect();
    let adapter_changes = adapter_actions(root, distribution, &old.harnesses, true)?;
    old.owned_paths
        .retain(|path| path.ownership != "managed-keys");
    let mut managed_adapters = Vec::new();
    for (action, mut owned, mut managed) in adapter_changes {
        if installer_created_adapters.contains(&owned.path) {
            owned.operation = "managed-keys-create/v1".into();
        }
        if let Some(previous) = old
            .managed_adapters
            .iter()
            .find(|previous| previous.path == managed.path)
        {
            managed.created_file = previous.created_file;
            managed.created_mcp_servers = previous.created_mcp_servers;
        }
        pending.push(action);
        managed_adapters.push(managed);
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
        managed_adapters,
        migration_evidence: old.migration_evidence,
    };
    execute_transaction(root, "update", pending, Some(&new_state))?;
    Ok(changed)
}

fn validate_operation_root(root: &Path) -> Result<(), String> {
    let root_metadata = root
        .symlink_metadata()
        .map_err(|error| format!("target root: {error}"))?;
    if root_metadata.file_type().is_symlink() || !root_metadata.is_dir() {
        return Err("target root must be a non-symlink directory".into());
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
    Ok(())
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
    let file_name = path
        .file_name()
        .ok_or("state path has no file name")?
        .to_string_lossy();
    create_private_dir(parent)?;
    let temporary = parent.join(format!(".{}.tmp-{}", file_name, std::process::id()));
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
        assert!(!safe_relative("context//skills"));
        assert!(!safe_relative("context/./skills"));
        assert!(!safe_relative("context/\0skills"));
    }
}
