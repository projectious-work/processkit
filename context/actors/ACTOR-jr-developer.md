---
apiVersion: processkit.projectious.work/v1
kind: Actor
metadata:
  id: ACTOR-jr-developer
  created: 2026-04-14T09:00:00Z
spec:
  type: ai-agent
  name: "Junior Developer (Claude Haiku 4.5)"
  active: true
  joined_at: 2026-04-14T09:00:00Z
  is_template: true
  templated_from: null
  roles:
    - ROLE-junior-developer
  expertise:
    - simple-edits
    - mechanical-refactor
    - obvious-bug-fix
  preferences:
    model: claude-haiku-4-5-20251001
    model_tier: haiku
    clone_policy:
      default_clones: 1
      max_clones_without_approval: 5
---
