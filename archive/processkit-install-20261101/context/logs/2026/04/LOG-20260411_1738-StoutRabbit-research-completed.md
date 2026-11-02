---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260411_1738-StoutRabbit-research-completed
  created: '2026-04-11T17:38:43+00:00'
spec:
  actor: ACTOR-20260421_0144-AmberDawn-legacy-historical-backfill
  event_type: research.completed
  timestamp: '2026-04-11T17:38:43+00:00'
  summary: 'Deep research completed on MCP routing: MetaMCP, PulseMCP Router, MasRouter
    (ACL 2025), and tool-schema-as-always-available-context trend. Five cross-cutting
    patterns identified. Decision recorded: build processkit-task-router MCP server.'
  subject: DEC-20260411_1738-BraveStream-build-task-router-mcp
  subject_kind: DecisionRecord
  details:
    discussion_id: DISC-20260411_1738-DeepBadger-what-is-the-right
    sources_reviewed:
    - MetaMCP (metatool-ai/metamcp)
    - PulseMCP Router (adamwattis/mcp-proxy-server)
    - MasRouter arxiv:2502.11133 ACL 2025
    - Anthropic Tool Search Tool (defer_loading, BM25)
    - Elastic Path four-layer pattern
    - Google ADK AgentTool
    key_patterns:
    - cascaded-coarse-to-fine
    - groups-as-routing-unit
    - description-carries-routing-weight
    - routing-must-not-call-llm
    - server__tool-prefix
---
