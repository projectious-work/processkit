# Changelog

All notable changes to processkit are documented here.
Versions follow [Semantic Versioning](https://semver.org/).

---

## [v0.10.0] — 2026-04-10

### Added

- **`index.resolve_entity()`** — new shared library function with 3-stage ID
  resolution: exact match → prefix match (missing slug) → word-pair match (bare
  word-pair like `StoutCrow`). Enables agents and humans to look up entities by
  the colloquial word-pair shorthand rather than needing the full canonical ID.

### Changed

- **Skills directory reorganized into 7 category subdirectories** (SteadyLeaf):
  `processkit/` (30), `engineering/` (46), `devops/` (15), `data-ai/` (11),
  `product/` (11), `documents/` (8), `design/` (5). All 126 skills moved in
  both `src/context/skills/` and `context/skills/`. All SKILL.md files updated
  with a consistent `category:` frontmatter field.
- **`skill-finder`** updated with a "By directory" table mapping the 7 categories
  to their on-disk subdirectory names.
- **`get_workitem`**, **`get_decision`**, **`get_entity`** (index-management) now
  use `resolve_entity()` and return `{"error": "..."}` instead of `null`/`None`
  when the entity is not found, and `{"error": "ambiguous..."}` with a candidate
  list when multiple entities match.
- **All `_load_*` helpers** (`_load_scope`, `_load_gate`, `_load_actor`,
  `_load_role`, `_load_discussion`, `_load_decision`, `_load_workitem`) updated
  to use `resolve_entity()` so word-pair lookup also works in write tools
  (transition, link, etc.).
- **`smoke-test-servers.py`** updated to find MCP server files in the new
  category subdirectory layout.

### Fixed

- `get_workitem` and `get_decision` previously returned `null` for not-found
  IDs, making it impossible for callers to distinguish "not found" from
  "found but empty". Both now return a structured error dict (SnappyCrane).
- Agents looking up entities by word-pair shorthand (e.g. `StoutCrow` instead
  of the full `BACK-20260410_1050-StoutCrow-create-brand-design-skill`) now
  resolve correctly via the new `resolve_entity()` fallback chain (SteadyPeak).

---

## [v0.9.0] — 2026-04-09

`src/` → `context/` mirror restructure (GrandLily). All processkit content
now lives under `src/context/` in the source tree and is mirrored to
`context/` in the target project root on `aibox sync`.

---

## [v0.8.0] — 2026-04-09

Auto-log side effects in all entity-mutating MCP servers. Every
`create_*`, `transition_*`, and `link_*` call now appends a `LogEntry`
without the caller doing anything extra.

---

## [v0.7.0] — 2026-04-09

Initial processkit v0.7.0 release. Core entity MCP servers, state machines,
schemas, and 85+ skills migrated from the original aibox templates.
