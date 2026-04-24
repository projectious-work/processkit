---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260424_0037-SharpBrook-mcp-servers-cache-schemas
  created: '2026-04-24T00:37:53+00:00'
spec:
  title: MCP servers cache schemas at startup — build hot-reload or reload_schemas
    tool
  state: backlog
  type: story
  priority: medium
  assignee: TEAMMEMBER-cora
  description: '**Observed pattern (v0.19.2 retro):** every schema edit under `context/schemas/`
    or PEP 723 dep edit under `context/skills/**/mcp/server.py` requires a full harness
    restart to take effect. This cost a restart each for SteadyCedar (pyyaml dep)
    and BraveDove (5-schema alternation widening) in the v0.19.2 cycle, stacking restart
    risk and lengthening the feedback loop from &lt;10 s (offline test) to minutes
    (harness cycle).


    **Proposed approaches:**

    - Watchdog-based hot-reload on schema file changes.

    - A `reload_schemas` MCP tool that any admin session can call.

    - PEP 723 dep re-resolve via env-recompute when the server sees a dep-set delta.


    **Done criteria:**

    - At least one of the above ships and a schema edit becomes observable live in
    ≤30s without a harness restart.

    - DX impact measured (a single-fix restart count drops to 0 for schema-only changes).


    **Target:** v0.20.0. **Owner:** cora.'
---
