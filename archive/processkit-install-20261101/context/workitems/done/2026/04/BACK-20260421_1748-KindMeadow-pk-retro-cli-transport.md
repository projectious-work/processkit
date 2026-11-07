---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260421_1748-KindMeadow-pk-retro-cli-transport
  created: '2026-04-21T17:48:39+00:00'
  updated: '2026-04-21T20:17:23+00:00'
spec:
  title: pk-retro CLI transport gap — --auto-workitems fails without injected MCP
    callables
  state: done
  type: bug
  priority: medium
  description: |
    pk_retro.py was built with `mcp_overrides` injection for unit tests but has no production transport to the running MCP servers. Running `pk_retro.py --release v0.18.2 --auto-workitems` emits "WARNING: create_artifact not available" and returns exit 1 because `mcp` dict is empty at runtime.

    Workaround used 2026-04-21: LLM session captured --dry-run body, then relayed create_artifact + log_event + create_workitem + action-item log_event through its own MCP session tools.

    Options for the proper fix:
    1. In-process loader — import the MCP server modules (artifact-management, event-log, workitem-management) the same way migration-management does, and wire their server functions into the mcp dict on startup.
    2. Subprocess MCP client — spawn each server as JSON-RPC subprocess.
    3. Declare pk-retro LLM-driven by contract — remove CLI MCP calls entirely; have the slash command prompt the LLM to render via --dry-run and make the MCP calls itself. Update SKILL.md and tests accordingly.

    Recommend option 1 (matches migration-management precedent, keeps tests unchanged, zero protocol overhead).

    Discovered by: dogfood run of /pk-retro --release v0.18.2 --auto-workitems on 2026-04-21.
  started_at: '2026-04-21T20:07:07+00:00'
  completed_at: '2026-04-21T20:17:23+00:00'
---

## Transition note (2026-04-21T20:07:07+00:00)

Dispatching Sonnet worker to implement in-process MCP loader (option 1 from WI description) — mirror migration-management's pattern of importing server modules directly.


## Transition note (2026-04-21T20:17:20+00:00)

In-process MCP loader shipped (option 1): pk_retro.py imports artifact-management, event-log, workitem-management server modules via importlib and wires their FastMCP tool callables into the mcp dict when mcp_overrides is None and --dry-run/--no-mcp is not set. 4 new loader tests added (31/31 pass with mcp[cli]); existing 27 tests unchanged. Drift guard clean.


## Transition note (2026-04-21T20:17:23+00:00)

Code complete + drift clean + tests green. Committing.
