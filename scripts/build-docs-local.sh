#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_ROOT="$REPO_ROOT/docs-site"
HUGO="$SITE_ROOT/.tools/hugo"
DOCS_BASE_URL="${DOCS_BASE_URL:-https://projectious-work.github.io/processkit/}"
BUILD_DIR="${DOCS_BUILD_DIR:-$SITE_ROOT/public}"

[[ -x "$HUGO" ]] || {
    echo "error: local Hugo is not installed" >&2
    echo "Run scripts/setup-docs-local.sh once." >&2
    exit 1
}
[[ -f "$SITE_ROOT/themes/docsy/theme.toml" ]] || {
    echo "error: pinned Docsy submodule is not initialized" >&2
    echo "Run scripts/setup-docs-local.sh once." >&2
    exit 1
}
[[ -d "$SITE_ROOT/node_modules" ]] || {
    echo "error: pinned Docsy assets are not installed" >&2
    echo "Run scripts/setup-docs-local.sh once." >&2
    exit 1
}

"$HUGO" --source "$SITE_ROOT" \
    --gc \
    --minify \
    --cleanDestinationDir \
    --destination "$BUILD_DIR" \
    --baseURL "$DOCS_BASE_URL" \
    "$@"

: >"$BUILD_DIR/.nojekyll"
echo "documentation built locally in $BUILD_DIR"
