---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260430_1516-SunnyOak-decision-created
  created: '2026-04-30T15:16:32+00:00'
spec:
  event_type: decision.created
  timestamp: '2026-04-30T15:16:32+00:00'
  summary: 'Created DecisionRecord ''DEC-20260430_1416-SmoothTiger-adopt-breaking-v2-implementation-plan-for'':
    ''Adopt breaking v2 implementation plan for SteadyTiger v0.3 processkit support'''
  subject: DEC-20260430_1416-SmoothTiger-adopt-breaking-v2-implementation-plan-for
  subject_kind: DecisionRecord
  actor: DEC-20260430_1416-SmoothTiger-adopt-breaking-v2-implementation-plan-for
  details:
    recovered_after: initial record_decision call wrote the entity but failed before
      logging because the index cache contained an unloadable sqlite-vec virtual table
---
