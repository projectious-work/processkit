---
apiVersion: processkit.projectious.work/v2
kind: Capability
metadata:
  id: CAP-alpha-validation
  created: "2026-07-23T00:02:00Z"
spec:
  name: alpha-validation
  description: Validate the generated alpha ontology contracts.
  state: active
  kind: ability
  providers:
    - TEAMMEMBER-alpha-reviewer
  outputs:
    - ART-ClearPath-alpha-evidence
---

Capability fixture for the dependency-complete alpha.
