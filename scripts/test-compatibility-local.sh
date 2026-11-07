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
    TARGET_ROOT="$(mktemp -d "${TMPDIR:-/tmp}/processkit-migrated.XXXXXX")"
    git -C "$REPO_ROOT" archive "$version" src |
        tar -x -C "$EXACT_ROOT"
    mkdir -p "$EXACT_ROOT/src/context/workitems/2026/07"
    mkdir -p "$EXACT_ROOT/src/context/logs/2026/07"
    mkdir -p "$EXACT_ROOT/src/context/artifacts"
    mkdir -p "$EXACT_ROOT/src/context/bindings"
    mkdir -p "$EXACT_ROOT/src/context/roles"
    mkdir -p "$EXACT_ROOT/src/context/team-members/legacy-agent"
    printf '%s\n' \
        '---' \
        'apiVersion: processkit.projectious.work/v2' \
        'kind: WorkItem' \
        'metadata:' \
        '  id: BACK-legacy-fixture' \
        'spec:' \
        '  title: Legacy migration fixture' \
        '  state: backlog' \
        '---' \
        >"$EXACT_ROOT/src/context/workitems/2026/07/BACK-legacy-fixture.md"
    printf '%s\n' \
        '---' \
        'apiVersion: processkit.projectious.work/v2' \
        'kind: LogEntry' \
        'metadata:' \
        '  id: LOG-legacy-fixture' \
        'spec:' \
        '  event_type: test.fixture' \
        '  actor: system' \
        '  timestamp: 2026-07-30T00:00:00Z' \
        '---' \
        >"$EXACT_ROOT/src/context/logs/2026/07/LOG-legacy-fixture.md"
    for fixture in \
        'artifacts Artifact ART-legacy-fixture legacy-artifact.md' \
        'bindings Binding BIND-legacy-fixture legacy-binding.md' \
        'roles Role ROLE-legacy-fixture legacy-role.md' \
        'team-members/legacy-agent TeamMember TEAMMEMBER-legacy-fixture team-member.md'
    do
        set -- $fixture
        printf '%s\n' \
            '---' \
            'apiVersion: processkit.projectious.work/v2' \
            "kind: $2" \
            'metadata:' \
            "  id: $3" \
            'spec: {}' \
            '---' \
            >"$EXACT_ROOT/src/context/$1/$4"
    done
    "$REPO_ROOT/installer/target/debug/processkit" inspect-compatibility \
        --root "$EXACT_ROOT/src" --distribution "$REPO_ROOT/src" --json |
        jq -e --arg version "$version" '
          .status == "exact-release"
          and .matches == [{
            manifestId: (
              "v0-release-" + ($version | ltrimstr("v") | gsub("\\."; "-"))
            ),
            migration: .matches[0].migration,
            ownershipBaseline: (
              ".processkit/installer/compatibility/" + $version
              + "-ownership.json"
            ),
            releaseVersion: $version
          }]
          and .migration.disposition == "evidence-only"
        ' >/dev/null
    "$REPO_ROOT/installer/target/debug/processkit" migrate-v0 \
        --source "$EXACT_ROOT/src" \
        --root "$TARGET_ROOT" \
        --distribution "$REPO_ROOT/src" \
        --profile minimal \
        --plan-only \
        --json |
        jq -e '
          .status == "planned"
          and .target.disposition == "not-modified"
          and .corpus.summary.blocked == 0
        ' >/dev/null
    test -z "$(find "$TARGET_ROOT" -mindepth 1 -print -quit)"
    "$REPO_ROOT/installer/target/debug/processkit" migrate-v0 \
        --source "$EXACT_ROOT/src" \
        --root "$TARGET_ROOT" \
        --distribution "$REPO_ROOT/src" \
        --profile minimal \
        --yes \
        --json |
        jq -e --arg version "$version" '
          .status == "transitioned-to-fresh-target"
          and .source.releaseVersion == $version
          and .source.disposition == "preserved-read-only"
          and .target.release.version != null
          and .corpus.status == "applied"
          and .corpus.entryCount == 6
          and (.corpus.planSha256 | test("^[0-9a-f]{64}$"))
          and .corpus.plan.status == "planned"
          and .corpus.plan.summary == {
            blocked: 0,
            copyCompatible: 5,
            preserveImmutable: 1
          }
          and (.corpus.plan.entries | map(.disposition) | sort) == [
            "copy-compatible",
            "copy-compatible",
            "copy-compatible",
            "copy-compatible",
            "copy-compatible",
            "preserve-immutable"
          ]
          and (.corpus.plan.entries | all(.fieldLoss == []))
          and .corpus.plan.excludedRoots == []
          and .errors == []
        ' >/dev/null
    cmp \
        "$EXACT_ROOT/src/context/workitems/2026/07/BACK-legacy-fixture.md" \
        "$TARGET_ROOT/context/workitems/2026/07/BACK-legacy-fixture.md"
    cmp \
        "$EXACT_ROOT/src/context/logs/2026/07/LOG-legacy-fixture.md" \
        "$TARGET_ROOT/context/logs/2026/07/LOG-legacy-fixture.md"
    for migrated in \
        context/artifacts/legacy-artifact.md \
        context/bindings/legacy-binding.md \
        context/roles/legacy-role.md \
        context/team-members/legacy-agent/team-member.md
    do
        cmp "$EXACT_ROOT/src/$migrated" "$TARGET_ROOT/$migrated"
    done
    jq -e --arg version "$version" '
      (.migrationEvidence | length) == 1
      and .migrationEvidence[0].entryCount == 6
      and .migrationEvidence[0].manifestId == (
        "v0-release-" + ($version | ltrimstr("v") | gsub("\\."; "-"))
      )
      and .migrationEvidence[0].sourceRelease == $version
      and .migrationEvidence[0].plan.status == "planned"
      and (.migrationEvidence[0].plan.entries | length) == 6
      and (.migrationEvidence[0].planSha256 | test("^[0-9a-f]{64}$"))
    ' "$TARGET_ROOT/.processkit/state.json" >/dev/null
    "$REPO_ROOT/installer/target/debug/processkit" verify \
        --root "$TARGET_ROOT" --json |
        jq -e '.status == "verified"' >/dev/null
    "$REPO_ROOT/installer/target/debug/processkit" migrate-v0 \
        --source "$EXACT_ROOT/src" \
        --root "$TARGET_ROOT" \
        --distribution "$REPO_ROOT/src" \
        --profile minimal \
        --yes \
        --json |
        jq -e '
          .status == "already-transitioned"
          and .target.disposition == "verified-existing-migration"
          and .corpus.status == "already-applied"
          and .errors == []
        ' >/dev/null
    jq -e '(.migrationEvidence | length) == 1' \
        "$TARGET_ROOT/.processkit/state.json" >/dev/null
    printf '\nlocal drift\n' \
        >>"$TARGET_ROOT/context/workitems/2026/07/BACK-legacy-fixture.md"
    set +e
    DRIFT_RESULT="$(
        "$REPO_ROOT/installer/target/debug/processkit" verify \
            --root "$TARGET_ROOT" --json
    )"
    DRIFT_STATUS=$?
    set -e
    test "$DRIFT_STATUS" -eq 4
    jq -e '
      .status == "drifted"
      and (.errors | any(.code == "migrated-path-drift"))
    ' <<<"$DRIFT_RESULT" >/dev/null
    cp \
        "$EXACT_ROOT/src/context/workitems/2026/07/BACK-legacy-fixture.md" \
        "$TARGET_ROOT/context/workitems/2026/07/BACK-legacy-fixture.md"
    test ! -e "$EXACT_ROOT/src/.processkit/state.json"
    rm -rf "$EXACT_ROOT"
    rm -rf "$TARGET_ROOT"
