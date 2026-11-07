#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
    echo "usage: $0 <release.json> <release.sig> <public-key-or-trust-dir>" >&2
    exit 2
fi

ENVELOPE="$1"
SIGNATURE="$2"
TRUST_INPUT="$3"

for path in "$ENVELOPE" "$SIGNATURE"; do
    [[ -f "$path" ]] || { echo "error: required file missing: $path" >&2; exit 1; }
done
[[ -f "$TRUST_INPUT" || -d "$TRUST_INPUT" ]] || {
    echo "error: trust input missing: $TRUST_INPUT" >&2
    exit 1
}
command -v jq >/dev/null || { echo "error: jq is required" >&2; exit 1; }
command -v openssl >/dev/null || { echo "error: openssl is required" >&2; exit 1; }

KEY_ID="$(jq -er '.signing.keyId' "$ENVELOPE")"
if [[ -d "$TRUST_INPUT" ]]; then
    PUBLIC_KEY="$TRUST_INPUT/$KEY_ID.pub.pem"
    if [[ ! -f "$PUBLIC_KEY" ]]; then
        PUBLIC_KEY=""
        while IFS= read -r candidate; do
            candidate_id="$(
                openssl pkey -pubin -in "$candidate" -outform DER 2>/dev/null |
                    sha256sum | awk '{print $1}'
            )"
            if [[ "$candidate_id" == "$KEY_ID" ]]; then
                PUBLIC_KEY="$candidate"
                break
            fi
        done < <(find "$TRUST_INPUT" -maxdepth 1 -type f -name '*.pub.pem' -print)
    fi
else
    PUBLIC_KEY="$TRUST_INPUT"
fi
[[ -f "$PUBLIC_KEY" ]] || {
    echo "error: signing key is not in the local trust store: $KEY_ID" >&2
    exit 1
}
ACTUAL_KEY_ID="$(
    openssl pkey -pubin -in "$PUBLIC_KEY" -outform DER |
        sha256sum | awk '{print $1}'
)"
[[ "$ACTUAL_KEY_ID" == "$KEY_ID" ]] || {
    echo "error: release key id does not match trusted public key" >&2
    exit 1
}
jq -e '
  .apiVersion == "processkit.projectious.work/local-release/v1alpha1"
  and .kind == "LocalRelease"
  and .release.name == "processkit"
  and (.release.version | type == "string" and length > 0)
  and (.archive.sha256 | test("^[a-f0-9]{64}$"))
  and (.archive.size | type == "number" and . > 0)
  and (.archive.topLevelDirectory | type == "string" and length > 0)
  and (.descriptor.file == ".processkit/installer/release-descriptor.json")
  and (.descriptor.sha256 | test("^[a-f0-9]{64}$"))
  and (.provenance.file == "PROVENANCE.toml")
  and (.provenance.sha256 | test("^[a-f0-9]{64}$"))
  and (.provenance.generatedForTag == .release.version)
  and .signing.algorithm == "Ed25519"
  and (.installerAssets | type == "array" and length > 0)
  and all(.installerAssets[];
    (.file | type == "string" and length > 0)
    and (.sha256 | test("^[a-f0-9]{64}$"))
    and (.target | test("^[A-Za-z0-9_.-]+$"))
    and (.size | type == "number" and . > 0)
  )
  and ([.installerAssets[].file] | unique | length)
      == (.installerAssets | length)
  and ([.installerAssets[].target] | unique | length)
      == (.installerAssets | length)
' "$ENVELOPE" >/dev/null || {
    echo "error: invalid local release envelope" >&2
    exit 1
}

openssl pkeyutl -verify -rawin -pubin \
    -inkey "$PUBLIC_KEY" \
    -in "$ENVELOPE" \
    -sigfile "$SIGNATURE" >/dev/null

