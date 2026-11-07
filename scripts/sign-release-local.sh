#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 3 ]]; then
    echo "usage: $0 <release.json> <private-key.pem> <release.sig>" >&2
    exit 2
fi

ENVELOPE="$1"
PRIVATE_KEY="$2"
SIGNATURE="$3"

[[ -f "$ENVELOPE" ]] || { echo "error: release envelope missing" >&2; exit 1; }
[[ -f "$PRIVATE_KEY" ]] || { echo "error: private key missing" >&2; exit 1; }
command -v openssl >/dev/null || { echo "error: openssl is required" >&2; exit 1; }

umask 077
openssl pkeyutl -sign -rawin \
    -inkey "$PRIVATE_KEY" \
    -in "$ENVELOPE" \
    -out "$SIGNATURE"
echo "signed: $SIGNATURE"
