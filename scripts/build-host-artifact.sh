#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
    echo "usage: $0 <version> <target> <source-sha>" >&2
    exit 2
fi

VERSION="$1"
TARGET="$2"
SOURCE_SHA="$3"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

[[ "$VERSION" =~ ^v1\.[0-9]+\.[0-9]+-[0-9A-Za-z.-]+$ ]] || {
    echo "error: exact v1 prerelease required" >&2
    exit 1
}
[[ "$SOURCE_SHA" =~ ^[0-9a-f]{40}$ ]] || {
    echo "error: full source SHA required" >&2
    exit 1
}
[[ "$(git -C "$REPO_ROOT" rev-parse HEAD)" == "$SOURCE_SHA" ]] || {
    echo "error: checkout does not match source SHA" >&2
    exit 1
}
[[ "$(git -C "$REPO_ROOT" rev-parse "$VERSION^{commit}")" == "$SOURCE_SHA" ]] || {
    echo "error: tag does not match source SHA" >&2
    exit 1
}
[[ -z "$(git -C "$REPO_ROOT" status --porcelain)" ]] || {
    echo "error: host checkout is dirty" >&2
    exit 1
}
host_target="$(rustc -vV | sed -n 's/^host: //p')"
[[ "$host_target" == "$TARGET" ]] || {
    echo "error: Rust host $host_target does not match target $TARGET" >&2
    exit 1
}

cargo build --locked --release \
    --manifest-path "$REPO_ROOT/installer/Cargo.toml"
binary="$REPO_ROOT/installer/target/release/processkit"
"$binary" --version | grep -F "${VERSION#v}"

mkdir -p "$REPO_ROOT/dist"
asset="$REPO_ROOT/dist/processkit-$VERSION-$TARGET"
cp "$binary" "$asset"
chmod 755 "$asset"
if command -v sha256sum >/dev/null; then
    (cd "$REPO_ROOT/dist" && sha256sum "${asset##*/}") >"$asset.sha256"
else
    (cd "$REPO_ROOT/dist" && shasum -a 256 "${asset##*/}") >"$asset.sha256"
fi
jq -n --sort-keys \
    --arg version "$VERSION" \
    --arg target "$TARGET" \
    --arg sourceSha "$SOURCE_SHA" \
    --arg hostOs "$(uname -s)" \
    --arg hostArch "$(uname -m)" \
    --arg hostKernel "$(uname -r)" \
    --arg rustHost "$host_target" \
    --arg rustcVersion "$(rustc --version)" \
    '{version:$version,target:$target,sourceSha:$sourceSha,
      buildEnvironment:"local-host",
      host:{os:$hostOs,arch:$hostArch,kernel:$hostKernel,rustHost:$rustHost,
        rustcVersion:$rustcVersion},
      smokeTest:"processkit --version"}' \
    >"$asset.provenance.json"