ARCHIVE="$(jq -er '.archive.file' "$ENVELOPE")"
EXPECTED="$(jq -er '.archive.sha256' "$ENVELOPE")"
VERSION="$(jq -er '.release.version' "$ENVELOPE")"
[[ "$ARCHIVE" == "processkit-$VERSION.tar.gz" ]] || {
    echo "error: archive filename and release version disagree" >&2
    exit 1
}
[[ "$ARCHIVE" != */* && "$ARCHIVE" != *\\* ]] || {
    echo "error: unsafe archive filename in release envelope" >&2
    exit 1
}
[[ "$(jq -er '.archive.topLevelDirectory' "$ENVELOPE")" == \
    "processkit-$VERSION" ]] || {
    echo "error: archive root and release version disagree" >&2
    exit 1
}
ARCHIVE_PATH="$(dirname "$ENVELOPE")/$ARCHIVE"
[[ "$(stat -c %s "$ARCHIVE_PATH")" == \
    "$(jq -er '.archive.size' "$ENVELOPE")" ]] || {
    echo "error: release archive size mismatch" >&2
    exit 1
}
ACTUAL="$(sha256sum "$ARCHIVE_PATH" | awk '{print $1}')"
[[ "$ACTUAL" == "$EXPECTED" ]] || {
    echo "error: release archive digest mismatch" >&2
    exit 1
}
ARCHIVE_ROOT="$(jq -er '.archive.topLevelDirectory' "$ENVELOPE")"
if tar -tzf "$ARCHIVE_PATH" |
    awk -v root="$ARCHIVE_ROOT/" '
      $0 != substr(root, 1, length(root) - 1) &&
      index($0, root) != 1 { exit 1 }
    ' >/dev/null; then
    :
else
    echo "error: release archive contains an unexpected top-level path" >&2
    exit 1
fi
DESCRIPTOR_FILE="$(jq -er '.descriptor.file' "$ENVELOPE")"
DESCRIPTOR_EXPECTED="$(jq -er '.descriptor.sha256' "$ENVELOPE")"
DESCRIPTOR_ACTUAL="$(
    tar -xOzf "$ARCHIVE_PATH" "$ARCHIVE_ROOT/$DESCRIPTOR_FILE" |
        sha256sum | awk '{print $1}'
)"
[[ "$DESCRIPTOR_ACTUAL" == "$DESCRIPTOR_EXPECTED" ]] || {
    echo "error: bound release descriptor digest mismatch" >&2
    exit 1
}
PROVENANCE_FILE="$(jq -er '.provenance.file' "$ENVELOPE")"
PROVENANCE_EXPECTED="$(jq -er '.provenance.sha256' "$ENVELOPE")"
PROVENANCE_ACTUAL="$(
    tar -xOzf "$ARCHIVE_PATH" "$ARCHIVE_ROOT/$PROVENANCE_FILE" |
        sha256sum | awk '{print $1}'
)"
[[ "$PROVENANCE_ACTUAL" == "$PROVENANCE_EXPECTED" ]] || {
    echo "error: bound release provenance digest mismatch" >&2
    exit 1
}
GENERATED_FOR_TAG="$(jq -er '.provenance.generatedForTag' "$ENVELOPE")"
tar -xOzf "$ARCHIVE_PATH" "$ARCHIVE_ROOT/$PROVENANCE_FILE" |
    grep -Fx "generated_for_tag = \"$GENERATED_FOR_TAG\"" >/dev/null || {
    echo "error: bound release provenance tag mismatch" >&2
    exit 1
}
CHECKSUM="$(dirname "$ENVELOPE")/$ARCHIVE.sha256"
[[ -f "$CHECKSUM" ]] || { echo "error: checksum sidecar missing" >&2; exit 1; }
(
    cd "$(dirname "$ENVELOPE")"
    sha256sum -c "$(basename "$CHECKSUM")" >/dev/null
)

while IFS= read -r asset; do
    INSTALLER="$(jq -er '.file' <<<"$asset")"
    INSTALLER_EXPECTED="$(jq -er '.sha256' <<<"$asset")"
    INSTALLER_TARGET="$(jq -er '.target' <<<"$asset")"
    INSTALLER_SIZE="$(jq -er '.size' <<<"$asset")"
    [[ "$INSTALLER" != */* && "$INSTALLER" != *\\* ]] || {
        echo "error: unsafe installer filename in release envelope" >&2
        exit 1
    }
    [[ "$INSTALLER" == "processkit-$VERSION-$INSTALLER_TARGET" ]] || {
        echo "error: installer filename and release version disagree" >&2
        exit 1
    }
    INSTALLER_PATH="$(dirname "$ENVELOPE")/$INSTALLER"
    [[ -f "$INSTALLER_PATH" ]] || {
        echo "error: installer asset missing: $INSTALLER" >&2
        exit 1
    }
    [[ "$(stat -c %s "$INSTALLER_PATH")" == "$INSTALLER_SIZE" ]] || {
        echo "error: installer asset size mismatch" >&2
        exit 1
    }
    INSTALLER_ACTUAL="$(sha256sum "$INSTALLER_PATH" | awk '{print $1}')"
    [[ "$INSTALLER_ACTUAL" == "$INSTALLER_EXPECTED" ]] || {
        echo "error: installer asset digest mismatch" >&2
        exit 1
    }
done < <(jq -c '.installerAssets[]' "$ENVELOPE")

echo "verified local release: $VERSION"
