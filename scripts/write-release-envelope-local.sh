#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 3 ]]; then
    echo "usage: $0 <version> <public-key.pem> <target> [target ...]" >&2
    exit 2
fi

VERSION="$1"
PUBLIC_KEY="$2"
shift 2
TARGETS=("$@")
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ARCHIVE="$REPO_ROOT/dist/processkit-$VERSION.tar.gz"
ENVELOPE="$REPO_ROOT/dist/processkit-$VERSION.release.json"

"$REPO_ROOT/scripts/check-release-version-local.sh" "$VERSION"
[[ -f "$ARCHIVE" ]] || {
    echo "error: release archive missing: $ARCHIVE" >&2
    exit 1
}
[[ -f "$PUBLIC_KEY" ]] || {
    echo "error: public key missing: $PUBLIC_KEY" >&2
    exit 1
}

ASSETS='[]'
declare -A SEEN_TARGETS=()
for target in "${TARGETS[@]}"; do
    [[ "$target" =~ ^[A-Za-z0-9_.-]+$ ]] || {
        echo "error: unsafe Rust target: $target" >&2
        exit 1
    }
    [[ -z "${SEEN_TARGETS[$target]:-}" ]] || {
        echo "error: duplicate Rust target: $target" >&2
        exit 1
    }
    SEEN_TARGETS["$target"]=1
    installer="$REPO_ROOT/dist/processkit-$VERSION-$target"
    [[ -f "$installer" && ! -L "$installer" ]] || {
        echo "error: installer asset missing: $installer" >&2
        exit 1
    }
    installer_sha="$(sha256sum "$installer" | awk '{print $1}')"
    installer_size="$(stat -c %s "$installer")"
    ASSETS="$(
        jq -c \
            --arg file "$(basename "$installer")" \
            --arg sha256 "$installer_sha" \
            --arg target "$target" \
            --argjson size "$installer_size" \
            '. + [{
              file: $file,
              sha256: $sha256,
              target: $target,
              size: $size
            }]' <<<"$ASSETS"
    )"
done

archive_sha="$(sha256sum "$ARCHIVE" | awk '{print $1}')"
archive_size="$(stat -c %s "$ARCHIVE")"
key_id="$(
    openssl pkey -pubin -in "$PUBLIC_KEY" -outform DER |
        sha256sum | awk '{print $1}'
)"
descriptor_sha="$(
    sha256sum "$REPO_ROOT/src/.processkit/installer/release-descriptor.json" |
        awk '{print $1}'
)"
provenance_sha="$(
    sha256sum "$REPO_ROOT/src/PROVENANCE.toml" | awk '{print $1}'
)"

jq -n --sort-keys \
    --arg version "$VERSION" \
    --arg file "$(basename "$ARCHIVE")" \
    --arg sha256 "$archive_sha" \
    --argjson archive_size "$archive_size" \
    --arg archive_root "processkit-$VERSION" \
    --arg descriptor_sha256 "$descriptor_sha" \
    --arg provenance_sha256 "$provenance_sha" \
    --arg key_id "$key_id" \
    --argjson installer_assets "$ASSETS" \
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
      installerAssets: $installer_assets
    }' >"$ENVELOPE"

echo "wrote release envelope with ${#TARGETS[@]} installer asset(s): $ENVELOPE"
