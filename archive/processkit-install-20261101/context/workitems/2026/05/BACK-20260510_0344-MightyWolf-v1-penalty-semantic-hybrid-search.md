---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260510_0344-MightyWolf-v1-penalty-semantic-hybrid-search
  created: '2026-05-10T03:44:22+00:00'
  labels:
    github_issue: 21
    cluster: v1-drift
    follow-up-of: WarmOak
  updated: '2026-05-10T03:47:27+00:00'
spec:
  title: 'WarmOak follow-up: extend v1-entity penalty to semantic_search and hybrid_search'
  state: in-progress
  type: task
  priority: medium
  description: Deferral from BACK-WarmOak (gh#21). v1-entity multiplicative penalty
    applied to query_entities, get_entity, search_entities. Extend the same penalty
    + re-rank to semantic_search_entities and hybrid_search_entities in index-management/mcp/server.py.
    Mirror to src/context/.
  started_at: '2026-05-10T03:47:27+00:00'
---

## Transition note (2026-05-10T03:47:27+00:00)

Starting implementation: extend v1-entity multiplicative penalty to semantic_search_entities and hybrid_search_entities
