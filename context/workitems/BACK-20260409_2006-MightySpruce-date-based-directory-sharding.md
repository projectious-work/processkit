---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260409_2006-MightySpruce-date-based-directory-sharding
  created: '2026-04-09T20:06:24+00:00'
  labels:
    component: paths
    area: src
  updated: '2026-04-09T21:07:59+00:00'
spec:
  title: Date-based directory sharding for high-volume entity kinds
  state: done
  type: task
  priority: medium
  description: 'Implement the dormant sharding config stub: update paths.py to add
    entity_dir_for(kind, created_at) that routes to context/logs/{year}/{month}/ when
    sharding is enabled for a kind. Update all entity-creating MCP servers to use
    this path. Enable LogEntry sharding by default in index-management/config/settings.toml.
    Index already uses rglob so it handles subdirs automatically.'
  started_at: '2026-04-09T21:07:43+00:00'
  completed_at: '2026-04-09T21:07:59+00:00'
---
