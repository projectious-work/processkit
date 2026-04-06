# Backlog — processkit

Tracked deferred work, in priority order. Once the workitem-management
MCP server is in regular use here, this list should migrate to actual
WorkItem files under `context/workitems/`.

## High priority

### BACK-001 — Three-level rewrite of 85 migrated skills
Each migrated skill currently has the original aibox structure
(`When to Use` + `Instructions`) which roughly maps to Level 1+2 content
but is not labeled with explicit `## Level 1/2/3` headers. Add the
explicit structure, condense the intros to ≤3 sentences, and promote
existing `references/` material into Level 3 sections where appropriate.

Estimated scale: 85 files × ~30min each = ~40 hours of careful editing.
Can be batched by category (process first, then language, then framework, etc.).

### BACK-002 — Remaining 15 primitive schemas
Only WorkItem, LogEntry, DecisionRecord have full JSON schemas in
`src/primitives/schemas/`. Add schemas for: Actor, Role, Binding, Scope,
Category, Gate, Metric, Schedule, Constraint, Context, Discussion,
Process, StateMachine, Artifact. CrossReference is intentionally not a
file primitive.

Each schema is ~50–100 lines of YAML. Block the corresponding
management skill's full validation until the schema lands.

### BACK-003 — MCP servers for the remaining process primitives
v0.3.0 ships 6 servers (index-management, id-management, event-log,
workitem-management, decision-record, binding-management). Add servers for:
- actor-profile (create_actor, update_actor, list_actors)
- role-management (create_role, list_roles, link_role_to_actor)
- scope-management (create_scope, list_scopes, transition_scope)
- gate-management (create_gate, evaluate_gate, list_gates)
- discussion-management (open_discussion, resolve_discussion, link_decision)

Each is ~150–250 lines, similar shape to the existing servers.

### BACK-004 — Process templates as first-class Process entities
The aibox templates currently include four .md files for processes
(bug-fix, code-review, feature-development, release). Migrate them to
the formal Process primitive shape (apiVersion/kind/metadata/spec with
steps/roles/gates) and put them under `src/processes/`.

## Medium priority

### BACK-005 — FTS5 search in the index
The current `search_entities` uses `LIKE %text%`. Switch to SQLite
FTS5 for proper tokenization and ranking. Schema migration needed.

### BACK-006 — Incremental indexing
`reindex` is currently a full sweep. Add an incremental mode that
diffs the filesystem against the index and updates only changed rows.
Useful for projects with thousands of entities.

### BACK-007 — WAL mode for concurrent MCP servers
Two servers writing at the same time hit `database is locked`. Enable
SQLite WAL mode in `index.open_db()` and verify all writes are
short-lived.

### BACK-008 — Per-primitive docs-site pages
Currently the docs-site has one `primitives/overview.md` listing all
18 primitives. Add a page per primitive: `primitives/workitem.md`,
`primitives/decisionrecord.md`, etc. Could be auto-generated from
the schema files.

### BACK-009 — Per-skill docs-site pages or auto-generated catalog
Currently `skills/catalog/` has 13 category pages migrated from aibox.
Update them to reflect processkit-specific naming and the 16 new
process-primitive skills. Or auto-generate from `src/skills/*/SKILL.md`
frontmatter.

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

## Done

### v0.1.0 (2026-04-06)
- Repo bootstrap, entity file format spec, 3 schemas, 2 state machines

### v0.2.0 (2026-04-06)
- src/ restructure, 101 skills (85 migrated + 16 new), 5 package tiers,
  docs-site bootstrap, apiVersion change to processkit.projectious.work/v1

### v0.3.0 (awaiting push + tag)
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
