---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260429_1605-StoutMaple-semantic-context-search-with
  created: '2026-04-29T16:05:50+00:00'
  labels:
    component: index
    area: src
    technology: sqlite-vec
    phase: '2'
  updated: '2026-04-29T16:34:37+00:00'
spec:
  title: Semantic context search with sqlite-vec
  state: done
  type: story
  priority: medium
  description: Add optional semantic and hybrid context retrieval using sqlite-vec
    after FTS5 search is in place. Scope includes provider-neutral embedding policy,
    chunking, vector cache schema, sqlite-vec loading, hybrid ranking, tests, docs,
    and privacy/governance notes.
  started_at: '2026-04-29T16:28:14+00:00'
  completed_at: '2026-04-29T16:34:37+00:00'
---

## Transition note (2026-04-29T16:28:14+00:00)

Starting Phase 2 sqlite-vec semantic/hybrid search implementation.


## Transition note (2026-04-29T16:34:31+00:00)

Optional sqlite-vec vector table, semantic status/search, hybrid search fallback, docs, and smoke coverage implemented; sqlite-vec KNN verified with a temporary fixture.


## Transition note (2026-04-29T16:34:37+00:00)

Phase 2 accepted after smoke, drift guard, and sqlite-vec KNN verification passed.
