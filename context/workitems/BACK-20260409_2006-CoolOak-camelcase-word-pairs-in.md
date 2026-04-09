---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260409_2006-CoolOak-camelcase-word-pairs-in
  created: '2026-04-09T20:06:20+00:00'
  labels:
    component: ids
    area: src
  updated: '2026-04-09T21:07:58+00:00'
spec:
  title: CamelCase word pairs in entity IDs — lib update + project migration
  state: done
  type: task
  priority: high
  description: Change _word_pair() in src/lib/processkit/ids.py to produce CamelCase
    (e.g. BoldVale) instead of kebab-case (bold-vale). Add word_style config param.
    Update config.py, id-management server.py (src/ and context/), and id-management/config/settings.toml.
    Migrate all existing entities in context/ (WorkItem, LogEntry, Artifact, DecisionRecord,
    Discussion) to new format.
  started_at: '2026-04-09T21:07:43+00:00'
  completed_at: '2026-04-09T21:07:58+00:00'
---
