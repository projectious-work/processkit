---
apiVersion: processkit.projectious.work/v1
kind: Migration
metadata:
  id: MIG-20260820_0729-RuntimeSync-aibox-runtime
  created: 2026-08-20 07:29:53+00:00
  updated: '2026-08-20T07:48:06+00:00'
spec:
  source: aibox-runtime-home
  source_url: aibox://runtime-home
  from_version: 0.27.2
  to_version: 0.34.0
  state: applied
  generated_by: aibox apply
  generated_at: 2026-08-20 07:29:53+00:00
  summary: 0 changed upstream, 0 conflicts, 2 new, 0 removed (2 groups affected)
  affected_groups:
  - runtime-git
  - runtime-misc
  affected_files:
  - path: .config/git/aibox-github.inc
    classification: new-upstream
  - path: .local/bin/aibox-agent-signal
    classification: new-upstream
  started_at: '2026-08-20T07:48:06+00:00'
  applied_at: '2026-08-20T07:48:06+00:00'
  progress_notes:
  - timestamp: '2026-08-20T07:48:06+00:00'
    actor: mcp
    note: Confirmed during project reconciliation; no conflicts and only two new runtime
      files.
---

# Migration MIG-20260820_0729-RuntimeSync-aibox-runtime

Managed `.aibox-home/` runtime changes from `0.27.2` to `0.34.0`.

0 changed upstream, 0 conflicts, 2 new, 0 removed (2 groups affected)

## Counts

- unchanged: 41
- changed-locally-only: 0
- changed-upstream-only: 0
- conflict: 0
- new-upstream: 2
- removed-upstream: 0

- removed-upstream-stale: 0

## Per-intermediate review

Every released version between `from_version` and `to_version` whose              template snapshot is present on disk is listed below, with the number              of files that changed between consecutive snapshots. Useful for              catching scaffolding changes that were introduced and later reverted              across the span of a multi-version upgrade.

- `0.27.2` → `0.27.5`: 2 file(s) changed of 42
- `0.27.5` → `0.28.2`: 0 file(s) changed of 42
- `0.28.2` → `0.28.9`: 2 file(s) changed of 42
- `0.28.9` → `0.28.14`: 5 file(s) changed of 43
- `0.28.14` → `0.28.17`: 6 file(s) changed of 43
- `0.28.17` → `0.28.19`: 5 file(s) changed of 43
- `0.28.19` → `0.29.0`: 1 file(s) changed of 43
- `0.29.0` → `0.31.0`: 0 file(s) changed of 43

## Changes by group

### runtime-git

**new-upstream**

- `.aibox-home/.config/git/aibox-github.inc` -> `.aibox-home/.config/git/aibox-github.inc`

### runtime-misc

**new-upstream**

- `.aibox-home/.local/bin/aibox-agent-signal` -> `.aibox-home/.local/bin/aibox-agent-signal`
