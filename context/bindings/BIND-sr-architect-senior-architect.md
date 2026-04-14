---
apiVersion: processkit.projectious.work/v1
kind: Binding
metadata:
  id: BIND-sr-architect-senior-architect
  created: 2026-04-14T09:00:00Z
spec:
  type: role-assignment
  subject: ACTOR-sr-architect
  subject_kind: Actor
  target: ROLE-senior-architect
  target_kind: Role
  valid_from: 2026-04-14
  description: "Large / complex design and bug diagnosis."
  conditions:
    scope: permanent
    source_decision: DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
---
