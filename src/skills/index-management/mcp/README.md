# index-management MCP server

SQLite-backed index over all entity files in the project. Provides
query/search/lookup tools used directly by agents and indirectly by other
processkit MCP servers (which call `upsert_entity` after writing files).

## Tools

| Tool                                                           | Purpose                                          |
|----------------------------------------------------------------|--------------------------------------------------|
| `reindex()`                                                    | Walk `context/`, rebuild the index from scratch  |
| `query_entities(kind?, state?, limit?)`                        | List entities matching filters                   |
| `get_entity(id)`                                               | Fetch one entity by ID                           |
| `search_entities(text, limit?)`                                | Full-text search (LIKE-based at v0.3.0)         |
| `query_events(event_type?, subject?, actor?, limit?)`          | Query the LogEntry events table                  |
| `list_errors()`                                                | Files that failed to parse during last reindex   |
| `stats()`                                                      | Count of entities/events/errors in the index     |

## Database

`<project-root>/context/.aibox/index.sqlite` — gitignored, rebuildable
from source files.

## Running

From a processkit checkout:

```bash
cd /path/to/your/project   # contains aibox.toml and context/
uv run /path/to/processkit/src/skills/index-management/mcp/server.py
```

When installed by aibox into a consumer project (Phase 4.3+):

```bash
uv run .claude/skills/index-management/mcp/server.py
```

Either form first cold-starts uv (~5–10s), then runs the MCP server on
STDIO. Subsequent runs are near-instant due to uv's environment cache.

## Limitations at v0.3.0

- Single-writer (no `WAL` mode yet — agents are sequential)
- Search is `LIKE %text%`, not FTS5
- No incremental indexing — `reindex()` is a full sweep

## Configuration

Override the database path:

```toml
# aibox.toml
[context.index]
path = "context/.aibox/index.sqlite"
```

or via env var:

```bash
PROCESSKIT_INDEX_DB=/tmp/test.sqlite uv run .../server.py
```

(env var support lands in v0.3.1)
