---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260510_0344-NobleIvy-aggregate-mcp-lazy-per-skill-imports
  created: '2026-05-10T03:44:28+00:00'
  labels:
    github_issue: 31
    cluster: runtime
    depends_on_aibox: BACK-20260510_0325-DaringAsh
  updated: '2026-05-10T03:54:04+00:00'
spec:
  title: 'aggregate-mcp: lazy per-skill module imports (gh#31)'
  state: review
  type: story
  priority: high
  description: 'Triaged from gh#31. Add lazy_catalog mode to aggregate-mcp server:
    defer per-skill module imports until first tool call referencing that skill; maintain
    fast discovery surface (cached/lightweight metadata scan); surface runtime.import_mode:
    ''lazy'' in list_aggregate_tools. Opt-in via env var or separate entrypoint to
    preserve eager-mode users. Note: BACK-20260502_0857-ThriftyWren (gateway-lazy-catalog-loading-lane)
    is in review and overlaps — first step is to reconcile against that prior work.'
  started_at: '2026-05-10T03:48:10+00:00'
---

## Transition note (2026-05-10T03:48:10+00:00)

Reconciliation: case (c) — ThriftyWren shipped reusable lazy-catalog infra (GatewayRegistry with import_mode='lazy-catalog', catalog read/write, make_lazy_tool) on main and wired it into processkit-gateway/mcp/server.py. The aggregate-mcp server still uses eager pattern via collect_gateway_tools(). gh#31 is specifically about aggregate-mcp surface — extending aggregate-mcp to opt into the existing GatewayRegistry lazy-catalog mode via PROCESSKIT_MCP_LAZY env var. Reusing existing tool-catalog.json under processkit-gateway/mcp/.


## Transition note (2026-05-10T03:54:04+00:00)

Implemented lazy_catalog mode for aggregate-mcp, reusing the GatewayRegistry shipped by ThriftyWren (BACK-20260502_0857). Opt-in via PROCESSKIT_MCP_LAZY=1 or PROCESSKIT_MCP_MODE=lazy_catalog; default remains eager. Catalog source resolves to processkit-gateway/mcp/tool-catalog.json (overridable via PROCESSKIT_MCP_CATALOG_PATH). Public tool surface and collision/dedup naming preserved across both modes. Tests: 8/8 pass (eager unchanged, lazy skips per-skill imports until first call, owning-skill-only import isolation, ListTools surface identical between modes, missing-catalog falls back to eager). Cold-start benchmark: lazy_catalog 1.58x faster (median 268ms vs 422ms wall, -154ms). Decision recorded as DEC-20260510_0348-BoldLynx. Branch feat/gh31-aggregate-mcp-lazy.
