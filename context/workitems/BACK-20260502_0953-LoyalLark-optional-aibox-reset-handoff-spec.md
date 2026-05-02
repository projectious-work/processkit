---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260502_0953-LoyalLark-optional-aibox-reset-handoff-spec
  created: '2026-05-02T09:53:07+00:00'
  updated: '2026-05-02T17:13:46+00:00'
spec:
  title: Optional aibox reset handoff specification
  state: review
  type: task
  priority: high
  description: Write processkit-owned handoff/spec material for an optional harder
    aibox reset path. Recommend implementation as an opt-in mode of aibox apply or
    aibox reset, with user choice required. Preserve normal current processkit migrations
    as the default upgrade path.
  parent: BACK-20260502_0952-SunnyButter-final-release-blockers-aibox-handoff
  started_at: '2026-05-02T17:13:37+00:00'
---

## Transition note (2026-05-02T17:13:37+00:00)

Implementation started in main session.


## Transition note (2026-05-02T17:13:46+00:00)

Documented optional aibox apply/reset path and normal migrations-as-default boundary in the handover document.
