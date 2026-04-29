---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260429_1605-StoutMaple-semantic-context-search-with
  created: '2026-04-29T16:05:50+00:00'
  labels:
    component: index
    area: src
    technology: sqlite-vec
    phase: '2'
spec:
  title: Semantic context search with sqlite-vec
  state: backlog
  type: story
  priority: medium
  description: Add optional semantic and hybrid context retrieval using sqlite-vec
    after FTS5 search is in place. Scope includes provider-neutral embedding policy,
    chunking, vector cache schema, sqlite-vec loading, hybrid ranking, tests, docs,
    and privacy/governance notes.
---
