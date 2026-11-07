#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 4 ]]; then
    echo "usage: $0 <version> <private-key.pem> <public-key.pem> <target> [target ...]" >&2
    exit 2
fi

VERSION="$1"
PRIVATE_KEY="$2"
PUBLIC_KEY="$3"
shift 3
TARGETS=("$@")
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ENVELOPE="$REPO_ROOT/dist/processkit-$VERSION.release.json"
SIGNATURE="$REPO_ROOT/dist/processkit-$VERSION.release.sig"

"$REPO_ROOT/scripts/write-release-envelope-local.sh" \
    "$VERSION" "$PUBLIC_KEY" "${TARGETS[@]}"
"$REPO_ROOT/scripts/sign-release-local.sh" \
    "$ENVELOPE" "$PRIVATE_KEY" "$SIGNATURE"
"$REPO_ROOT/scripts/verify-release-local.sh" \
    "$ENVELOPE" "$SIGNATURE" "$PUBLIC_KEY"

echo "finalized signed release matrix with ${#TARGETS[@]} target(s)"
