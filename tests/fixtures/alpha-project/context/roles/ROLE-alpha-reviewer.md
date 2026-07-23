---
apiVersion: processkit.projectious.work/v2
kind: Role
metadata:
  id: ROLE-alpha-reviewer
  created: "2026-07-23T00:01:00Z"
spec:
  name: alpha-reviewer
  description: Reviews alpha ontology contracts and evidence.
  responsibilities:
    - Review generated schema compatibility.
  skills_required:
    - schema-management
---

Role fixture for the dependency-complete alpha.
