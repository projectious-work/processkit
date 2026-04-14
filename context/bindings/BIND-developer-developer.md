---
apiVersion: processkit.projectious.work/v1
kind: Binding
metadata:
  id: BIND-developer-developer
  created: 2026-04-14T09:00:00Z
spec:
  type: role-assignment
  subject: ACTOR-developer
  subject_kind: Actor
  target: ROLE-developer
  target_kind: Role
  valid_from: 2026-04-14
  description: "Feature implementation and bug fixes against architect plans."
  conditions:
    scope: permanent
    source_decision: DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
---
