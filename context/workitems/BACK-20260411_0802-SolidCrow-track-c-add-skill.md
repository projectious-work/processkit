---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260411_0802-SolidCrow-track-c-add-skill
  created: '2026-04-11T08:02:21+00:00'
spec:
  title: Track C — Add skill-consultation prompts to all processkit MCP tool descriptions
  state: backlog
  type: task
  priority: medium
  description: 'Every entity-mutating processkit MCP tool description should carry
    an explicit reminder to consult skill-finder before calling it. Tool descriptions
    are embedded in the tool schema and visible to every harness in every turn — this
    is the provider-independent replacement for pre-tool-use hooks.


    Scope: all create_*, transition_*, link_* tools across the 13 MCP servers. Read-only
    tools (get_*, query_*, list_*) do not need the prompt.


    Related decision: DEC-RoyalComet'
---
