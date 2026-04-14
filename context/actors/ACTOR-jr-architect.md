---
apiVersion: processkit.projectious.work/v1
kind: Actor
metadata:
  id: ACTOR-jr-architect
  created: 2026-04-14T09:00:00Z
spec:
  type: ai-agent
  name: "Junior Architect (Claude Sonnet 4.6)"
  active: true
  joined_at: 2026-04-14T09:00:00Z
  roles:
    - ROLE-junior-architect
  expertise:
    - focused-design
    - moderate-bug-diagnosis
  preferences:
    model: claude-sonnet-4-6
    model_tier: sonnet
    clone_policy:
      default_clones: 1
      max_clones_without_approval: 5
---
