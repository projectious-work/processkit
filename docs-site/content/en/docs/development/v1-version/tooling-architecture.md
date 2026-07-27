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

## Doctor Remediation Contract

Every `pk-doctor` finding with `action_required: true` must have a typed
disposition. Supported dispositions are:

- `safe_fix`: a bounded, idempotent repair
- `migration_needed`: a planned data or identity transformation
- `archive_needed`: a lifecycle-preserving archive operation
- `policy_decision_needed`: a structured, reviewable exception
- `external_dependency`: a named downstream or infrastructure blocker

Executable dispositions must name a gateway tool, provide schema-valid
arguments, and declare whether confirmation, data-loss approval, preflight,
or dry-run support is required. Release validation must introspect the
gateway catalog and fail when a declared tool is absent or its input schema
is incompatible with the finding.

Prose guidance alone is not an actionable remediation. When processkit
cannot execute or formally recognize the required disposition, the finding
must be informational and link to tracked implementation work instead of
claiming that the derived project can resolve it.

## Policy Exceptions

A policy exception is structured data, not an arbitrary DecisionRecord. It
must identify the check and finding fingerprint, affected scope, rationale,
approver or accepted decision, and an expiry or review condition. Doctor
resolves exceptions through a shared policy service and reports stale,
over-broad, or unmatched exceptions. The underlying DecisionRecord remains
the durable rationale, while the exception supplies the machine-readable
suppression contract.

## Schema Generation

Shipped schema sources live under `src/context/schemas/src/`, which becomes
`context/schemas/src/` in an installed project. Runtime tools consume a
committed `context/schemas/_generated/*.yaml` tree. Keeping both paths inside
`src/` ensures that derived projects can regenerate schemas without fetching
repository-only build inputs.

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
on aibox; it must be runnable through processkit's local test commands.

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
SQLite from files for recovery, local fixtures, and release checks.

## Declarative Migration Execution

Migration management must support a processkit-native lifecycle:

1. `draft_migration` records intent, source and target versions, operations,
   and expected source hashes.
2. `plan_migration` validates schemas, references, permissions, collisions,
   and append-only constraints without writing.
3. `execute_migration` applies the approved plan through the shared atomic
   write, event, and index-update path.
4. A failed execution aborts before commit or leaves a recovery journal that
   can be resumed or rolled back deterministically.

The initial declarative operation vocabulary should cover `move_path`,
`update_field`, `rename_entity`, `rewrite_reference`, and `archive_payload`.
Migration files must not embed arbitrary executable scripts. Each operation
declares preconditions and expected hashes so a plan cannot silently apply to
changed input.

## Stable Identity And History

Identity changes should preserve historical truth without rewriting
append-only LogEntries. The preferred model is a canonical replacement plus
durable predecessor/successor relations and an ID alias index. Reads through
an old ID resolve to the canonical entity while returning the alias path used
for resolution.

History rewriting is exceptional. It requires an explicit migration policy,
original-content hashes, archived source payloads, and an auditable event. A
filename-style warning alone never justifies rewriting event history.
