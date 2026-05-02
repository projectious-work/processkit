---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260502_0953-CalmRobin-demotion-contract-cleanup-release-work
  created: '2026-05-02T09:53:07+00:00'
  updated: '2026-05-02T17:13:37+00:00'
spec:
  title: Model process metric demotion contract cleanup
  state: review
  type: task
  priority: high
  description: Finalize shipped v2 demotion contract for Model, Process, and Metric.
    Keep demoted primitives out of src/context deliverables, classify live context
    state as legacy migration source, update task-router compatibility behavior or
    docs, and tighten doctor/release guards.
  parent: BACK-20260502_0952-SunnyButter-final-release-blockers-aibox-handoff
  started_at: '2026-05-02T09:53:29+00:00'
---

## Transition note (2026-05-02T09:53:29+00:00)

Assigned to third parallel implementation lane.


## Transition note (2026-05-02T17:13:37+00:00)

Removed shipped demoted primitive leaks, cleaned model-assignment target_kind usage, documented legacy process overrides; verified release tarball excludes models/processes.
