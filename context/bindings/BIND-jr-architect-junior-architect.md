---
apiVersion: processkit.projectious.work/v1
kind: Binding
metadata:
  id: BIND-jr-architect-junior-architect
  created: 2026-04-14T09:00:00Z
spec:
  type: role-assignment
  subject: ACTOR-jr-architect
  subject_kind: Actor
  target: ROLE-junior-architect
  target_kind: Role
  valid_from: 2026-04-14
  description: "Small-to-medium design and architectural Q&A."
  conditions:
    scope: permanent
    source_decision: DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
---
