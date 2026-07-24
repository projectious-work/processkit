use clap::{Parser, Subcommand, ValueEnum};
use serde::Serialize;
use sha2::{Digest, Sha256};
use std::fs;
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
        #[arg(long, value_enum, default_value_t = OutputFormat::Json)]
        format: OutputFormat,
    },
}

#[derive(Clone, Copy, ValueEnum)]
enum OutputFormat { Json, Human }

#[derive(serde::Deserialize)]
struct Distribution { apiVersion: String, kind: String, metadata: Metadata, spec: Spec }
#[derive(serde::Deserialize)]
struct Metadata { name: String, version: String }
#[derive(serde::Deserialize)]
struct Spec { components: Vec<ComponentSpec>, profiles: std::collections::BTreeMap<String, Profile> }
#[derive(serde::Deserialize)]
struct Profile { include: Vec<String> }
#[derive(serde::Deserialize)]
struct ComponentSpec { id: String, source: Source, destination: String, operation: String, ownership: String }
#[derive(serde::Deserialize)]
struct Source { file: Option<String>, include: Option<Vec<String>> }

#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct Plan { api_version: &'static str, status: String, distribution: DistributionInfo,
    selected_profiles: Vec<String>, harnesses: Vec<String>, changes: Vec<Change>,
    conflicts: Vec<Problem>, warnings: Vec<Problem>, errors: Vec<Problem> }
#[derive(Serialize)]
#[serde(rename_all = "camelCase")]
struct DistributionInfo { name: String, version: String, manifest_sha256: String }
#[derive(Serialize, Ord, PartialOrd, Eq, PartialEq)]
struct Change { destination: String, component: String, operation: String, ownership: String, kind: String, source_sha256: String }
#[derive(Serialize, Ord, PartialOrd, Eq, PartialEq)]
struct Problem { code: String, path: String, message: String }

