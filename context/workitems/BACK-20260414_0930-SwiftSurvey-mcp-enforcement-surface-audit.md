---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260414_0930-SwiftSurvey-mcp-enforcement-surface-audit
  legacy_id: BACK-20260414_0930-SwiftSurvey-mcp-enforcement-surface-audit
  created: '2026-04-14T09:30:00+00:00'
  labels:
    component: processkit-core
    area: enforcement
spec:
  title: Audit — which processkit skills ship MCP servers, which tools exist, what is merged in harness configs
  state: done
  progress_notes: "Audit completed. 15 MCP-bearing skills identified; no merged config found in repo. Artifact: ART-20260414_0935-AuditSurface-mcp-enforcement-surface"
  type: task
  priority: high
  description: >
    Produce a table of every skill under context/skills/processkit/:
    does it ship mcp/server.py? what tools does it expose
    (create_*, transition_*, link_*, record_*, query_*, ...)? is its
    mcp-config.json block merged into any harness config in this repo?
    This audit is evidence input for the Sr Researcher's report.
  assigned_to: ACTOR-assistant
  blocks:
    - BACK-20260414_0930-ReliableReach-processkit-enforcement-research
---
