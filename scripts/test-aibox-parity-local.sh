#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/processkit-aibox-parity.XXXXXX")"
trap 'rm -rf "$TEST_ROOT"' EXIT

DIRECT="$TEST_ROOT/direct"
ADAPTER="$TEST_ROOT/adapter"
REQUEST="$TEST_ROOT/request.json"
mkdir -p "$DIRECT" "$ADAPTER"

"$REPO_ROOT/installer/target/debug/processkit" install \
    --root "$DIRECT" \
    --distribution "$REPO_ROOT/src" \
    --profile minimal \
    --harness codex \
    --yes --json >/dev/null

jq -n \
    --arg root "$ADAPTER" \
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
    --request "$REQUEST" >/dev/null

# aibox integrates only through the execute envelope. Root-specific values are
# normalized before comparing the processkit-owned installed state.
jq --sort-keys 'del(.installedAt, .updatedAt)' \
    "$DIRECT/.processkit/state.json" >"$TEST_ROOT/direct.json"
jq --sort-keys 'del(.installedAt, .updatedAt)' \
    "$ADAPTER/.processkit/state.json" >"$TEST_ROOT/adapter.json"
diff -u "$TEST_ROOT/direct.json" "$TEST_ROOT/adapter.json"
diff -u "$DIRECT/.mcp.json" "$ADAPTER/.mcp.json"

echo "direct CLI and aibox execute-envelope installed-state parity passed"
