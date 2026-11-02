---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260727_0618-HelpfulBird-hugo-docsy-docs-migration
  created: '2026-07-27T06:18:13+00:00'
  updated: '2026-07-28T05:56:05+00:00'
spec:
  title: Migrate documentation to Hugo + Docsy, brand the site, and introduce the
    processkit logo
  state: done
  type: task
  priority: high
  description: |
    Per DEC-20260727_0617-NeatJay: replace the Docusaurus `docs-site/` with a Hugo + Docsy site at the repository root, styled from the projectious-work/brand design system and matching the projectious-work/kubeclaw reference implementation.

    Scope on this branch (v1.x-dev):
    - Hugo scaffolding: hugo.yaml, themes/docsy submodule, package.json (Bootstrap + Font Awesome), scripts/{build,serve,deploy}-docs.sh with DOCS_VERSION support.
    - Brand layer: assets/scss/_variables_project.scss and _styles_project.scss, layouts/_partials/{favicons,hooks/head-end,version-banner}.html.
    - New processkit logo (midnight process ring, white arrowhead, orange checkpoint dot) as SVG variants plus PNG raster set and favicons; wired into navbar, favicons, and README.
    - Content migration: docs-site/docs/**.md converted to content/docs/** with Hugo front matter, _index.md section pages, and relref-based internal links; landing page content/_index.md.
    - README.md rewritten in the kubeclaw style (centred logo, badges, what-this-is / what-this-is-not, docs table).
    - Remove docs-site/.

    Follow-up on v0.x-dev: the same site, publishing to the gh-pages root (DOCS_VERSION=main), carrying the v0.x content set; v1.x-dev publishes under /v1.x/.

    Publishing stays manual — the repository uses no GitHub Actions.
  started_at: '2026-07-27T06:18:16+00:00'
  completed_at: '2026-07-28T05:56:04+00:00'
---

## Transition note (2026-07-27T06:18:16+00:00)

Starting on v1.x-dev: Hugo scaffolding, brand layer, logo, content migration, README.


## Transition note (2026-07-27T20:10:37+00:00)

Both branches committed locally and unpushed. v1.x-dev b2aa8b2 (78 pages, publishes to /v1.x/); v0.x-dev 8a0a817 (72 pages, publishes to the gh-pages root). Hugo builds clean on both (211 / 195 pages) and check-src-context-drift.sh --release-deliverable passes on both. Awaiting owner review before pushing and before the first deploy-docs.sh run. pk-doctor could not be run to completion — the MCP call exceeded the 1804s idle timeout, a pre-existing tooling issue unrelated to this change.


## Transition note (2026-07-28T05:56:04+00:00)

Shipped. Branch protection required pull requests (0 approvals), so the work landed via PR #137 into v0.x-dev (7068717) and PR #136 into v1.x-dev (6be38fc), both merged. Deployed to gh-pages ef556c2: v0.x at the site root, v1.x under /v1.x/. Verified live — root and /v1.x/ both return 200, each serving its own release-line banner, the new mark inlined in the navbar, the fingerprinted favicon set, and a Release line menu listing both lines. The root publish preserved the /v1.x/ subtree as designed. Superseded on layout by DEC-20260727_2116-FaithfulMoon: the site stayed at docs-site/content/en/ rather than moving to the repository root, because a Hugo migration had already landed on origin/v1.x-dev mid-session. Discarded repo-root scaffolding remains recoverable on wip/hugo-root-layout and wip/v0x-hugo-root-layout.
