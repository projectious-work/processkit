---
apiVersion: processkit.projectious.work/v2
kind: Container
metadata:
  id: SCOPE-alpha-delivery
  created: "2026-07-23T00:04:00Z"
spec:
  kind: scope
  name: alpha-delivery
  description: Complete the dependency-correct alpha ontology slice.
  state: active
  goals:
    - Generate all alpha schemas.
  members:
    - BACK-20260719_0001-ClearPath-alpha-work
---

Scope discriminator fixture for the dependency-complete alpha.
