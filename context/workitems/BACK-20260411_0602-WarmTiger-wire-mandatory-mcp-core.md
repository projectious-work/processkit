---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260411_0602-WarmTiger-wire-mandatory-mcp-core
  created: '2026-04-11T06:02:08+00:00'
  labels:
    component: installer
    area: aibox
    affects: mcp-registration
spec:
  title: Wire mandatory MCP core set into aibox installer registration
  state: backlog
  type: task
  priority: medium
  description: 'aibox must register the mandatory processkit MCP core set in the harness
    config at install/sync time. Mandatory servers: index-management, id-management,
    workitem-management, discussion-management, decision-record, event-log. All six
    must be present regardless of package tier. Tier-specific servers (actor-profile,
    role-management, scope-management, gate-management, binding-management, model-recommender)
    are registered based on the installed tier. The canonical list of mandatory servers
    is declared in AGENTS.md under the AI agents section. aibox should read this list
    and validate/generate the merged mcp-config accordingly.'
---
