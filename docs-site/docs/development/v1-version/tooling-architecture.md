---
title: Tooling Architecture
description: MCP, schema, and index architecture for processkit v1.0.
---

# Tooling Architecture

The v1.0 tooling architecture follows the RFC: schemas are generated
from Jinja + YAML sources, writes flow through MCP tools, and indexes are
extended rather than replaced.

## MCP Server Shape

MCP is the stable runtime contract for agents and harnesses. Files remain
human-inspectable, but canonical mutations happen through tools.

The v1.0 server surface should include:

- a processkit gateway that exposes the common read/write surface
- per-domain management tools for work, decisions, records, gates,
  discussions, roles, bindings, migrations, and skills
- an index-management surface for reads, search, relation traversal, and
  interface queries
- a schema-management surface with `regenerate_schemas`
- a doctor/audit surface for validation, drift, and release readiness

The gateway can aggregate tools for harness convenience, but tool
ownership should remain domain-specific so validation and lifecycle rules
stay close to the schema they enforce.

## MCP Helper Library

Every MCP server should use shared helpers rather than reimplementing
process rules. The helper layer should provide:

- ID allocation and collision checks
- generated schema loading
- draft-2020-12 JSON Schema validation
- state-machine loading and transition validation
- strict/tolerant validation-mode lookup
- frontmatter and body parsing/serialization
- atomic file writes under the canonical storage layout
- event-log emission for mutating actions
- index upsert/delete calls after successful writes
- typed error responses with actionable remediation
- Python type-signature to JSON Schema consistency checks
- golden fixture helpers for MCP contract tests

The RFC requires MCP tools to have valid Python type signatures and
matching draft-2020-12 JSON Schemas before release candidate.

## Schema Generation

Schema sources live under `schemas/src/`. Runtime tools consume a flat,
committed `_generated/*.yaml` tree.

Composition rules:

- `extends: parent.yaml` declares composition inheritance
- `{% include %}` includes T fragments into templates
- `__merge: replace|concat|name-merge` declares per-field merge strategy
- generated schemas declare interfaces such as `Record` or `Versioned`
- generated files are committed so agents and reviewers can diff runtime
  contracts directly

The required MCP endpoint is:

```python
regenerate_schemas(kinds: list | None) -> {rebuilt, unchanged, errors}
```

`kinds=None` performs a full rebuild. A non-empty list rebuilds only the
requested generated schemas and their dependencies. `aibox apply` may
trigger full rebuilds by default, but schema generation must not depend
on aibox; it must be runnable in processkit tests and CI directly.

## Validation Modes

Validation is phase-gated:

- migrated kinds validate strictly
- kinds still being migrated validate tolerantly and emit warnings
- validation mode is queryable through MCP per kind
- release gates fail on invalid strict entities

This lets alpha/beta users test incomplete migrations without allowing
known-invalid final entities to pass unnoticed.

## Indexing Database

The RFC keeps the existing SQLite/FTS5 direction and extends it with
interface-level grouping. The index is an accelerator and query surface,
not the source of truth. Git-backed entity files remain canonical.

The minimum index stores:

- entity identity, kind, discriminator, state, title, timestamps, and path
- declared interfaces from generated schemas
- frontmatter fields needed for common filters
- typed relation edges from Bindings and inline references
- event subjects and actors for timeline queries
- full-text rows for titles, bodies, specs, and selected metadata
- validation and generation metadata for drift checks

The required read patterns are:

- `get_entity(id)`
- search by text
- query by kind, state, owner, and container
- traverse relation edges
- backlinks or cited-by navigation
- `query_by_interface(interface, filters...)`

`query_by_interface(Record, ...)` is load-bearing because it lets agents
retrieve DecisionRecords, LogEntries, measurements, approvals, and other
record-like entities without guessing every concrete kind.

## Index Update Flow

Writes should follow one transaction-like path:

1. MCP tool receives a typed request.
2. The tool loads the generated schema and current validation mode.
3. The helper validates input and transition guards.
4. The entity file is written atomically.
5. Required LogEntries or Events are emitted.
6. The changed entity, relations, and events are upserted into SQLite.
7. The response returns the entity ID, path, state, validation mode, and
   index update status.

If index update fails after a file write, the response must surface drift
and `pk-doctor` must detect it. A separate `reindex` tool should rebuild
SQLite from files for recovery, CI fixtures, and release checks.

