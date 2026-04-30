---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260429_1953-QuietDaisy-measure-processkit-context-consumption
  created: '2026-04-29T19:53:06+00:00'
  labels:
    area: context
    release: next
    source: user-request
spec:
  title: Measure processkit context consumption
  state: backlog
  type: spike
  priority: medium
  description: 'Investigate and implement optional measurability for context consumed
    by processkit itself. Candidate metrics: rendered AGENTS.md bytes/tokens, active
    skill instruction bytes/tokens, MCP tool schema count/serialized size, status
    briefing payload size, and per-harness startup prompt contribution. The implementation
    should be optional, provider-neutral, and should avoid sending project content
    to external tokenizers unless the user opts in.'
---
