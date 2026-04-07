# Backlog — processkit

Tracked deferred work, in priority order. Once the workitem-management
MCP server is in regular use here, this list should migrate to actual
WorkItem files under `context/workitems/`.

## High priority

### BACK-001 — Three-level rewrite of 85 migrated skills — **DONE in v0.5.1**
All 85 migrated skills now follow the canonical three-level format
(plus the python-best-practices exemplar). Each has metadata.version
1.1.0, explicit spec.when_to_use, condensed description, and
Level 1/2/3 body sections. Done in 14 parallel subagent invocations
across 7 rounds. See the v0.5.1 Done section for details.

### BACK-002 — Remaining 14 primitive schemas — **DONE in v0.5.0**
All 18 primitive schemas now ship under `src/primitives/schemas/`.
CrossReference remains intentionally not a file primitive. See the
v0.5.0 Done section for the list.

### BACK-003 — MCP servers for the remaining process primitives — **DONE in v0.5.0**
All 5 missing servers shipped: actor-profile, role-management,
scope-management, gate-management, discussion-management. processkit
now ships 11 MCP servers total. Smoke test exercises all of them
end-to-end.

### BACK-004 — Process templates as first-class Process entities — **DONE in v0.5.0**
All four legacy aibox process .md files (bug-fix, code-review,
feature-development, release) promoted to `kind: Process` entities
under `src/processes/`. Each validates against process.yaml.

## Medium priority

### BACK-005 — FTS5 search in the index
The current `search_entities` uses `LIKE %text%`. Switch to SQLite
FTS5 for proper tokenization and ranking. Schema migration needed.

### BACK-006 — Incremental indexing
`reindex` is currently a full sweep. Add an incremental mode that
diffs the filesystem against the index and updates only changed rows.
Useful for projects with thousands of entities.

### BACK-007 — WAL mode for concurrent MCP servers — **DONE in v0.5.0**
SQLite WAL mode enabled in `src/lib/processkit/index.py` `open_db()`.
Multiple readers + single writer no longer hit `database is locked`.

### BACK-008 — Per-primitive docs-site pages
Currently the docs-site has one `primitives/overview.md` listing all
19 primitives. Add a page per primitive: `primitives/workitem.md`,
`primitives/decisionrecord.md`, `primitives/migration.md`, etc. Could
be auto-generated from the schema files.

### BACK-009 — Per-skill docs-site pages or auto-generated catalog
Currently `skills/catalog/` has 13 category pages migrated from aibox.
Update them to reflect processkit-specific naming and the 21 new
process-primitive skills (including migration-management,
owner-profiling, and context-grooming added in v0.4.0). Or auto-generate
from `src/skills/*/SKILL.md` frontmatter.

### BACK-010 — `aibox process install <git-url>` consumer flow
This depends on aibox Phase 4.6, but processkit needs to publish a
`package.yaml` standard for community packages. Document the format
in `docs-site/docs/reference/community-packages.md`.

## Low priority / nice-to-have

### BACK-011 — Provider-independence audit for `.claude/skills/`
The aibox-scaffolded `.claude/skills/` directory is Claude-specific by
naming convention, but the SKILL.md format (with `name`/`description`
frontmatter) is used by other providers too. Investigate whether a
provider-neutral path is feasible (e.g. `.skills/` or `agent/skills/`)
and what each provider requires. **Deferred per user — review this
after the migration work for processkit.**

**Sibling work (already done):** the agent entry file has been split
into provider-neutral `AGENTS.md` (canonical) plus thin `CLAUDE.md`
pointer. This BACK-011 is the directory-level equivalent: same
principle, applied to the `skills/` directory layout. Resolve them
together — the AGENTS.md/CLAUDE.md split is the precedent.

### BACK-012 — `processkit-helpers` published as a real Python package
Currently the lib lives at `src/lib/processkit/` and MCP servers
import via sys.path manipulation. If it grows or external tools want
to use it, publish it as a proper package on PyPI. Trade-off: another
release surface.

### BACK-013 — Validation hook for skill DAG
Add `aibox lint`-style validation that checks `spec.uses` references
form a DAG with no cycles, no missing references, and that
process-primitive skills only reference lower layers.

### BACK-014 — Migrate this BACKLOG.md to BACK-NNN entity files
Once `workitem-management` MCP server is in use here, convert each
entry above to a real WorkItem under `context/workitems/`. This file
becomes a stub pointing at the index.

### BACK-015 — Evaluate full src/ → target-root mirror restructure
Architectural question deferred to v1.0 planning. Today, `src/` mixes
two semantically different things:

