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

## Status at v0.2.0

**No MCP servers ship yet.** v0.2.0 is the skill migration release.
MCP servers land in **v0.3.0**, starting with five foundation servers:

- `index-management` — SQLite index over all entity files
- `event-log` — `log_event`, `query_events`, `recent_events`
- `workitem-management` — `create_workitem`, `transition_workitem`, `query_workitems`, `link_workitems`
- `decision-record` — `record_decision`, `query_decisions`, `link_decision`
- `binding-management` — `create_binding`, `query_bindings`, `resolve_bindings_for`

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
      "args": ["run", ".claude/skills/<skill-name>/mcp/server.py"]
    }
  }
}
```

`aibox init` (from aibox Phase 4.3) will merge these fragments into the
consuming project's MCP config file.
