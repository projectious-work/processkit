---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260409_1742-ProudTiger-process-behavioral-norms-encoded
  created: '2026-04-09T17:42:57+00:00'
spec:
  event_type: process.behavioral_norms_encoded
  timestamp: '2026-04-09T17:42:57+00:00'
  summary: Encoded four behavioral norms into skills and AGENTS.md
  actor: ACTOR-claude
  details:
    norms:
    - Commit to actions immediately (deferred entity creation anti-pattern) — AGENTS.md,
      src/scaffolding/AGENTS.md, agent-management Anti-patterns
    - Encode corrections immediately (mid-session observe+encode workflow) — agent-management
      Overview
    - Session-handover behavioral retrospective step — session-handover skill
    - Upstream contribution convention — AGENTS.md, src/scaffolding/AGENTS.md, CONTRIBUTING.md
    trigger: User caught deferred workitem creation during backlog review
---
