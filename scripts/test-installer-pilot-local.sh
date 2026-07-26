#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PILOT_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/processkit-pilot.XXXXXX")"
REQUEST="$(mktemp "${TMPDIR:-/tmp}/processkit-request.XXXXXX.json")"
RESULT="$(mktemp "${TMPDIR:-/tmp}/processkit-result.XXXXXX.json")"
trap 'rm -rf "$PILOT_ROOT"; rm -f "$REQUEST" "$RESULT"' EXIT

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
    --request "$REQUEST" >"$RESULT"
jq -e '.status == "installed"' "$RESULT" >/dev/null
jq -e '
  .mcpServers["processkit-gateway"].env.PROCESSKIT_MCP_MODE == "gateway"
' "$PILOT_ROOT/.mcp.json" >/dev/null

jq -n \
    --arg root "$PILOT_ROOT" \
    '{
      apiVersion: "processkit.projectious.work/installer/v1alpha1",
      operation: "verify",
      root: $root
    }' >"$REQUEST"
"$REPO_ROOT/installer/target/debug/processkit" execute \
    --request "$REQUEST" >"$RESULT"
jq -e '
      .status == "verified"
      and .checked > 0
      and (.errors | length) == 0
    ' "$RESULT" >/dev/null

jq -n \
    --arg root "$PILOT_ROOT" \
    --arg distribution "$REPO_ROOT/src" \
    '{
      apiVersion: "processkit.projectious.work/installer/v1alpha1",
      operation: "update",
      root: $root,
      distributionPath: $distribution,
      yes: true
    }' >"$REQUEST"
"$REPO_ROOT/installer/target/debug/processkit" execute \
    --request "$REQUEST" >"$RESULT"
jq -e '
  .status == "updated"
  and .changes == [{"count": 0}]
' "$RESULT" >/dev/null
jq -e '
  any(.managedAdapters[]; .adapter == "codex" and .createdFile == true)
' "$PILOT_ROOT/.processkit/state.json" >/dev/null || {
    jq '.managedAdapters' \
        "$PILOT_ROOT/.processkit/state.json" >&2
    exit 1
}

jq -n \
    --arg root "$PILOT_ROOT" \
    '{
      apiVersion: "processkit.projectious.work/installer/v1alpha1",
      operation: "uninstall",
      root: $root,
      yes: true
    }' >"$REQUEST"
"$REPO_ROOT/installer/target/debug/processkit" execute \
    --request "$REQUEST" >"$RESULT"
jq -e '.status == "uninstalled"' "$RESULT" >/dev/null
[[ ! -e "$PILOT_ROOT/.mcp.json" ]] || {
    echo "error: managed Codex adapter remained after uninstall" >&2
    exit 1
}

# A user may add unrelated root data and MCP servers after installation.
# Update and uninstall must preserve both while removing only managed keys.
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
    --request "$REQUEST" >"$RESULT"
jq '
  .userSetting = true
  | .mcpServers.userServer = {
      command: "user-command",
      args: [],
      env: {}
    }
' "$PILOT_ROOT/.mcp.json" >"$RESULT"
mv "$RESULT" "$PILOT_ROOT/.mcp.json"

jq -n \
    --arg root "$PILOT_ROOT" \
    --arg distribution "$REPO_ROOT/src" \
    '{
      apiVersion: "processkit.projectious.work/installer/v1alpha1",
      operation: "update",
      root: $root,
      distributionPath: $distribution,
      yes: true
    }' >"$REQUEST"
"$REPO_ROOT/installer/target/debug/processkit" execute \
    --request "$REQUEST" >"$RESULT"
jq -n \
    --arg root "$PILOT_ROOT" \
    '{
      apiVersion: "processkit.projectious.work/installer/v1alpha1",
      operation: "uninstall",
      root: $root,
      yes: true
    }' >"$REQUEST"
"$REPO_ROOT/installer/target/debug/processkit" execute \
    --request "$REQUEST" >"$RESULT"
jq -e '
  .userSetting == true
  and .mcpServers.userServer.command == "user-command"
  and (.mcpServers | has("processkit-gateway") | not)
' "$PILOT_ROOT/.mcp.json" >/dev/null

echo "standalone installer pilot passed"
