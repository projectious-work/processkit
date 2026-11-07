---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260502_0857-ThriftyWren-gateway-lazy-catalog-loading-lane
  created: '2026-05-02T08:57:13+00:00'
  updated: '2026-05-02T09:34:02+00:00'
spec:
  title: Gateway lazy catalog and module loading lane
  state: review
  type: story
  priority: critical
  assignee: ACTOR-codex
  description: Split catalog from implementation import, add static/generated or cached
    tool catalog, preserve schema/name/annotation metadata, lazy-import only owning
    source server on first call, and add cache/idle eviction semantics where feasible.
  parent: BACK-20260502_0857-StoutGarnet-full-gateway-daemon-tiger-release-readiness
  started_at: '2026-05-02T08:57:33+00:00'
---

## Transition note (2026-05-02T08:57:33+00:00)

Starting lazy catalog and loading implementation.


## Transition note (2026-05-02T09:34:02+00:00)

Catalog-backed lazy registration implemented, catalog generated, and lazy gateway import/call path verified.
