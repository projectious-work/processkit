#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <version>" >&2
    exit 2
fi

VERSION="$1"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
NORMALIZED="${VERSION#v}"
CARGO_VERSION="$(awk -F'"' '/^version = / {print $2; exit}' \
    "$REPO_ROOT/installer/crates/processkit/Cargo.toml")"
LOCK_VERSION="$(awk '
    $0 == "name = \"processkit\"" { package = 1; next }
    package && /^version = / { gsub(/"/, "", $3); print $3; exit }
' "$REPO_ROOT/installer/Cargo.lock")"
DIST_VERSION="$(awk '/^  version:/ {print $2; exit}' \
    "$REPO_ROOT/src/.processkit/installer/distribution.yaml")"
LIB_VERSION="$(awk -F'"' '/^__version__ = / {print $2; exit}' \
    "$REPO_ROOT/src/context/skills/_lib/processkit/__init__.py")"
PROVENANCE_VERSION="$(awk -F'"' '/^generated_for_tag = / {print $2; exit}' \
    "$REPO_ROOT/src/PROVENANCE.toml")"

fail=0
for pair in \
    "Cargo.toml:$CARGO_VERSION" \
    "Cargo.lock:$LOCK_VERSION" \
    "distribution.yaml:$DIST_VERSION" \
    "processkit.__version__:$LIB_VERSION"; do
    label="${pair%%:*}"
    actual="${pair#*:}"
    if [[ "$actual" != "$NORMALIZED" ]]; then
        echo "error: $label version is $actual, expected $NORMALIZED" >&2
        fail=1
    fi
done

if [[ "$PROVENANCE_VERSION" != "v$NORMALIZED" ]]; then
    echo "error: provenance version is $PROVENANCE_VERSION, expected v$NORMALIZED" >&2
    fail=1
fi
if ! awk -v version="v$NORMALIZED" \
    '$0 ~ "^## \\[" version "\\]" { found = 1 } END { exit !found }' \
    "$REPO_ROOT/CHANGELOG.md"; then
    echo "error: changelog has no v$NORMALIZED release heading" >&2
    fail=1
fi

if [[ "$fail" -ne 0 ]]; then
    exit 1
fi
echo "release versions agree: v$NORMALIZED"
