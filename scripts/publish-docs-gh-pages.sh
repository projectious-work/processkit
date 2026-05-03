#!/usr/bin/env bash
# publish-docs-gh-pages.sh - build and publish the Docusaurus docs site.
#
# This is intentionally local release machinery, not a GitHub Actions
# workflow. It builds docs-site/ and pushes the generated static site to
# the gh-pages branch.
#
# Usage:
#   scripts/publish-docs-gh-pages.sh
#   scripts/publish-docs-gh-pages.sh v0.25.1

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

if ! git -C "$REPO_ROOT" diff --quiet; then
    echo "error: working tree has unstaged changes; commit or stash before publishing docs" >&2
    exit 1
fi

if ! git -C "$REPO_ROOT" diff --cached --quiet; then
    echo "error: index has staged changes; commit or unstage before publishing docs" >&2
    exit 1
fi

if [[ ! -d "$DOCS_DIR/node_modules" ]]; then
    echo "installing docs dependencies with npm ci" >&2
    npm --prefix "$DOCS_DIR" ci
fi

echo "building Docusaurus docs site" >&2
npm --prefix "$DOCS_DIR" run build

if [[ ! -f "$BUILD_DIR/index.html" ]]; then
    echo "error: docs build did not produce build/index.html" >&2
    exit 1
fi

if git -C "$REPO_ROOT" ls-remote --exit-code --heads "$REMOTE" "$BRANCH" >/dev/null 2>&1; then
    echo "checking out $REMOTE/$BRANCH into temporary worktree" >&2
    git -C "$REPO_ROOT" fetch "$REMOTE" "$BRANCH"
    git -C "$REPO_ROOT" worktree add "$PUBLISH_DIR" "refs/remotes/$REMOTE/$BRANCH"
    git -C "$PUBLISH_DIR" switch -C "$BRANCH"
else
    echo "creating new orphan $BRANCH worktree" >&2
    git -C "$REPO_ROOT" worktree add --detach "$PUBLISH_DIR" HEAD
    git -C "$PUBLISH_DIR" switch --orphan "$BRANCH"
fi

git -C "$PUBLISH_DIR" rm -r --ignore-unmatch . >/dev/null
(cd "$BUILD_DIR" && tar -cf - .) | (cd "$PUBLISH_DIR" && tar -xf -)
touch "$PUBLISH_DIR/.nojekyll"

git -C "$PUBLISH_DIR" add -A

if git -C "$PUBLISH_DIR" diff --cached --quiet; then
    echo "docs site already up to date on $BRANCH" >&2
    exit 0
fi

git -C "$PUBLISH_DIR" commit -m "docs: publish $VERSION documentation"
git -C "$PUBLISH_DIR" push "$REMOTE" "$BRANCH:$BRANCH"

echo "published docs to https://projectious-work.github.io/processkit/" >&2
