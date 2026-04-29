---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260429_1605-KindThorn-implement-index-search-in
  created: '2026-04-29T16:05:50+00:00'
spec:
  title: 'Implement index search in two phases: FTS5 first, sqlite-vec second'
  state: accepted
  decision: 'Proceed with a two-phase implementation: first replace LIKE-based index
    search with SQLite FTS5 while preserving the existing MCP API, then add optional
    sqlite-vec semantic/hybrid retrieval as a separate follow-up capability.'
  context: The accepted implementation plan prioritizes a low-risk FTS5 upgrade already
    represented by backlog item BACK-20260409_1449-BoldVale-fts5-full-text-search,
    then introduces semantic search only after keyword search is stable.
  rationale: FTS5 is built into the local SQLite build and requires no new dependency.
    sqlite-vec provides semantic retrieval benefits but introduces embedding policy,
    dependency packaging, privacy, chunking, cache invalidation, and evaluation work.
  consequences: Phase 1 can ship as a contained index-management improvement. Phase
    2 requires a new linked work item and should not block FTS5 delivery.
  related_workitems:
  - BACK-20260409_1449-BoldVale-fts5-full-text-search
  decided_at: '2026-04-29T16:05:50+00:00'
---
