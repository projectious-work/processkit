#!/usr/bin/env bash
set -euo pipefail

# Build locally and push the generated site to the gh-pages branch.
# GitHub Actions and workflow files are intentionally not used.

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_ROOT="$REPO_ROOT/docs-site"
PAGES_BRANCH="${PAGES_BRANCH:-gh-pages}"
BUILD_DIR="$SITE_ROOT/public"

read_param() {
    # Reads a single quoted scalar from hugo.yaml's params block.
    sed -n "s/^[[:space:]]*$1:[[:space:]]*\"\(.*\)\"[[:space:]]*$/\1/p" \
        "$SITE_ROOT/hugo.yaml" | head -n 1
}

# Which subtree of gh-pages this branch owns. processkit publishes two
# release lines to one Pages site: v0.x-dev owns the root and v1.x-dev owns
# /v1.x/. The value comes from hugo.yaml so this script is identical on both
# branches; "main" and the empty string both mean the root.
DOCS_VERSION="${DOCS_VERSION-$(read_param docs_deploy_path)}"
PRODUCTION_URL="${PRODUCTION_URL:-$(read_param productionURL)}"
DOCS_BASE_URL="${DOCS_BASE_URL:-$PRODUCTION_URL}"

if [[ "$DOCS_VERSION" == "main" ]]; then
    DOCS_VERSION=""
fi

if [[ -n "$DOCS_VERSION" ]]; then
    [[ "$DOCS_VERSION" =~ ^[A-Za-z0-9._-]+$ ]] || {
        echo "error: DOCS_VERSION contains unsafe characters" >&2
        exit 1
    }
    DOCS_BASE_URL="${DOCS_BASE_URL%/}/$DOCS_VERSION/"
fi

DOCS_BASE_URL="$DOCS_BASE_URL" \
    "$REPO_ROOT/scripts/build-docs-local.sh"

WORKTREE_DIR="$(mktemp -d "${TMPDIR:-/tmp}/processkit-pages.XXXXXX")"
cleanup() {
    git -C "$REPO_ROOT" worktree remove --force "$WORKTREE_DIR" \
        >/dev/null 2>&1 || true
    rmdir "$WORKTREE_DIR" >/dev/null 2>&1 || true
}
trap cleanup EXIT

if git -C "$REPO_ROOT" show-ref --verify --quiet \
    "refs/heads/$PAGES_BRANCH"; then
    git -C "$REPO_ROOT" worktree add "$WORKTREE_DIR" "$PAGES_BRANCH"
elif git -C "$REPO_ROOT" ls-remote --exit-code origin \
    "refs/heads/$PAGES_BRANCH" >/dev/null 2>&1; then
    git -C "$REPO_ROOT" fetch origin \
        "$PAGES_BRANCH:$PAGES_BRANCH"
    git -C "$REPO_ROOT" worktree add "$WORKTREE_DIR" "$PAGES_BRANCH"
else
    git -C "$REPO_ROOT" worktree add --detach "$WORKTREE_DIR"
    git -C "$WORKTREE_DIR" checkout --orphan "$PAGES_BRANCH"
fi

if [[ -z "$DOCS_VERSION" ]]; then
    # Preserve already-published version directories when refreshing the root.
    find "$WORKTREE_DIR" -mindepth 1 -maxdepth 1 \
        ! -name .git ! -name 'v[0-9]*' \
        -exec rm -rf {} +
    cp -R "$BUILD_DIR/." "$WORKTREE_DIR/"
else
    VERSION_DIR="$WORKTREE_DIR/$DOCS_VERSION"
    mkdir -p "$VERSION_DIR"
    find "$VERSION_DIR" -mindepth 1 -maxdepth 1 -exec rm -rf {} +
    cp -R "$BUILD_DIR/." "$VERSION_DIR/"
fi

: >"$WORKTREE_DIR/.nojekyll"
git -C "$WORKTREE_DIR" add -A
if git -C "$WORKTREE_DIR" diff --cached --quiet; then
    echo "no documentation changes to publish"
    exit 0
fi

git -C "$WORKTREE_DIR" commit \
    -m "docs: publish Hugo site ${DOCS_VERSION:-root}"
git -C "$WORKTREE_DIR" push origin "$PAGES_BRANCH"
echo "documentation published locally to $PAGES_BRANCH (${DOCS_VERSION:-root})"