fn safe_relative(value: &str) -> bool {
    let path = Path::new(value);
    !path.is_absolute() && !path.components().any(|c| matches!(c, Component::ParentDir | Component::RootDir | Component::Prefix(_)))
}
fn digest(path: &Path) -> Result<String, String> {
    let bytes = fs::read(path).map_err(|e| format!("{}: {e}", path.display()))?;
    Ok(format!("{:x}", Sha256::digest(bytes)))
}
fn main() {
    let cli = Cli::parse();
    match cli.command { Command::Plan { root, distribution, profile, harness, format } => {
        match plan(&root, &distribution, profile, harness) {
            Ok(plan) => match format { OutputFormat::Json => println!("{}", serde_json::to_string_pretty(&plan).unwrap()),
                OutputFormat::Human => { println!("{} {}: {} change(s), {} conflict(s)", plan.distribution.name, plan.distribution.version, plan.changes.len(), plan.conflicts.len()); for change in plan.changes { println!("{} {}", change.kind, change.destination); } } },
            Err(error) => { eprintln!("processkit: {error}"); std::process::exit(3); }
        }
    }}
}
fn plan(root: &Path, distribution_root: &Path, mut profiles: Vec<String>, mut harnesses: Vec<String>) -> Result<Plan, String> {
    if profiles.is_empty() { profiles.push("managed".into()); }
    profiles.sort(); profiles.dedup(); harnesses.sort(); harnesses.dedup();
    let manifest = distribution_root.join(".processkit/installer/distribution.yaml");
    let text = fs::read_to_string(&manifest).map_err(|e| format!("manifest: {e}"))?;
    let distribution: Distribution = serde_yaml::from_str(&text).map_err(|e| format!("manifest YAML: {e}"))?;
    if distribution.apiVersion != "processkit.projectious.work/distribution/v1alpha1" || distribution.kind != "Distribution" { return Err("unsupported distribution API or kind".into()); }
    let mut selected = std::collections::BTreeSet::new();
    for profile in &profiles { let item = distribution.spec.profiles.get(profile).ok_or_else(|| format!("unknown profile: {profile}"))?; selected.extend(item.include.iter().cloned()); }
    let mut changes = Vec::new(); let mut conflicts = Vec::new(); let mut errors = Vec::new();
    for component in distribution.spec.components.into_iter().filter(|c| selected.contains(&c.id)) {
        if !matches!(component.operation.as_str(), "copy/v1" | "preserve-user/v1") { errors.push(Problem { code: "unsupported-operation".into(), path: component.id.clone(), message: component.operation.clone() }); continue; }
        if !safe_relative(&component.destination) { errors.push(Problem { code: "unsafe-destination".into(), path: component.destination.clone(), message: "destination must be relative".into() }); continue; }
        let sources = match source_paths(distribution_root, &component.source) {
            Ok(items) => items,
            Err(message) => { errors.push(Problem { code: "invalid-source".into(), path: component.id.clone(), message }); continue; }
        };
        for (source_path, relative) in sources {
            let destination = if component.destination == "." { relative } else { format!("{}/{}", component.destination.trim_end_matches('/'), relative) };
            let target = root.join(&destination);
            if target.symlink_metadata().map(|m| m.file_type().is_symlink()).unwrap_or(false) { conflicts.push(Problem { code: "symlink-target".into(), path: destination, message: "refusing symlink target".into() }); continue; }
            if target.exists() && component.operation == "preserve-user/v1" { changes.push(Change { destination, component: component.id.clone(), operation: component.operation.clone(), ownership: component.ownership.clone(), kind: "preserve".into(), source_sha256: digest(&source_path)? }); }
            else if target.exists() { conflicts.push(Problem { code: "existing-target".into(), path: destination, message: "managed replacement requires an explicit update policy".into() }); }
            else { changes.push(Change { destination, component: component.id.clone(), operation: component.operation.clone(), ownership: component.ownership.clone(), kind: "create".into(), source_sha256: digest(&source_path)? }); }
        }
    }
    changes.sort(); conflicts.sort(); errors.sort();
    let status = if !errors.is_empty() { "invalid" } else if !conflicts.is_empty() { "conflict" } else { "planned" }.into();
    Ok(Plan { api_version: API_VERSION, status, distribution: DistributionInfo { name: distribution.metadata.name, version: distribution.metadata.version, manifest_sha256: digest(&manifest)? }, selected_profiles: profiles, harnesses, changes, conflicts, warnings: vec![], errors })
}

fn source_paths(root: &Path, source: &Source) -> Result<Vec<(PathBuf, String)>, String> {
    if let Some(file) = &source.file {
        if !safe_relative(file) { return Err("file source must be relative".into()); }
        let path = root.join(file);
        if !path.is_file() { return Err(format!("source file is missing: {file}")); }
        return Ok(vec![(path, file.clone())]);
    }
    let includes = source.include.as_ref().ok_or("source requires file or include")?;
    if includes.len() != 1 || !includes[0].ends_with("/**") { return Err("Phase 1 accepts one recursive include pattern".into()); }
    let prefix = includes[0].trim_end_matches("/**");
    if !safe_relative(prefix) { return Err("include source must be relative".into()); }
    let base = root.join(prefix);
    if !base.is_dir() { return Err(format!("include source is missing: {}", includes[0])); }
    let mut paths = Vec::new();
    for entry in walkdir::WalkDir::new(&base).follow_links(false).into_iter().filter_map(Result::ok) {
        if entry.file_type().is_symlink() { return Err(format!("source symlink is not allowed: {}", entry.path().display())); }
        if entry.file_type().is_file() {
            let relative = entry.path().strip_prefix(root).map_err(|_| "source escaped distribution root")?;
            paths.push((entry.path().to_path_buf(), relative.to_string_lossy().replace('\\', "/")));
        }
    }
    paths.sort_by(|a, b| a.1.cmp(&b.1));
    Ok(paths)
}

#[cfg(test)]
mod tests {
    use super::safe_relative;
    #[test]
    fn rejects_escaping_paths() {
        assert!(safe_relative("context/skills"));
        assert!(!safe_relative("../context"));
        assert!(!safe_relative("/context"));
    }
}
