---
apiVersion: processkit.projectious.work/v1
kind: Role
metadata:
  id: ROLE-junior-developer
  created: 2026-04-14T09:00:00Z
spec:
  name: junior-developer
  description: "Implements low-complexity code changes, simple bug fixes, and mechanical refactors from a clear plan."
  responsibilities:
    - "Apply well-specified, single-file edits: typos, simple refactors, string renames"
    - "Fix obvious bugs where the failure mode and fix are already identified"
    - "Run the project's tests after each change and report the result verbatim"
    - "Escalate to developer when a task starts needing judgement calls"
  skills_required:
    - code-generation
    - git-workflow
  default_scope: permanent
  model_tier: haiku
---
