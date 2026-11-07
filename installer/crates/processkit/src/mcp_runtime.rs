//! Native supervision for the shipped Python MCP gateway.

use serde::{Deserialize, Serialize};
use sha2::{Digest, Sha256};
use std::fs;
use std::path::{Path, PathBuf};
use std::process::{Command, ExitStatus, Output};
use std::time::Duration;

const API_VERSION: &str = "processkit.projectious.work/runtime/v1alpha1";
const GATEWAY_PATH: &str = "context/skills/processkit/processkit-gateway/mcp/server.py";
const RUNTIME_POLICY_PATH: &str = ".processkit/runtime/python-uv.json";

#[derive(Clone, Copy, Debug)]
pub(super) enum McpTransport {
    Stdio,
    StreamableHttp,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub(super) struct McpVerification {
    api_version: &'static str,
    kind: &'static str,
    status: &'static str,
    root: PathBuf,
    gateway: PathBuf,
    uv_version: String,
    errors: Vec<String>,
}

impl McpVerification {
    pub(super) fn summary(&self) -> String {
        format!(
            "MCP runtime verified: {} ({})",
            self.gateway.display(),
            self.uv_version
        )
    }
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct RuntimePolicy {
    api_version: String,
    kind: String,
    aggregate_sha256: String,
    dependency_profiles: Vec<DependencyProfile>,
    dependency_resolution: DependencyResolution,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct DependencyResolution {
    resolved_versions_locked: bool,
    hashes_required: bool,
    lock_file: String,
    lock_sha256: String,
}

#[derive(Deserialize)]
#[serde(rename_all = "camelCase")]
struct DependencyProfile {
    sha256: String,
    server_paths: Vec<String>,
    dependencies: Vec<String>,
    requires_python: String,
}

#[derive(Debug, Serialize)]
#[serde(rename_all = "camelCase")]
pub(super) struct RuntimePreparation {
    api_version: &'static str,
    kind: &'static str,
    status: &'static str,
    root: PathBuf,
    policy_sha256: String,
    profile_count: usize,
    cache_dir: Option<PathBuf>,
    errors: Vec<String>,
}

impl RuntimePreparation {
    pub(super) fn summary(&self) -> String {
        format!(
            "{}: {} dependency profile(s), policy {}",
            self.status, self.profile_count, self.policy_sha256
        )
    }
}

fn runtime_paths(root: &Path) -> Result<(PathBuf, PathBuf), String> {
    let metadata = fs::symlink_metadata(root).map_err(|error| format!("project root: {error}"))?;
    if !metadata.is_dir() || metadata.file_type().is_symlink() {
        return Err("project root must be a non-symlink directory".into());
    }
    let root = root
        .canonicalize()
        .map_err(|error| format!("project root: {error}"))?;
    let gateway = root.join(GATEWAY_PATH);
    let metadata =
        fs::symlink_metadata(&gateway).map_err(|error| format!("MCP gateway: {error}"))?;
    if !metadata.is_file() || metadata.file_type().is_symlink() {
        return Err("MCP gateway must be a regular, non-symlink file".into());
    }
    Ok((root, gateway))
}

fn uv_version(uv: &Path) -> Result<String, String> {
    let mut command = Command::new(uv);
    command.arg("--version");
    let output =
        output_with_busy_retry(&mut command).map_err(|error| format!("launch uv: {error}"))?;
    if !output.status.success() {
        return Err(format!("uv --version exited with {}", output.status));
    }
    let version =
        String::from_utf8(output.stdout).map_err(|_| "uv --version emitted non-UTF-8 output")?;
    let version = version.trim();
    if version.is_empty() {
        return Err("uv --version emitted empty output".into());
    }
    Ok(version.to_owned())
}

pub(super) fn verify_mcp(root: &Path) -> Result<McpVerification, String> {
    verify_mcp_with_uv(root, Path::new("uv"))
}

fn verify_mcp_with_uv(root: &Path, uv: &Path) -> Result<McpVerification, String> {
    let (root, gateway) = runtime_paths(root)?;
    Ok(McpVerification {
        api_version: API_VERSION,
        kind: "McpVerification",
        status: "verified",
        root,
        gateway,
        uv_version: uv_version(uv)?,
        errors: Vec::new(),
    })
}

pub(super) fn prepare_runtime(
    root: &Path,
    cache_dir: Option<&Path>,
    offline: bool,
) -> Result<RuntimePreparation, String> {
    prepare_runtime_with_uv(root, cache_dir, offline, Path::new("uv"))
}

fn prepare_runtime_with_uv(
    root: &Path,
    cache_dir: Option<&Path>,
    offline: bool,
    uv: &Path,
) -> Result<RuntimePreparation, String> {
    let (root, _) = runtime_paths(root)?;
    let policy_path = root.join(RUNTIME_POLICY_PATH);
    let metadata = fs::symlink_metadata(&policy_path)
        .map_err(|error| format!("Python runtime policy: {error}"))?;
    if !metadata.is_file() || metadata.file_type().is_symlink() {
        return Err("Python runtime policy must be a regular, non-symlink file".into());
    }
    let policy_bytes =
        fs::read(&policy_path).map_err(|error| format!("Python runtime policy: {error}"))?;
    let policy: RuntimePolicy = serde_json::from_slice(&policy_bytes)
        .map_err(|error| format!("Python runtime policy JSON: {error}"))?;
    if policy.api_version != "processkit.projectious.work/python-runtime/v1alpha1"
        || policy.kind != "PythonRuntimePolicy"
        || !valid_digest(&policy.aggregate_sha256)
        || policy.dependency_profiles.is_empty()
    {
        return Err("unsupported or incomplete Python runtime policy".into());
    }
    if !policy.dependency_resolution.resolved_versions_locked
        || !policy.dependency_resolution.hashes_required
        || !valid_digest(&policy.dependency_resolution.lock_sha256)
    {
        return Err("Python runtime policy does not require a hashed lock".into());
    }
    let lock_relative = Path::new(&policy.dependency_resolution.lock_file);
    if lock_relative.is_absolute()
        || lock_relative
            .components()
            .any(|part| !matches!(part, std::path::Component::Normal(_)))
    {
        return Err("Python runtime policy contains an unsafe lock path".into());
    }
    let lock_path = root.join(lock_relative);
    let lock_metadata = fs::symlink_metadata(&lock_path)
        .map_err(|error| format!("Python runtime lock: {error}"))?;
    if !lock_metadata.is_file() || lock_metadata.file_type().is_symlink() {
        return Err("Python runtime lock must be a regular, non-symlink file".into());
    }
    let lock_bytes =
        fs::read(&lock_path).map_err(|error| format!("Python runtime lock: {error}"))?;
    let lock_sha256 = format!("{:x}", Sha256::digest(&lock_bytes));
    if lock_sha256 != policy.dependency_resolution.lock_sha256 {
        return Err("Python runtime lock digest differs from policy".into());
    }
    if !lock_bytes
        .windows(14)
        .any(|window| window == b"--hash=sha256:")
    {
        return Err("Python runtime lock does not contain package hashes".into());
    }

    let cache_dir = prepare_cache(cache_dir, offline)?;
    for profile in &policy.dependency_profiles {
        if !valid_digest(&profile.sha256)
            || profile.server_paths.is_empty()
            || profile.dependencies.is_empty()
            || profile.requires_python.is_empty()
        {
            return Err("Python runtime policy contains an invalid dependency profile".into());
        }
        for server_path in &profile.server_paths {
            let relative = Path::new(server_path);
            if relative.is_absolute()
                || relative
                    .components()
                    .any(|part| !matches!(part, std::path::Component::Normal(_)))
            {
                return Err("Python runtime policy contains an unsafe server path".into());
            }
            let server = root.join(relative);
            let metadata = fs::symlink_metadata(&server)
                .map_err(|error| format!("runtime server {}: {error}", relative.display()))?;
            if !metadata.is_file() || metadata.file_type().is_symlink() {
                return Err(format!(
                    "runtime server must be a regular file: {}",
                    relative.display()
                ));
            }
        }
        let mut command = Command::new(uv);
        command
            .arg("run")
            .arg("--no-project")
            .args(["--with-requirements", lock_path.to_string_lossy().as_ref()])
            .args(["--python", &profile.requires_python]);
        if offline {
            command.arg("--offline");
        }
        for dependency in &profile.dependencies {
            if dependency.is_empty() || dependency.contains(char::is_whitespace) {
                return Err("Python runtime policy contains an unsafe dependency".into());
            }
        }
        command.args(["python", "-c", "pass"]);
        command.current_dir(&root);
        if let Some(cache) = &cache_dir {
            command.env("UV_CACHE_DIR", cache);
        }
        let output = output_with_busy_retry(&mut command)
            .map_err(|error| format!("prepare runtime profile {}: {error}", profile.sha256))?;
        if !output.status.success() {
            return Err(format!(
                "runtime profile {} is not {}: {}",
                profile.sha256,
                if offline { "offline-ready" } else { "prepared" },
                redacted_line(&output.stderr)
            ));
        }
    }
    Ok(RuntimePreparation {
        api_version: API_VERSION,
        kind: "RuntimePreparation",
        status: if offline { "offline-ready" } else { "prepared" },
        root,
        policy_sha256: policy.aggregate_sha256,
        profile_count: policy.dependency_profiles.len(),
        cache_dir,
        errors: Vec::new(),
    })
}

fn prepare_cache(cache_dir: Option<&Path>, offline: bool) -> Result<Option<PathBuf>, String> {
    let Some(path) = cache_dir else {
        return Ok(None);
    };
    if !path.is_absolute() {
        return Err("runtime cache directory must be absolute".into());
    }
    if !offline {
        fs::create_dir_all(path)
            .map_err(|error| format!("create runtime cache directory: {error}"))?;
    }
    let metadata =
        fs::symlink_metadata(path).map_err(|error| format!("runtime cache directory: {error}"))?;
    if !metadata.is_dir() || metadata.file_type().is_symlink() {
        return Err("runtime cache directory must be a non-symlink directory".into());
    }
    path.canonicalize()
        .map(Some)
        .map_err(|error| format!("runtime cache directory: {error}"))
}

fn valid_digest(value: &str) -> bool {
    value.len() == 64
        && value
            .bytes()
            .all(|byte| byte.is_ascii_hexdigit() && !byte.is_ascii_uppercase())
}

fn redacted_line(stderr: &[u8]) -> String {
    String::from_utf8_lossy(stderr)
        .lines()
        .next()
        .unwrap_or("no stderr")
        .chars()
        .take(240)
        .collect()
}

pub(super) fn serve_mcp(
    root: &Path,
    transport: McpTransport,
    host: &str,
    port: u16,
    path: &str,
) -> Result<i32, String> {
    serve_mcp_with_uv(root, transport, host, port, path, Path::new("uv"))
}

fn serve_mcp_with_uv(
    root: &Path,
    transport: McpTransport,
    host: &str,
    port: u16,
    path: &str,
    uv: &Path,
) -> Result<i32, String> {
    let (root, gateway) = runtime_paths(root)?;
    let mut command = Command::new(uv);
    command.arg("run").arg(&gateway).arg("serve");
    match transport {
        McpTransport::Stdio => {
            command.args(["--transport", "stdio"]);
        }
        McpTransport::StreamableHttp => {
            if !matches!(host, "127.0.0.1" | "::1" | "localhost") {
                return Err("streamable HTTP host must be loopback for native supervision".into());
            }
            if !path.starts_with('/') || path.contains(char::is_whitespace) {
                return Err("MCP HTTP path must be an absolute path without whitespace".into());
            }
            command
                .args(["--transport", "streamable-http", "--host", host])
                .args(["--port", &port.to_string(), "--path", path]);
        }
    }
    command.current_dir(root);
    let status = status_with_busy_retry(&mut command)
        .map_err(|error| format!("launch MCP gateway: {error}"))?;
    Ok(status.code().unwrap_or(1))
}

pub(super) fn proxy_mcp(root: &Path, url: &str) -> Result<i32, String> {
    proxy_mcp_with_uv(root, url, Path::new("uv"))
}

fn proxy_mcp_with_uv(root: &Path, url: &str, uv: &Path) -> Result<i32, String> {
    let (root, gateway) = runtime_paths(root)?;
    if !(url.starts_with("http://127.0.0.1:")
        || url.starts_with("http://localhost:")
        || url.starts_with("http://[::1]:"))
    {
        return Err("MCP proxy URL must use HTTP on an explicit loopback host".into());
    }
    let mut command = Command::new(uv);
    command
        .arg("run")
        .arg(gateway)
        .args(["stdio-proxy", "--url", url])
        .current_dir(root);
    let status = status_with_busy_retry(&mut command)
        .map_err(|error| format!("launch MCP stdio proxy: {error}"))?;
    Ok(status.code().unwrap_or(1))
}

fn output_with_busy_retry(command: &mut Command) -> std::io::Result<Output> {
    for attempt in 0..20 {
        match command.output() {
            Err(error) if error.raw_os_error() == Some(26) && attempt < 19 => {
                std::thread::sleep(Duration::from_millis(5));
            }
            result => return result,
        }
    }
    unreachable!("bounded process launch loop always returns")
}

fn status_with_busy_retry(command: &mut Command) -> std::io::Result<ExitStatus> {
    for attempt in 0..20 {
        match command.status() {
            Err(error) if error.raw_os_error() == Some(26) && attempt < 19 => {
                std::thread::sleep(Duration::from_millis(5));
            }
            result => return result,
        }
    }
    unreachable!("bounded process launch loop always returns")
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::io::Write;
    use std::os::unix::fs::PermissionsExt;

    fn fixture() -> (tempfile::TempDir, tempfile::TempDir, PathBuf, String) {
        let root = tempfile::tempdir().unwrap();
        let gateway = root.path().join(GATEWAY_PATH);
        fs::create_dir_all(gateway.parent().unwrap()).unwrap();
        fs::write(&gateway, "print('fixture')\n").unwrap();
        let second = root.path().join("context/second.py");
        fs::create_dir_all(second.parent().unwrap()).unwrap();
        fs::write(&second, "print('fixture')\n").unwrap();
        let policy = root.path().join(RUNTIME_POLICY_PATH);
        fs::create_dir_all(policy.parent().unwrap()).unwrap();
        let lock = root
            .path()
            .join(".processkit/runtime/python-requirements.lock");
        let lock_payload = "mcp==1.0.0 --hash=sha256:0000000000000000000000000000000000000000000000000000000000000000\n";
        fs::write(&lock, lock_payload).unwrap();
        let lock_sha = format!("{:x}", Sha256::digest(lock_payload.as_bytes()));
        fs::write(
            &policy,
            format!(
                r#"{{
                  "apiVersion": "processkit.projectious.work/python-runtime/v1alpha1",
                  "kind": "PythonRuntimePolicy",
                  "aggregateSha256": "{digest}",
                  "dependencyResolution": {{
                    "resolvedVersionsLocked": true,
                    "hashesRequired": true,
                    "lockFile": ".processkit/runtime/python-requirements.lock",
                    "lockSha256": "{lock_sha}"
                  }},
                  "dependencyProfiles": [
                    {{
                      "sha256": "{digest}",
                      "serverPaths": ["{GATEWAY_PATH}"],
                      "dependencies": ["mcp[cli]>=1.0,<2.0"],
                      "requiresPython": ">=3.10"
                    }},
                    {{
                      "sha256": "{digest}",
                      "serverPaths": ["context/second.py"],
                      "dependencies": ["pyyaml>=6.0"],
                      "requiresPython": ">=3.10"
                    }}
                  ]
                }}"#,
                digest = "0".repeat(64),
                lock_sha = lock_sha,
            ),
        )
        .unwrap();

        let tools = tempfile::tempdir().unwrap();
        let log = tools.path().join("args.log");
        let uv = tools.path().join("uv");
        let mut uv_file = fs::File::create(&uv).unwrap();
        uv_file
            .write_all(
                format!(
                    "#!/bin/sh\nif [ \"$1\" = --version ]; then echo 'uv fixture'; \
                 else printf '%s\\n' \"$@\" > '{}'; fi\n",
                    log.display()
                )
                .as_bytes(),
            )
            .unwrap();
        uv_file.sync_all().unwrap();
        drop(uv_file);
        let mut permissions = fs::metadata(&uv).unwrap().permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(&uv, permissions).unwrap();
        (root, tools, uv, log.display().to_string())
    }

