# processkit documentation site

The user-facing processkit documentation is built with Hugo Extended and
Docsy. The structure and local operating model follow
`projectious-work/kubeclaw`; visual tokens and assets follow
`projectious-work/brand`.

No GitHub Actions workflow or hosted documentation builder is used.

## Local setup

Run the one-time setup from the repository root:

```sh
scripts/setup-docs-local.sh
```

The script installs a checksum-pinned Hugo Extended binary under
`docs-site/.tools/`, checks out the pinned Docsy submodule, and installs
the locked frontend assets.

## Local build and preview

```sh
scripts/check-docs-local.sh
scripts/serve-docs-local.sh
```

The generated site is written to `docs-site/public/`. Once setup is
complete, build and validation do not download dependencies.

## Local publication

```sh
scripts/publish-docs-gh-pages.sh
```

This builds the site locally, creates a temporary `git worktree`, commits
the prebuilt output, and pushes the `gh-pages` branch. GitHub Pages serves
those files; it does not build them.

Set `DOCS_VERSION=v1.0.0-beta.1` to publish beneath a versioned path.

## Structure

```text
docs-site/
├── assets/                 # projectious brand SCSS and processkit mark
├── content/en/             # canonical publishable Markdown
├── layouts/                # Docsy overrides and Markdown render hooks
├── static/                 # favicons and static assets
├── themes/docsy/           # pinned Git submodule
├── hugo.yaml
├── package.json
└── package-lock.json
```
