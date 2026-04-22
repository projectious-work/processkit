---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260422_0925-MightyOtter-v0-19-1-release
  created: '2026-04-22T09:25:57+00:00'
  updated: '2026-04-22T15:44:51+00:00'
spec:
  title: v0.19.1 — release automation workflow + release-semver SKILL.md tightening
  state: done
  type: task
  priority: high
  description: 'Patch release addressing the v0.19.0 post-mortem finding: `git push
    --tags` does not create a GitHub Release. Tag v0.19.0 was pushed but no Release
    entry was created; `gh release create` had to be run manually.


    **Root cause**: the release-semver skill correctly splits prepare (bump + tag)
    from publish (distribution channel), but nothing prevents or detects stopping
    after prepare. Invoking `/pk-release` alone is the easy miss.


    **Fix (both trees)**

    1. `.github/workflows/release.yml` in the processkit repo root — on push of tag
    matching `v*`, extracts the matching CHANGELOG section and creates a GitHub Release
    via `softprops/action-gh-release@v2`. Permissions: `contents: write`. Title =
    tag name; body = CHANGELOG v<version> section.

    2. `src/.github/workflows/release.yml` — identical template shipped downstream
    so aibox-installed processkit projects get the same automation without hand-wiring.

    3. `context/skills/devops/release-semver/SKILL.md` (+ `src/` mirror): tighten
    the Publish section with a concrete `gh release create` example and the CI-workflow
    pattern. Add a Gotcha: "A `git push --tags` is not a GitHub Release — Releases
    are a separate artifact that must be created explicitly (or by a tag-push workflow)."


    **Known schema follow-up**: `workitem.yaml` `assignee` pattern still requires
    `ACTOR-…` and rejects `TEAMMEMBER-…`. File as separate small fix (not blocking
    v0.19.1).


    **Dogfood the new workflow**: the v0.19.1 tag pushed after this WI should auto-create
    the Release. Verify via `gh release view v0.19.1`.


    **Done when**

    - Both workflow files exist and mirror byte-identical.

    - SKILL.md updates reference both the manual `gh release create` path and the
    shipped workflow.

    - `aibox.lock` bumped to v0.19.1; CHANGELOG has a `## [v0.19.1]` section.

    - `src/PROVENANCE.toml` regenerated.

    - Tag v0.19.1 pushed; GitHub Release v0.19.1 exists (auto-created).

    - Dual-tree drift clean.'
  started_at: '2026-04-22T09:26:25+00:00'
  completed_at: '2026-04-22T15:44:51+00:00'
---

## Transition note (2026-04-22T09:26:25+00:00)

Starting: workflow + SKILL.md fixes in both trees, then v0.19.1 bump + tag-push dogfood.


## Transition note (2026-04-22T15:44:46+00:00)

v0.19.1 shipped + Release verified. Scope pivoted mid-turn from CI workflow (DEC-MerryArch) to local-only (DEC-SnowyWolf) per owner's no-CI directive. Final deliverables: (1) release-semver SKILL.md collapsed to single bulletproof 9-step flow ending in gh release view as completion gate (both trees); (2) pk-doctor 6th check category release_integrity with graceful degradation when gh unavailable (both trees, 5 pre-existing historical tags flagged — v0.1.0-v0.6.0 — correct behavior); (3) DEC-SnowyWolf supersedes DEC-MerryArch; (4) no .github/workflows/ shipped. End-to-end dogfood: /pk-release-style flow executed manually (bump → CHANGELOG → PROVENANCE → commit → tag → push → gh release create → gh release view), Release live at https://github.com/projectious-work/processkit/releases/tag/v0.19.1. 5 LogEntries actor-backfilled.
