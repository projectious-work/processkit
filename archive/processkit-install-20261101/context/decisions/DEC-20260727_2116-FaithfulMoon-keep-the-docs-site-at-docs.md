---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260727_2116-FaithfulMoon-keep-the-docs-site-at-docs
  created: '2026-07-27T21:16:41+00:00'
spec:
  title: Keep the docs site at docs-site/content/en rather than the repository root
  state: accepted
  decision: 'Supersedes the layout clause of DEC-20260727_0617-NeatJay. The Hugo +
    Docsy site stays where v1.x-dev already put it — `docs-site/` with `contentDir:
    content/en` — instead of moving to the repository root. Both release lines carry
    the identical structure: the same pinned Docsy submodule at `docs-site/themes/docsy`,
    the same `render-link.html` markup hook resolving plain relative links, and the
    same local toolchain (`scripts/{setup,build,serve,check}-docs-local.sh`, `check-docs-links-local.py`,
    `publish-docs-gh-pages.sh`). Everything else in DEC-20260727_0617-NeatJay stands:
    v0.x at the gh-pages root, v1.x under /v1.x/, the version menu across both lines,
    the brand SCSS port, and the new processkit mark.'
  context: 'DEC-20260727_0617-NeatJay was recorded and implemented against a snapshot
    of v1.x-dev taken before nine commits landed on origin, among them a Hugo + Docsy
    migration of the same documentation (#123 through #132). The remote work chose
    `docs-site/` with an i18n-ready `content/en/` contentDir, added an installer documentation
    set, an alpha3 closure plan, a claude-code MCP page, a link checker, and a publish
    script. Pushing the repository-root layout would have deleted all of it. The owner
    reviewed the delta and chose to port the outstanding pieces onto the remote''s
    structure rather than replace it.'
  rationale: The remote layout is ahead on content and tooling, and it is what other
    in-flight branches and pull requests are written against; discarding it would
    invalidate work that had already been reviewed and merged. The `content/en/` contentDir
    also leaves room for translations that a root `content/` would have to be restructured
    to support later. The pieces the remote lacked — a product mark distinct from
    the projectious organisation mark, a fingerprinted multi-format favicon set, the
    full brand token port rather than a 130-line sketch, and two-line versioning —
    are additive and port cleanly onto it. Notably the remote's build script hardcoded
    a root `--baseURL`, which would have published the preview line over the released
    line regardless of what hugo.yaml said; that had to be fixed for the two-line
    split to work at all.
  alternatives:
  - option: Keep the repository-root layout and import the remote's new pages
    why_not: Rewrites work that just landed through reviewed pull requests and leaves
      those branches' authors with a structure that no longer exists.
  - option: Run both layouts side by side during a transition
    why_not: Two Hugo configurations publishing to one Pages site invites exactly
      the root-overwrite failure this decision exists to prevent.
  consequences: Documentation content lives at `docs-site/content/en/docs/`. Internal
    links stay plain and relative, resolved by the render-link hook, rather than using
    relref shortcodes — link breakage is caught by `check-docs-links-local.py` at
    validation time instead of failing the build. The repository-root scaffolding
    built earlier in the session is preserved on the branches `wip/hugo-root-layout`
    and `wip/v0x-hugo-root-layout` and can be deleted once the reconciled site is
    published. `build-docs-local.sh` no longer passes a hardcoded `--baseURL`; `serve-docs-local.sh`
    and `check-docs-local.sh` derive the base path from `hugo.yaml`, so each branch
    previews and validates at the path it actually publishes to.
  related_workitems:
  - BACK-20260727_0618-HelpfulBird-hugo-docsy-docs-migration
  decided_at: '2026-07-27T21:16:41+00:00'
---
