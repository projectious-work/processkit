---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260430_0918-MightySwan-add-context-consumption-checkpoint-reports
  created: '2026-04-30T09:18:57+00:00'
  labels:
    decision: DEC-20260430_0900-HappyComet-measure-processkit-context-overhead
  updated: '2026-04-30T09:32:46+00:00'
spec:
  title: Add context-consumption checkpoint reports
  state: done
  type: story
  priority: medium
  description: Implement the accepted checkpoint/report design for processkit context-consumption
    measurement. Done means users can create named local checkpoints, compare two
    checkpoints, and get a provider-neutral report that clearly labels local token
    counts as estimates rather than provider-billed usage.
  scope: processkit
  started_at: '2026-04-30T09:20:45+00:00'
  completed_at: '2026-04-30T09:32:46+00:00'
---

## Transition note (2026-04-30T09:20:45+00:00)

Continuing implementation after crash; accepted decision DEC-20260430_0900-HappyComet defines the checkpoint/report design.


## Transition note (2026-04-30T09:32:33+00:00)

Implemented checkpoint/report CLI, docs, index vec0 guard, and tests; focused and smoke checks pass.


## Transition note (2026-04-30T09:32:46+00:00)

Validated with py_compile, pk-doctor focused tests, drift guard, smoke-test-servers, and context_consumption doctor category.
