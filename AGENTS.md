# AGENTS.md

This file is the canonical, provider-neutral entry point for any AI coding
agent (or human collaborator) working on **processkit**. It follows
the [agents.md](https://agents.md) open standard.

If your harness auto-loads a provider-specific file (`CLAUDE.md`,
`CODEX.md`, `.cursor/rules`, ...), that file should be a thin pointer to
this one. Edit **this** file, not the pointers.

## About this project

processkit is a versioned library of process primitives, skills, and MCP
servers. It is provider-neutral, consumed by aibox, and dogfooded in
this repository.

**Why it exists.** processkit gives aibox and other agent environments a
versioned, provider-neutral layer for skills, processes, schemas, and
MCP servers so teams can share a consistent operating model and improve
it upstream.

## Setup

```sh
# install dependencies and build
npm --prefix docs-site install
npm --prefix docs-site run build

# run tests
uv run scripts/smoke-test-servers.py

# run linter / formatter check
# no repo-wide lint / formatter command is configured yet
# follow .editorconfig plus the 80-column rules in CONTRIBUTING.md
```

## Code style and conventions

- Hard-wrap Markdown prose, Python, and YAML at 80 columns. Exempt:
  tables, URLs, YAML frontmatter, fenced code blocks, and machine-
  generated TOML where readability would get worse.
- Use Conventional Commits: `feat:`, `fix:`, `refactor:`, `docs:`,
  `chore:`. Never use `--no-verify`.
- Keep the repo boundary clear: `src/` ships to consumers; `context/`
  is local to this repo. Never mix them.
- Prefer MCP tools for entity writes. Hand edits bypass schema
  validation, state-machine enforcement, and index sync.
- If you decide to create an entity, do it in the same turn. Deferred
  entity creation is routinely dropped.

## Pull requests

Open a PR for feature and bug-fix changes, link the relevant WorkItem ID
in the PR description and in commit messages, and request at least one
independent review. Use squash merge for PRs. The final squash commit
message should use a Conventional Commit prefix and include the related
WorkItem ID when applicable. Before merge, resolve all blocking comments
and make sure the relevant tests are green.

## processkit preferences

Runtime configuration lives in per-skill config files under
`context/skills/<name>/config/settings.toml`. The agent edits these
directly; MCP servers read them on every call — no restart needed.

- IDs use `format = "word"` with `word_style = "pascal"`,
  `datetime_prefix = true`, and `slug = true`.
- Directory names under `context/` use the default `index-management`
  mappings.
- Log entries are sharded by date under `context/logs/{year}/{month}/`.

---

## How this project is organized: processkit content

This project uses **[processkit](https://github.com/projectious-work/processkit.git)**,
pinned at `v0.13.0`, package tier(s) `product`, to manage process
content (skills, primitives, processes, schemas). All
processkit-installed material lives under `context/`:

```
context/
├── skills/         ← skill packages (SKILL.md, mcp/, references/, templates/)
├── schemas/        ← JSON schemas for the core primitives
├── state-machines/ ← state-machine definitions
├── processes/      ← process definitions (bug-fix, code-review, release, ...)
└── templates/      ← immutable upstream mirror used as a diff baseline
```

`context/templates/processkit/<version>/` is the verbatim upstream
snapshot. **Do not edit it.** Edit the live files at
`context/skills/<name>/SKILL.md`, `context/processes/<name>.md`, etc.,
directly. Local edits are detected at the next sync via three-way diff
against the templates mirror.

Every `context/` subdirectory has an `INDEX.md`. **Read those first** —
do not slurp `context/skills/` or any large directory at session start.
Load specific files only when the task demands it. This is the
three-level principle: start at Level 1 (intro), drop to Level 2
(workflows) when the task narrows, drop to Level 3 (full reference) for
edge cases.

## Working with entities

processkit models project state as **entities** — work items, decision
records, discussions, log entries, scopes, gates, bindings, and so on.
Each entity is a YAML file under `context/<kind>s/`, created lazily on
first use.

For each entity kind, processkit ships:

- **A schema** at `context/schemas/<kind>.yaml`
- **A state machine** at `context/state-machines/<kind>.yaml`
- **An MCP server** at `context/skills/<kind>-management/mcp/server.py`

### Read entities through the index

`context/skills/index-management/` exposes a SQLite-backed index over
every entity in `context/`. Call its tools — `query_entities(kind=...,
state=...)`, `get_entity(id)`, `search_entities(text)` — instead of `ls` /
`grep` / filesystem walks. The index is faster, context-cheaper, and
reflects the canonical state.

### Write entities through the per-kind MCP servers

Use the relevant MCP tool to create or transition entities —
`create_workitem` and `transition_workitem` from `workitem-management`,
`record_decision` from `decision-record`, and so on. Hand-editing entity
files works but bypasses index updates and state-machine validation, so
the index can drift and invalid transitions can slip through. Reserve
hand edits for cases the MCP tools genuinely don't cover.

### Wiring the MCP servers into your harness

Each MCP-bearing skill ships its own `mcp/mcp-config.json` declaring how
to launch the server (typically `uv run .../server.py`). Agent harnesses
(Claude Code, Codex CLI, Cursor, ...) discover MCP servers by reading a
single config file at startup, so the per-skill configs need to be
**merged** into the one file your harness reads, and that file needs to
live at the path your harness expects.

If this project was set up by an installer (e.g. an aibox-managed
devcontainer), the installer is responsible for that wiring — the merged
config is generated for you and you should not need to touch it. If
processkit was installed manually, the project owner is responsible for
merging the per-skill blocks and placing the result at the
harness-specific path themselves.

Either way, MCP-bearing skills require **`uv`** and **Python ≥ 3.10** on
PATH inside the environment where the harness runs the servers — each
`server.py` is a self-contained PEP 723 script and `uv run` resolves its
dependencies on first launch.

## AI agents on this project

Configured providers: **claude, codex**. Other agents may be working
on this project — coordinate through the entity layer
(`workitem-management`, `event-log`, `discussion-management`) rather than
assuming you are alone.

**Commit to actions immediately.** If you decide to create an entity
(WorkItem, DecisionRecord, etc.), call the tool in the same turn. Do
not say "I'll track that" and move on — deferred commitments are
routinely dropped and leave the entity layer out of sync with what was
discussed.

**Check the skill catalog before acting on domain tasks.** When a
domain-specific task arrives — writing a PRD, creating a release,
reviewing a skill, designing a schema — search the processkit skill
catalog first. Use `search_entities` via index-management or check
`skill-finder` before falling back to general knowledge. A matching
skill may exist with processkit-specific conventions (entity storage
paths, workitem linking, output formats) that general knowledge does
not know. Missing a skill wastes work and produces non-standard
output.

### Contributing improvements upstream

When you make a behavioral or content improvement to a file in
`context/` that was installed from processkit (it has a counterpart
in `context/templates/processkit/<version>/`), ask whether the
improvement is general enough to benefit all processkit consumers.

If yes:
1. Open a Discussion entity locally with `open_discussion` —
   title it "Upstream proposal: <short description>", note the
   changed file and the improvement in the body.
   This creates an audit trail so future sessions can see what
   was proposed and what was decided.
2. File an issue at the processkit repository so maintainers can
   consider it for the upstream catalog.

Nothing is mandatory — the project owner decides what to file
upstream. The Discussion entity records the decision either way.

## Team

This project has a permanent AI team of eight roles defined under
`context/roles/`, `context/actors/`, and `context/bindings/`. The
project manager (`ACTOR-pm-claude`, Opus) is the default session agent:
owns every incoming request, routes by kind + complexity, reviews
results, and plays devil's advocate against the owner and the rest of
the team.

Read [`context/team/roster.md`](context/team/roster.md) at session start
for the routing heuristic, clone policy (max 5 parallel per role
without owner sign-off), and budget orientation (Opus ≈5% / Sonnet ≈85%
/ Haiku ≈10%, not a hard limit). The charter lives in
`DEC-20260414_0900-TeamRoster-permanent-ai-team-composition`.

## Project-specific notes

- Load `context/skills/processkit/skill-gate/SKILL.md` at the start of
  any session involving processkit work.
- If there is even a 1% chance a processkit skill covers the task, call
  `route_task(task_description)` before acting. Use it before editing or
  creating files under `context/`, before calling `create_*` /
  `transition_*` / `link_*` / `record_*` / `open_*`, and before acting
  on a domain task without a skill loaded.
- Keep these MCP servers available: `index-management`,
  `id-management`, `workitem-management`, `discussion-management`,
  `decision-record`, `event-log`, `skill-finder`, and `task-router`.
  Do not hand-edit generated harness-specific merged MCP config.
- `context/templates/` is read-only. Edit the live files under
  `context/skills/`, `context/processes/`, etc. instead.
- After any hand-edit to an entity file, run `reindex()` so the SQLite
  index reflects the new state.
- Preferences live in two places: this file and the per-skill
  `context/skills/*/config/settings.toml` files. MCP servers read the
  config files directly at runtime.
- Never edit `.devcontainer/Dockerfile`; use
  `.devcontainer/Dockerfile.local`.
- `apiVersion` is locked through v1.x. Bump to `v2` only with a full
  migration.
- `_find_lib()` uses cwd; the smoke tests call `os.chdir()` before
  invoking servers.

---

<sub>Scaffolded by processkit `v0.13.0` on `2026-04-13`. Re-rendered on each installer sync.</sub>
