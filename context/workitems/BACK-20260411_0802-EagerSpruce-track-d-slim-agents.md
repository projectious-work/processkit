---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260411_0802-EagerSpruce-track-d-slim-agents
  created: '2026-04-11T08:02:25+00:00'
spec:
  title: Track D — Slim AGENTS.md and add explicit skill-guard if/then rules
  state: backlog
  type: task
  priority: medium
  description: 'Reduce AGENTS.md to under 60 lines of core content — push domain-specific
    instructions into the skills that own them. Add explicit if/then skill guards:

    - If editing any file under context/ → check skill-finder first

    - If creating or transitioning a processkit entity → use the relevant MCP server,
    not hand edits


    Research shows root AGENTS.md content under 60 lines significantly improves adherence
    to the instructions that remain.


    Related decision: DEC-RoyalComet'
---
