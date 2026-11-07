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
TARGET="$(rustc -vV | awk '/^host:/ {print $2}')"

"$REPO_ROOT/scripts/check-release-version-local.sh" "$VERSION"
"$REPO_ROOT/scripts/test-installer-local.sh"
"$REPO_ROOT/scripts/build-installer-local.sh" "$VERSION" "$TARGET"
"$REPO_ROOT/scripts/build-release-tarball.sh" "$VERSION"

"$REPO_ROOT/scripts/finalize-release-local.sh" \
    "$VERSION" "$PRIVATE_KEY" "$PUBLIC_KEY" "$TARGET"

echo "local release ready in $REPO_ROOT/dist"
