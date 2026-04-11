# AGENTS.md

processkit — versioned library of process primitives, skills, and MCP
servers. Provider-neutral; consumed by aibox. Dogfood repo.

## Session start

Load `context/skills/processkit/skill-gate/SKILL.md` at the start of
any session involving processkit work.

**1% rule:** if there is even a 1% chance a processkit skill covers
this task, call `route_task(task_description)` before acting. It
returns the right skill, any project-specific process override, and
the recommended MCP tool in one call. Fall back to reading skill-gate
SKILL.md if the MCP server is unavailable.

| If you are about to… | Do this first |
|---|---|
| Edit or create any file under `context/` | `route_task()` — returns skill + process override |
| Call `create_*` / `transition_*` / `link_*` / `record_*` / `open_*` | Confirm you are inside a named skill workflow |
| Write a new entity YAML by hand | Use the `create_*` MCP tool instead |
| Act on a domain task without a skill loaded | `route_task()` — 128+ skills + process overrides |

## Setup

```sh
uv run scripts/smoke-test-servers.py   # must be green before any commit
```

## Mandatory MCP servers

| Server | Purpose |
|---|---|
| `index-management` | Entity discovery, query, full-text search |
| `id-management` | ID generation |
| `workitem-management` | Work tracking |
| `discussion-management` | Structured deliberation |
| `decision-record` | Decision capture |
| `event-log` | Audit trail |
| `skill-finder` | Skill catalog navigation (called internally by task-router) |
| `task-router` | Primary routing entry point (`route_task`) — skill + process override + tool |

Tier-specific servers registered by aibox installer. Do not edit the
merged `.mcp.json` by hand.

## Conventions

- **80-col** hard wrap on Markdown, Python, YAML. Exempt: tables, URLs,
  YAML frontmatter, fenced code blocks.
- **Conventional Commits:** `feat:` `fix:` `refactor:` `docs:` `chore:`.
  Never `--no-verify`.
- **src/ vs context/:** `src/` ships to consumers; `context/` is local
  to this repo. Never mix them.
- **Entity writes:** always use MCP tools. Hand edits bypass schema
  validation, state-machine enforcement, and index sync.
- **Commit immediately.** If you decide to create an entity, call the
  tool in the same turn — deferred commits are routinely dropped.

## processkit preferences

IDs: `pascal` word-pair + datetime prefix (`YYYYMMDD_HHMM`) + slug.
Example: `BACK-20260409_1449-BoldVale-fts5-full-text-search`.
Logs sharded: `context/logs/{year}/{month}/`.

## Processes

Project-specific process definitions live in `context/processes/`
(`release.md`, `code-review.md`, `bug-fix.md`, `feature-development.md`).
Read the relevant file before executing any process-category skill —
these override skill defaults for this project. Every `context/`
subdirectory has an `INDEX.md`; read it before loading individual files.

Other agents may be working here — coordinate via workitems and
discussions, not assumptions.

## Critical notes

- **`context/templates/` is read-only** — a verbatim upstream snapshot.
  Edit the live files under `context/skills/`, `context/processes/`,
  etc. Editing the templates mirror loses work on next `aibox sync`.
- **After any hand-edit to an entity file, run `reindex()`** — index
  drifts silently otherwise and `query_entities` returns stale state.
- **Preferences live in two places** — this file AND the per-skill
  `context/skills/*/config/settings.toml`. Update both; MCP servers
  read settings.toml directly and ignore AGENTS.md at runtime.
- **Never edit `.devcontainer/Dockerfile`** — use `.devcontainer/Dockerfile.local`.
- **`apiVersion` is locked** through v1.x — bump to `v2` only with full migration.
- **`_find_lib()` uses cwd** — smoke tests call `os.chdir()` before invoking servers.

---
<sub>processkit v0.13.0 · 2026-04-11</sub>
