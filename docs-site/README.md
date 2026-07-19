# processkit docs-site

The user-facing documentation for processkit, built with
[Docusaurus 3](https://docusaurus.io/).

## Local development

```bash
cd docs-site
npm install           # first time only
npm run start         # localhost:3000
```

## Build

```bash
npm run build         # outputs to build/
npm run serve         # serve the built site locally
```

## Publish Locally

The documentation is published to
[GitHub Pages](https://projectious-work.github.io/processkit/) from a local
build. The repository does not use GitHub Actions.

```bash
scripts/publish-docs-gh-pages.sh
```

## Structure

```
docs-site/
├── docs/                    ← Markdown content
│   ├── intro.md
│   ├── getting-started/
│   ├── primitives/
│   ├── skills/
│   │   └── catalog/         ← per-category skill listings
│   ├── packages/
│   ├── processes/
│   ├── mcp-servers/
│   └── reference/
├── src/
│   └── css/custom.css
├── static/
├── docusaurus.config.js
├── sidebars.js
└── package.json
```

## Content conventions

- **Overview pages** introduce a section and link to the authoritative
  source files in the repo (`src/context/schemas/`,
  `src/context/skills/FORMAT.md`, etc.). This keeps the docs in sync
  with the source and avoids duplication.
- **Catalog pages** under `skills/catalog/` describe the skills in each
  category and should describe processkit as a standalone project first.
- **Reference pages** are deep technical documentation — apiVersion policy,
  ID formats, migration guide.
