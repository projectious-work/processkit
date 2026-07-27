#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_ROOT="$REPO_ROOT/docs-site"

if [[ -d "$REPO_ROOT/.github/workflows" ]] &&
    find "$REPO_ROOT/.github/workflows" -type f -print -quit |
        read -r _; then
    echo "error: documentation must not depend on GitHub workflows" >&2
    exit 1
fi

"$REPO_ROOT/scripts/build-docs-local.sh"
python3 "$REPO_ROOT/scripts/check-docs-links-local.py" \
    "$SITE_ROOT/public"

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