done

REJECT_SOURCE="$(mktemp -d "${TMPDIR:-/tmp}/processkit-reject.XXXXXX")"
REJECT_TARGET="$(mktemp -d "${TMPDIR:-/tmp}/processkit-reject-target.XXXXXX")"
mkdir -p "$REJECT_SOURCE/context/schemas"
cp "$REPO_ROOT/src/context/.processkit-mcp-manifest.json" \
    "$REJECT_SOURCE/context/.processkit-mcp-manifest.json"
cp "$REPO_ROOT/src/context/schemas/workitem.yaml" \
    "$REJECT_SOURCE/context/schemas/workitem.yaml"
if "$REPO_ROOT/installer/target/debug/processkit" migrate-v0 \
    --source "$REJECT_SOURCE" \
    --root "$REJECT_TARGET" \
    --distribution "$REPO_ROOT/src" \
    --yes >/dev/null 2>&1; then
    echo "candidate-only legacy source was accepted" >&2
    exit 1
fi
rm -rf "$REJECT_SOURCE" "$REJECT_TARGET"

BLOCKED_SOURCE="$(mktemp -d "${TMPDIR:-/tmp}/processkit-blocked.XXXXXX")"
BLOCKED_TARGET="$(mktemp -d "${TMPDIR:-/tmp}/processkit-blocked-target.XXXXXX")"
git -C "$REPO_ROOT" archive v0.28.4 src |
    tar -x -C "$BLOCKED_SOURCE"
mkdir -p "$BLOCKED_SOURCE/src/context/workitems"
printf '%s\n' \
    '---' \
    'apiVersion: processkit.projectious.work/v2' \
    'kind: UnknownEntity' \
    'metadata:' \
    '  id: UNKNOWN-legacy-fixture' \
    'spec: {}' \
    '---' \
    >"$BLOCKED_SOURCE/src/context/workitems/UNKNOWN-legacy-fixture.md"
