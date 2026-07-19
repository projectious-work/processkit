#!/usr/bin/env bash
# Build the documentation locally and publish the generated static site.

set -euo pipefail

VERSION="${1:-$(git describe --tags --exact-match 2>/dev/null || git rev-parse --short HEAD)}"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DOCS_DIR="$REPO_ROOT/docs-site"
BUILD_DIR="$DOCS_DIR/build"
REMOTE="${PROCESSKIT_DOCS_REMOTE:-origin}"
BRANCH="${PROCESSKIT_DOCS_BRANCH:-gh-pages}"
PUBLISH_DIR="$(mktemp -d)"

cleanup() {
    git -C "$REPO_ROOT" worktree remove --force "$PUBLISH_DIR" >/dev/null 2>&1 || true
}
trap cleanup EXIT

if [[ ! -f "$DOCS_DIR/package.json" ]]; then
    echo "error: docs-site/package.json not found" >&2
    exit 1
fi

if ! git -C "$REPO_ROOT" diff --quiet || \
   ! git -C "$REPO_ROOT" diff --cached --quiet; then
    echo "error: commit or stash changes before publishing docs" >&2
    exit 1
fi

if [[ ! -d "$DOCS_DIR/node_modules" ]]; then
    npm --prefix "$DOCS_DIR" ci
fi

npm --prefix "$DOCS_DIR" run build

if [[ ! -f "$BUILD_DIR/index.html" ]]; then
    echo "error: docs build did not produce build/index.html" >&2
    exit 1
fi

if git -C "$REPO_ROOT" show-ref --verify --quiet "refs/heads/$BRANCH"; then
    git -C "$REPO_ROOT" worktree add "$PUBLISH_DIR" "$BRANCH"
elif git -C "$REPO_ROOT" ls-remote --exit-code --heads \
     "$REMOTE" "$BRANCH" >/dev/null 2>&1; then
    git -C "$REPO_ROOT" fetch "$REMOTE" "$BRANCH"
    git -C "$REPO_ROOT" worktree add -b "$BRANCH" "$PUBLISH_DIR" \
        "$REMOTE/$BRANCH"
else
    git -C "$REPO_ROOT" worktree add --detach "$PUBLISH_DIR" HEAD
    git -C "$PUBLISH_DIR" switch --orphan "$BRANCH"
fi

git -C "$PUBLISH_DIR" rm -r --ignore-unmatch . >/dev/null
cp -a "$BUILD_DIR/." "$PUBLISH_DIR/"
touch "$PUBLISH_DIR/.nojekyll"
git -C "$PUBLISH_DIR" add -A

if git -C "$PUBLISH_DIR" diff --cached --quiet; then
    echo "documentation is already current" >&2
    exit 0
fi

git -C "$PUBLISH_DIR" commit -m "docs: publish $VERSION documentation"
git -C "$PUBLISH_DIR" push "$REMOTE" "$BRANCH:$BRANCH"

echo "published docs to https://projectious-work.github.io/processkit/" >&2
