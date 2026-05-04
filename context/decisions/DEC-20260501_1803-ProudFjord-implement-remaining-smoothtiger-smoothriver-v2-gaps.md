---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260501_1803-ProudFjord-implement-remaining-smoothtiger-smoothriver-v2-gaps
  created: '2026-05-01T18:03:50+00:00'
spec:
  title: Implement remaining SmoothTiger SmoothRiver v2 gaps with parallel team lanes
  state: accepted
  decision: 'Proceed with implementation using parallel workers on disjoint src/docs/test
    scopes, while preserving the split-track rule: src deliverables move to the SmoothTiger/SmoothRiver
    v2 direction and the running context tree remains temporarily v1 except for approved
    migrations.'
  context: The user approved the remaining implementation plan after a src-only audit
    found that v2 vocabulary, events, sharding, migration semantics, Hook inbox, eval/cost/projection
    scaffolding are present, but Model, Process, Schedule, and StateMachine demotions
    remain incomplete.
  rationale: 'Persisting the plan and approval protects against interruption. Parallel
    lanes fit the work shape: schemas/lib, MCP skills, doctor/tests, docs, migration
    materials, and projection/eval/cost follow-through can be developed independently
    and then integrated by the main session.'
  alternatives:
  - option: Continue with ad hoc single-threaded edits
    rejected_because: Higher interruption risk and less efficient for the broad but
      separable SmoothRiver gap list.
  - option: Keep old primitives in src and document them as legacy
    rejected_because: Conflicts with SmoothTiger's breaking v2 direction and no-hidden-shim
      stance.
  - option: Move live context to v2 at the same time
    rejected_because: Conflicts with the accepted split-track strategy that the running
      project tree temporarily remains v1.
  consequences: The next implementation should remove or demote remaining primitive
    surfaces in src, refactor dependent skills and docs, expand doctor/test coverage,
    and keep live context changes constrained to MCP-managed records and approved
    migrations.
  deciders:
  - ACTOR-user
  - ACTOR-codex
  decided_at: '2026-05-01T18:03:50+00:00'
---
