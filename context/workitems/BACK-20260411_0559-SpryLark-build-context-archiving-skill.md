---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260411_0559-SpryLark-build-context-archiving-skill
  created: '2026-04-11T05:59:35+00:00'
  labels:
    component: skills
    area: context
    related_decision: DEC-20260411_0559-RapidFjord-three-tier-hot-warm
  updated: '2026-04-30T12:39:50+00:00'
spec:
  title: Build context-archiving skill and MCP server — hot/cold tier management
  state: done
  type: story
  priority: medium
  description: 'Implement the cold tier of the three-tier storage architecture (DEC-20260411_0559-RapidFjord).
    The skill must: (1) detect entities and log shards past a configurable age/state
    threshold (e.g. state=done, older than N days); (2) package them into tar.gz archives
    (git-LFS tracked); (3) update the SQLite index storage_location field to point
    to the archive path so metadata remains queryable; (4) support extraction of full
    content for historical queries. The MCP server exposes tools for triggering archiving,
    querying cold-tier metadata, and extracting archived content. Event log archiving
    (JSONL → tar.gz) follows the same pattern: index retains id/timestamp/type/subject
    permanently, payload requires extraction.'
  started_at: '2026-04-30T11:03:42+00:00'
  completed_at: '2026-04-30T12:39:50+00:00'
---

## Transition note (2026-04-30T11:03:42+00:00)

Started context-archiving skill: added read-only skill docs and server code for policy/candidate planning. Destructive archive creation, extraction, and storage_location index updates remain open.


## Transition note (2026-04-30T12:38:53+00:00)

Implemented context-archiving v0.2 write path: dry-run planning, archive creation, manifest indexing, payload extraction, and archived LogEntry event indexing. Validation passed.


## Transition note (2026-04-30T12:39:50+00:00)

Implemented context-archiving v0.2 write path: dry-run planning, archive creation, manifest indexing, payload extraction, and archived LogEntry event indexing. Validation passed.
