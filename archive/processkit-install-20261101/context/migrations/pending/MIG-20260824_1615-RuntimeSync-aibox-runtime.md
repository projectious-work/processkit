---
apiVersion: processkit.projectious.work/v1
kind: Migration
metadata:
  id: MIG-20260824_1615-RuntimeSync-aibox-runtime
  created: 2026-08-24T16:15:43Z
spec:
  source: aibox-runtime-home
  source_url: "aibox://runtime-home"
  from_version: 0.34.1
  to_version: 0.34.7
  state: pending
  generated_by: aibox apply
  generated_at: 2026-08-24T16:15:43Z
  summary: 0 changed upstream, 0 conflicts, 3 new, 0 removed (2 groups affected)
  affected_groups:
    - runtime-misc
    - runtime-yazi
  affected_files:
    - { path: .config/yazi/plugins/preview-options.yazi/main.lua, classification: new-upstream }
    - { path: .local/bin/aibox-codex-notify, classification: new-upstream }
    - { path: .local/bin/aibox-size-tree, classification: new-upstream }
---

# Migration MIG-20260824_1615-RuntimeSync-aibox-runtime

Managed `.aibox-home/` runtime changes from `0.34.1` to `0.34.7`.

0 changed upstream, 0 conflicts, 3 new, 0 removed (2 groups affected)

## Counts

- unchanged: 46
- changed-locally-only: 0
- changed-upstream-only: 0
- conflict: 0
- new-upstream: 3
- removed-upstream: 0

- removed-upstream-stale: 0

## Changes by group

### runtime-misc

**new-upstream**

- `.aibox-home/.local/bin/aibox-size-tree` -> `.aibox-home/.local/bin/aibox-size-tree`
- `.aibox-home/.local/bin/aibox-codex-notify` -> `.aibox-home/.local/bin/aibox-codex-notify`

### runtime-yazi

**new-upstream**

- `.aibox-home/.config/yazi/plugins/preview-options.yazi/main.lua` -> `.aibox-home/.config/yazi/plugins/preview-options.yazi/main.lua`

