---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260409_2006-SpryFjord-date-time-prefix-in
  created: '2026-04-09T20:06:22+00:00'
  labels:
    component: ids
    area: src
  updated: '2026-04-09T21:07:59+00:00'
spec:
  title: Date-time prefix in entity IDs — lib update + project migration
  state: done
  type: task
  priority: high
  description: Add datetime_prefix option to ids.generate_id(). When enabled, prepend
    YYYYMMDD_HHMM (from entity's created timestamp) to the word pair. Format becomes
    PREFIX-YYYYMMDD_HHMM-CamelCase[-slug]. Update config.py, id-management server.py,
    and settings.toml. Migrate all existing entities (derive datetime from metadata.created).
    Enable by default for this project.
  started_at: '2026-04-09T21:07:43+00:00'
  completed_at: '2026-04-09T21:07:59+00:00'
---
