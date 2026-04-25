---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260424_0128-RapidSwan-pk-doctor-server-header
  created: '2026-04-24T01:28:39+00:00'
  updated: '2026-04-25T18:00:49+00:00'
spec:
  title: pk-doctor server_header_drift check — WARN on stale PEP 723 dep headers (supersedes
    SharpBrook, deferred)
  state: done
  type: task
  priority: low
  assignee: TEAMMEMBER-cora
  description: "Per DEC-QuickPine (SharpBrook split).\n\n**Scope (deferred — v0.22.0\
    \ or later, NOT v0.21.0):**\n- Add a pk-doctor check `server_header_drift`:\n\
    \  - Walk every `context/skills/processkit/*/mcp/server.py`.\n  - Hash each script's\
    \ PEP 723 header block (`# /// script ... # ///`).\n  - Compare against a manifest\
    \ (reuse `.processkit-mcp-manifest.json` or add a sibling).\n  - WARN with a \"\
    restart the harness to pick up dep changes in: &lt;list&gt;\" hint.\n- Detect-only.\
    \ No auto-fix (the fix is always a full harness restart, which is user-initiated).\n\
    \n**Why deferred:**\nThe schema-reload WI captures the majority of retro pain.\
    \ Dep-drift is the less common half. Shipping both in v0.21.0 bloats the release.\n\
    \n**Done when:**\n- `pk-doctor --category=server_header_drift` runs and correctly\
    \ flags an edited PEP 723 header vs. the manifest baseline.\n- The check is listed\
    \ in pk-doctor's README under Phase 1 checks.\n- Manifest regeneration happens\
    \ in `scripts/generate-mcp-manifest.py` (extend it or add a sibling).\n\nEstimate:\
    \ ~2 hours. Target: v0.22.0+. Supersedes BACK-20260424_0037-SharpBrook-mcp-servers-cache-schemas\
    \ (dep-drift half)."
  related_decisions:
  - DEC-20260424_0127-QuickPine-split-sharpbrook-ship-schema
  started_at: '2026-04-25T18:00:39+00:00'
  completed_at: '2026-04-25T18:00:49+00:00'
---
