---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260409_1449-BoldVale-fts5-full-text-search
  created: '2026-04-09T14:49:49+00:00'
  labels:
    component: index
    area: src
spec:
  title: FTS5 full-text search in the SQLite index
  state: backlog
  type: task
  priority: medium
  description: Switch search_entities from LIKE %text% to SQLite FTS5 for proper tokenisation
    and ranking. Requires adding a virtual FTS5 table to the index schema and a migration
    for existing index databases. Change is contained to src/lib/processkit/index.py.
---
