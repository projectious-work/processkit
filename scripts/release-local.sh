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

"$REPO_ROOT/scripts/test-installer-local.sh"
"$REPO_ROOT/scripts/build-release-tarball.sh" "$VERSION"

ARCHIVE_SHA="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
KEY_ID="$(
    openssl pkey -pubin -in "$PUBLIC_KEY" -outform DER |
        sha256sum | awk '{print $1}'
)"
jq -n --sort-keys \
    --arg version "$VERSION" \
    --arg file "$(basename "$ARCHIVE")" \
    --arg sha256 "$ARCHIVE_SHA" \
    --arg key_id "$KEY_ID" \
    '{
      apiVersion: "processkit.projectious.work/local-release/v1alpha1",
      kind: "LocalRelease",
      release: {name: "processkit", version: $version},
      archive: {file: $file, sha256: $sha256},
      signing: {algorithm: "Ed25519", keyId: $key_id}
    }' >"$ENVELOPE"

"$REPO_ROOT/scripts/sign-release-local.sh" \
    "$ENVELOPE" "$PRIVATE_KEY" "$SIGNATURE"
"$REPO_ROOT/scripts/verify-release-local.sh" \
    "$ENVELOPE" "$SIGNATURE" "$PUBLIC_KEY"

echo "local release ready in $REPO_ROOT/dist"
