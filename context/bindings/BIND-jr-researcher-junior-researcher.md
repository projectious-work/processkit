---
apiVersion: processkit.projectious.work/v1
kind: Binding
metadata:
  id: BIND-jr-researcher-junior-researcher
  created: 2026-04-14T09:00:00Z
spec:
  type: role-assignment
  subject: ACTOR-jr-researcher
  subject_kind: Actor
  target: ROLE-junior-researcher
  target_kind: Role
  valid_from: 2026-04-14
  description: "Focused research and summarisation tasks."
  conditions:
    scope: permanent
    source_decision: DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
---
