---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-index-management
  name: index-management
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "SQLite-backed index over all entity files in the project. The read-side foundation for every other MCP server."
  category: process
  layer: 0
  provides:
    primitives: []
    mcp_tools: [reindex, query_entities, get_entity, search_entities, query_events, list_errors, stats]
  when_to_use: "Use whenever an agent needs to look up entities by ID, kind, state, or text — instead of grepping the filesystem."
---

# Index Management

## Level 1 — Intro

`index-management` is the **read-side** foundation. It walks the project's
`context/` directory, parses every entity file, and writes a SQLite
database that other tools query. Its peer at Layer 0 is `id-management`
(the write side, which allocates new IDs). Both are foundational to
every entity-creating skill.

## Level 2 — Overview

### What it provides

- **`reindex()`** — rebuild the SQLite index from scratch
- **`query_entities(kind?, state?, limit?)`** — list entities matching filters
- **`get_entity(id)`** — fetch a single entity by ID
- **`search_entities(text, limit?)`** — full-text search across IDs, titles, bodies, specs
- **`query_events(event_type?, subject?, actor?, limit?)`** — query the event log
- **`list_errors()`** — files that failed to parse during the last reindex
- **`stats()`** — counts of entities/events/errors in the index

### When to use

The MCP server runs continuously inside the dev container. Agents call it
whenever they need fast lookup. Other MCP servers (`workitem-management`,
`decision-record`, etc.) call `reindex` after writing a new entity to
keep the index fresh.

### Where the database lives

`<project-root>/context/.aibox/index.sqlite`. Gitignored. Rebuildable
from source files at any time via `reindex()`.

## Level 3 — Full reference

### Database schema

Three tables — see `src/lib/processkit/index.py` for the DDL.

```sql
entities(id, kind, api_version, path, created, updated, title, state, labels_json, spec_json, body)
events(id, timestamp, event_type, actor, subject, subject_kind, summary, details_json, correlation_id, path)
errors(path, message)
```

`spec_json` holds the full `spec` block as JSON for queries we did not
anticipate. `entities` and `events` overlap for LogEntry rows: a LogEntry
appears in both, with the `events` table denormalizing the event-specific
fields for fast filtering.

### Reindex strategy

`reindex()` is **destructive and atomic** — it deletes all rows and
re-inserts. For typical projects this is fast (sub-second). For very
large projects, an incremental update mode lands later (Phase 4+).

### Errors table

Files that fail to parse get a row in the `errors` table instead of
crashing the reindex. `list_errors()` returns all such rows so the agent
can fix them. The errors table is cleared at the start of each reindex.

### Tools that other servers call

`workitem-management`, `decision-record`, `binding-management`, and
`event-log` all call `index_management.upsert_entity` after writing a
new file. This keeps the index in sync without a full reindex on every
mutation. From an MCP-protocol perspective each server has its own
process — they communicate by sharing the same SQLite database file
(WAL mode would be enabled in a future release for concurrent writes).

### Configuration

The index database path is configurable via:

- `aibox.toml` `[context.index] path = "..."` (relative to project root)
- The `PROCESSKIT_INDEX_DB` environment variable
- Default: `context/.aibox/index.sqlite`

### Limitations at v0.3.0

- **Single-writer.** If two MCP servers write at the same time, one will
  observe `database is locked`. The current design assumes one agent at
  a time, which is the typical case for AI-assisted dev sessions.
- **No FTS.** Search uses `LIKE %text%`. SQLite FTS5 integration lands
  in a later release.
- **No incremental indexing.** Every reindex is a full sweep.
