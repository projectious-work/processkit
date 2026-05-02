---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260502_0744-WildSwan-gateway-docs-release-lane
  created: '2026-05-02T07:44:34+00:00'
  labels:
    area: docs
    lane: release
  updated: '2026-05-02T08:41:22+00:00'
spec:
  title: Gateway docs release lane
  state: done
  type: story
  priority: medium
  assignee: ACTOR-codex
  description: Update docs-site and skill docs for gateway architecture, non-aibox
    usage, aibox boundary, security/session model, release notes, and compatibility
    checklist.
  parent: BACK-20260502_0743-CalmHawk-implement-provider-neutral-gateway-daemon
  started_at: '2026-05-02T08:41:17+00:00'
  completed_at: '2026-05-02T08:41:22+00:00'
---

## Transition note (2026-05-02T08:41:17+00:00)

Updated docs navigation and installation/overview pages for the new processkit-gateway mode.


## Transition note (2026-05-02T08:41:20+00:00)

Release-facing docs now describe per-skill, aggregate, gateway stdio, and future daemon/proxy deployment modes.


## Transition note (2026-05-02T08:41:22+00:00)

Docs build completed successfully with the existing unrelated /processkit/ broken-link warning.
