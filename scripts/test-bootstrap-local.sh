#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TEST_ROOT="$(mktemp -d)"
trap 'rm -rf "$TEST_ROOT"' EXIT
VERSION="v1.2.3-alpha.1"
TARGET="aarch64-unknown-linux-gnu"
RELEASE_DIR="$TEST_ROOT/repo/releases/download/$VERSION"
BIN_DIR="$TEST_ROOT/bin"
mkdir -p "$RELEASE_DIR"

PRIVATE_KEY="$TEST_ROOT/private.pem"
PUBLIC_KEY="$RELEASE_DIR/processkit-$VERSION-public.pem"
openssl genpkey -algorithm Ed25519 -out "$PRIVATE_KEY" >/dev/null 2>&1
openssl pkey -in "$PRIVATE_KEY" -pubout -out "$PUBLIC_KEY" >/dev/null 2>&1
KEY_SHA="$(
    openssl pkey -pubin -in "$PUBLIC_KEY" -outform DER |
        sha256sum | awk '{print $1}'
)"

ASSET="processkit-$VERSION-$TARGET"
cp /bin/true "$RELEASE_DIR/$ASSET"
ASSET_SHA="$(sha256sum "$RELEASE_DIR/$ASSET" | awk '{print $1}')"
ASSET_SIZE="$(wc -c <"$RELEASE_DIR/$ASSET" | tr -d '[:space:]')"
printf '%s  %s\n' "$ASSET_SHA" "$ASSET" >"$RELEASE_DIR/$ASSET.sha256"

ENVELOPE="$RELEASE_DIR/processkit-$VERSION.release.json"
jq -n --sort-keys \
    --arg version "$VERSION" \
    --arg key "$KEY_SHA" \
    --arg asset "$ASSET" \
    --arg target "$TARGET" \
    --arg sha "$ASSET_SHA" \
    --argjson size "$ASSET_SIZE" \
    '{
      apiVersion: "processkit.projectious.work/local-release/v1alpha1",
      kind: "LocalRelease",
      release: {name: "processkit", version: $version},
      signing: {algorithm: "Ed25519", keyId: $key},
      installerAssets: [{
        file: $asset,
        sha256: $sha,
        target: $target,
        size: $size
      }]
    }' >"$ENVELOPE"
openssl pkeyutl -sign -rawin \
    -inkey "$PRIVATE_KEY" \
    -in "$ENVELOPE" \
    -out "$RELEASE_DIR/processkit-$VERSION.release.sig"

"$REPO_ROOT/scripts/install-processkit.sh" "$VERSION" \
    --repo "file://$TEST_ROOT/repo" \
    --target "$TARGET" \
    --key-sha256 "$KEY_SHA" \
    --bin-dir "$BIN_DIR"
[[ -x "$BIN_DIR/processkit" ]]

if "$REPO_ROOT/scripts/install-processkit.sh" "$VERSION" \
    --repo "file://$TEST_ROOT/repo" \
    --target "$TARGET" \
    --key-sha256 "$(printf '0%.0s' {1..64})" \
    --bin-dir "$TEST_ROOT/rejected" >/dev/null 2>&1; then
    echo "error: bootstrap accepted an untrusted release key" >&2
    exit 1
fi
[[ ! -e "$TEST_ROOT/rejected/processkit" ]]

echo "bootstrap trust and installation tests passed"
