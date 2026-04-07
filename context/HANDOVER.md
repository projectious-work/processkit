# Handover Briefing — processkit

**For the next AI agent (or human) taking over processkit development.**

This briefing assumes you are coming in cold and have just opened the
processkit dev container for the first time. Read this end-to-end before
making any changes. It covers what processkit is, the architectural
decisions you must not accidentally undo, how the pieces fit together,
what's done, what's next, and the gotchas that will trip you up.

Last updated: 2026-04-07 (v0.5.1).

## What changed in v0.5.1 (read this section first if you already know v0.5.0)

v0.5.1 is a focused content release: BACK-001 — the three-level
rewrite of all 85 migrated skills.

1. **All 106 skills now follow the canonical three-level format.**
   The 21 process-primitive skills shipped in v0.4.0/v0.5.0 already
   used the format; v0.5.1 brings the remaining 85 migrated skills
   into alignment.
2. **Per-skill changes:** every rewritten skill has
   `metadata.version: 1.1.0` (bumped from 1.0.0), an explicit
   `spec.when_to_use` field, a condensed `spec.description` (drops
   the duplicated "Use when..." clause), and a body restructured into
   `## Level 1 — Intro`, `## Level 2 — Overview` (with `### sub-
   headings`), and `## Level 3 — Full reference` sections. Original
   content is preserved semantically; deeper material is promoted
   into Level 3 either inline or by reference to the existing
   `references/` subdirectory.
3. **80-column hard wrap** applied to all rewritten prose, with the
   smart exemptions documented in v0.5.0 (tables, fenced code blocks,
   URLs, frontmatter, TOML).
4. **Reference exemplar:** `src/skills/python-best-practices/SKILL.md`
   was rewritten first as the canonical reference; subsequent rounds
   used it as the gold-standard structural exemplar.
5. **Execution model:** the rewrite was done by 14 parallel
   general-purpose subagent invocations across 7 rounds (2 agents per
   round), with each round committed separately. The orchestrator
   verified format markers (Level 1/2/3 headers, version 1.1.0,
   when_to_use field) before committing.
6. **No code or schema changes.** v0.5.1 is content-only. The 11 MCP
   servers, 18 primitive schemas, 4 Process entities, and lib code
   are unchanged from v0.5.0. Smoke test still green.

For the v0.5.0 orientation, keep reading.

## What changed in v0.5.0 (read this section first if you already know v0.4.0)

v0.5.0 lands the consumer-side install layout (per the aibox handover
v2) and fills the major content gaps from BACK-002, BACK-003, BACK-004:

1. **Provider-neutral install paths.** Nothing lands under `.claude/`
   anymore. Installed processkit content goes to `context/skills/`,
   `context/skills/_lib/processkit/`, `context/schemas/`,
   `context/state-machines/`, `context/processes/`. The lib's
   `paths.py` was updated and the `_find_lib()` walk in MCP servers
   resolves correctly for both checkout and consumer-install layouts.
2. **Runtime cache moved.** The SQLite index now lives at
   `context/.cache/processkit/index.sqlite` (gitignored). The whole
   `context/.aibox/` directory is gone; the dead override paths in
   `paths.py` were dropped.
3. **Reference-templates model replaces processkit.manifest.** aibox
   copies the upstream cache verbatim to
   `context/templates/processkit/<version>/` and reads SHAs on the fly
   for 3-way diffs. `aibox.lock` at the project root pins source URL,
   version, and resolved commit (Cargo-style). All docs that mentioned
   the manifest were updated.
4. **AGENTS.md as canonical agent entry.** New `AGENTS.md` at the repo
   root holds the authoritative instructions; `CLAUDE.md` is a thin
   pointer. The shipped template lives at `src/scaffolding/AGENTS.md`
   for consumer projects. Per agents.md ecosystem convention.
5. **All 18 primitive schemas shipped (BACK-002).** WorkItem, LogEntry,
   DecisionRecord, Migration were already in. v0.5.0 adds Actor, Role,
   Scope, Gate, Discussion (priority five), then Binding, Category,
   Metric, Schedule, Constraint, Context, Process, StateMachine,
   Artifact. CrossReference is intentionally NOT a file primitive.
6. **All 11 MCP servers shipped (BACK-003).** v0.4.0 had six (Layer 0
   trio + workitem + decision + binding); v0.5.0 adds actor-profile,
   role-management, scope-management, gate-management,
   discussion-management. Each is exercised end-to-end by
   `scripts/smoke-test-servers.py`.
7. **4 Process entities under src/processes/ (BACK-004).** bug-fix,
   code-review, feature-development, release — promoted from the
   legacy aibox process .md files into formal `kind: Process`
   entities with full step lists, role assignments, gates, and
   definition_of_done.
8. **Release-asset tarball convention (DEC-025 / aibox BACK-106).**
   New `scripts/build-release-tarball.sh` produces a reproducible
   `dist/processkit-<version>.tar.gz` plus a sha256 sidecar. Top-level
   entry inside the tarball is `processkit-<version>/`. The release
   process in CONTRIBUTING.md and HANDOVER.md was updated to build +
   upload the asset after tagging. aibox prefers the release asset
   over a git fetch on the happy version-tag path.