"$REPO_ROOT/installer/target/debug/processkit" migrate-v0 \
    --source "$BLOCKED_SOURCE/src" \
    --root "$BLOCKED_TARGET" \
    --distribution "$REPO_ROOT/src" \
    --plan-only \
    --json |
    jq -e '
      .status == "blocked"
      and .target.disposition == "not-modified"
      and .corpus.summary.blocked == 1
      and .corpus.errors[0].code == "kind-directory-mismatch"
    ' >/dev/null
test -z "$(find "$BLOCKED_TARGET" -mindepth 1 -print -quit)"
rm -rf "$BLOCKED_SOURCE" "$BLOCKED_TARGET"

OWNERSHIP_SOURCE="$(mktemp -d "${TMPDIR:-/tmp}/processkit-owned.XXXXXX")"
OWNERSHIP_TARGET="$(mktemp -d "${TMPDIR:-/tmp}/processkit-owned-target.XXXXXX")"
git -C "$REPO_ROOT" archive v0.28.4 src |
    tar -x -C "$OWNERSHIP_SOURCE"
OWNERSHIP_BASELINE="$REPO_ROOT/src/.processkit/installer/compatibility/"
OWNERSHIP_BASELINE+="v0.28.4-ownership.json"
OWNED_PATH="$(jq -r '.files | keys[0]' "$OWNERSHIP_BASELINE")"
printf '\nlocally modified\n' >>"$OWNERSHIP_SOURCE/src/$OWNED_PATH"
"$REPO_ROOT/installer/target/debug/processkit" migrate-v0 \
    --source "$OWNERSHIP_SOURCE/src" \
    --root "$OWNERSHIP_TARGET" \
    --distribution "$REPO_ROOT/src" \
    --plan-only \
    --json |
    jq -e '
      .status == "blocked"
      and .target.disposition == "not-modified"
      and (.corpus.errors | any(
        .code == "modified-product-owned-path"
        and (.remediation | length) > 0
      ))
    ' >/dev/null
test -z "$(find "$OWNERSHIP_TARGET" -mindepth 1 -print -quit)"
rm -rf "$OWNERSHIP_SOURCE" "$OWNERSHIP_TARGET"

INTERRUPT_SOURCE="$(mktemp -d "${TMPDIR:-/tmp}/processkit-migrate-interrupt.XXXXXX")"
INTERRUPT_TARGET="$(mktemp -d "${TMPDIR:-/tmp}/processkit-migrate-recover.XXXXXX")"
git -C "$REPO_ROOT" archive v0.28.4 src |
    tar -x -C "$INTERRUPT_SOURCE"
mkdir -p "$INTERRUPT_SOURCE/src/context/workitems/2026/07"
printf '%s\n' \
    '---' \
    'apiVersion: processkit.projectious.work/v2' \
    'kind: WorkItem' \
    'metadata:' \
    '  id: BACK-interrupted-migration' \
    'spec:' \
    '  title: Interrupted migration fixture' \
    '  state: backlog' \
    '---' \
    >"$INTERRUPT_SOURCE/src/context/workitems/2026/07/BACK-interrupted-migration.md"
set +e
PROCESSKIT_INSTALLER_FAIL_OPERATION=migrate-v0-corpus \
PROCESSKIT_INSTALLER_FAIL_AFTER_ACTION=0 \
    "$REPO_ROOT/installer/target/debug/processkit" migrate-v0 \
    --source "$INTERRUPT_SOURCE/src" \
    --root "$INTERRUPT_TARGET" \
    --distribution "$REPO_ROOT/src" \
    --profile minimal \
    --yes >/dev/null 2>&1
INTERRUPT_STATUS=$?
set -e
test "$INTERRUPT_STATUS" -eq 75
test "$(find "$INTERRUPT_TARGET/.processkit/transactions" \
    -name '*.json' -type f | wc -l)" -eq 1
"$REPO_ROOT/installer/target/debug/processkit" recover \
    --root "$INTERRUPT_TARGET" --yes --json |
    jq -e '.status == "recovered" and .recovered == 1' >/dev/null
test ! -e \
    "$INTERRUPT_TARGET/context/workitems/2026/07/BACK-interrupted-migration.md"
jq -e '(.migrationEvidence // []) == []' \
    "$INTERRUPT_TARGET/.processkit/state.json" >/dev/null
"$REPO_ROOT/installer/target/debug/processkit" verify \
    --root "$INTERRUPT_TARGET" --json |
    jq -e '.status == "verified"' >/dev/null
test -f \
    "$INTERRUPT_SOURCE/src/context/workitems/2026/07/BACK-interrupted-migration.md"
rm -rf "$INTERRUPT_SOURCE" "$INTERRUPT_TARGET"

echo "processkit-native compatibility, corpus application, and recovery passed"
