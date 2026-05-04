---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260502_0707-WarmComet-schema-demotion-v2-lane
  created: '2026-05-02T07:07:18+00:00'
  updated: '2026-05-02T07:27:20+00:00'
spec:
  title: Schema demotion lane - finish v2 primitive surface
  state: done
  type: task
  priority: high
  assignee: ACTOR-codex
  description: 'Developer lane. Write scope: src/context/schemas/, src/context/models/,
    src/context/processes/, src/context/state-machines/, and src/context/skills/_lib/processkit/.
    Complete Model, Process, Schedule, and StateMachine v2 demotion decisions in src/
    without hidden compatibility shims. Fix closed vocabulary enforcement gaps such
    as Migration.kind. Avoid live context entity migration outside approved MCP paths.'
  parent: BACK-20260502_0706-NobleSwan-gateway-v2-recovery-epic
  started_at: '2026-05-02T07:08:07+00:00'
  completed_at: '2026-05-02T07:27:20+00:00'
---

## Transition note (2026-05-02T07:08:07+00:00)

Developer lane starting.


## Transition note (2026-05-02T07:27:00+00:00)

Implementation complete: shipped src Model/Process/Schedule/StateMachine demotion and Migration.kind validation landed; smoke verification passed.


## Transition note (2026-05-02T07:27:20+00:00)

Accepted after full smoke and targeted pk-doctor checks.
