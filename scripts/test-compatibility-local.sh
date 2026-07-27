#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/processkit-compatibility.XXXXXX")"
trap 'rm -rf "$TEST_ROOT"' EXIT
mkdir -p "$TEST_ROOT/context/schemas"
cp "$REPO_ROOT/src/context/.processkit-mcp-manifest.json" \
    "$TEST_ROOT/context/.processkit-mcp-manifest.json"
cp "$REPO_ROOT/src/context/schemas/workitem.yaml" \
    "$TEST_ROOT/context/schemas/workitem.yaml"

BEFORE="$TEST_ROOT/before.json"
AFTER="$TEST_ROOT/after.json"
"$REPO_ROOT/installer/target/debug/processkit" inspect-compatibility \
    --root "$TEST_ROOT" --distribution "$REPO_ROOT/src" --json >"$BEFORE"
jq -e '
  .status == "legacy-project-candidate"
  and .matches == []
  and .migration.disposition == "none"
' "$BEFORE" >/dev/null

printf 'contradictory = true\n' >"$TEST_ROOT/aibox.toml"
printf '{}\n' >"$TEST_ROOT/aibox.lock"
printf '{}\n' >"$TEST_ROOT/.mcp.json"
"$REPO_ROOT/installer/target/debug/processkit" inspect-compatibility \
    --root "$TEST_ROOT" --distribution "$REPO_ROOT/src" --json >"$AFTER"
diff -u "$BEFORE" "$AFTER"

printf 'not a processkit schema\n' >"$TEST_ROOT/context/schemas/workitem.yaml"
"$REPO_ROOT/installer/target/debug/processkit" inspect-compatibility \
    --root "$TEST_ROOT" --distribution "$REPO_ROOT/src" --json |
    jq -e '.status == "not-detected"' >/dev/null

for version in v0.27.1 v0.28.4; do
    EXACT_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/processkit-exact.XXXXXX")"
    git -C "$REPO_ROOT" archive "$version" src |
        tar -x -C "$EXACT_ROOT"
    "$REPO_ROOT/installer/target/debug/processkit" inspect-compatibility \
        --root "$EXACT_ROOT/src" --distribution "$REPO_ROOT/src" --json |
        jq -e --arg version "$version" '
          .status == "exact-release"
          and .matches == [{
            manifestId: (
              "v0-release-" + ($version | ltrimstr("v") | gsub("\\."; "-"))
            ),
            migration: .matches[0].migration,
            releaseVersion: $version
          }]
          and .migration.disposition == "evidence-only"
        ' >/dev/null
    rm -rf "$EXACT_ROOT"
done

echo "processkit-native compatibility detection passed"
