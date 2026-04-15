---
apiVersion: processkit.projectious.work/v1
kind: Actor
metadata:
  id: ACTOR-jr-researcher
  created: 2026-04-14T09:00:00Z
spec:
  type: ai-agent
  name: "Junior Researcher (Claude Sonnet 4.6)"
  active: true
  joined_at: 2026-04-14T09:00:00Z
  is_template: true
  templated_from: null
  roles:
    - ROLE-junior-researcher
  expertise:
    - focused-research
    - summarisation
    - comparison-tables
  preferences:
    model: claude-sonnet-4-6
    model_tier: sonnet
    clone_policy:
      default_clones: 1
      max_clones_without_approval: 5
---
