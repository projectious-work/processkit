#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_ROOT="$REPO_ROOT/docs-site"
TOOLS_ROOT="$SITE_ROOT/.tools"
HUGO_VERSION="0.157.0"
HUGO="$TOOLS_ROOT/hugo"
DOCSY_REVISION="01c827ea890e8e498f6046a7666a3031f318cc7f"

case "$(uname -s):$(uname -m)" in
    Linux:x86_64)
        HUGO_PLATFORM="linux-amd64"
        HUGO_SHA256="5b2fdfe4646a48ee98107035024fd6640299bff31c4486c259eeeb9f4c822492"
        ;;
    Linux:aarch64 | Linux:arm64)
        HUGO_PLATFORM="linux-arm64"
        HUGO_SHA256="398efd55428589b928afc65df2410f97efc83608f7a3324d1435196f17adaa0a"
        ;;
    *)
        echo "error: no pinned Hugo binary for $(uname -s)/$(uname -m)" >&2
        echo "Install Hugo Extended $HUGO_VERSION as $HUGO." >&2
        exit 1
        ;;
esac

command -v curl >/dev/null || {
    echo "error: curl is required for one-time local docs setup" >&2
    exit 1
}
command -v npm >/dev/null || {
    echo "error: Node.js and npm are required for Docsy assets" >&2
    exit 1
}

if [[ ! -x "$HUGO" ]] ||
    [[ "$("$HUGO" version 2>/dev/null || true)" != *"v$HUGO_VERSION"* ]]; then
    ARCHIVE="hugo_extended_${HUGO_VERSION}_${HUGO_PLATFORM}.tar.gz"
    URL="https://github.com/gohugoio/hugo/releases/download/v$HUGO_VERSION/$ARCHIVE"
    TEMP_DIR="$(mktemp -d "${TMPDIR:-/tmp}/processkit-hugo.XXXXXX")"
    cleanup() {
        rm -rf "$TEMP_DIR"
    }
    trap cleanup EXIT
    curl --fail --location --output "$TEMP_DIR/$ARCHIVE" "$URL"
    printf '%s  %s\n' "$HUGO_SHA256" "$TEMP_DIR/$ARCHIVE" |
        sha256sum --check --status
    mkdir -p "$TOOLS_ROOT"
    tar -xzf "$TEMP_DIR/$ARCHIVE" -C "$TEMP_DIR" hugo
    mv "$TEMP_DIR/hugo" "$HUGO"
    chmod +x "$HUGO"
fi

git -C "$REPO_ROOT" submodule update --init --recursive \
    docs-site/themes/docsy
git -C "$SITE_ROOT/themes/docsy" checkout --detach "$DOCSY_REVISION"
npm --prefix "$SITE_ROOT" ci

echo "local documentation toolchain is ready"
"$HUGO" version
