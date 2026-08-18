#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_ROOT="$REPO_ROOT/docs-site"
HUGO="$SITE_ROOT/.tools/hugo"
# Unset by default: hugo.yaml's own baseURL is the source of truth, and it
# differs per release line (root on v0.x-dev, /v1.x/ on v1.x-dev). Passing a
# hardcoded --baseURL here would silently publish the preview line at the
# root. publish-docs-gh-pages.sh sets this explicitly when it needs to.
DOCS_BASE_URL="${DOCS_BASE_URL:-}"
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

BASE_URL_ARGS=()
if [[ -n "$DOCS_BASE_URL" ]]; then
    BASE_URL_ARGS=(--baseURL "$DOCS_BASE_URL")
fi

"$HUGO" --source "$SITE_ROOT" \
    --gc \
    --minify \
    --cleanDestinationDir \
    --destination "$BUILD_DIR" \
    "${BASE_URL_ARGS[@]}" \
    "$@"

: >"$BUILD_DIR/.nojekyll"
echo "documentation built locally in $BUILD_DIR"
