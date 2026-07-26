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
  any(
    .ownedPaths[];
    .ownership == "managed-keys"
    and .operation == "managed-keys-create/v1"
  )
' "$PILOT_ROOT/.processkit/state.json" >/dev/null || {
    jq '.ownedPaths[] | select(.ownership == "managed-keys")' \
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

echo "standalone installer pilot passed"
