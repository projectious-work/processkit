---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260501_1739-ProudCrane-adopt-smoothtiger-informed-split-track-v2
  created: '2026-05-01T17:39:22+00:00'
  updated: '2026-05-01T17:39:37+00:00'
spec:
  title: Adopt SmoothTiger-informed split-track v2 implementation sequence
  state: accepted
  decision: 'Use a split-track sequence: src/ deliverables implement the SmoothTiger/SmoothRiver
    v2 direction as soon as possible with no hidden compatibility shims; the live
    project tree remains temporarily on v1 only as a migration staging/runtime state
    while migrations to processkit v0.24.0 complete through migration-management.'
  context: This refines the earlier recovery strategy after reviewing DEC-20260430_1416-SmoothTiger-adopt-breaking-v2-implementation-plan-for
    and the external originating work plan ART-20260430_1242-SmoothRiver-processkit-project-work-plan
    at https://github.com/projectious-work/internal/blob/main/context/artifacts/ART-20260430_1242-SmoothRiver-processkit-project-work-plan.md.
    SmoothTiger states that v2 schema and index contracts become authoritative, no
    backward-compatibility shims should be introduced, and v1 contexts are handled
    only through an explicit migration path. SmoothRiver provides the sprint scope
    for schema vocabulary, sharding, migration semantics, doctor checks, Metric/Model
    demotion, Hook inbox, AgentCard projection, eval gates, cost enforcement, Process/Schedule
    demotion, and later projections.
  rationale: The split lets src/ move toward the accepted breaking v2 deliverable
    contract while preserving the currently running project tree long enough to execute
    pending migrations safely. It avoids treating live v1 context as a long-term compatibility
    target and avoids accidental context/src mirroring that would corrupt the migration
    staging boundary.
  alternatives:
  - option: Keep context/ and src/context/ fully mirrored throughout recovery
    reason_not_chosen: Would erase the intended staging boundary and risk forcing
      the active project runtime into a half-migrated v2 state.
  - option: Add v1/v2 compatibility shims in src/ to tolerate both contracts indefinitely
    reason_not_chosen: Contradicts DEC-SmoothTiger, which chooses a breaking v2 program
      and explicit migration path instead of hidden compatibility layers.
  consequences: Plans must separate src/ v2 implementation from live context/ migration
    health. Live context/ stays v1 only until explicit migration steps are complete.
    Missing SmoothRiver/SmoothTiger items after runtime migration become the implementation
    backlog, ordered by the SmoothRiver sprint sequence and verified against no-shim
    v2 semantics.
  related_workitems:
  - BACK-20260409_1652-WildButter-create-polish-and-deploy
  decided_at: '2026-05-01T17:39:22+00:00'
  supersedes: DEC-20260501_1651-MerryStream-adopt-split-track-v2-deliverable-and
---
