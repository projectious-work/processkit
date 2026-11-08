---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  name: example-decision
  labels:
    area: replace-with-area
spec:
  title: Example decision
  status: proposed
  date: "2026-01-01"
  deciders:
    - Replace with the person, role, or team that decides
  summary: Replace with the decision in one or two sentences.
  triggers:
    - Replace with a situation in which this decision matters
  context: Replace with the situation and forces that led to the decision.
  decision: Replace with what was decided.
  consequences: Replace with what follows from the decision.
  alternatives: []
---

Replace with optional explanatory notes. processkit serves this text at
level 2 as section `notes`; it carries no fields.
