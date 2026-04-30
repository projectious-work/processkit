---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260430_1632-GrandThorn-migration-v2-context-converted
  created: '2026-04-30T16:32:33+00:00'
spec:
  event_type: migration.v2-context-converted
  timestamp: '2026-04-30T16:32:33+00:00'
  summary: Converted 21 processkit entities to processkit.projectious.work/v2
  subject: processkit-v2
  subject_kind: Migration
  actor: processkit-migration-management
  details:
    changed_paths:
    - context/schemas/actor.yaml
    - context/schemas/category.yaml
    - context/schemas/constraint.yaml
    - context/schemas/context.yaml
    - context/schemas/decisionrecord.yaml
    - context/schemas/discussion.yaml
    - context/schemas/gate.yaml
    - context/schemas/metric.yaml
    - context/schemas/process.yaml
    - context/schemas/role.yaml
    - context/schemas/schedule.yaml
    - context/schemas/scope.yaml
    - context/schemas/statemachine.yaml
    - context/schemas/team-member.yaml
    - context/skills/processkit/model-recommender/default-bindings/MANIFEST.yaml
    - context/state-machines/decisionrecord.yaml
    - context/state-machines/discussion.yaml
    - context/state-machines/migration.yaml
    - context/state-machines/note.yaml
    - context/state-machines/scope.yaml
    - context/state-machines/workitem.yaml
    errors: []
---
