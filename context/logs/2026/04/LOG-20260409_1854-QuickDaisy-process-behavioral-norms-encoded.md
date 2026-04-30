---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260409_1854-QuickDaisy-process-behavioral-norms-encoded
  created: '2026-04-09T18:54:24+00:00'
spec:
  event_type: process.behavioral_norms_encoded
  timestamp: '2026-04-09T18:54:24+00:00'
  summary: Encoded "check skill catalog before domain tasks" norm across AGENTS.md
    and agent-management
  actor: ACTOR-claude
  details:
    files:
    - AGENTS.md
    - src/scaffolding/AGENTS.md
    - src/skills/agent-management/SKILL.md
    - context/skills/agent-management/SKILL.md
    trigger: Agent failed to find prd-writing skill when user said PRD — skill not
      in product package and catalog not consulted
---
