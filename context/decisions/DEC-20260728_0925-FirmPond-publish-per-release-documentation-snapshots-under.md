---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260728_0925-FirmPond-publish-per-release-documentation-snapshots-under
  created: '2026-07-28T09:25:20+00:00'
spec:
  title: Publish per-release documentation snapshots under their tag, with no back-fill
  state: accepted
  decision: |
    The documentation version menu carries two levels: the release line (v0.x, v1.x) and, under each, the individual releases published from it. A release snapshot is deployed with `DOCS_VERSION=<tag> scripts/publish-docs-gh-pages.sh`, which publishes it to `/<tag>/` on gh-pages — a path the root publish already preserves via its `v[0-9]*` exclusion. The line URL itself (`/` for v0.x, `/v1.x/` for v1.x) always serves the newest release on that line, and the menu entry for that release is marked `kind: current`.

    Only releases published from 2026-07-28 onwards are listed. Historic tags are not back-filled: no snapshot is built for v0.28.3 and earlier, or for v1.0.0-alpha.1 and alpha.2.

    Adding a release to the menu is a step in the release procedure: deploy the snapshot, then in `docs-site/hugo.yaml` move `kind: current` to the new entry and add the previous release below it. Both branches carry the same `versions` block so either line's menu can reach the other line's releases.
  context: 'The version menu shipped with the Hugo migration was flat: two entries,
    one per release line, with no way to reach the documentation for a specific release.
    Readers pinning an exact version — which SECURITY.md and the README both tell
    them to do — had no way to read the documentation that matched it. Docsy''s stock
    navbar-version-selector renders one flat list, so a two-level menu required a
    project override. Requested by the owner during review on 2026-07-28.'
  rationale: |
    Publishing snapshots under the bare tag (`/v0.28.4/`) rather than nesting them under the line (`/v0.x/v0.28.4/`) reuses the sibling-preservation rule the root publish already implements, so no deploy logic changes and no future line needs special handling. Marking the newest release `current` and pointing it at the line URL avoids publishing the same build twice.

    Declining to back-fill is deliberate: reconstructing documentation for already-shipped tags means checking out each tag, building it against a Hugo configuration and theme pin that did not exist then, and publishing a result no one has reviewed. The value is low — those releases are documented by their changelog entries and release notes — and the risk of publishing a subtly wrong snapshot under an authoritative-looking URL is real.
  alternatives:
  - option: Keep the flat menu, one entry per line
    why_not: Leaves a reader pinned to an exact version with no matching documentation,
      which contradicts the pinning advice the project gives them.
  - option: Nest snapshots under the line (/v0.x/v0.28.4/)
    why_not: Requires the root publish to preserve a deeper path than its current
      v[0-9]* rule covers, and gives the released line a directory it does not otherwise
      need.
  - option: Back-fill snapshots for all historic tags
    why_not: Builds old content against a toolchain it never saw, and publishes unreviewed
      output at URLs that look authoritative.
  consequences: 'The release procedure gains two steps: deploy a documentation snapshot
    for the tag, and update the `versions` block on both branches. Missing them leaves
    the menu claiming an older release is current. `docs-site/layouts/_partials/navbar-version-selector.html`
    is a project override of a Docsy partial and will need review when the theme pin
    moves. The submenu opens on hover, keyboard focus, and click, so it has three
    interaction paths to keep working. Snapshot directories accumulate on gh-pages,
    one per release, and nothing prunes them.'
  related_workitems:
  - BACK-20260727_0618-HelpfulBird-hugo-docsy-docs-migration
  decided_at: '2026-07-28T09:25:20+00:00'
---
