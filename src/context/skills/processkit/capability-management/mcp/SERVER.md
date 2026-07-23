# capability-management MCP server

Manage v1 Capability entities through generated schema and state-machine
contracts.

## Tools

| Tool | Purpose |
|---|---|
| `create_capability` | Create a draft Capability |
| `get_capability` | Read one Capability |
| `update_capability` | Update descriptive and relation fields |
| `transition_capability` | Apply a valid lifecycle transition |
| `list_capabilities` | List Capabilities by state |

Every successful write returns index and event status.
