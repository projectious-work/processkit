---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260430_0919-SilentRabbit-workitem-created
  created: '2026-04-30T09:19:35+00:00'
spec:
  event_type: workitem.created
  timestamp: '2026-04-30T09:19:35+00:00'
  summary: 'Created WorkItem ''BACK-20260430_0918-MightySwan-add-context-consumption-checkpoint-reports'':
    ''Add context-consumption checkpoint reports'''
  actor: codex
  subject: BACK-20260430_0918-MightySwan-add-context-consumption-checkpoint-reports
  subject_kind: WorkItem
  details:
    note: 'create_workitem wrote the WorkItem file but failed before auto-log/reindex
      with ''no such module: vec0''; index was rebuilt via index-management.reindex
      before this compensating event.'
---
