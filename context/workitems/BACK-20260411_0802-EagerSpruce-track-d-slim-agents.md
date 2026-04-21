---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260411_0802-EagerSpruce-track-d-slim-agents
  created: '2026-04-11T08:02:25+00:00'
  updated: '2026-04-21T07:25:56+00:00'
spec:
  title: Track D — Slim AGENTS.md and add explicit skill-guard if/then rules
  state: done
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
  started_at: '2026-04-21T02:09:19+00:00'
  completed_at: '2026-04-21T07:25:56+00:00'
---

## Transition note (2026-04-21T02:09:19+00:00)

Dispatching worker — slim AGENTS.md to <60 lines + if/then skill guards.


## Transition note (2026-04-21T07:25:51+00:00)

AGENTS.md slimmed 321 → 90 raw / 59 core lines; 8 if/then skill guards; content moved to skill-gate + skill-builder SKILL.md; both trees in sync.


## Transition note (2026-04-21T07:25:56+00:00)

Shipped in commit below.
