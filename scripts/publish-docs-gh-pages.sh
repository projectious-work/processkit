#!/usr/bin/env bash
set -euo pipefail

# Build locally and push the generated site to the gh-pages branch.
# GitHub Actions and workflow files are intentionally not used.

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SITE_ROOT="$REPO_ROOT/docs-site"
PAGES_BRANCH="${PAGES_BRANCH:-gh-pages}"
DOCS_VERSION="${DOCS_VERSION:-main}"
DOCS_BASE_URL="${DOCS_BASE_URL:-https://projectious-work.github.io/processkit/}"
BUILD_DIR="$SITE_ROOT/public"

[[ "$DOCS_VERSION" =~ ^[A-Za-z0-9._-]+$ ]] || {
    echo "error: DOCS_VERSION contains unsafe characters" >&2
    exit 1
}
if [[ "$DOCS_VERSION" != "main" ]]; then
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

if [[ "$DOCS_VERSION" == "main" ]]; then
    # Preserve already-published version directories when refreshing main.
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
    -m "docs: publish Hugo site $DOCS_VERSION"
git -C "$WORKTREE_DIR" push origin "$PAGES_BRANCH"
echo "documentation published locally to $PAGES_BRANCH"
