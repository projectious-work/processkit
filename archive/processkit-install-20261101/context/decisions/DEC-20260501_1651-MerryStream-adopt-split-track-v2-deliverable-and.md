---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260501_1651-MerryStream-adopt-split-track-v2-deliverable-and
  created: '2026-05-01T16:51:34+00:00'
  updated: '2026-05-01T17:39:37+00:00'
spec:
  title: Adopt split-track v2 deliverable and v1 live-tree migration strategy
  state: superseded
  decision: Implement v2 direction in src/ deliverables as soon as possible, while
    the running project tree remains temporarily on v1 and completes migrations to
    processkit v0.24.0.
  context: 'Recovery found the worktree split between v2 package deliverables under
    src/context and v1-style live project context under context/. The user clarified
    the intended strategy: src/ is the forward-facing deliverable surface and should
    converge on v2 quickly; the live project tree should prioritize operational continuity
    on v1 until migrations to processkit v0.24.0 are executed.'
  rationale: This separates packaged release work from the dogfooding runtime state.
    It avoids forcing the active processkit project onto a half-migrated v2 context
    while still allowing src/ to make forward progress toward the v2 contract.
  alternatives:
  - option: Immediate full v2 conversion of live context/
    reason_not_chosen: Higher operational risk while migrations are pending and current
      project MCP tooling is running against the live tree.
  - option: Rollback src/ to v1 until live context/ is ready
    reason_not_chosen: Delays v2 deliverables and conflicts with the stated priority
      to implement the v2 direction in src/ as soon as possible.
  consequences: Implementation plans must treat context/ and src/context/ as intentionally
    split for now. Do not blindly mirror v2 source changes into live context/. Migrations
    should be executed through migration-management, and src/ verification should
    be evaluated independently from live-tree migration health.
  related_workitems:
  - BACK-20260409_1652-WildButter-create-polish-and-deploy
  decided_at: '2026-05-01T16:51:34+00:00'
  superseded_by: DEC-20260501_1739-ProudCrane-adopt-smoothtiger-informed-split-track-v2
---
