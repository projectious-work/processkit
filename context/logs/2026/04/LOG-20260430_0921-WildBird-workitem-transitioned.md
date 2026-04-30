---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260430_0921-WildBird-workitem-transitioned
  created: '2026-04-30T09:21:00+00:00'
spec:
  event_type: workitem.transitioned
  timestamp: '2026-04-30T09:21:00+00:00'
  summary: Transitioned WorkItem 'BACK-20260430_0918-MightySwan-add-context-consumption-checkpoint-reports'
    from 'backlog' to 'in-progress'
  actor: BACK-20260430_0918-MightySwan-add-context-consumption-checkpoint-reports
  subject: BACK-20260430_0918-MightySwan-add-context-consumption-checkpoint-reports
  subject_kind: WorkItem
  details:
    from_state: backlog
    to_state: in-progress
    note: 'Compensating event: transition_workitem updated the WorkItem but failed
      before auto-log/reindex with ''no such module: vec0''.'
---