9. **WAL mode** in the SQLite index (BACK-007 — done in passing this
   release).
10. **80-column line-width policy** with smart exemptions, encoded in
    `.editorconfig` and documented in `AGENTS.md` and `CONTRIBUTING.md`.
    Existing wide-prose files (the 85 migrated skills, the docs-site
    catalog) will be wrapped as part of BACK-001 / BACK-009.
11. **Two new state machines.** scope (planned → active → completed +
    cancelled) and discussion (active ↔ resolved → archived).
12. **Aibox issues filed:** projectious-work/aibox#33 (AGENTS.md
    scaffolding), projectious-work/aibox#34 (sync perimeter docs).

For the v0.4.0 orientation, keep reading.

## What changed in v0.4.0 (read this section first if you already know v0.3.0)

v0.4.0 grew out of a long design discussion in the aibox repo. Quick orientation:

1. **New 19th primitive: `Migration`.** First-class entity for
   pending/in-progress/applied transitions between upstream versions.
   Has a state machine (`pending → in-progress → applied`, plus
   `rejected`). Schema at `src/primitives/schemas/migration.yaml`.
2. **Three new process-primitive skills (now 21, not 18):**
   - `migration-management` (Layer 3) — workflow for working through
     migration documents.
   - `owner-profiling` (Layer 4) — interview-driven owner profile
     bootstrap. Four templates (identity, working-style, goals-and-context,
     team-and-relationships) plus an interview protocol and an
     observable-signals reference.
   - `context-grooming` (Layer 4) — periodic context cleanup with a
     review-then-act workflow and a default ruleset.
3. **`src/PROVENANCE.toml`** — single file mapping every shipped file
   to its last-changed git tag. Source of truth for the diff script.
   Regenerated at release time by `scripts/stamp-provenance.sh`.
4. **Two scripts in `scripts/`:**
   - `stamp-provenance.sh` — release-time generator for PROVENANCE.toml
   - `processkit-diff.sh` — generic diff between two tags (text/toml/json
     output). Consumed by aibox sync to drive Migration generation.
5. **Privacy tiers** documented in `src/primitives/FORMAT.md`. Three tiers:
   `public`, `project-private` (default), `user-private`. The filesystem
   rule is `context/**/private/` in `.gitignore`. The `owner-profiling`
   skill uses this convention for `team-and-relationships.md`.
6. **Context efficiency** documented in `src/skills/agent-management/SKILL.md`
   (new "Context budget and lazy loading" section) — tells agents to use
   the index MCP server, lazy-load skills, respect `[context.budget]` in
   `aibox.toml`. Paired with the new `context-grooming` skill.
7. **Skill count: 106** (was 103 at v0.3.0). The three new skills are all
   markdown-only (no MCP servers yet).
8. **Reference-templates model (LANDED IN AIBOX, see commit 4c8bde3):**
   `aibox init` copies the upstream cache verbatim to
   `context/templates/processkit/<version>/`. `aibox sync` reads SHAs
   from those reference templates on the fly to do its 3-way diff
   (template vs cache vs live). No `processkit.manifest` file —
   superseded. Pinned source URL + version + resolved commit live in
   `aibox.lock` at the project root (Cargo-style). The runtime cache
   (`~/.cache/aibox/processkit/<v>/`) is reproducible from the
   git-tracked lock + reference templates.
9. **Configurable upstream source URL:** `[processkit] source = "..."`
   in `aibox.toml` accepts any git URL. Companies can fork processkit
   and have their projects consume the fork. PROVENANCE.toml's `[source]`
   block identifies which fork the provenance belongs to.

For the original v0.3.0 orientation, keep reading the sections below.

---

## 1. What processkit is, in two sentences

