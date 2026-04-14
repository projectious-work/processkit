---
apiVersion: processkit.projectious.work/v1
kind: Actor
metadata:
  id: ACTOR-sr-architect
  created: 2026-04-14T09:00:00Z
spec:
  type: ai-agent
  name: "Senior Architect (Claude Opus 4.6)"
  active: true
  joined_at: 2026-04-14T09:00:00Z
  roles:
    - ROLE-senior-architect
  expertise:
    - software-architecture
    - system-design
    - complex-bug-diagnosis
  preferences:
    model: claude-opus-4-6
    model_tier: opus
    clone_policy:
      default_clones: 1
      max_clones_without_approval: 2
      notes: "Rarely parallelised; two Opus architects only for genuinely independent designs."
---
