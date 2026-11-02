---
apiVersion: processkit.projectious.work/v1
kind: Migration
metadata:
  id: MIG-20260728_1913-RuntimeSync-aibox-runtime
  created: 2026-07-28 19:13:57+00:00
  updated: '2026-07-28T19:39:45+00:00'
spec:
  source: aibox-runtime-home
  source_url: aibox://runtime-home
  from_version: 0.27.5
  to_version: 0.28.17
  state: applied
  generated_by: aibox apply
  generated_at: 2026-07-28 19:13:57+00:00
  summary: 0 changed upstream, 0 conflicts, 0 new, 0 removed (0 groups affected)
  affected_groups: []
  affected_files: []
  started_at: '2026-07-28T19:39:45+00:00'
  applied_at: '2026-07-28T19:39:45+00:00'
  progress_notes:
  - timestamp: '2026-07-28T19:39:45+00:00'
    actor: mcp
    note: 'Verified runtime sync is an intentional no-op: 0 changed, 0 conflicts,
      0 additions, and 0 removals.'
---

# Migration MIG-20260728_1913-RuntimeSync-aibox-runtime

Managed `.aibox-home/` runtime changes from `0.27.5` to `0.28.17`.

0 changed upstream, 0 conflicts, 0 new, 0 removed (0 groups affected)

## Counts

- unchanged: 42
- changed-locally-only: 0
- changed-upstream-only: 0
- conflict: 0
- new-upstream: 0
- removed-upstream: 0

- removed-upstream-stale: 0

## Per-intermediate review

Every released version between `from_version` and `to_version` whose              template snapshot is present on disk is listed below, with the number              of files that changed between consecutive snapshots. Useful for              catching scaffolding changes that were introduced and later reverted              across the span of a multi-version upgrade.

- `0.27.5` → `0.28.2`: 0 file(s) changed of 42
- `0.28.2` → `0.28.9`: 2 file(s) changed of 42
- `0.28.9` → `0.28.14`: 5 file(s) changed of 43

_No user-relevant changes._
