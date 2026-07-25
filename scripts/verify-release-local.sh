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
  and .signing.algorithm == "Ed25519"
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
ACTUAL="$(sha256sum "$(dirname "$ENVELOPE")/$ARCHIVE" | awk '{print $1}')"
[[ "$ACTUAL" == "$EXPECTED" ]] || {
    echo "error: release archive digest mismatch" >&2
    exit 1
}
CHECKSUM="$(dirname "$ENVELOPE")/$ARCHIVE.sha256"
[[ -f "$CHECKSUM" ]] || { echo "error: checksum sidecar missing" >&2; exit 1; }
(
    cd "$(dirname "$ENVELOPE")"
    sha256sum -c "$(basename "$CHECKSUM")" >/dev/null
)
echo "verified local release: $VERSION"
