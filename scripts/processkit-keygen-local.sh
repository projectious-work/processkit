#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
    echo "usage: $0 <private-key.pem> <public-key.pem>" >&2
    exit 2
fi

PRIVATE_KEY="$1"
PUBLIC_KEY="$2"

if [[ -e "$PRIVATE_KEY" || -e "$PUBLIC_KEY" ]]; then
    echo "error: refusing to overwrite an existing key" >&2
    exit 1
fi
command -v openssl >/dev/null || {
    echo "error: openssl is required" >&2
    exit 1
}

mkdir -p "$(dirname "$PRIVATE_KEY")" "$(dirname "$PUBLIC_KEY")"
umask 077
openssl genpkey -algorithm ED25519 -out "$PRIVATE_KEY"
openssl pkey -in "$PRIVATE_KEY" -pubout -out "$PUBLIC_KEY"
chmod 600 "$PRIVATE_KEY"
chmod 644 "$PUBLIC_KEY"

KEY_ID="$(
    openssl pkey -pubin -in "$PUBLIC_KEY" -outform DER |
        sha256sum | awk '{print $1}'
)"
echo "created local Ed25519 release key"
echo "public key id: $KEY_ID"
