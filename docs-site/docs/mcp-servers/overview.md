---
sidebar_position: 1
title: "Overview"
---

# MCP Servers — Overview

processkit skills ship **Python MCP servers** that give agents
mechanical correctness on top of probabilistic reasoning. For entity
work, agents should use the MCP tools rather than hand-editing files:
write tools validate schemas, enforce state machines, and append
LogEntries where the server owns the side effect.

## Status

**Twenty-five MCP server scripts ship** across processkit's primitive,
workflow, projection, routing, gateway, and guard skills. Most ship
default `mcp-config.json` fragments. `aggregate-mcp` remains an
alternate compatibility entry point and does not register itself by
default; `context-archiving` also ships a server script without a
default config fragment.

Server scripts live under
`context/skills/processkit/<skill>/mcp/server.py` and share a Python
utility library at `context/skills/_lib/processkit/`.

The current direction is gateway first for harnesses that pay startup
cost per stdio process. Per-skill servers remain canonical, but clients
may register one gateway process instead of the granular set when they
want one provider-neutral processkit tool surface.

processkit itself is usable without aibox. aibox is an installer and
supervisor that can fetch processkit content, merge harness config, and
manage a devcontainer. A user may also install the files by another
method and point any MCP-capable harness at the shipped Python server
commands directly.

### Layer 0 — Foundation

| Server | Tools |
|---|---|
| [`index-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/index-management/mcp/) | `reindex`, `query_entities`, `get_entity`, `search_entities`, `query_events`, `list_errors`, `stats` |
| [`id-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/id-management/mcp/) | `generate_id`, `validate_id`, `list_used_ids`, `format_info` |
| [`event-log`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/event-log/mcp/) | `log_event`, `query_events`, `recent_events` |

### Layer 1 — Identity

| Server | Tools |
|---|---|
| [`actor-profile`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/actor-profile/mcp/) | `create_actor`, `get_actor`, `update_actor`, `deactivate_actor`, `list_actors` |
| [`role-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/role-management/mcp/) | `create_role`, `create_role_template`, `get_role`, `update_role`, `list_roles`, `link_role_to_actor` |
| [`team-manager`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/team-manager/mcp/) | TeamMember identity, active interlocutor, consistency, and agent-card helpers |

### Layer 2 — Core entities

| Server | Tools |
|---|---|
| [`workitem-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/workitem-management/mcp/) | `create_workitem`, `create_process_instance`, `create_sep_handoff`, `transition_workitem`, `query_workitems`, `get_workitem`, `link_workitems` |
| [`decision-record`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/decision-record/mcp/) | `record_decision`, `transition_decision`, `query_decisions`, `get_decision`, `supersede_decision`, `link_decision_to_workitem` |
| [`artifact-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/artifact-management/mcp/) | `create_artifact`, `get_artifact`, `query_artifacts`, `update_artifact` |
| [`note-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/note-management/mcp/) | `prepare_hook_inbox_dirs`, `create_note`, `capture_inbox_item`, `claim_inbox_item`, `complete_inbox_item`, `fail_inbox_item` |
| [`scope-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/scope-management/mcp/) | `create_scope`, `get_scope`, `list_scopes`, `transition_scope` |
| [`gate-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/gate-management/mcp/) | `create_gate`, `create_gate_template`, `get_gate`, `list_gates`, `evaluate_gate` |
| [`binding-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/binding-management/mcp/) | `create_binding`, `create_time_window`, `create_budget_application`, `end_binding`, `query_bindings`, `resolve_bindings_for` |
| [`discussion-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/discussion-management/mcp/) | `open_discussion`, `get_discussion`, `list_discussions`, `transition_discussion`, `add_outcome` |
| [`migration-management`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/migration-management/mcp/) | `list_migrations`, `get_migration`, `start_migration`, `apply_migration`, `reject_migration`, `migrate_context_to_v2` |
| [`model-recommender`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/model-recommender/mcp/) | `list_models`, `get_profile`, `query_models`, `compare_models`, `get_pricing`, `check_availability`, `get_config`, `set_config` |

### Layer 3 — Workflow and projections

| Server | Tools |
|---|---|
| [`agent-card`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/agent-card/mcp/) | `project_agent_card` |
| [`eval-gate-authoring`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/eval-gate-authoring/mcp/) | `collect_run_outputs`, `codify_eval`, `calibrate_judge`, `bind_eval_to_runs` |
| [`security-projections`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/security-projections/mcp/) | `project_agent_ids_rule`, `project_tetragon_tracing_policy` |

### Gateway

| Server | Tools |
|---|---|
| [`processkit-gateway`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/processkit-gateway/mcp/) | `list_gateway_tools`, `gateway_health`, plus imported per-skill tools |
| [`aggregate-mcp`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/aggregate-mcp/mcp/) | `list_aggregate_tools` plus imported per-skill tools |

