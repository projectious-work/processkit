---
apiVersion: processkit.projectious.work/v2
kind: TeamMember
metadata:
  id: TEAMMEMBER-alpha-reviewer
  created: "2026-07-23T00:03:00Z"
spec:
  name: Alpha Reviewer
  type: ai-agent
  state: active
  slug: alpha-reviewer
  default_role: ROLE-alpha-reviewer
  default_seniority: specialist
  skills:
    - schema-management
  capabilities:
    - CAP-alpha-validation
---

TeamMember composition fixture for the dependency-complete alpha.
