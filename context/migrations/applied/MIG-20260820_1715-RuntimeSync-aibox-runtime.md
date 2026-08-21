---
apiVersion: processkit.projectious.work/v1
kind: Migration
metadata:
  id: MIG-20260820_1715-RuntimeSync-aibox-runtime
  created: 2026-08-20 17:15:12+00:00
  updated: '2026-08-20T18:23:18+00:00'
spec:
  source: aibox-runtime-home
  source_url: aibox://runtime-home
  from_version: 0.34.0
  to_version: 0.34.1
  state: applied
  generated_by: aibox apply
  generated_at: 2026-08-20 17:15:12+00:00
  summary: 0 changed upstream, 0 conflicts, 3 new, 0 removed (1 groups affected)
  affected_groups:
  - runtime-misc
  affected_files:
  - path: .codex/themes/aibox.tmTheme
    classification: new-upstream
  - path: .config/bat/themes/aibox.tmTheme
    classification: new-upstream
  - path: .config/opencode/themes/aibox.json
    classification: new-upstream
  started_at: '2026-08-20T18:23:18+00:00'
  applied_at: '2026-08-20T18:23:18+00:00'
  progress_notes:
  - timestamp: '2026-08-20T18:23:18+00:00'
    actor: mcp
    note: 'Applied during pk-reconcile: runtime-home 0.34.0 to 0.34.1; three new theme
      files, no conflicts or removals.'
---

# Migration MIG-20260820_1715-RuntimeSync-aibox-runtime

Managed `.aibox-home/` runtime changes from `0.34.0` to `0.34.1`.

0 changed upstream, 0 conflicts, 3 new, 0 removed (1 groups affected)

## Counts

- unchanged: 43
- changed-locally-only: 0
- changed-upstream-only: 0
- conflict: 0
- new-upstream: 3
- removed-upstream: 0

- removed-upstream-stale: 0

## Changes by group

### runtime-misc

**new-upstream**

- `.aibox-home/.config/bat/themes/aibox.tmTheme` -> `.aibox-home/.config/bat/themes/aibox.tmTheme`
- `.aibox-home/.config/opencode/themes/aibox.json` -> `.aibox-home/.config/opencode/themes/aibox.json`
- `.aibox-home/.codex/themes/aibox.tmTheme` -> `.aibox-home/.codex/themes/aibox.tmTheme`