`processkit-gateway` is the provider-neutral gateway entry point. It can
run as a direct stdio server, as a streamable HTTP daemon, or behind a
lightweight stdio proxy for harnesses that only support command-backed
MCP. Eager stdio remains the simplest mode. Daemon mode can use a
catalog-backed lazy registration path so the gateway lists tools without
importing every backing skill server at startup.

`aggregate-mcp` is the legacy one-process compatibility bridge. Both
gateway surfaces keep unique tool names unchanged. If two source servers
expose the same helper name, later duplicates are registered as
`<skill_slug>__<tool_name>`.

### Routing (cross-layer)

| Server | Tools |
|---|---|
| [`skill-finder`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/skill-finder/mcp/) | `find_skill`, `list_skills` |
| [`task-router`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/task-router/mcp/) | `route_task` — returns skill + process override + MCP tool in one call |
| [`skill-gate`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/processkit/skill-gate/mcp/) | `acknowledge_contract`, `check_contract_acknowledged`, `skip_decision_record` |

A standalone smoke test (no MCP transport, just direct function calls)
runs all servers via:

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

Consumers need only Python ≥ 3.10 and `uv` — both already present in
aibox containers. First run pays a small cost for `uv` to resolve and
cache dependencies; subsequent runs are near-instant.

## Transport

Per-skill servers and `aggregate-mcp` use stdio. `processkit-gateway`
supports stdio and streamable HTTP:

```bash
uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  serve --transport stdio

uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  serve --transport streamable-http --host 127.0.0.1 --port 8000 \
  --path /mcp

uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  stdio-proxy --url http://127.0.0.1:8000/mcp
```

The streamable HTTP daemon binds to localhost by default. Do not expose
it on a non-local interface unless a deployment layer adds explicit
authentication and network policy.

## Configuration

Most skills that ship an MCP server include an `mcp/mcp-config.json`
fragment:

```json
{
  "mcpServers": {
    "<skill-name>": {
      "command": "uv",
      "args": ["run", "context/skills/processkit/<skill-name>/mcp/server.py"]
    }
  }
}
```

`aibox init` merges these fragments into the consuming project's MCP
config file. Harnesses that support gateway mode may register
`processkit-gateway` instead of merging the per-skill fragments:

```json
{
  "mcpServers": {
    "processkit-gateway": {
      "command": "uv",
      "args": [
        "run",
        "context/skills/processkit/processkit-gateway/mcp/server.py"
      ],
      "env": {
        "PROCESSKIT_MCP_MODE": "gateway"
      }
    }
  }
}
```

The install path is
`context/skills/processkit/<skill-name>/` — the `processkit/`
category subdirectory is part of the path. Provider-specific harness
files (e.g. `.mcp.json` for Claude Code) are written by aibox at the
right location for whichever harness the user picked.

## Mode matrix

| Mode | Status | Process count | Best fit | Notes |
|---|---|---:|---|---|
| Per-skill MCP servers | Canonical | Many | Fine-grained permissions and maximum compatibility | Each skill owns its server and config fragment. |
| `aggregate-mcp` | Compatibility | One | Existing one-process configs | Legacy bridge; not the preferred new gateway name. |
| `processkit-gateway` stdio | Current gateway | One | Claude Code, Codex, OpenCode, and other command-launching harnesses | Provider-neutral eager stdio server. |
| Daemon plus stdio proxy | Current gateway | One daemon plus lightweight proxies | Harnesses that restart stdio frequently | Requires a supervisor such as aibox or a user-managed daemon process. |

## Which servers are mandatory

For per-skill registration, the following servers should always be
registered regardless of package tier. Without them, agents cannot use
the entity layer correctly:

| Server | Why mandatory |
|---|---|
| `index-management` | Entity discovery and full-text search |
| `id-management` | ID generation for all entity kinds |
| `workitem-management` | Work tracking |
| `discussion-management` | Structured deliberation |
| `decision-record` | Decision capture |
| `event-log` | Audit trail |

The same tools may be reached through `processkit-gateway` or
`aggregate-mcp` when a harness uses a one-process entry point.

Tier-specific servers (`actor-profile`, `role-management`,
`scope-management`, `gate-management`, `binding-management`,
`model-recommender`, and the workflow/projection servers) are registered
based on the installed package tier. `artifact-management` and
`note-management` are available in tiers that include their skills.

## Compliance expectations

Agents should call `route_task(task_description)` before write-side
processkit tool calls and use `find_skill` when a processkit skill might
apply. Entity reads go through `index-management`; entity writes go
through the owning management server. If a state change is not already
logged by the MCP write tool, append a LogEntry with `event-log`.
