---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260424_0128-BraveBird-reload-schemas-mcp-tool
  created: '2026-04-24T01:28:31+00:00'
  updated: '2026-04-24T01:29:18+00:00'
spec:
  title: reload_schemas MCP tool + _lib helper on 4 schema-active servers (supersedes
    SharpBrook, v0.21.0)
  state: backlog
  type: story
  priority: medium
  assignee: TEAMMEMBER-cora
  description: 'Per DEC-QuickPine (SharpBrook split).


    **Scope (v0.21.0):**

    - Add `reload_caches()` helper to `_lib/processkit/schema.py` (and `state_machine.py`
    if needed) that invokes `load_schema.cache_clear()` + `load.cache_clear()`.

    - Expose a thin MCP `reload_schemas` tool on each of the 4 schema-active servers:
    workitem-management, decision-record, event-log, artifact-management. Each tool
    is a ~20-line wrapper that calls the shared helper and returns `{ok, cleared:
    [names]}`.

    - Test: add a small test per server that loads a schema, writes a new field onto
    disk, calls `reload_schemas`, and verifies the new field is now visible without
    restarting the server. Offline (no harness).

    - Document in each server''s SERVER.md and the release CHANGELOG.


    **Non-goals:**

    - Watchdog / auto-reload (rejected per DEC-QuickPine).

    - PEP 723 dep reload (tracked separately — see the server_header_drift WI).

    - Covering every schema-using server; the 4 listed cover the measured pain.


    **Done when:**

    - `reload_schemas` tool is callable on the 4 servers.

    - Live test passes for each.

    - `pk-doctor commands_consistency` still green.

    - Drift guard still green (both trees updated).


    Estimate: ~half a day. Target: v0.21.0. Supersedes BACK-20260424_0037-SharpBrook-mcp-servers-cache-schemas
    (schema-reload half).'
  related_decisions:
  - DEC-20260424_0127-QuickPine-split-sharpbrook-ship-schema
---
