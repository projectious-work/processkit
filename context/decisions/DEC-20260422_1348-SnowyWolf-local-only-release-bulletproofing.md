---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260422_1348-SnowyWolf-local-only-release-bulletproofing
  created: '2026-04-22T13:48:39+00:00'
  updated: '2026-04-22T13:54:52+00:00'
spec:
  title: 'Local-only release bulletproofing: single-turn release-semver flow + pk-doctor
    release_integrity check (no CI workflows)'
  state: accepted
  decision: 'Supersede `DEC-20260422_0926-MerryArch` (which proposed a `.github/workflows/release.yml`
    tag-push workflow). Do **not** add GitHub Actions workflows — vendor-specific,
    metered, and against the owner''s cost stance. Instead, make the release process
    bulletproof through two strictly local mechanisms: (1) **Prevention** — collapse
    `/pk-release` into a single end-to-end flow that prepares *and* publishes in the
    same turn, with an explicit `gh release create` step and a mandatory verification
    (`gh release view`) before the command is considered complete. Remove the split
    between `/pk-release` and `/pk-publish` that made half-done releases possible.
    (2) **Detection** — add a 6th pk-doctor check category `release_integrity` that
    enumerates every local `v*` git tag, probes GitHub (via `gh release view`) for
    a matching Release, and emits a WARN for any tag without one. Gracefully INFO
    when `gh` is unavailable. Both mechanisms ship in v0.19.1, replacing the now-discarded
    CI workflow approach.'
  context: 'User rejected the CI-workflow approach on two grounds: vendor lock-in
    (GitHub Actions only helps GitHub-hosted projects) and cost (Actions minutes are
    metered on private or heavy-use accounts). Both arguments are durable — processkit
    should not assume a paid CI runtime. The original v0.19.0 miss was the agent stopping
    after prepare; the root cause is fixable entirely within the processkit layer
    (skill flow + doctor check) without reaching for CI.'
  rationale: (1) **Local-only stays with processkit's value proposition.** processkit
    is a file-based, provider-neutral toolkit; CI workflow files break that story.
    (2) **Single-turn /pk-release prevents the miss structurally.** If the slash command's
    documented flow ends with `gh release create` + verification, an agent that claims
    "done" without running those steps is violating the skill — caught by skill-reviewer
    or review. No human discipline required mid-release. (3) **pk-doctor provides
    the safety net.** Even if the skill is mis-invoked or skipped, `release_integrity`
    catches missing Releases on the next `/pk-doctor` run. Warnings, not errors —
    it flags the gap without blocking the repo. (4) **`gh release create` is free.**
    It's a single REST API call, runs locally, no metered runtime. (5) **Split prepare/publish
    is the wrong abstraction here.** It was useful when publishing meant pushing to
    crates.io / PyPI (multi-minute work that justified a checkpoint). For processkit's
    current reality — the release artifact is the GitHub Release page — the two phases
    collapse to one natural turn.
  alternatives:
  - option: Keep the CI workflow; user just learns to live with the cost
    rejected_because: User explicitly rejected on cost + vendor-lock grounds; durable
      objection.
  - option: Third-party non-GitHub CI (e.g., local runner, custom webhook)
    rejected_because: Adds more infrastructure than it removes; not provider-neutral
      either; violates simplicity.
  - option: Only add pk-doctor detection; don't change the skill flow
    rejected_because: Detection catches the miss after the fact; it doesn't prevent
      it. Pairing detection with prevention is stronger and both are cheap.
  - option: Only change the skill flow; skip the pk-doctor check
    rejected_because: No safety net if the skill is ever bypassed or a future agent
      mis-interprets the flow. Belt-plus-suspenders here is worth the ~60 LOC.
  - option: Pre-commit / pre-push git hook that blocks tag pushes without a prior
      Release
    rejected_because: git hooks are local-machine only and not version-controlled
      by default; unreliable across contributors.
  consequences: '- `.github/workflows/release.yml` and `src/.github/workflows/release.yml`
    will NOT ship. Local files removed from this session''s uncommitted state.\n-
    `release-semver/SKILL.md` (both trees) rewritten: single flow, mandatory verification
    step, updated Gotcha ("prepare-only is not a release; the flow only completes
    when `gh release view vX.Y.Z` succeeds").\n- `/pk-publish` slash command deprecated
    (kept as an alias for recovery scenarios: tag already pushed, Release missing).\n-
    pk-doctor gains a 6th check category `release_integrity`. Depends on `gh` CLI
    being installed and authenticated in the local environment — INFO (not ERROR)
    when unavailable.\n- v0.19.1 still ships this turn, now with the revised scope.
    The v0.19.1 Release itself will be created via the new single-flow command, dogfooding
    the prevention mechanism.\n- `DEC-20260422_0926-MerryArch` transitions to `superseded`
    with a pointer to this DEC.'
  related_workitems:
  - BACK-20260422_0925-MightyOtter-v0-19-1-release
  decided_at: '2026-04-22T13:48:39+00:00'
  supersedes: DEC-20260422_0926-MerryArch-auto-create-github-releases
---
