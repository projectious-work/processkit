#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "usage: $0 <version> [rust-target]" >&2
    exit 2
fi

VERSION="$1"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET="${2:-$(rustc -vV | awk '/^host:/ {print $2}')}"
CARGO_VERSION="v$(awk -F'\"' '/^version = / {print $2; exit}' \
    "$REPO_ROOT/installer/crates/processkit/Cargo.toml")"
DIST_VERSION="v$(awk '/^  version:/ {print $2; exit}' \
    "$REPO_ROOT/src/.processkit/installer/distribution.yaml")"

if [[ "$VERSION" != "$CARGO_VERSION" || "$VERSION" != "$DIST_VERSION" ]]; then
    echo "error: release, installer, and distribution versions must agree" >&2
    echo "release=$VERSION installer=$CARGO_VERSION distribution=$DIST_VERSION" >&2
    exit 1
fi

if ! command -v cc >/dev/null; then
    export "CARGO_TARGET_$(tr '[:lower:]-' '[:upper:]_' <<<"$TARGET")_LINKER"="$REPO_ROOT/scripts/zig-cc-local.sh"
    export ZIG_GLOBAL_CACHE_DIR="${TMPDIR:-/tmp}/processkit-zig-global"
    export ZIG_LOCAL_CACHE_DIR="${TMPDIR:-/tmp}/processkit-zig-local"
fi

cargo build --locked --release --target "$TARGET" \
    --manifest-path "$REPO_ROOT/installer/Cargo.toml"
mkdir -p "$REPO_ROOT/dist"
ASSET="$REPO_ROOT/dist/processkit-$VERSION-$TARGET"
cp "$REPO_ROOT/installer/target/$TARGET/release/processkit" "$ASSET"
chmod 755 "$ASSET"
(
    cd "$REPO_ROOT/dist"
    sha256sum "$(basename "$ASSET")" >"$(basename "$ASSET").sha256"
)
"$ASSET" --version
echo "built installer: $ASSET"
