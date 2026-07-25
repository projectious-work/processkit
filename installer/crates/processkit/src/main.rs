use clap::{ArgAction, Parser, Subcommand, ValueEnum};
use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::collections::{BTreeSet, HashSet};
use std::fs;
use std::fs::OpenOptions;
use std::io::Write;
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
}

#[derive(Clone, Copy, ValueEnum)]
enum OutputFormat {
    Json,
    Human,
}

#[derive(Deserialize)]
struct Distribution {
    apiVersion: String,
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
    schema: Option<String>,
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
    phase: String,
    created_paths: Vec<JournalPath>,
}
#[derive(Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
struct JournalPath {
    path: String,
    sha256: String,
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
    if distribution.apiVersion != "processkit.projectious.work/distribution/v1alpha1"
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
    }
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
    let lock_path = state_dir.join("lock");
    let mut lock = OpenOptions::new()
        .write(true)
        .create_new(true)
        .open(&lock_path)
        .map_err(|_| "another processkit operation is already in progress")?;
    writeln!(lock, "install-{}", std::process::id()).map_err(|error| error.to_string())?;
    let transaction = format!("install-{}", std::process::id());
    let staging = state_dir.join(".staging").join(&transaction);
    let journal_path = state_dir
        .join("transactions")
        .join(format!("{transaction}.json"));
    let mut journal = Journal {
        api_version: API_VERSION.into(),
        phase: "prepared".into(),
        created_paths: Vec::new(),
    };
    let result = (|| -> Result<InstallationState, String> {
        fs::create_dir_all(staging.join("new"))
            .map_err(|error| format!("create staging directory: {error}"))?;
        write_json_atomic(&journal_path, &journal)?;
        let mut owned_paths = Vec::new();
        for change in &plan.changes {
            if change.kind != "create" {
                continue;
            }
            if !safe_relative(&change.destination)
                || has_symlink_ancestor(root, &change.destination)?
            {
                return Err(format!(
                    "unsafe target during install: {}",
                    change.destination
                ));
            }
            if digest(&change.source)? != change.source_sha256 {
                return Err(format!(
                    "release source changed during install: {}",
                    change.destination
                ));
            }
            let staged = staging.join("new").join(&change.destination);
            if let Some(parent) = staged.parent() {
                fs::create_dir_all(parent).map_err(|error| error.to_string())?;
            }
            fs::copy(&change.source, &staged).map_err(|error| error.to_string())?;
            if digest(&staged)? != change.source_sha256 {
                return Err(format!("staged digest mismatch: {}", change.destination));
            }
            let target = root.join(&change.destination);
            if target.exists() {
                return Err(format!(
                    "target appeared during install: {}",
                    change.destination
                ));
            }
            if let Some(parent) = target.parent() {
                fs::create_dir_all(parent).map_err(|error| error.to_string())?;
            }
            if has_symlink_ancestor(root, &change.destination)? {
                return Err(format!(
                    "target ancestry changed during install: {}",
                    change.destination
                ));
            }
            fs::rename(&staged, &target).map_err(|error| error.to_string())?;
            journal.created_paths.push(JournalPath {
                path: change.destination.clone(),
                sha256: change.source_sha256.clone(),
            });
            journal.phase = "applying".into();
            write_json_atomic(&journal_path, &journal)?;
            owned_paths.push(OwnedPath {
                path: change.destination.clone(),
                component: change.component.clone(),
                operation: change.operation.clone(),
                ownership: change.ownership.clone(),
                installed_sha256: change.source_sha256.clone(),
            });
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
        write_json_atomic(&state_path, &state)?;
        journal.phase = "committed".into();
        write_json_atomic(&journal_path, &journal)?;
        Ok(state)
    })();
    if result.is_err() {
        for entry in journal.created_paths.iter().rev() {
            let target = root.join(&entry.path);
            if target.is_file()
                && !target
                    .symlink_metadata()
                    .map(|meta| meta.file_type().is_symlink())
                    .unwrap_or(true)
            {
                let _ = fs::remove_file(target);
            }
        }
        let _ = fs::remove_file(&state_path);
    }
    let _ = fs::remove_dir_all(&staging);
    let _ = fs::remove_file(&journal_path);
    let _ = fs::remove_file(&lock_path);
    result
}

fn recover(root: &Path, yes: bool) -> Result<usize, String> {
    if !yes {
        return Err("recovery requires --yes because it can remove staged files".into());
    }
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
        if journal.phase == "committed" {
            fs::remove_file(&journal_path).map_err(|error| error.to_string())?;
            let _ = fs::remove_dir_all(state_dir.join(".staging").join(transaction));
            recovered += 1;
            continue;
        }
        if state_dir.join("state.json").exists() {
            return Err(
                "manual recovery required: state exists for an uncommitted transaction".into(),
            );
        }
        for created in journal.created_paths.iter().rev() {
            if !safe_relative(&created.path) || has_symlink_ancestor(root, &created.path)? {
                return Err("manual recovery required: unsafe journal target".into());
            }
            let target = root.join(&created.path);
            if !target.exists() {
                continue;
            }
            if target
                .symlink_metadata()
                .map_err(|error| error.to_string())?
                .file_type()
                .is_symlink()
                || !target.is_file()
                || digest(&target)? != created.sha256
            {
                return Err("manual recovery required: target no longer matches journal".into());
            }
            fs::remove_file(target).map_err(|error| error.to_string())?;
        }
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
    let state_path = root.join(".processkit/state.json");
    let state: InstallationState = serde_json::from_slice(
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
    for path in &removable {
        fs::remove_file(root.join(&path.path)).map_err(|error| error.to_string())?;
    }
    if state.owned_paths.len() == removable.len() {
        fs::remove_file(&state_path).map_err(|error| error.to_string())?;
    }
    Ok(removable.len())
}

fn write_json_atomic<T: Serialize>(path: &Path, value: &T) -> Result<(), String> {
    let parent = path.parent().ok_or("state path has no parent")?;
    fs::create_dir_all(parent).map_err(|error| error.to_string())?;
    let temporary = parent.join(format!(
        ".{}.tmp-{}",
        path.file_name().unwrap().to_string_lossy(),
        std::process::id()
    ));
    fs::write(
        &temporary,
        serde_json::to_vec_pretty(value).map_err(|error| error.to_string())?,
    )
    .map_err(|error| error.to_string())?;
    fs::rename(temporary, path).map_err(|error| error.to_string())
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
