---
apiVersion: processkit.projectious.work/v2
kind: Proposition
metadata:
  id: PROP-20260722_0002-ClearPath-alpha-risk
  created: "2026-07-22T00:02:00Z"
spec:
  kind: risk
  statement: Derived projects may rely on incomplete alpha contracts.
  status: open
  confidence: 0.7
  likelihood: possible
  probability: 0.4
  impact: major
  risk_status: mitigating
  response: mitigate
  mitigation: Publish explicit validation modes and alpha adoption guidance.
  owner: TEAMMEMBER-cora
  affected_entities:
    - BACK-20260719_0001-ClearPath-alpha-work
---

Risk discriminator fixture for the v1 alpha.
