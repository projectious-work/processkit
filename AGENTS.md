# AGENTS.md

processkit — versioned library of process primitives, skills, and MCP
servers. Provider-neutral; consumed by aibox. Dogfood repo.

## Session start

Load `context/skills/processkit/skill-gate/SKILL.md` at the start of
any session involving processkit work.

**1% rule:** if there is even a 1% chance a processkit skill covers
this task, call `find_skill(task_description)` before acting. Fall
back to reading skill-finder SKILL.md if the MCP server is unavailable.

| If you are about to… | Do this first |
|---|---|
| Edit or create any file under `context/` | `find_skill()` or read skill-finder |
| Call `create_*` / `transition_*` / `link_*` / `record_*` / `open_*` | Confirm you are inside a named skill workflow |
| Write a new entity YAML by hand | Use the `create_*` MCP tool instead |
| Act on a domain task without a skill loaded | Check skill-finder — 128+ skills in catalog |

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
| `skill-finder` | Skill catalog navigation (`find_skill`, `list_skills`) |

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

## Critical notes

- **Never edit `.devcontainer/Dockerfile`** — use `.devcontainer/Dockerfile.local`.
- **`apiVersion` is locked** through v1.x — bump to `v2` only with full migration.
- **`_find_lib()` uses cwd** — smoke tests call `os.chdir()` before invoking servers.

---
<sub>processkit v0.11.1 · 2026-04-11</sub>
