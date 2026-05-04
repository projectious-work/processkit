---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260502_0744-ProudClover-doctor-manifest-gateway-drift-lane
  created: '2026-05-02T07:44:22+00:00'
  labels:
    area: doctor
    lane: manifest-drift
  updated: '2026-05-02T08:41:07+00:00'
spec:
  title: Doctor manifest gateway drift lane
  state: done
  type: story
  priority: high
  assignee: ACTOR-codex
  description: Add mcp_gateway doctor checks, teach mcp_config_drift and manifest
    generation about intentional gateway/proxy mode, and guard against starting both
    granular and gateway configs unintentionally.
  parent: BACK-20260502_0743-CalmHawk-implement-provider-neutral-gateway-daemon
  started_at: '2026-05-02T08:41:03+00:00'
  completed_at: '2026-05-02T08:41:07+00:00'
---

## Transition note (2026-05-02T08:41:03+00:00)

Added gateway manifest handling and pk-doctor checks for gateway config presence and drift.


## Transition note (2026-05-02T08:41:05+00:00)

Regenerated context and src MCP manifests with gateway config tracked separately from aggregate granular hash.


## Transition note (2026-05-02T08:41:07+00:00)

Targeted doctor checks and doctor unit tests pass with 0 errors and 0 warnings.
