#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_ROOT="$REPO_ROOT/docs-site"
HUGO="$SITE_ROOT/.tools/hugo"
# Mirrors the published path for this release line so relative links
# resolve the same way locally as they do on GitHub Pages.
DOCS_BASE_PATH="$(sed -n 's|^baseURL:[[:space:]]*"https\?://[^/]*\(/.*\)"[[:space:]]*$|\1|p' \
    "$SITE_ROOT/hugo.yaml" | head -n 1)"
DOCS_BASE_URL="${DOCS_BASE_URL:-http://localhost:1313${DOCS_BASE_PATH:-/}}"

[[ -x "$HUGO" && -f "$SITE_ROOT/themes/docsy/theme.toml" &&
    -d "$SITE_ROOT/node_modules" ]] || {
    echo "error: local docs toolchain is incomplete" >&2
    echo "Run scripts/setup-docs-local.sh once." >&2
    exit 1
}

"$HUGO" server \
    --source "$SITE_ROOT" \
    --buildDrafts \
    --disableFastRender \
    --baseURL "$DOCS_BASE_URL" \
    "$@"
