#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PILOT_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/processkit-pilot.XXXXXX")"
REQUEST="$(mktemp "${TMPDIR:-/tmp}/processkit-request.XXXXXX.json")"
trap 'rm -rf "$PILOT_ROOT"; rm -f "$REQUEST"' EXIT

jq -n \
    --arg root "$PILOT_ROOT" \
    --arg distribution "$REPO_ROOT/src" \
    '{
      apiVersion: "processkit.projectious.work/installer/v1alpha1",
      operation: "install",
      root: $root,
      distributionPath: $distribution,
      profiles: ["minimal"],
      harnesses: ["codex"],
      yes: true
    }' >"$REQUEST"

"$REPO_ROOT/installer/target/debug/processkit" execute \
    --request "$REQUEST" |
    jq -e '.status == "installed"' >/dev/null
jq -e '
  .mcpServers["processkit-gateway"].env.PROCESSKIT_MCP_MODE == "gateway"
' "$PILOT_ROOT/.mcp.json" >/dev/null

jq -n \
    --arg root "$PILOT_ROOT" \
    '{
      apiVersion: "processkit.projectious.work/installer/v1alpha1",
      operation: "uninstall",
      root: $root,
      yes: true
    }' >"$REQUEST"
"$REPO_ROOT/installer/target/debug/processkit" execute \
    --request "$REQUEST" |
    jq -e '.status == "uninstalled"' >/dev/null
[[ ! -e "$PILOT_ROOT/.mcp.json" ]] || {
    echo "error: managed Codex adapter remained after uninstall" >&2
    exit 1
}

echo "standalone installer pilot passed"
