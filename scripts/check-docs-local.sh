#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_ROOT="$REPO_ROOT/docs-site"

"$REPO_ROOT/scripts/build-docs-local.sh"

# The base path differs per release line (root on v0.x-dev, /v1.x/ on
# v1.x-dev), so derive it from the site's own baseURL rather than assuming.
BASE_PATH="$(sed -n 's|^baseURL:[[:space:]]*"https\?://[^/]*\(/.*\)"[[:space:]]*$|\1|p' \
    "$SITE_ROOT/hugo.yaml" | head -n 1)"
BASE_PATH="${BASE_PATH:-/}"

python3 "$REPO_ROOT/scripts/check-docs-links-local.py" \
    --base-path "$BASE_PATH" \
    "$SITE_ROOT/public"
python3 "$REPO_ROOT/scripts/check-docs-contrast.py" "$SITE_ROOT/public"

if [[ -f "$SITE_ROOT/docusaurus.config.js" ||
    -f "$SITE_ROOT/sidebars.js" ]]; then
    echo "error: obsolete Docusaurus runtime files remain" >&2
    exit 1
fi
if find "$SITE_ROOT/content" -type d -name private -print -quit |
    read -r _; then
    echo "error: private content directory would enter the Hugo site" >&2
    exit 1
fi

echo "local Hugo documentation validation passed"
