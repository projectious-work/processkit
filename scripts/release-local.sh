#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
    echo "usage: $0 <version> <private-key.pem> <public-key.pem>" >&2
    exit 2
fi

VERSION="$1"
PRIVATE_KEY="$2"
PUBLIC_KEY="$3"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ARCHIVE="$REPO_ROOT/dist/processkit-$VERSION.tar.gz"
ENVELOPE="$REPO_ROOT/dist/processkit-$VERSION.release.json"
SIGNATURE="$REPO_ROOT/dist/processkit-$VERSION.release.sig"
TARGET="$(rustc -vV | awk '/^host:/ {print $2}')"
INSTALLER="$REPO_ROOT/dist/processkit-$VERSION-$TARGET"

"$REPO_ROOT/scripts/check-release-version-local.sh" "$VERSION"
"$REPO_ROOT/scripts/test-installer-local.sh"
"$REPO_ROOT/scripts/build-installer-local.sh" "$VERSION" "$TARGET"
"$REPO_ROOT/scripts/build-release-tarball.sh" "$VERSION"

ARCHIVE_SHA="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
ARCHIVE_SIZE="$(stat -c %s "$ARCHIVE")"
KEY_ID="$(
    openssl pkey -pubin -in "$PUBLIC_KEY" -outform DER |
        sha256sum | awk '{print $1}'
)"
INSTALLER_SHA="$(sha256sum "$INSTALLER" | awk '{print $1}')"
INSTALLER_SIZE="$(stat -c %s "$INSTALLER")"
DESCRIPTOR_SHA="$(
    sha256sum "$REPO_ROOT/src/.processkit/installer/release-descriptor.json" |
        awk '{print $1}'
)"
PROVENANCE_SHA="$(
    sha256sum "$REPO_ROOT/src/PROVENANCE.toml" | awk '{print $1}'
)"
jq -n --sort-keys \
    --arg version "$VERSION" \
    --arg file "$(basename "$ARCHIVE")" \
    --arg sha256 "$ARCHIVE_SHA" \
    --argjson archive_size "$ARCHIVE_SIZE" \
    --arg archive_root "processkit-$VERSION" \
    --arg descriptor_sha256 "$DESCRIPTOR_SHA" \
    --arg provenance_sha256 "$PROVENANCE_SHA" \
    --arg key_id "$KEY_ID" \
    --arg installer_file "$(basename "$INSTALLER")" \
    --arg installer_sha256 "$INSTALLER_SHA" \
    --argjson installer_size "$INSTALLER_SIZE" \
    --arg target "$TARGET" \
    '{
      apiVersion: "processkit.projectious.work/local-release/v1alpha1",
      kind: "LocalRelease",
      release: {name: "processkit", version: $version},
      archive: {
        file: $file,
        sha256: $sha256,
        size: $archive_size,
        topLevelDirectory: $archive_root
      },
      descriptor: {
        file: ".processkit/installer/release-descriptor.json",
        sha256: $descriptor_sha256
      },
      provenance: {
        file: "PROVENANCE.toml",
        sha256: $provenance_sha256,
        generatedForTag: $version
      },
      signing: {algorithm: "Ed25519", keyId: $key_id},
      installerAssets: [{
        file: $installer_file,
        sha256: $installer_sha256,
        target: $target,
        size: $installer_size
      }]
    }' >"$ENVELOPE"

"$REPO_ROOT/scripts/sign-release-local.sh" \
    "$ENVELOPE" "$PRIVATE_KEY" "$SIGNATURE"
"$REPO_ROOT/scripts/verify-release-local.sh" \
    "$ENVELOPE" "$SIGNATURE" "$PUBLIC_KEY"

echo "local release ready in $REPO_ROOT/dist"
