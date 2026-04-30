# note-management MCP server

Capture Notes and operate the v2 Hook inbox convention.

## Tools

| Tool | Purpose |
|---|---|
| `create_note(title, body, type?, tags?, source?)` | Capture a Note entity |
| `capture_inbox_item(title, body, source?, tags?)` | Capture a Hook-inbox fleeting Note and place a receipt under `tasks/inbox/` |
| `claim_inbox_item(id, actor?)` | Mark a captured inbox Note as claimed |
| `complete_inbox_item(id, result?)` | Mark a claimed inbox Note as done |
| `fail_inbox_item(id, reason)` | Mark a claimed inbox Note as failed |
| `reload_schemas()` | Clear in-process schema + state-machine caches |

## Running

```bash
uv run context/skills/processkit/note-management/mcp/server.py
```
