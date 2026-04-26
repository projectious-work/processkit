#!/usr/bin/env bash
# build-release-tarball.sh — build the processkit release tarball.
#
# Produces:
#   dist/processkit-<version>.tar.gz
#   dist/processkit-<version>.tar.gz.sha256
#
# Contents (top-level inside the tarball is "processkit-<version>/"):
#   processkit-<version>/
#     primitives/
#     skills/
#     processes/
#     packages/
#     lib/
#     scaffolding/
#     PROVENANCE.toml
#     INDEX.md
#     LICENSE       (copied from repo root)
#     CHANGELOG.md  (copied from repo root, if present)
#
# Reproducibility: --owner=0 --group=0 --mtime=<tag-date> --sort=name.
# This is the producer side of DEC-025 (release-asset tarballs); aibox
# consumes the asset on the happy version-tag path and falls back to
# git fetch otherwise.
#
# Usage:
#   scripts/build-release-tarball.sh v0.5.0
#
# The tag must already exist in the local git history (the script reads
# the tag's commit date for --mtime).

set -euo pipefail

if [[ $# -ne 1 ]]; then
    echo "usage: $0 <version-tag>" >&2
    echo "example: $0 v0.5.0" >&2
    exit 2
fi

VERSION="$1"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DIR="$REPO_ROOT/src"
DIST_DIR="$REPO_ROOT/dist"
STAGING_PARENT="$(mktemp -d)"
STAGING_DIR="$STAGING_PARENT/processkit-$VERSION"
TARBALL="$DIST_DIR/processkit-$VERSION.tar.gz"
CHECKSUM="$TARBALL.sha256"

cleanup() {
    rm -rf "$STAGING_PARENT"
}
trap cleanup EXIT

if [[ ! -d "$SRC_DIR" ]]; then
    echo "error: $SRC_DIR not found — must run from a processkit checkout" >&2
    exit 1
fi

# Resolve the tag's commit date for reproducible mtime. If the tag does
# not yet exist (cutting a fresh release), fall back to HEAD's commit date.
if git -C "$REPO_ROOT" rev-parse "$VERSION" >/dev/null 2>&1; then
    MTIME="$(git -C "$REPO_ROOT" log -1 --format=%cI "$VERSION")"
else
    echo "warning: tag $VERSION not found; using HEAD commit date" >&2
    MTIME="$(git -C "$REPO_ROOT" log -1 --format=%cI HEAD)"
fi

mkdir -p "$DIST_DIR"
mkdir -p "$STAGING_DIR"

# Regenerate the MCP-config manifest so the release tarball carries the
# current aggregate hash (consumed by `aibox sync` to detect per-skill
# mcp-config changes that don't bump the processkit version).  See
# DEC-20260423_2049-VastLake and projectious-work/aibox#54.
echo "regenerating MCP-config manifest" >&2
if ! uv run "$REPO_ROOT/scripts/generate-mcp-manifest.py"; then
    echo "error: generate-mcp-manifest.py failed" >&2
    exit 1
fi

# Drift guard: ensure context/ (dogfood) and src/context/ (shipped template)
# are in sync before building the tarball.  If this fails, the release tree
# is inconsistent with what the changelog claims; fix the drift first.
echo "running drift guard: context/ vs src/context/" >&2
if ! "$REPO_ROOT/scripts/check-src-context-drift.sh"; then
    echo "" >&2
    echo "error: drift guard failed — src/context/ does not match context/." >&2
    echo "Run 'scripts/check-src-context-drift.sh --verbose' to inspect the diff," >&2
    echo "copy updated files from context/ into src/context/, or add a justified" >&2
    echo "entry to the ALLOWLIST_* constants in check-src-context-drift.sh." >&2
    exit 1
fi

# Provenance freshness guard: ensure src/PROVENANCE.toml has been re-stamped
# for the version we're about to build, so the published tarball does not
# advertise a stale generated_for_tag. See projectious-work/processkit#13.
echo "running provenance guard: stamp-provenance --check $VERSION" >&2
if ! "$REPO_ROOT/scripts/stamp-provenance.sh" --check "$VERSION"; then
    echo "" >&2
    echo "error: provenance guard failed — src/PROVENANCE.toml is stale for $VERSION." >&2
    echo "Run 'scripts/stamp-provenance.sh $VERSION' to regenerate," >&2
    echo "review the diff, and commit before re-running this script." >&2
    exit 1
fi

# Copy the entire src/ tree into the staging dir at the top level.
# Excludes: __pycache__/, .pyc files, .DS_Store, dotfiles inside src.
echo "staging src/ → $STAGING_DIR/" >&2
(cd "$SRC_DIR" && tar --exclude='__pycache__' \
                       --exclude='*.pyc' \
                       --exclude='.DS_Store' \
                       -cf - .) | (cd "$STAGING_DIR" && tar -xf -)

# Optionally include LICENSE and CHANGELOG.md from the repo root.
[[ -f "$REPO_ROOT/LICENSE" ]] && cp "$REPO_ROOT/LICENSE" "$STAGING_DIR/"
[[ -f "$REPO_ROOT/CHANGELOG.md" ]] && cp "$REPO_ROOT/CHANGELOG.md" "$STAGING_DIR/"

# Build the tarball reproducibly. The top-level entry inside the tarball
# is "processkit-<version>/" (so consumers unpack into the right
# top-level dir without a strip-components flag).
echo "tarballing → $TARBALL" >&2
(cd "$STAGING_PARENT" && \
    tar --owner=0 --group=0 \
        --mtime="$MTIME" \
        --sort=name \
        --format=ustar \
        -czf "$TARBALL" \
        "processkit-$VERSION")

# Compute and write the sibling checksum file.
# Format matches `sha256sum`'s output: `<hash>  <filename>`.
echo "computing sha256 → $CHECKSUM" >&2
(cd "$DIST_DIR" && sha256sum "processkit-$VERSION.tar.gz" > "processkit-$VERSION.tar.gz.sha256")

echo
echo "built:"
ls -lh "$TARBALL" "$CHECKSUM"
echo
echo "to upload as a release asset:"
echo "    gh release upload $VERSION $TARBALL $CHECKSUM"
