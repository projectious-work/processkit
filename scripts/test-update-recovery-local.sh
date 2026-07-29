#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEST_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/processkit-recovery.XXXXXX")"
PROJECT_ROOT="$TEST_ROOT/project"
DIST_A="$TEST_ROOT/distribution-a"
DIST_B="$TEST_ROOT/distribution-b"
FIXTURE="$REPO_ROOT/installer/crates/processkit/tests/fixtures/plans/empty/distribution"
PROCESSKIT="$REPO_ROOT/installer/target/debug/processkit"
trap 'rm -rf "$TEST_ROOT"' EXIT

cp -a "$FIXTURE" "$DIST_A"
cp -a "$FIXTURE" "$DIST_B"
mkdir -p "$PROJECT_ROOT"

MANIFEST="$DIST_B/.processkit/installer/distribution.yaml"
sed -i 's/version: 0.0.0-test/version: 0.0.1-test/' "$MANIFEST"
printf '%s\n' "updated payload" >"$DIST_B/payload/hello.txt"
MANIFEST_SHA="$(sha256sum "$MANIFEST" | awk '{print $1}')"
DESCRIPTOR="$DIST_B/.processkit/installer/release-descriptor.json"
jq --arg sha "$MANIFEST_SHA" \
    '.distribution.manifestSha256 = $sha' \
    "$DESCRIPTOR" >"$TEST_ROOT/descriptor.json"
mv "$TEST_ROOT/descriptor.json" "$DESCRIPTOR"

"$PROCESSKIT" install \
    --root "$PROJECT_ROOT" \
    --distribution "$DIST_A" \
    --profile managed \
    --yes >/dev/null
printf '%s\n' "owned by the project" >"$PROJECT_ROOT/user-owned.txt"
OLD_STATE_SHA="$(sha256sum "$PROJECT_ROOT/.processkit/state.json" |
    awk '{print $1}')"

set +e
PROCESSKIT_INSTALLER_FAIL_AFTER_ACTION=0 \
    "$PROCESSKIT" update \
    --root "$PROJECT_ROOT" \
    --distribution "$DIST_B" \
    --yes >/dev/null 2>"$TEST_ROOT/interrupted.stderr"
INTERRUPTED_STATUS=$?
set -e
[[ "$INTERRUPTED_STATUS" -eq 75 ]] || {
    echo "error: update failpoint exited $INTERRUPTED_STATUS, expected 75" >&2
    exit 1
}
find "$PROJECT_ROOT/.processkit/transactions" \
    -maxdepth 1 -type f -name 'update-*.json' -print -quit |
    grep -q . || {
    echo "error: interrupted update left no recovery journal" >&2
    exit 1
}

"$PROCESSKIT" recover --root "$PROJECT_ROOT" --yes --json \
    >"$TEST_ROOT/recover.json"
jq -e '.status == "recovered" and .recovered == 1' \
    "$TEST_ROOT/recover.json" >/dev/null
cmp "$DIST_A/payload/hello.txt" "$PROJECT_ROOT/payload/hello.txt"
[[ "$(sha256sum "$PROJECT_ROOT/.processkit/state.json" | awk '{print $1}')" \
    == "$OLD_STATE_SHA" ]]
grep -Fx "owned by the project" "$PROJECT_ROOT/user-owned.txt" >/dev/null
"$PROCESSKIT" verify --root "$PROJECT_ROOT" --json \
    >"$TEST_ROOT/verify-after-recovery.json"
jq -e '.status == "verified" and (.errors | length) == 0' \
    "$TEST_ROOT/verify-after-recovery.json" >/dev/null

"$PROCESSKIT" update \
    --root "$PROJECT_ROOT" \
    --distribution "$DIST_B" \
    --yes >/dev/null
cmp "$DIST_B/payload/hello.txt" "$PROJECT_ROOT/payload/hello.txt"
jq -e '.release.version == "0.0.1-test"' \
    "$PROJECT_ROOT/.processkit/state.json" >/dev/null
grep -Fx "owned by the project" "$PROJECT_ROOT/user-owned.txt" >/dev/null
"$PROCESSKIT" verify --root "$PROJECT_ROOT" --json \
    >"$TEST_ROOT/verify-after-update.json"
jq -e '.status == "verified" and (.errors | length) == 0' \
    "$TEST_ROOT/verify-after-update.json" >/dev/null

echo "interrupted update recovery acceptance passed"
