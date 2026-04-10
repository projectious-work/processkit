# AGENTS.md

This file is the canonical, provider-neutral entry point for any AI coding
agent (or human collaborator) working on **processkit**. It follows
the [agents.md](https://agents.md) open standard.

If your harness auto-loads a provider-specific file (`CLAUDE.md`,
`CODEX.md`, `.cursor/rules`, …), that file should be a thin pointer to
this one. Edit **this** file, not the pointers.

## About this project

processkit is a versioned library of **process primitives, skills, and
MCP servers** for AI-assisted work environments. It ships:

- **19 process primitives** — WorkItem, DecisionRecord, LogEntry, Actor,
  Role, Scope, Gate, Discussion, Binding, Metric, Migration, and more —
  each with a JSON Schema, a default state machine, and an MCP server.
- **128+ skill packages** — multi-artifact bundles (SKILL.md + examples
  + templates + optional MCP server) covering process orchestration,
  software engineering, data science, product, design, and more.
  Organised into five installable package tiers: `minimal`, `managed`,
  `software`, `research`, `product`.
- **Process templates** — code-review, bug-fix, feature-development,
  release — as formal `kind: Process` entities.
- **A shared Python library** (`src/lib/processkit/`) used by all MCP
  servers for entity I/O, schema validation, state-machine enforcement,
  and SQLite indexing.

processkit is itself developed using
[aibox](https://github.com/projectious-work/aibox) — its devcontainer is
generated and managed by aibox (dogfooding). aibox is a companion project
that provides containerised AI development environments and consumes
processkit as its content layer, installing selected package tiers into
consumer projects. The two sides coordinate via semver version pinning.

**Why it exists.** processkit is the lowest common denominator for
building process infrastructure in any AI-assisted environment. It is not
tied to any specific methodology, tool, or platform: its primitives
compose into agile workflows, waterfall projects, research pipelines,
non-software business processes, or anything in between. A team can use
processkit to replace a task tracker (Jira), a knowledge base (Notion,
Obsidian), or a lightweight BPM tool — or to build all three from a
single, forkable source of truth.

The library is deliberately forkable: organisations can maintain a
private fork with custom skills and primitives, and that fork remains
consumable by any downstream tool (such as aibox) without changes to the
consumer. processkit also aims to be a curated, trusted catalog of
refined skills and MCP servers — providing as complete a foundation as is
practical, so teams spend time on their domain rather than rebuilding
common tooling.

## Setup

```sh
# No compilation step — content repo.
# MCP servers are self-contained PEP 723 scripts; uv resolves deps on
# first run.
uv run scripts/smoke-test-servers.py --help   # verify uv + Python ≥ 3.10

# Run tests
uv run scripts/smoke-test-servers.py

# Lint (structural validation only — no automated prose-width tool yet)
# aibox lint                     # checks apiVersion / kind / metadata.id
# 80-column prose wrap is author-enforced (see .editorconfig)
```

## Code style and conventions

- **80-column hard wrap** on Markdown prose, Python, and YAML.
  Exemptions: table rows, fenced code blocks, URLs, YAML frontmatter,
  TOML.
- **YAML:** 2-space indent, no tabs; quote strings only when required.
- **Python:** PEP 8, type hints in public APIs,
  `from __future__ import annotations`. Match `src/lib/processkit/`
  style.
- **Skill descriptions:** one-sentence imperative (`"Manage X."`) — not
  narrative.
- **Commit messages:** follow Conventional Commits — `feat:`, `fix:`,
  `refactor:`, `docs:`, `test:`, `chore:`, `ci:`. See the `git-workflow`
  skill for the full convention. Never use `--no-verify`.
- **Rule — `src/` vs everything else:** everything under `src/` is
  shipped to consumers; everything outside is about this repo. Never
  mix them.
- **Rule — two meanings of "skills/processes":** `src/skills/` =
  shipped content; `context/skills/` = skills for the agent working
  *on* this repo. Do not conflate.

## Pull requests

Trunk-based development — `main` is the only long-lived branch; commit
directly to `main` for day-to-day work. Releases are semver git tags
(`v0.x.y`).

**Release checklist:**

1. Add "What changed in vX.Y.Z" entry to the context handover /
   CHANGELOG
2. Update backlog Done section
3. Update docs-site for any user-visible changes
4. `uv run scripts/smoke-test-servers.py` — must be green
5. `scripts/stamp-provenance.sh vX.Y.Z` — regenerates
   `src/PROVENANCE.toml`
6. Commit, then `git tag -a vX.Y.Z -m "..."`
7. `git push origin main && git push origin vX.Y.Z`
8. `scripts/build-release-tarball.sh vX.Y.Z` →
   `gh release upload` the tarball + sha256
9. `cd docs-site && npm run deploy` *(first public deploy is an open
   TODO — do NOT push to `gh-pages` directly)*

---

## How this project is organized: processkit content

> **AGENTS.md scope principle.** Keep this file as complete as necessary
> but as lean as possible. It contains only what an agent needs at session
> start that cannot be derived from the project structure or entities.
> Configuration, preferences, and team descriptions that have their own
> lifecycle belong in entities (Actor, Process, Artifact), not here.

This project uses **[processkit](https://github.com/projectious-work/processkit.git)**,
pinned at `v0.7.0`, package tier(s) `product`, to manage process content
(skills, primitives, processes, schemas). All processkit-installed
material lives under `context/`:

```
context/
├── skills/         ← skill packages (SKILL.md, mcp/, references/, templates/)
├── schemas/        ← JSON schemas for the core primitives
├── state-machines/ ← state-machine definitions
├── processes/      ← process definitions (bug-fix, code-review, release, …)
├── templates/      ← immutable upstream mirror used as a diff baseline
├── artifacts/      ← Artifact entities (documents, runbooks, PRDs, …)
├── decisions/      ← DecisionRecord entities
├── discussions/    ← Discussion entities
├── notes/          ← Note entities (Zettelkasten capture layer)
├── workitems/      ← WorkItem entities
├── logs/           ← LogEntry entities (date-sharded: logs/{year}/{month}/)
├── migrations/     ← Migration entities (applied/, pending/)
├── owner/          ← Owner profile (identity, working-style, goals)
├── actors/         ← Actor entities (humans and AI agents)
└── roles/          ← Role entities
```

Entity directories (`artifacts/`, `workitems/`, etc.) are created lazily
on first use — not all will exist in a fresh install.

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
every entity in `context/`. Call its tools — `query_entities(kind=…,
state=…)`, `get_entity(id)`, `search_entities(text)` — instead of `ls`
/ `grep` / filesystem walks. The index is faster, context-cheaper, and
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
to launch the server (typically `uv run …/server.py`). Agent harnesses
(Claude Code, Codex CLI, Cursor, …) discover MCP servers by reading a
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

Configured providers: **claude**. Other agents may be working on this
project — coordinate through the entity layer (`workitem-management`,
`event-log`, `discussion-management`) rather than assuming you are alone.

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

## processkit preferences

This table is the authoritative view of active project preferences.
The `settings.toml` files under `context/skills/<name>/config/` mirror
these values in TOML form so MCP servers can parse them without reading
AGENTS.md. When changing a preference, update both this table and the
corresponding settings.toml. MCP servers read settings.toml on every
call — no restart needed.

| Preference | Value |
|---|---|
| ID word-pair style | `camel` — e.g. `BoldVale` |
| ID datetime prefix | enabled — format `YYYYMMDD_HHMM` embedded in ID |
| ID slug | enabled — content-derived from entity title |
| Example ID | `BACK-20260409_1449-BoldVale-fts5-full-text-search` |
| Directory layout | processkit defaults (`workitems/`, `logs/`, …) |
| Log sharding | date-based — `context/logs/{year}/{month}/` |

---

## Project-specific notes

- **The lib is NOT a published package.** `src/lib/processkit/` is
  sys.path-injected via `_find_lib()`. Never list it as a PEP 723
  dependency.
- **`paths.find_project_root()` walks up from `cwd`.** Smoke tests call
  `os.chdir(workdir)` before invoking servers. Calling server functions
  directly without setting cwd resolves paths against the wrong project.
- **`lru_cache` on schema/state-machine loaders.** `state_machine.load`
  and `schema.load_schema` cache their results. In tests spanning
  multiple temp projects, call `.cache_clear()` between them.
- **`load_schema` signature is cache-sensitive.** The `schemas_dir`
  parameter must be hashable (a `Path` or `None`). Do not pass a `dict`
  or list.
- **Index freshness.** `index.existing_ids(db, kind)` assumes the index
  is current. After any out-of-band file edits (not via MCP tools), run
  `reindex()`.
- **`index_db_path()` creates directories as a side effect.** Calling it
  just to inspect the path will create `context/.cache/processkit/`.
- **Never edit `.devcontainer/Dockerfile` directly.** It is gitignored
  and regenerated by `aibox sync`. Add custom layers to
  `.devcontainer/Dockerfile.local` instead.
- **`apiVersion` changes are breaking.** `processkit.projectious.work/v1`
  is locked through v1.x. Bumping to `v2` triggers a migration cycle —
  do not bump without committing to the full migration story.

---

<sub>Scaffolded by processkit `v0.7.0` on `2026-04-09`. Re-rendered on each installer sync.</sub>