processkit is the **content layer** for [aibox](https://github.com/projectious-work/aibox) — primitives, skills, process templates, and Python MCP servers that aibox installs into consumer projects. Where aibox provides the containerized runtime, processkit provides everything that runs inside it.

The analogy: `aibox` is to AI work environments as `uv` is to Python environments. **`processkit` is what goes IN the box.**

## 2. The bootstrap loop — read this first

processkit and aibox have a deliberate two-way dependency:

- aibox (from a future version) consumes processkit content via git tags
- processkit is itself developed *using* aibox (its `.devcontainer/` is generated by aibox 0.14.1)

This loop is resolved by **version pinning on both sides**:

- **`aibox.toml` here pins aibox 0.14.1.** That version still ships embedded skills and does NOT yet consume processkit. So today this repo can be developed with aibox tooling without a chicken-and-egg problem.
- **The future aibox version that adds processkit consumption** (Phase 4.2 in DISC-002) will pin a specific processkit tag in its defaults.
- **Neither side follows the other automatically.** Every upgrade is deliberate.

**🚨 DO NOT bump `[aibox] version` in `aibox.toml` here** until BOTH:
- (a) aibox ≥ X has working processkit consumption logic (Phase 4.2+), AND
- (b) processkit has a tag ≥ Y that X knows how to consume.

Coordinate the upgrade with whoever maintains aibox. Until then, stay on aibox 0.14.1 — it works.

## 3. Repository orientation

```
processkit/
├── README.md                  ← what processkit is, the bootstrap loop
├── AGENTS.md                  ← canonical agent entry (provider-neutral); the "two meanings of skills" rule
├── CLAUDE.md                  ← thin pointer to AGENTS.md (Claude Code auto-loads it)
├── CONTRIBUTING.md            ← operating manual (read this second)
├── LICENSE                    ← MIT
├── aibox.toml                 ← pins aibox 0.14.1 (do not edit)
├── .aibox-version             ← 0.14.1 (matches aibox.toml)
├── .gitignore                 ← from aibox init; .devcontainer/{Dockerfile,compose,devcontainer.json} are gitignored
│
├── src/                       ← ████ EVERYTHING IN HERE GETS SHIPPED TO CONSUMERS ████
│   ├── INDEX.md               ← the rule: src/ vs everything else
│   ├── PROVENANCE.toml        ← (v0.4.0+) file → last-changed-tag map (240 entries)
│   │
│   ├── primitives/            ← 19 primitives (was 18 — Migration added in v0.4.0)
│   │   ├── INDEX.md
│   │   ├── FORMAT.md          ← THE entity file format spec (three-level + privacy)
│   │   ├── schemas/
│   │   │   ├── workitem.yaml          ← JSON Schema for WorkItem.spec
│   │   │   ├── logentry.yaml          ← append_only: true
│   │   │   ├── decisionrecord.yaml    ← ADR-style fields
│   │   │   └── migration.yaml         ← v0.4.0 — pending/in-progress/applied
│   │   └── state-machines/
│   │       ├── workitem.yaml          ← backlog → in-progress → review → done
│   │       ├── decisionrecord.yaml    ← proposed → accepted → superseded
│   │       └── migration.yaml         ← v0.4.0 — pending → in-progress → applied + rejected
│   │
│   ├── skills/                ← 106 skill directories (85 migrated + 21 process-primitive)
│   │   ├── INDEX.md           ← layer hierarchy + status
│   │   ├── FORMAT.md          ← skill package format spec (three-level)
│   │   ├── index-management/  ← Layer 0, MCP server (read side)
│   │   ├── id-management/     ← Layer 0, MCP server (write side)
│   │   ├── event-log/         ← Layer 0, MCP server (uses both above)
│   │   ├── actor-profile/     ← Layer 1
│   │   ├── role-management/   ← Layer 1
│   │   ├── workitem-management/    ← Layer 2, MCP server
│   │   ├── decision-record/        ← Layer 2, MCP server
│   │   ├── binding-management/     ← Layer 2, MCP server
│   │   ├── scope-management/       ← Layer 2
│   │   ├── category-management/    ← Layer 2
│   │   ├── cross-reference-management/ ← Layer 2
│   │   ├── process-management/         ← Layer 3
│   │   ├── state-machine-management/   ← Layer 3
│   │   ├── gate-management/            ← Layer 3
│   │   ├── schedule-management/        ← Layer 3
│   │   ├── constraint-management/      ← Layer 3
│   │   ├── migration-management/       ← Layer 3 (v0.4.0)
│   │   ├── discussion-management/      ← Layer 4
│   │   ├── metrics-management/         ← Layer 4
│   │   ├── owner-profiling/            ← Layer 4 (v0.4.0) — interview-driven owner profile
│   │   ├── context-grooming/           ← Layer 4 (v0.4.0) — periodic context cleanup
│   │   └── <85 migrated skills>        ← layer: null (technical/language/etc)
│   │
│   ├── lib/                   ← shared Python library for MCP servers (NOT a skill)
│   │   ├── README.md
│   │   └── processkit/
│   │       ├── __init__.py    ← KIND_PREFIXES, DEFAULT_DIRS, API_VERSION
│   │       ├── entity.py      ← Entity dataclass + load/from_text/new
│   │       ├── frontmatter.py ← YAML frontmatter parse/render
│   │       ├── ids.py         ← generate_id with collision avoidance
│   │       ├── paths.py       ← find_project_root, context_dir, schemas_dir
│   │       ├── schema.py      ← load_schema, validate_spec (jsonschema)
│   │       ├── state_machine.py ← load + validate_transition
│   │       ├── config.py      ← read aibox.toml settings
│   │       └── index.py       ← SQLite indexer + existing_ids helper
│   │
│   ├── processes/             ← INDEX.md only (Phase 4 work — see backlog)
│   ├── scaffolding/           ← project-init templates installed at consumer's project root (AGENTS.md, ...)
│   └── packages/              ← 5 tier definitions
│       ├── INDEX.md
│       ├── minimal.yaml       ← Layer 0 foundations + workitem + hygiene
│       ├── managed.yaml       ← extends minimal + all process-primitive skills + lightweight artifacts
│       ├── software.yaml      ← extends managed + arch/api/db/infra/sec/obs/perf
│       ├── research.yaml      ← extends managed + data/ML/AI
│       └── product.yaml       ← extends software + design/framework/mobile/docs
│
├── docs-site/                 ← Docusaurus 3 site, deploys to gh-pages (manual)
│   ├── README.md
│   ├── package.json           ← @docusaurus/core 3.9.2
│   ├── docusaurus.config.js   ← baseUrl /processkit/
│   ├── sidebars.js
│   ├── src/css/custom.css
│   └── docs/
│       ├── intro.md
│       ├── getting-started/
│       ├── primitives/        ← overview/format/state-machines/relationships
│       ├── skills/            ← overview/format/hierarchy + catalog/ (13 category pages)
│       ├── packages/          ← overview + 5 tier pages
│       ├── processes/overview.md
│       ├── mcp-servers/overview.md
│       └── reference/         ← apiversion-policy, id-formats, migration, privacy (v0.4.0)
│
├── scripts/
│   ├── smoke-test-servers.py  ← end-to-end test for all 6 MCP servers
│   ├── stamp-provenance.sh    ← (v0.4.0) regenerates src/PROVENANCE.toml at release time
│   └── processkit-diff.sh     ← (v0.4.0) generic diff between two tags (text/toml/json)
│
├── context/                   ← THIS REPO's own management artifacts (NOT shipped)
│   ├── BACKLOG.md             ← BACK-001..BACK-014 deferred items
│   ├── HANDOVER.md            ← this file
│   ├── OWNER.md               ← stub — owner to fill in
│   ├── PRD.md                 ← derived from aibox DISC-002
│   ├── PROJECTS.md            ← stub
│   ├── archive/
│   └── processes/             ← internal process notes (bug-fix, code-review, release, feature-development)
│
├── .claude/skills/            ← skills for THIS repo's agent (NOT shipped)
│   ├── agent-management/
│   ├── estimation-planning/
│   ├── fastapi-patterns/
│   ├── pandas-polars/
│   ├── python-best-practices/
│   └── retrospective/
│
└── .devcontainer/             ← generated by aibox 0.14.1
    ├── Dockerfile             ← gitignored, regenerated by `aibox sync`
    ├── docker-compose.yml     ← gitignored
    ├── devcontainer.json      ← gitignored
    ├── Dockerfile.local       ← committed (user overlay, currently empty)
    └── docker-compose.override.yml ← committed (user overlay)
```

## 4. The two non-negotiable rules

These are baked into every other decision. **Memorize them.**

### Rule 1 — `src/` vs everything else

> **Everything under `src/` is shipped to consumers.**
> **Everything outside `src/` is about THIS repo itself.**

If you put repo-internal stuff under `src/`, consumers will get it. If you put shipped content outside `src/`, no one will see it. The two halves never mix.

### Rule 2 — two meanings of "skills" / "processes" in this repo

| Location              | What it is                                              |
|-----------------------|---------------------------------------------------------|
| `src/skills/`         | Multi-artifact skill packages SHIPPED to consumers     |
| `src/processes/`      | Process definitions SHIPPED to consumers                |
| `.claude/skills/`     | Skills for the agent working ON this repo (not shipped)|
| `context/processes/`  | THIS repo's own process notes (not shipped)             |

When AGENTS.md (or its provider-specific pointer like CLAUDE.md) says "the agent should call workitem-management", it means a server in `src/skills/workitem-management/mcp/` that consumers use — NOT something in `.claude/skills/`. Don't conflate these.

## 5. Architectural decisions — the "why"

The full DECISIONS log lives in the **aibox** repo at `context/DECISIONS.md` (DEC-017..DEC-024). The condensed version of what affects you here:

### DEC-017 — aibox scope is dev-environment only
RBAC, governance, certificates, signed commits, workflow execution, deterministic event logging, Docker abstraction — all explicitly out of scope. processkit inherits this scope. Don't reintroduce them.

### DEC-018 — Two-repo split
aibox is infra (CLI + container images). processkit is content (skills + primitives + MCP servers). They communicate via git tags. **You are in the content repo.** If you find yourself wanting to write Rust, you are in the wrong repo.

### DEC-019 — Skills are multi-artifact packages
A skill is a directory: `SKILL.md` (three-level) + `examples/` + `templates/` + optional `mcp/`. Not a single markdown file. Skills declare `uses:` for downward dependencies.

### DEC-020 — MCP servers = official Python SDK + uv PEP 723 inline deps
Each `server.py` is a standalone uv-runnable script. STDIO transport only. No PyPI publishing. Container needs only Python ≥ 3.10 and `uv`, both already present.

### DEC-021 — SQLite index lives in processkit, not aibox
The `index-management` MCP server owns the indexer (`src/lib/processkit/index.py`). aibox CLI only does structural validation (`apiVersion`, `kind`, `metadata.id`).

### DEC-022 — Configurable ID format
Two independent axes in `aibox.toml`: `id_format` (`word`/`uuid`) × `id_slug` (`true`/`false`). The kind prefix (`BACK`, `LOG`, `DEC`, ...) is fixed. See `src/skills/id-management/SKILL.md`.

### DEC-023 — Binding (generalized RoleBinding)
The 18th primitive. Use a Binding when a relationship has scope, time, or its own attributes. Use a frontmatter cross-reference otherwise.

### DEC-024 — Per-kind directory sharding
Configurable in `aibox.toml` `[context.sharding.<kind>]`. Default is flat.

## 6. The Layer 0 split (this is subtle, read carefully)

processkit's skill hierarchy has 5 layers (0–4). Higher layers depend on lower; the rule is strictly downward — **with one documented exception in Layer 0**.

```
Layer 0: index-management, id-management, event-log
           ├ index-management — read side, depends on nothing
           ├ id-management    — write side, uses index-management
           └ event-log        — uses both above (intra-layer edge)

Layer 1: actor-profile, role-management
Layer 2: workitem-management, decision-record, scope-management,
         category-management, cross-reference-management, binding-management
Layer 3: process-management, state-machine-management, gate-management,
         schedule-management, constraint-management
Layer 4: discussion-management, metrics-management
```

**Why the intra-layer edge in Layer 0:** indexing and ID allocation are two halves of the entity-creation problem (read side, write side). They're peers. Putting `event-log` "above" them by bumping its layer would force every other layer up by one. Documenting one intra-layer edge is the smaller cost.

**Every entity-creating skill declares both Layer 0 foundations in `uses:`:**

```yaml
spec:
  uses: [event-log, actor-profile, index-management, id-management]
```

If you add a new entity-creating skill, copy this pattern.

## 7. The MCP server architecture

Six servers ship at v0.3.0. They share `src/lib/processkit/` for everything common.

### Layout per server

```
src/skills/<skill>/mcp/
  server.py          ← uv-runnable, PEP 723 inline deps, STDIO transport
  mcp-config.json    ← fragment merged into consumer's mcp config
  README.md          ← what tools the server provides
```

### server.py boilerplate

Every server starts with the same ~30 lines (verbatim):

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "mcp[cli]>=1.0",
#   "pyyaml>=6.0",
#   "jsonschema>=4.0",
# ]
# ///
"""..."""
from __future__ import annotations
import os, sys
from pathlib import Path

def _find_lib() -> Path:
    env = os.environ.get("PROCESSKIT_LIB_PATH")
    if env:
        return Path(env).resolve()
    here = Path(__file__).resolve().parent
    while True:
        for c in (here / "src" / "lib", here / "_lib"):
            if (c / "processkit" / "__init__.py").is_file():
                return c
        if here.parent == here:
            raise RuntimeError("processkit lib not found")
        here = here.parent

sys.path.insert(0, str(_find_lib()))

from mcp.server.fastmcp import FastMCP  # noqa: E402
from processkit import config, entity, ids, index, paths, schema, state_machine  # noqa: E402

server = FastMCP("processkit-<skill-name>")
```

Then `@server.tool()` decorators register each tool, and `if __name__ == "__main__": server.run(transport="stdio")` at the bottom.

`_find_lib()` walks up from the script looking for `src/lib/processkit/` (checkout layout) or `_lib/processkit/` (aibox-installed layout). The `PROCESSKIT_LIB_PATH` env var overrides for non-standard installs.

### The standard create-entity pattern

Every server that creates a new entity follows this pattern:

```python
root = paths.find_project_root()
cfg = config.load_config(root)
target_dir = paths.context_dir("<Kind>", root)
target_dir.mkdir(parents=True, exist_ok=True)

# Get existing IDs for collision avoidance
db = index.open_db()
try:
    existing = index.existing_ids(db, "<Kind>")
finally:
    db.close()

new_id = ids.generate_id(
    "<Kind>",
    format=cfg.id_format,
    slug_text=title if cfg.id_slug else None,
    existing=existing,
)

spec = {...}
errors = schema.validate_spec("<Kind>", spec)
if errors:
    return {"error": "schema validation failed", "details": errors}

ent = entity.new("<Kind>", new_id, spec)
target = target_dir / f"{new_id}.md"
ent.write(target)

# Update the index in place
db = index.open_db()
try:
    index.upsert_entity(db, ent)
finally:
    db.close()

return {"id": new_id, "path": str(target), ...}
```

This pattern keeps the index fresh after every write, so subsequent `existing_ids()` calls see all known IDs.

### The state-machine transition pattern

```python
ent = _load_entity(root, id)
if ent is None:
    return {"error": f"... {id!r} not found"}
from_state = ent.spec.get("state")
try:
    state_machine.validate_transition("<machine-name>", from_state, to_state)
except state_machine.StateMachineError as e:
    return {"error": str(e)}

ent.spec["state"] = to_state
# auto-stamp lifecycle fields
ent.write()

db = index.open_db()
try:
    index.upsert_entity(db, ent)
finally:
    db.close()

return {"ok": True, "from_state": from_state, "to_state": to_state}
```

`validate_transition` raises `StateMachineError` with an informative message listing the allowed targets. The server catches and returns the message as a structured error.

### Shared lib API summary

| Module | Public API | What it does |
|---|---|---|
| `entity` | `Entity` dataclass, `new(kind, id, spec)`, `load(path)`, `from_text(text)` | Read/write entity files |
| `frontmatter` | `parse(text) → (dict, body)`, `render(dict, body)` | Round-trip YAML frontmatter |
| `ids` | `generate_id(kind, format, slug_text, existing, rng)` | Allocate unique IDs |
| `paths` | `find_project_root()`, `context_dir(kind)`, `primitive_schemas_dir()`, `state_machines_dir()`, `index_db_path()` | Locate things |
| `schema` | `load_schema(kind)`, `validate_spec(kind, spec) → [errors]`, `list_known_kinds()` | JSON Schema validation |
| `state_machine` | `load(name) → StateMachine`, `validate_transition(name, from, to)` | State machine ops |
| `config` | `load_config(root) → Config` | Read aibox.toml |
| `index` | `open_db()`, `reindex(root, db)`, `upsert_entity(db, ent)`, `existing_ids(db, kind)`, `query_entities(db, ...)`, `get_entity(db, id)`, `search_entities(db, text)`, `query_events(db, ...)`, `list_errors(db)` | SQLite indexer |

`KIND_PREFIXES` and `DEFAULT_DIRS` are exported from `processkit.__init__`.

## 8. The smoke test

`scripts/smoke-test-servers.py` is the fastest feedback loop while editing servers or the lib. It imports each server module directly (bypassing the MCP transport — no client needed), creates a temp project, and exercises a realistic workflow:

1. id-management `generate_id` / `validate_id` / `format_info`
2. workitem-management `create_workitem` → `transition_workitem` (good and rejected)
3. event-log `log_event`
4. decision-record `record_decision(state="accepted")`
5. workitem-management `link_workitems`
6. binding-management `create_binding` → `resolve_bindings_for`
7. index-management `reindex` → `query_entities` → `search_entities` → `query_events`

```bash
uv run scripts/smoke-test-servers.py
```

Should print `=== ALL SERVER SMOKE TESTS PASSED ===`. If it doesn't, do not commit.

The 2 errors in `reindex stats` are from the test fixture's seeded `INDEX.md` files (correctly tracked in the errors table without crashing). Real workflows have 0 errors.

## 9. Status — what's done at v0.4.0

| Area | Done | Not done |
|---|---|---|
| Entity format spec | Yes — includes optional `privacy:` field (v0.4.0) | — |
| Primitive schemas | 4 of 19 (WorkItem, LogEntry, DecisionRecord, **Migration**) | 15 missing — BACK-002 |
| State machines | 3 of 19 (workitem, decisionrecord, **migration**) | Schedule, Discussion, Scope all need machines |
| Process-primitive skills | 21 of 21 (added migration-management, owner-profiling, context-grooming in v0.4.0) | — |
| Migrated skills | 85, with mechanically updated frontmatter | Three-level rewrite — BACK-001 |
| MCP servers | 6 (index-, id-, event-log, workitem-, decision-, binding-) | Servers for actor, role, scope, gate, discussion + the v0.4.0 skills — BACK-003 |
| Package tiers | 5 (minimal, managed, software, research, product) | Update minimal/managed to include the 3 new v0.4.0 skills |
| Docs site | All v0.4.0 changes reflected (intro, primitives/overview, reference/migration, reference/privacy) | Per-primitive pages, per-skill pages — BACK-008/009 |
| Smoke test | All 6 servers covered | Real MCP-protocol test — needs aibox Phase 4 |
| Library | 8 modules, 700 LOC, smoke-tested + Migration kind in registry | FTS5 search — BACK-005, WAL mode — BACK-007, incremental reindex — BACK-006 |
| Processes (top level) | INDEX.md only | Migrate aibox process .md files to formal Process shape — BACK-004 |
| **PROVENANCE.toml** | **v0.4.0 — seed file present, scripts/stamp-provenance.sh ready** | Will be properly populated on first proper release; v0.5.0 should be the first hop where the diff script can compare two PROVENANCE.toml versions. |
| **Generic diff script** | **v0.4.0 — scripts/processkit-diff.sh** | — |
| **Privacy tier convention** | **v0.4.0 — documented in FORMAT.md, reference/privacy.md, used by owner-profiling** | aibox lint validation — needs aibox Phase 4.4 |

## 10. Next priorities (read context/BACKLOG.md for the full list)

In rough order of "what would I do next":

1. **BACK-002 — Remaining 15 primitive schemas.** v0.4.0 added Migration's
   schema, so 4 of 19 are done (workitem, logentry, decisionrecord, migration).
   Most management skills can't fully validate their entities until their
   schema exists. Each schema is 50–100 lines of JSON Schema in YAML.
   Pattern is set by `src/primitives/schemas/workitem.yaml` or the v0.4.0
   `migration.yaml`.

2. **BACK-003 — MCP servers for the other process-primitive skills.**
   Especially `actor-profile` (everything else references actors) and
   `scope-management` (scopes are referenced by Bindings). The three new
   v0.4.0 skills (migration-management, owner-profiling, context-grooming)
   also ship markdown-only and would benefit from MCP servers eventually.
   Each server is ~150–250 lines, copy the boilerplate from any existing one.

3. **BACK-001 — Three-level rewrite of 85 migrated skills.** Big batch of
   editing. Can be parallelized by category. The 21 process-primitive skills
   (v0.4.0 count) are the reference style.

4. **BACK-007 — SQLite WAL mode.** Cheap fix, unlocks parallel agents.

5. **BACK-009 — Refresh skill catalog pages in docs-site.** They were copied
   from aibox and still describe the aibox 84-skill set, not the processkit
   106-skill set (v0.4.0 count).

6. **BACK-005 — FTS5 search.** Replace `LIKE %text%` with proper tokenized
   search in `src/lib/processkit/index.py`.

7. **(NEW post-v0.4.0)** — wire `aibox lint` validation for the new
   `privacy:` field once aibox Phase 4.4 lands. The convention is documented
   but not yet enforced by tooling.

8. **(NEW post-v0.4.0)** — proper test for `scripts/processkit-diff.sh`
   end-to-end. Currently the script is verified manually (graceful error
   on missing PROVENANCE.toml at v0.3.0). The first real test happens at
   v0.5.0 when both tags have a stamped PROVENANCE.toml.

For everything else see `context/BACKLOG.md`.

## 11. Coordination with aibox

aibox is the sister repo. processkit's content is consumed by aibox's `aibox init` (once that consumption logic lands in aibox Phase 4). Today the relationship is:

- **aibox imports nothing from processkit yet.** The consumption logic is on aibox's roadmap (DISC-002 §16 Phase 4.2).
- **processkit imports aibox 0.14.1's container scaffolding** (`.devcontainer/`, the aibox CLI for `aibox sync`, etc.).
- **DEC records live in aibox.** When you make a decision that affects processkit, write the DEC entry in aibox's `context/DECISIONS.md` and reference it from processkit's docs.

The aibox repo: https://github.com/projectious-work/aibox
DISC-002 (the master plan): `aibox/context/discussions/DISC-002-aibox-refocus.md`

If something requires aibox-side work (e.g. "aibox needs to install src/lib/processkit/ alongside skills"), open an issue there or update DISC-002's phase plan.

## 12. Critical gotchas

### G1 — `__pycache__` is gitignored, but `dist/` is not

The `.gitignore` from aibox 0.14.1 covers `__pycache__/`, `*.pyc`, etc. But check before committing — if you accidentally generate a `dist/` directory or anything similar, gitignore it before staging.

### G2 — The lib is NOT a published package

Don't try to `pip install processkit-lib`. Don't reference it in PEP 723 deps as `processkit-lib`. It is a sys.path-injected import, full stop. The only way to load it is via `_find_lib()` boilerplate. If you change this, document the change everywhere (CONTRIBUTING.md, src/lib/README.md, every server.py, this file).

### G3 — The smoke test needs `os.chdir(workdir)` to work

`paths.find_project_root()` walks up from cwd. The smoke test sets cwd to the temp project before importing servers. If you run server functions directly without setting cwd, they will resolve paths against the WRONG project. This is by design (the server is supposed to be invoked from inside a project), but it bites in tests.

### G4 — `state_machine.load` and `schema.load_schema` are `lru_cache`-decorated

Both functions cache their results. In tests where you create temp projects, you must call `.cache_clear()` between projects or you'll get stale results. The smoke test does this — copy that pattern.

### G5 — Schemas use unhashable types in caches

`load_schema(kind, schemas_dir=None)` is `lru_cache(maxsize=64)`. The `schemas_dir` parameter has a default of `None`; if you pass a `Path`, that's hashable, but if you pass a `dict` or list, you'll get a TypeError. Don't change the signature without thinking about this.

### G6 — `index.existing_ids(db, kind)` assumes the index is fresh

The index is fresh in normal operation because every server `upsert_entity()`s after each write. If you hand-edit entity files outside the MCP path, the index goes stale and `existing_ids()` may return a partial set, which can cause ID collisions. **Run `reindex()` after any out-of-band file edits.**

### G7 — `index_db_path` creates parent directories as a side effect

`paths.index_db_path()` calls `db_dir.mkdir(parents=True, exist_ok=True)` to ensure the `context/.cache/processkit/` directory exists. If you call it just to "see what the path would be", you'll create directories. To avoid: construct the path manually instead.

### G8 — aibox-sync perimeter

aibox 0.14.1 originally generated several files in this repo when it
was bootstrapped via `aibox init`. Today, the legitimate scope of
`aibox sync` is **exactly** these gitignored devcontainer files:

- `.devcontainer/Dockerfile`
- `.devcontainer/docker-compose.yml`
- `.devcontainer/devcontainer.json`

**No other file in this repo is in scope for `aibox sync`.** AGENTS.md,
CLAUDE.md, README.md, `src/`, `context/`, `scripts/` — none of these
are touched by `aibox sync`. If aibox ever does touch one of them,
that is an aibox-side bug to fix on the aibox side, not a
processkit-side concern. Do not pre-block on "but what if aibox sync
overwrites X" — the answer is "it does not, by definition; if it did,
it's a bug".

If you ever need to regenerate the devcontainer files, run `aibox sync`
(NOT `aibox init`). `aibox init` would overwrite `aibox.toml` and
reset the version pin. **Never run `aibox init` in this repo again.**

### G9 — Don't edit `.devcontainer/Dockerfile` directly

It's gitignored AND auto-regenerated by `aibox sync`. Add custom layers to `.devcontainer/Dockerfile.local` instead (it's appended as the final layer).

### G10 — apiVersion changes are breaking

The current `apiVersion` is `processkit.projectious.work/v1`. Bumping to `v2` triggers a migration cycle. Don't bump it unless you're committing to the migration story.

## 13. Style and conventions

- **Markdown:** GitHub-flavored. Tables wherever they help. Code fences with language tags.
- **YAML:** 2-space indent, no tabs. Quote strings only when necessary.
- **Python:** PEP 8, type hints in public APIs, `from __future__ import annotations`. Match the lib's style.
- **Skill descriptions:** one-sentence imperative ("Manage X.") not narrative ("This skill manages X.").
- **Three-level structure:** Level 1 = 1–3 sentences. Level 2 = key workflows. Level 3 = full reference.
- **No emojis** in shipped content unless explicitly asked.
- **Commit messages:** descriptive, multi-paragraph for non-trivial changes. Use the existing commit history as the style reference (`git log --oneline`).
- **No `--no-verify` on commits.** No bypassing hooks. If you need to bypass for a real reason, ask first.

## 14. Git workflow

- **Branch:** main is the only long-lived branch. Trunk-based development. Tags are releases.
- **Tags:** semver. v0.x.y for pre-1.0. The current cadence:
  - v0.1.0 = foundation (format spec, schemas, state machines)
  - v0.2.0 = skill migration (101 skills, 5 packages, docs-site)
  - v0.3.0 = MCP servers (6 servers, shared lib, smoke test)
  - v0.4.0 = Migration primitive, owner-profiling, context-grooming, PROVENANCE.toml, configurable upstream source, privacy tiers
  - v1.0.0 = first stable release (not yet scheduled)
- **Releasing a new tag:**
  1. Update this file (HANDOVER.md) — add a "What changed in vX.Y.Z" preamble
  2. Update `context/BACKLOG.md` Done section
  3. Update docs-site if user-visible changes shipped
  4. Run `uv run scripts/smoke-test-servers.py`
  5. **Run `scripts/stamp-provenance.sh vX.Y.Z`** (regenerates `src/PROVENANCE.toml`)
  6. Commit, then `git tag -a vX.Y.Z -m "..."`
  7. `git push origin main && git push origin vX.Y.Z`
  8. **Build and upload the release-asset tarball** (DEC-025; aibox's preferred consumption path):
     ```bash
     scripts/build-release-tarball.sh vX.Y.Z
     gh release upload vX.Y.Z \
         dist/processkit-vX.Y.Z.tar.gz \
         dist/processkit-vX.Y.Z.tar.gz.sha256
     ```
  9. Optionally `cd docs-site && npm run deploy` for docs publication

- **DO NOT push to `gh-pages`** directly. Use `npm run deploy` from docs-site.

## 15. Out of scope (don't try to add these)

Per DEC-017 and the DISC-002 non-goals:

- **RBAC enforcement** — Roles describe responsibilities, they do NOT restrict actions
- **Signed commits / verification manifests** — governance concern, not processkit
- **Workflow execution engine** — processkit defines processes, agents/humans execute them
- **Deterministic event logging** — LogEntries are agent-written (probabilistic). No second event source.
- **Container infrastructure** — that's aibox
- **CLI surface** — processkit is consumed, never run as a command
- **REST/gRPC tool interfaces** — MCP-only

If you find yourself wanting any of these, you're probably in the wrong project. Either talk to the aibox team (for governance/infra) or write a separate companion repo.

## 16. Where to find more

| Question | Where |
|---|---|
| What does processkit do? | `README.md` |
| What's the format of an entity file? | `src/primitives/FORMAT.md` |
| What's the format of a skill? | `src/skills/FORMAT.md` |
| How do I add a new skill / primitive / MCP server? | `CONTRIBUTING.md` |
| What's deferred / prioritized? | `context/BACKLOG.md` |
| Why was X decided? | aibox's `context/DECISIONS.md` (DEC-017..DEC-024) |
| What does the docs site look like? | `https://projectious-work.github.io/processkit/` (after first deploy) |
| Where's the master plan? | aibox's `context/discussions/DISC-002-aibox-refocus.md` |
| How does the agent's smoke test work? | `scripts/smoke-test-servers.py` |
| How do I run a server by hand? | `uv run src/skills/<skill>/mcp/server.py` from inside a project |

## 17. Final notes

You are inheriting a small but cohesive codebase. The intentional simplicity is valuable — it took several rounds of design to land here. Resist the urge to add abstraction, configuration knobs, or features that aren't on the backlog. When in doubt:

1. Read the relevant SKILL.md or FORMAT.md
2. Read the relevant DEC entry in aibox
3. Run the smoke test to confirm your mental model matches reality
4. Ask before bumping aibox version pin or apiVersion

Everything in this repo is reachable by reading 4–5 files. Lean into that.

Good luck.
