---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260423_0829-TrueQuail-aibox-installer-reconcile-mcp
  created: '2026-04-23T08:29:15+00:00'
  updated: '2026-04-23T20:57:59+00:00'
spec:
  title: 'aibox installer: reconcile .mcp.json on per-skill-config drift, not just
    version delta'
  state: review
  type: task
  priority: high
  description: '**Problem.** The aibox installer regenerates `/workspace/.mcp.json`
    only when `processkit.from_version != processkit.to_version`. When new MCP servers
    are added inside a release cycle (e.g. v0.19.0 introduced `processkit-team-manager`
    and `processkit-migration-management`, v0.19.1 did not bump the relevant piece),
    per-skill `mcp-config.json` drift stays invisible to downstream harnesses until
    the *next* version bump. Root-caused during session 2026-04-23 ProudStone; workaround
    was to hand-merge all 18 per-skill `mcp-config.json` files into `.mcp.json`, violating
    the compliance-contract rule "Do not hand-edit the generated harness MCP config
    — edit the per-skill mcp-config.json and let the installer re-merge."\n\n**Desired
    behavior.** Installer detects drift between the hash of all per-skill `mcp-config.json`
    files and the current `.mcp.json` contents, and re-merges when they diverge —
    independent of the processkit version delta.\n\n**Target release.** v0.19.2 (alongside
    BraveDove schema-drift fix).\n\n**Notes.**\n- Drift detection could be a sha256
    of the sorted concatenation of all `context/skills/*/mcp-config.json` files, stored
    in a manifest the installer checks.\n- Must keep the escape hatch that lets the
    compliance-contract rule hold: if installer always re-merges on drift, the "hand
    edit" fallback is no longer needed.\n- Traceability: see LOG-20260423_0818-ProudStone-session-handover
    (open thread #2).'
  started_at: '2026-04-23T20:50:13+00:00'
---

## Transition note (2026-04-23T20:50:13+00:00)

Scope split confirmed by owner (DEC-20260423_2049-VastLake). Processkit ships manifest + pk-doctor check + docs; aibox-side fix tracked at projectious-work/aibox#54. Dispatching implementation.


## Transition note (2026-04-23T20:57:59+00:00)

Processkit-side contributions shipped: (1) scripts/generate-mcp-manifest.py generator; (2) context/.processkit-mcp-manifest.json + src/ mirror; (3) pk-doctor mcp_config_drift check (both trees, registered) — runs clean INFO; (4) AGENTS.md MCP-config-manifest section. Drift guard green. Aibox-side reconcile tracked separately at projectious-work/aibox#54. Keeping this WI in review until aibox PR lands; on merge, transition to done.
