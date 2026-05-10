---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260510_0344-DeepOwl-release-prep-close-audit-transitions-bump
  created: '2026-05-10T03:44:13+00:00'
  labels:
    release: v0.26.0
    cluster: release-prep
spec:
  title: v0.26.0 release prep — close issues, audit, transitions, version bump
  state: backlog
  type: epic
  priority: high
  description: |
    Cluster of 4 release-prep tasks for v0.26.0 (post-VastVale). Children dispatched as ephemeral subagents:
    - A1: close gh#18, #19, #20, #22 with PR #24 reference (Haiku)
    - A2: run pk-release-audit + pk-doctor on dogfood; report findings (Sonnet)
    - A3: transition the 12 session WorkItems from review → done (Haiku)
    - A4: bump aibox.toml version 0.25.8 → 0.26.0 (Haiku, gated on A2 green)
---
