---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260502_0857-TidyBear-gateway-doctor-manifest-measurement-lane
  created: '2026-05-02T08:57:22+00:00'
  updated: '2026-05-02T09:27:37+00:00'
spec:
  title: Gateway doctor manifest measurement lane
  state: in-progress
  type: story
  priority: high
  assignee: ACTOR-codex
  description: Extend pk-doctor, mcp_config_drift, manifest generation, preauth, and
    measurement scripts for eager gateway, daemon mode, proxy mode, mixed registration,
    stale manifests, process counts, and memory/RSS reporting where practical.
  parent: BACK-20260502_0857-StoutGarnet-full-gateway-daemon-tiger-release-readiness
  started_at: '2026-05-02T09:27:37+00:00'
---

## Transition note (2026-05-02T09:27:37+00:00)

Started doctor/measurement work for daemon, proxy, and lazy gateway modes.
