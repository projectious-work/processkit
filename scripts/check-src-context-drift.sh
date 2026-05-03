#!/usr/bin/env bash
# check-src-context-drift.sh — CI/release-time drift guard
#
# Compares /workspace/context/ (dogfood tree) against /workspace/src/context/
# (the template tree shipped to consumers in the release tarball).
#
# History: v0.15.0–v0.18.0 shipped four releases where src/context/ was
# missing content that had already landed in dogfood context/. The v0.18.1
# hotfix re-synced the trees. This script makes that class of drift
# detectable at release time rather than post-publish.
#
# Exit codes:
#   0 — selected guard passed
#   1 — genuine drift or release-contract violation detected
#   2 — usage error

set -euo pipefail

# ---------------------------------------------------------------------------
# ALLOWLIST — paths that are legitimately absent from or different in
# src/context/ and should be ignored by the diff.  Edit this list when you
# add a new justified divergence; include a comment explaining why.
# ---------------------------------------------------------------------------

# Dogfood-project runtime directories: contain live project state for the
# processkit repo itself — actors, artifacts, decisions, discussions, logs,
# migrations, notes, roles, team, workitems, bindings.  These are consumed
# by the dogfood aibox instance and must NOT ship to consumers.
ALLOWLIST_DOGFOOD_ONLY_DIRS=(
    "actors"
    "artifacts"
    "bindings"
    "decisions"
    "discussions"
    "logs"
    "migrations"
    "notes"
    "roles"
    "team"
    "workitems"
)

# templates/ — versioned template snapshots live only under
# context/templates/; src/context/ intentionally has no templates/ subtree
# because consumers receive templates via the tarball root, not via context/.
ALLOWLIST_TEMPLATES=1

# INDEX.md at the context/ root — dogfood-specific overview document;
# src/context/ ships its own INDEX.md (or none) independently.
ALLOWLIST_DOGFOOD_INDEX=1

# .cache/ — transient model/runtime cache; never shipped.
ALLOWLIST_CACHE_DIR=1

# .state/ — runtime state markers (e.g. skill-gate acknowledgement files);
# presence varies per installation.
ALLOWLIST_STATE_DIR=1

# .gitkeep files — empty placeholder files used by git to track otherwise-
# empty directories.  They may appear in src/context/ and not in dogfood
# or vice-versa with no semantic impact.
ALLOWLIST_GITKEEP=1

# __pycache__/ — transient Python bytecode; excluded from tarball already.
ALLOWLIST_PYCACHE=1

# .processkit-provenance.toml — release-time provenance stamp written into
# context/ by scripts/stamp-provenance.sh after the tarball is built.  It
# records the dogfood instance's installed processkit version and ships only
# in the dogfood tree; src/context/ never carries a provenance stamp because
# consumers stamp their own at install time.
ALLOWLIST_PROVENANCE=1

# scripts/ subdirs under src/context/skills/*/ that contain only .gitkeep (or
# are empty) — template-only artifacts.  The release installer creates these
# empty scripts/ placeholders in consumer installs for structural consistency,
# but the dogfood context/ tree does not need them because dogfood only keeps
# scripts/ dirs that have real content (pk-doctor, skill-gate).  The diff
# reports them as "Only in <SRC>/skills/<pkg>/<skill>: scripts"; we filter
# those entries out after verifying the src-side scripts/ dir is empty-ish.
ALLOWLIST_EMPTY_SRC_SCRIPTS=1

# ---------------------------------------------------------------------------

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
DOGFOOD="$REPO_ROOT/context"
SRC="$REPO_ROOT/src/context"

VERBOSE=0
SHOW_HELP=0
MODE="drift"

for arg in "$@"; do
    case "$arg" in
        --help|-h)  SHOW_HELP=1 ;;
        --verbose)  VERBOSE=1   ;;
        --release-deliverable) MODE="release-deliverable" ;;
        *)
            echo "unknown option: $arg" >&2
            echo "usage: $0 [--help] [--verbose] [--release-deliverable]" >&2
            exit 2
            ;;
    esac
done

if [[ $SHOW_HELP -eq 1 ]]; then
    cat <<'EOF'
check-src-context-drift.sh — drift and release-deliverable guards

SYNOPSIS
    scripts/check-src-context-drift.sh [--verbose]
    scripts/check-src-context-drift.sh --release-deliverable

DESCRIPTION
    Compares the dogfood context tree (context/) against the template tree
    that ships to consumers (src/context/), filtering out paths that are
    legitimately different via a top-of-file allowlist.

    Exits 0 when the trees are in sync (after allowlisting).
    Exits 1 when genuine drift is detected and prints offending paths.

    Run this before every release.  Wire it into build-release-tarball.sh
    so a drift-free tree is a hard pre-condition for building the tarball.

    With --release-deliverable, this script validates the shipped
    src/context/ contract directly instead of treating live dogfood context/
    drift as a release blocker. Dogfood state can legitimately contain
    project memory, generated harness state, and legacy migration-source
    files that must not ship in a processkit release.

