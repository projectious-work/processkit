---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260429_1953-QuietDaisy-measure-processkit-context-consumption
  created: '2026-04-29T19:53:06+00:00'
  labels:
    area: context
    release: next
    source: user-request
  updated: '2026-04-30T08:49:36+00:00'
spec:
  title: Measure processkit context consumption
  state: done
  type: spike
  priority: medium
  description: 'Investigate and implement optional measurability for context consumed
    by processkit itself. Candidate metrics: rendered AGENTS.md bytes/tokens, active
    skill instruction bytes/tokens, MCP tool schema count/serialized size, status
    briefing payload size, and per-harness startup prompt contribution. The implementation
    should be optional, provider-neutral, and should avoid sending project content
    to external tokenizers unless the user opts in.'
  started_at: '2026-04-30T08:49:23+00:00'
  completed_at: '2026-04-30T08:49:36+00:00'
---

## Transition note (2026-04-30T08:49:23+00:00)

Implemented pk-doctor INFO-only context consumption measurement and context budget loading.


## Transition note (2026-04-30T08:49:29+00:00)

Implementation and validation complete.


## Transition note (2026-04-30T08:49:36+00:00)

Validated with py_compile, team-manager tests, pk-doctor context_consumption, drift guard, and server smoke test.
