---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260422_0926-MerryArch-auto-create-github-releases
  created: '2026-04-22T09:26:42+00:00'
  updated: '2026-04-22T13:54:52+00:00'
spec:
  title: Auto-create GitHub Releases via tag-push workflow; mirror to src/ for downstream
    projects
  state: superseded
  decision: 'Ship `.github/workflows/release.yml` at the processkit repo root that,
    on push of any `v*` tag, extracts the matching section from `CHANGELOG.md` and
    creates a GitHub Release via `softprops/action-gh-release@v2`. Mirror the same
    workflow into `src/.github/workflows/release.yml` so downstream projects installed
    through aibox inherit the automation. Tighten the `release-semver` SKILL.md''s
    Publish section with a concrete `gh release create` example and the shipped-workflow
    pattern, and add an explicit Gotcha: "a `git push --tags` is not a GitHub Release."
    Cut v0.19.1 to deliver this fix and dogfood the workflow.'
  context: 'During v0.19.0 release, `/pk-release` was invoked (prepare phase: bump
    + CHANGELOG + tag + push) but `/pk-publish` was not invoked afterwards. The tag
    landed on GitHub but no Release entry existed — downstream consumers of `gh api`
    / the Releases page / aibox sync would have missed the release. The fix required
    a manual `gh release create`. The miss is easy to repeat: a developer can stop
    after `/pk-release` without realising the publish step is separate.'
  rationale: '(1) **Automation over discipline.** A tag-push workflow removes the
    human step entirely: any future `v*` tag push reliably produces a Release with
    CHANGELOG-derived notes. (2) **Mirror to src/.** processkit is consumed by downstream
    projects via aibox; shipping the workflow under `src/.github/workflows/` means
    those projects inherit the automation without needing to copy it by hand. (3)
    **Doc tightening is secondary but cheap.** The SKILL.md currently says "Publish
    according to the project''s distribution channel" — too abstract. A concrete `gh
    release create` command, plus the CI-workflow snippet, makes the publish-phase
    expectation unambiguous for humans and agents. (4) **Dogfood the fix in the same
    release.** Cutting v0.19.1 with the workflow already committed means pushing the
    tag validates the end-to-end automation. Follow-up: the `decisionrecord.yaml`
    deciders[] pattern still requires `ACTOR-*` — that schema needs TEAMMEMBER-* support;
    filed separately.'
  alternatives:
  - option: 'Discipline-only: require /pk-publish after /pk-release; add a Gotcha
      but no CI'
    rejected_because: Relies on every future release-runner remembering the second
      step. Exactly the failure mode that caused v0.19.0's miss.
  - option: Merge /pk-release and /pk-publish into a single step
    rejected_because: Publishing is irreversible; keeping prepare and publish distinct
      preserves a reviewable checkpoint. Automating publish via CI is safer than short-circuiting
      the slash command.
  - option: Pk-doctor category that flags tags missing Releases
    rejected_because: Good complement but doesn't prevent the miss; we chose to prioritise
      prevention (CI) over detection (doctor). Doctor check can be added later as
      a second-line defence.
  - option: Use release-please or goreleaser instead of softprops/action-gh-release
    rejected_because: Those tools own the CHANGELOG/versioning workflow; processkit
      already has its own release-semver skill + manual CHANGELOG. softprops is a
      minimal single-purpose action that only does the GH Release step — matches our
      existing pipeline exactly.
  consequences: '`.github/workflows/` directory created at repo root (first workflow).
    Requires the repo to allow GitHub Actions (already enabled). `softprops/action-gh-release@v2`
    added as a transitive dependency (pinned to a major version). `src/.github/workflows/release.yml`
    shipped in aibox-synced template tree — downstream processkit projects will gain
    the workflow on next sync. Existing Releases (v0.19.0 and earlier) unchanged.
    A future tag-push that lacks a matching CHANGELOG section will get a fallback
    placeholder body; acceptable minor ugliness, not a blocker. v0.19.1 patch release
    required to ship the workflow. Separately flagged: the schema pattern for deciders[]
    / assignee is still `ACTOR-*` and needs TEAMMEMBER-* support (not blocking this
    fix).'
  related_workitems:
  - BACK-20260422_0925-MightyOtter-v0-19-1-release
  decided_at: '2026-04-22T09:26:42+00:00'
  superseded_by: DEC-20260422_1348-SnowyWolf-local-only-release-bulletproofing
---
