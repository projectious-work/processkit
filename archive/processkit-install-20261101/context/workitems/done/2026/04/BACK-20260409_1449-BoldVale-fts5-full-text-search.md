---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260409_1449-BoldVale-fts5-full-text-search
  created: '2026-04-09T14:49:49+00:00'
  labels:
    component: index
    area: src
  updated: '2026-04-29T16:24:45+00:00'
spec:
  title: FTS5 full-text search in the SQLite index
  state: done
  type: task
  priority: medium
  description: Switch search_entities from LIKE %text% to SQLite FTS5 for proper tokenisation
    and ranking. Requires adding a virtual FTS5 table to the index schema and a migration
    for existing index databases. Change is contained to src/lib/processkit/index.py.
  started_at: '2026-04-29T16:05:50+00:00'
  completed_at: '2026-04-29T16:24:45+00:00'
---

## Transition note (2026-04-29T16:05:50+00:00)

Starting Phase 1 FTS5 implementation.


## Transition note (2026-04-29T16:24:39+00:00)

FTS5 side table, ranked search, LIKE fallback, docs, and smoke coverage implemented; validation passed.


## Transition note (2026-04-29T16:24:45+00:00)

Phase 1 accepted after smoke coverage and drift guard passed.