OPTIONS
    --verbose   Also print the full filtered diff output, not just the
                summary of offending paths.
    --release-deliverable
                Validate src/context/ as the release artifact boundary.
    --help      Show this help and exit.

ALLOWLIST
    Edit the ALLOWLIST_* constants at the top of this script.  Each entry
    must have a comment explaining why the divergence is intentional.

FIXING DRIFT
    1. Run this script to see the offending paths.
    2. Copy the missing or updated files from context/ into src/context/.
    3. Re-run to confirm the guard passes.
    4. If the divergence is genuinely intentional, add a justified entry to
       the ALLOWLIST_* constants at the top of the script.
EOF
    exit 0
fi

if [[ ! -d "$DOGFOOD" ]]; then
    echo "error: dogfood tree not found: $DOGFOOD" >&2
    exit 1
fi
if [[ ! -d "$SRC" ]]; then
    echo "error: src context tree not found: $SRC" >&2
    exit 1
fi

if [[ "$MODE" == "release-deliverable" ]]; then
    failures=()

    required_dirs=(
        "artifacts"
        "bindings"
        "roles"
        "schemas"
        "skills"
        "state-machines"
        "team"
        "team-members"
    )
    for d in "${required_dirs[@]}"; do
        if [[ ! -d "$SRC/$d" ]]; then
            failures+=("missing required release directory: src/context/$d")
        fi
    done

    forbidden_dirs=(
        ".cache"
        ".state"
        "decisions"
        "discussions"
        "logs"
        "migrations"
        "notes"
        "templates"
        "workitems"
    )
    for d in "${forbidden_dirs[@]}"; do
        if [[ -e "$SRC/$d" ]]; then
            failures+=("dogfood-only path must not ship: src/context/$d")
        fi
    done

    if [[ -d "$SRC/artifacts" ]]; then
        while IFS= read -r -d '' f; do
            rel="${f#$SRC/}"
            base="$(basename "$f")"
            if [[ ! "$base" =~ ^ART-[0-9]{8}_[0-9]{4}-(ModelSpec|ModelProfile)-[a-z0-9-]+\.md$ ]]; then
                failures+=("non-model artifact must not ship: src/context/$rel")
                continue
            fi
            if ! grep -q '^kind: Artifact$' "$f"; then
                failures+=("model artifact missing kind: Artifact: src/context/$rel")
            fi
            if ! grep -Eq '^  kind: model-(spec|profile)$' "$f"; then
                failures+=("model artifact missing spec.kind=model-spec/profile: src/context/$rel")
            fi
        done < <(find "$SRC/artifacts" -type f -print0)
    fi

    demoted_dirs=(
        "metrics"
        "models"
        "processes"
        "schedules"
        "statemachines"
    )
    for d in "${demoted_dirs[@]}"; do
        if [[ -e "$SRC/$d" ]]; then
            failures+=("demoted primitive path must not ship: src/context/$d")
        fi
    done

    demoted_schemas=(
        "metric.yaml"
        "model.yaml"
        "process.yaml"
        "schedule.yaml"
        "statemachine.yaml"
    )
    for f in "${demoted_schemas[@]}"; do
        if [[ -e "$SRC/schemas/$f" ]]; then
            failures+=("demoted primitive schema must not ship: src/context/schemas/$f")
        fi
    done

    if [[ ! -f "$SRC/.processkit-mcp-manifest.json" ]]; then
        failures+=("missing MCP manifest: src/context/.processkit-mcp-manifest.json")
    fi

    if command -v rg >/dev/null 2>&1; then
        if rg -n '(^kind:\s*(Model|Process|Metric|Schedule)\s*$|target_kind:\s*(Model|Process|Metric|Schedule)\s*$)' "$SRC" >/dev/null 2>&1; then
            failures+=(
                "shipped src/context contains demoted entity vocabulary "
                "(kind or target_kind for Model/Process/Metric/Schedule)"
            )
        fi
    fi

    if [[ ${#failures[@]} -eq 0 ]]; then
        echo "OK: src/context release deliverable contract passed." >&2
        exit 0
    fi

    echo "RELEASE DELIVERABLE CONTRACT VIOLATIONS:" >&2
    printf '  - %s\n' "${failures[@]}" >&2
    echo "" >&2
    echo "To fix:" >&2
    echo "  1. Keep project memory and legacy migration-source state in context/." >&2
    echo "  2. Keep shipped release content under src/context/." >&2
    echo "  3. Remove demoted primitive directories/schemas from src/context/." >&2
    exit 1
fi

# ---------------------------------------------------------------------------
# Run the diff and filter
# ---------------------------------------------------------------------------

raw_diff="$(diff -rq "$DOGFOOD" "$SRC" 2>/dev/null || true)"

if [[ $VERBOSE -eq 1 ]]; then
    echo "=== raw diff (before filtering) ===" >&2
    echo "$raw_diff" >&2
    echo "===================================" >&2
fi

# Build the grep -E pattern for the dogfood-only directory names.
dogfood_dir_pattern=""
for d in "${ALLOWLIST_DOGFOOD_ONLY_DIRS[@]}"; do
    if [[ -n "$dogfood_dir_pattern" ]]; then
        dogfood_dir_pattern="$dogfood_dir_pattern|"
    fi
    # Match "Only in <DOGFOOD>: <dirname>" (top-level or nested)
    dogfood_dir_pattern="${dogfood_dir_pattern}Only in ${DOGFOOD}[^:]*: ${d}$"
done

filtered_diff="$raw_diff"

# Apply each allowlist filter in turn.
if [[ -n "$dogfood_dir_pattern" ]]; then
    filtered_diff="$(echo "$filtered_diff" | grep -Ev "$dogfood_dir_pattern" || true)"
fi

if [[ $ALLOWLIST_TEMPLATES -eq 1 ]]; then
    # Match both "Only in .../context/: templates" (top-level dir entry) and
    # any path containing /templates/ (nested entries within the templates tree).
    filtered_diff="$(echo "$filtered_diff" | grep -Ev '(/templates|: templates$)' || true)"
fi

if [[ $ALLOWLIST_DOGFOOD_INDEX -eq 1 ]]; then
    filtered_diff="$(echo "$filtered_diff" | grep -v "Only in ${DOGFOOD}: INDEX.md" || true)"
fi

if [[ $ALLOWLIST_CACHE_DIR -eq 1 ]]; then
    filtered_diff="$(echo "$filtered_diff" | grep -v '/\.cache' || true)"
    filtered_diff="$(echo "$filtered_diff" | grep -v "Only in ${DOGFOOD}: \.cache" || true)"
fi

if [[ $ALLOWLIST_STATE_DIR -eq 1 ]]; then
    filtered_diff="$(echo "$filtered_diff" | grep -v '/\.state' || true)"
    filtered_diff="$(echo "$filtered_diff" | grep -v "Only in ${DOGFOOD}: \.state" || true)"
fi

if [[ $ALLOWLIST_GITKEEP -eq 1 ]]; then
    filtered_diff="$(echo "$filtered_diff" | grep -v '\.gitkeep' || true)"
fi

if [[ $ALLOWLIST_PYCACHE -eq 1 ]]; then
    filtered_diff="$(echo "$filtered_diff" | grep -v '__pycache__' || true)"
fi

if [[ $ALLOWLIST_PROVENANCE -eq 1 ]]; then
    filtered_diff="$(echo "$filtered_diff" | grep -v "Only in ${DOGFOOD}: \.processkit-provenance\.toml" || true)"
fi

if [[ $ALLOWLIST_EMPTY_SRC_SCRIPTS -eq 1 ]]; then
    # Drop "Only in <SRC>/skills/.../<skill>: scripts" lines where the
    # src-side scripts/ dir is empty or contains only .gitkeep.  Re-materialise
    # each candidate path and check ls output.  Non-empty scripts/ dirs (which
    # DO exist in dogfood context/) will not appear in the diff output anyway,
    # so those are not affected by this filter.
    _kept_lines=""
    while IFS= read -r _line; do
        if [[ "$_line" =~ ^Only\ in\ (${SRC}/skills/[^:]+):\ scripts$ ]]; then
            _parent="${BASH_REMATCH[1]}"
            _candidate="$_parent/scripts"
            if [[ -d "$_candidate" ]]; then
                _contents="$(ls -A "$_candidate" 2>/dev/null | grep -v '^\.gitkeep$' || true)"
                if [[ -z "$_contents" ]]; then
                    continue  # filter out: empty or gitkeep-only
                fi
            fi
        fi
        if [[ -n "$_line" ]]; then
            _kept_lines+="$_line"$'\n'
        fi
    done <<< "$filtered_diff"
    filtered_diff="${_kept_lines%$'\n'}"
fi

# Strip blank lines that filtering can leave behind.
filtered_diff="$(echo "$filtered_diff" | grep -v '^[[:space:]]*$' || true)"

# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

if [[ -z "$filtered_diff" ]]; then
    echo "OK: context/ and src/context/ are in sync (drift guard passed)." >&2
    exit 0
else
    echo "DRIFT DETECTED: context/ and src/context/ have diverged." >&2
    echo "" >&2
    echo "Offending paths:" >&2
    echo "$filtered_diff" >&2
    echo "" >&2
    echo "To fix:" >&2
    echo "  1. Review the paths above." >&2
    echo "  2. Copy new/updated files from context/ into src/context/." >&2
    echo "  3. Re-run: scripts/check-src-context-drift.sh" >&2
    echo "  4. If the difference is intentional, add a justified entry to the" >&2
    echo "     ALLOWLIST_* constants at the top of scripts/check-src-context-drift.sh." >&2
    exit 1
fi