- **Catalog content** (`src/{primitives,skills,processes,packages,lib}/`)
  — the processkit library, addressed by tooling and namespaced when
  installed (e.g. under a consumer's `.processkit/`)
- **Project-init scaffolding** (`src/scaffolding/`) — files copied
  verbatim to a consumer project's repo root at install time

A bolder alternative: make `src/` itself a literal mirror of a
fresh consumer project root. Then `src/AGENTS.md` → target's
`/AGENTS.md`, `src/context/...` → target's `/context/...`, and catalog
content moves under `src/.processkit/{primitives,skills,...}` or a
similar namespace. Pros: src/ becomes self-explanatory ("this is what
a consumer gets"). Cons: huge breaking move — every reference in
PROVENANCE.toml, the lib's `_find_lib()`, the smoke test, every
server, the docs-site, FORMAT.md, INDEX.md files, and consumer
expectations would change at once.

Decision: keep `src/scaffolding/` as a contained subtree for now.
Revisit at v1.0 planning when the apiVersion bump (v1) is on the
table anyway and a coordinated restructure is cheaper.

## Done

### v0.5.1 (2026-04-07)
- **BACK-001 complete.** Three-level rewrite of all 85 migrated
  skills. Every skill under `src/skills/` now has explicit
  `## Level 1 — Intro`, `## Level 2 — Overview`, and `## Level 3 —
  Full reference` sections. Frontmatter on each rewritten skill has:
  - `metadata.version` bumped 1.0.0 → 1.1.0
  - `spec.description` condensed (drops the duplicated "Use when..."
    clause)
  - explicit `spec.when_to_use` field added
  - 80-column hard wrap on all prose (tables, code blocks, URLs,
    frontmatter exempt)
- **Reference exemplar** `src/skills/python-best-practices/SKILL.md`
  rewritten first as the canonical structural reference.
- **Execution:** 14 parallel general-purpose subagent invocations
  across 7 rounds (one category or pair of categories per round, two
  agents per round). 8 commits total (1 exemplar + 7 rounds).
- **Original content preserved semantically** — no fabricated
  technical claims. `references/` subdirectories left untouched;
  relevant material was either inlined into Level 3 or pointed to
  from Level 3 for the longest treatments.
- v0.5.1 is content-only — no code or schema changes from v0.5.0,
  smoke test still green.

### v0.5.0 (2026-04-07)
- **Provider-neutral install paths.** All MCP server `mcp-config.json`
  fragments now use `context/skills/<name>/mcp/server.py`. The lib's
  `paths.py` resolves consumer-installed schemas at `context/schemas/`
  and state machines at `context/state-machines/`. The `_find_lib()`
  walk-up locates `context/skills/_lib/processkit/` for the
  consumer-install layout. Per the aibox handover v2.
- **Runtime cache moved.** `paths.index_db_path()` returns
  `context/.cache/processkit/index.sqlite`. `context/.aibox/` is gone.
  `.gitignore` adds `context/.cache/` and `context/**/private/`.
- **Reference-templates model docs.** All references to
  `processkit.manifest` removed (manifest model superseded). Docs
  updated to describe `aibox.lock` at the project root and the
  verbatim reference templates at `context/templates/processkit/<v>/`.
- **AGENTS.md as canonical agent entry.** New `AGENTS.md` at the repo
  root holds the authoritative instructions; `CLAUDE.md` is a thin
  pointer (~22 lines). The shipped template is at
  `src/scaffolding/AGENTS.md` for consumer projects. The old
  `context/AIBOX.md` (pure duplication of HANDOVER/BACKLOG/CLAUDE) was
  deleted.
- **HANDOVER.md G8 rewritten** as the formal aibox-sync perimeter rule
  (only `.devcontainer/{Dockerfile,docker-compose.yml,devcontainer.json}`
  are in scope; anything else aibox touches is an aibox-side bug).
- **BACK-002: 14 new primitive schemas.** Actor, Role, Scope, Gate,
  Discussion (priority five), Binding, Category, Metric, Schedule,
  Constraint, Context, Process, StateMachine, Artifact. All 18
  primitive schemas now ship (CrossReference is intentionally not a
  file primitive). All validate as JSON Schema draft 2020-12.
- **2 new state machines.** scope (planned → active → completed +
  cancelled) and discussion (active ↔ resolved → archived).
- **BACK-003: 5 new MCP servers.** actor-profile, role-management,
  scope-management, gate-management, discussion-management. Each
  follows the existing boilerplate, validates against its schema,
  and is exercised end-to-end in `scripts/smoke-test-servers.py`. The
  smoke test now creates 11+ entities across 11 servers in a single
  run. Total processkit MCP servers: 11.
- **BACK-004: 4 Process entities** under `src/processes/` — bug-fix,
  code-review, feature-development, release. Promoted from the legacy
  aibox `.md` files into formal `kind: Process` entities with full
  step lists, role assignments, gates, and definition_of_done. Each
  validates against process.yaml.
- **BACK-007: WAL mode** in `src/lib/processkit/index.py` — multiple
  readers and a single writer can now coexist without "database is
  locked".
- **80-column line-width policy** with smart exemptions (tables,
  fenced code blocks, URLs, frontmatter, TOML). Encoded in
  `.editorconfig`; documented in `AGENTS.md` and `CONTRIBUTING.md`.
- **`scripts/build-release-tarball.sh`** — reproducible producer of
  `dist/processkit-<version>.tar.gz` + sha256 sidecar. Tested with a
  v0.5.0-test dry-run. The release process in `CONTRIBUTING.md` and
  `HANDOVER.md` now includes the build + upload step.
- **Aibox issues filed:** projectious-work/aibox#33 (AGENTS.md
  scaffolding), projectious-work/aibox#34 (sync perimeter docs).
- **Skill `provides.mcp_tools`** declared on the 5 new servers'
  SKILL.md files. Each also adds `index-management` + `id-management`
  to `spec.uses` (the Layer 0 foundations rule).
- **`src/skills/agent-management/SKILL.md`** generalized: removed
  hard-coded `CLAUDE.md` and `context/AIBOX.md` references; the
  context-budget example acknowledges that the config file location
  depends on how processkit was installed.
- **`src/skills/context-grooming/`** updated to reference
  `context/skills/` (the new install location) instead of
  `.claude/skills/`.

### v0.1.0 (2026-04-06)
- Repo bootstrap, entity file format spec, 3 schemas, 2 state machines

### v0.2.0 (2026-04-06)
- src/ restructure, 101 skills (85 migrated + 16 new), 5 package tiers,
  docs-site bootstrap, apiVersion change to processkit.projectious.work/v1

### v0.3.0 (2026-04-06)
- src/lib/processkit shared library + `index.existing_ids` helper
- 6 MCP servers: index-management and id-management as Layer 0 peers
  (read/write sides), plus event-log, workitem-management,
  decision-record, binding-management
- 4 entity-creating servers refactored to use the index for collision
  avoidance (drops the per-server `_existing_ids` filesystem helper)
- Smoke test harness covering all 6 servers (`scripts/smoke-test-servers.py`)
- CONTRIBUTING.md (with foundation-deps section)
- BACKLOG.md
- minimal package now includes both Layer 0 foundations
- 103 total skill directories (85 migrated + 18 new process-primitive)

### v0.4.0 (2026-04-07)
- **Migration primitive** (the 19th) — schema, state machine,
  registered in `KIND_PREFIXES` (prefix `MIG`), `DEFAULT_DIRS`
  (`migrations`). Skill `migration-management` (Layer 3) ships the
  workflow with templates and a body briefing format.
- **owner-profiling skill** (Layer 4) — interview-driven owner profile
  bootstrap. Four templates (identity, working-style, goals-and-context,
  team-and-relationships), interview protocol reference, observable-signals
  reference (ported from aibox `context/research/owner-profiling-skill-2026-03.md`).
  Markdown-only (no MCP server yet).
- **context-grooming skill** (Layer 4) — periodic context cleanup with a
  ruleset, a grooming-report template, and a review-then-act workflow.
  Markdown-only.
- **`src/PROVENANCE.toml` convention** — single file mapping every shipped
  file to its last-changed git tag. Seed file present. Generator script
  `scripts/stamp-provenance.sh` for release-time regeneration.
- **`scripts/processkit-diff.sh`** — generic diff between two tags
  (text/toml/json). Reads PROVENANCE.toml at each tag and emits added/
  removed/changed/unchanged sets. Consumed by aibox sync (Phase 4).
- **Privacy tier convention** — `privacy:` field in entity metadata
  (optional, default `project-private`). Three tiers: `public`,
  `project-private`, `user-private`. Filesystem rule
  `context/**/private/` for `.gitignore`. Documented in
  `src/primitives/FORMAT.md` and `docs-site/docs/reference/privacy.md`.
  Used by owner-profiling for `team-and-relationships.md`.
- **Context efficiency** — new "Context budget and lazy loading" section
  in `src/skills/agent-management/SKILL.md`. Documents the
  `[context.budget]` section for `aibox.toml`, the always_load /
  on_demand pattern, and the relationship to `context-grooming`.
- **docs-site updates** — primitives/overview (19 primitives),
  reference/migration (rewrite for v0.4.0 model), reference/privacy
  (new page), intro (new status, new feature list), sidebars
  (privacy reference added).
- **README.md** updated for v0.4.0.
- **HANDOVER.md** updated with "What changed in v0.4.0" preamble +
  status table.
- **106 total skill directories** (85 migrated + 21 new process-primitive).
