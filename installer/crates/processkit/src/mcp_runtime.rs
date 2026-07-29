//! Native supervision for the shipped Python MCP gateway.

use serde::Serialize;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

const API_VERSION: &str = "processkit.projectious.work/runtime/v1alpha1";
const GATEWAY_PATH: &str = "context/skills/processkit/processkit-gateway/mcp/server.py";

#[derive(Clone, Copy, Debug)]
pub(super) enum McpTransport {
    Stdio,
    StreamableHttp,
}

#[derive(Serialize)]
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
    let output = Command::new(uv)
        .arg("--version")
        .output()
        .map_err(|error| format!("launch uv: {error}"))?;
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
    let status = command
        .current_dir(root)
        .status()
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
    let status = Command::new(uv)
        .arg("run")
        .arg(gateway)
        .args(["stdio-proxy", "--url", url])
        .current_dir(root)
        .status()
        .map_err(|error| format!("launch MCP stdio proxy: {error}"))?;
    Ok(status.code().unwrap_or(1))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::os::unix::fs::PermissionsExt;

    fn fixture() -> (tempfile::TempDir, tempfile::TempDir, PathBuf, String) {
        let root = tempfile::tempdir().unwrap();
        let gateway = root.path().join(GATEWAY_PATH);
        fs::create_dir_all(gateway.parent().unwrap()).unwrap();
        fs::write(&gateway, "print('fixture')\n").unwrap();

        let tools = tempfile::tempdir().unwrap();
        let log = tools.path().join("args.log");
        let uv = tools.path().join("uv");
        fs::write(
            &uv,
            format!(
                "#!/bin/sh\nif [ \"$1\" = --version ]; then echo 'uv fixture'; \
                 else printf '%s\\n' \"$@\" > '{}'; fi\n",
                log.display()
            ),
        )
        .unwrap();
        let mut permissions = fs::metadata(&uv).unwrap().permissions();
        permissions.set_mode(0o755);
        fs::set_permissions(&uv, permissions).unwrap();
        (root, tools, uv, log.display().to_string())
    }

    #[test]
    fn verify_reports_gateway_and_uv() {
        let (root, _tools, uv, _) = fixture();
        let result = verify_mcp_with_uv(root.path(), &uv).unwrap();
        assert_eq!(result.status, "verified");
        assert_eq!(result.uv_version, "uv fixture");
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
}