    #[test]
    fn verify_reports_gateway_and_uv() {
        let (root, _tools, _uv, _) = fixture();
        let result = verify_mcp_with_uv(root.path(), Path::new("/bin/echo")).unwrap();
        assert_eq!(result.status, "verified");
        assert!(!result.uv_version.is_empty());
    }

    #[test]
    fn serve_constructs_direct_loopback_arguments() {
        let (root, _tools, uv, log) = fixture();
        let code = serve_mcp_with_uv(
            root.path(),
            McpTransport::StreamableHttp,
            "127.0.0.1",
            8123,
            "/mcp",
            &uv,
        )
        .unwrap();
        assert_eq!(code, 0);
        let args = fs::read_to_string(log).unwrap();
        assert!(args.contains("streamable-http"));
        assert!(args.contains("8123"));
    }

    #[test]
    fn serve_rejects_non_loopback_http() {
        let (root, _tools, uv, _) = fixture();
        let error = serve_mcp_with_uv(
            root.path(),
            McpTransport::StreamableHttp,
            "0.0.0.0",
            8000,
            "/mcp",
            &uv,
        )
        .unwrap_err();
        assert!(error.contains("loopback"));
    }

    #[test]
    fn offline_preparation_checks_every_profile() {
        let (root, _tools, uv, _) = fixture();
        let cache = tempfile::tempdir().unwrap();
        let result = prepare_runtime_with_uv(root.path(), Some(cache.path()), true, &uv).unwrap();
        assert_eq!(result.status, "offline-ready");
        assert_eq!(result.profile_count, 2);
    }

    #[test]
    fn offline_preparation_requires_existing_cache() {
        let (root, _tools, uv, _) = fixture();
        let missing = root.path().join("missing-cache");
        let error = prepare_runtime_with_uv(root.path(), Some(&missing), true, &uv).unwrap_err();
        assert!(error.contains("runtime cache directory"));
    }

    #[test]
    fn preparation_rejects_tampered_runtime_lock() {
        let (root, _tools, uv, _) = fixture();
        fs::write(
            root.path()
                .join(".processkit/runtime/python-requirements.lock"),
            "mcp==9.9.9 --hash=sha256:ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff\n",
        )
        .unwrap();
        let error = prepare_runtime_with_uv(root.path(), None, false, &uv).unwrap_err();
        assert!(error.contains("digest differs"));
    }
}
