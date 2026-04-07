---
sidebar_position: 1
title: "Overview"
---

# MCP Servers — Overview

processkit skills ship optional **Python MCP servers** that give agents
mechanical correctness on top of probabilistic reasoning. An agent can
either edit entity files directly (following the SKILL.md instructions)
or call an MCP tool (which validates against the schema and state machine).
Both are first-class; MCP is not required.

## Status at v0.3.0

**Six MCP servers ship.** They live under `src/skills/<skill>/mcp/` and
share a small Python utility library at `src/lib/processkit/`.

| Server                                                                                                          | Layer | Tools                                                                                          |
|-----------------------------------------------------------------------------------------------------------------|-------|------------------------------------------------------------------------------------------------|
| [`index-management`](https://github.com/projectious-work/processkit/blob/main/src/skills/index-management/mcp/) | 0     | `reindex`, `query_entities`, `get_entity`, `search_entities`, `query_events`, `list_errors`, `stats` |
| [`id-management`](https://github.com/projectious-work/processkit/blob/main/src/skills/id-management/mcp/)       | 0     | `generate_id`, `validate_id`, `list_used_ids`, `format_info`                                   |
| [`event-log`](https://github.com/projectious-work/processkit/blob/main/src/skills/event-log/mcp/)               | 0     | `log_event`, `query_events`, `recent_events`                                                   |
| [`workitem-management`](https://github.com/projectious-work/processkit/blob/main/src/skills/workitem-management/mcp/) | 2 | `create_workitem`, `transition_workitem`, `query_workitems`, `get_workitem`, `link_workitems` |
| [`decision-record`](https://github.com/projectious-work/processkit/blob/main/src/skills/decision-record/mcp/)   | 2     | `record_decision`, `transition_decision`, `query_decisions`, `get_decision`, `supersede_decision`, `link_decision_to_workitem` |
| [`binding-management`](https://github.com/projectious-work/processkit/blob/main/src/skills/binding-management/mcp/) | 2 | `create_binding`, `end_binding`, `query_bindings`, `resolve_bindings_for`                   |

A standalone smoke test (no MCP transport, just direct function calls)
runs all five via:

```bash
uv run scripts/smoke-test-servers.py
```

## Runtime requirements

Each MCP server is a standalone Python script using PEP 723 inline
dependency metadata:

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp[cli]>=1.0"]
# ///
from mcp.server.fastmcp import FastMCP
server = FastMCP("<skill-name>")
...
if __name__ == "__main__":
    server.run(transport="stdio")
```

Consumers need only Python ≥ 3.10 and `uv` — both already present in aibox
containers. First run pays a small cost for `uv` to resolve and cache
dependencies; subsequent runs are near-instant.

## Transport

STDIO only. No HTTP, no SSE. STDIO is the most interoperable MCP transport
and works with every major AI provider.

## Configuration

Each skill that ships an MCP server includes an `mcp/mcp-config.json`
fragment:

```json
{
  "mcpServers": {
    "<skill-name>": {
      "command": "uv",
      "args": ["run", "context/skills/<skill-name>/mcp/server.py"]
    }
  }
}
```

`aibox init` merges these fragments into the consuming project's MCP
config file. The install path is provider-neutral
(`context/skills/<skill-name>/`) — provider-specific harness files
(e.g. `.mcp.json` for Claude Code) are written by aibox at the right
location for whichever harness the user picked.
