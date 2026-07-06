---
title: Architecture Specification
description: Architectural direction for processkit v1.0.
---

# Architecture Specification

## System Role

processkit v1.0 is a provider-neutral process and memory substrate. It
stores canonical project entities in git-backed files and exposes safe
read/write behavior through MCP servers.

Agent runtimes are consumers. processkit provides context, process
state, governance, and memory; it does not own the agent loop.

## Canonical Model

The v1.0 ontology follows the RFC's T/P/D/C framing:

- `T`: terminology and shared fragments without their own lifecycle
- `P`: persistent primitives with schema and lifecycle
- `D`: discriminator variants of primitives
- `C`: compositions of primitives and terminology fragments

The full RFC target is 89 concepts. The alpha should implement only a
small proven subset before expanding. The detailed inventory is captured
in [Ontology Reference](./ontology-reference.md).

## Required Internal Semantics

The canonical model must preserve:

- stable processkit entity IDs
- schema-backed kinds and discriminators
- lifecycle state machines
- typed Bindings and queryable relations
- structured LogEntries
- validation modes per kind
- generated schemas
- MCP tools as the normal write path
- interface-aware queries such as `query_by_interface`

These semantics must not be collapsed into plain markdown links,
free-form notes, or OKF's permissive interchange model.

## Schema Generation

The RFC's build-time schema generation remains the preferred direction:

- source schemas live under a source tree
- templates and fragments compose schemas
- generated flat schemas are committed
- runtime tools consume generated schemas
- a rebuild endpoint supports full or partial regeneration

The required endpoint shape remains:

```text
regenerate_schemas(kinds: list | None) -> {rebuilt, unchanged, errors}
```

The generated schema architecture, MCP helper expectations, and index
update flow are specified in
[Tooling Architecture](./tooling-architecture.md).

## Validation

Validation is phase-gated:

- migrated kinds use strict validation
- migrating kinds use tolerant validation with warnings
- validation mode must be visible through MCP
- release gates must fail on invalid strict entities

## Indexing And Query

The index must support:

- full-text search
- entity lookup by ID
- relation traversal
- interface grouping
- query by interface
- backlinks or cited-by navigation

Interface-aware query is a core v1.0 feature because agents should be
able to ask for records, decisions, artifacts, logs, or approvals
without hard-coding every concrete kind.

The implementation should keep the index as a SQLite/FTS5 accelerator
over canonical files. It must store declared schema interfaces, typed
relations, event subjects, and enough metadata to support
`query_by_interface` without replacing the git-backed entity files as
the source of truth.

## OKF Boundary

OKF is an import/export profile, not the internal canonical model.

Exports should:

- emit conformant OKF v0.1 bundles
- include OKF `type`
- preserve `processkit_id`, kind, and interfaces in extension
  frontmatter
- emit normal markdown links for generic OKF consumers
- preserve typed relation metadata for processkit-aware consumers

Imports should:

- mark content as external knowledge
- preserve unknown OKF frontmatter
- avoid pretending external OKF concepts have full processkit lifecycle
  semantics

## Runtime Integration

processkit should provide examples and integration surfaces for:

- LangGraph
- Google ADK
- OpenAI Agents SDK
- Microsoft Agent Framework
- coding agents such as OpenHands, SWE-agent, Copilot Agent, and Aider

The stable contract should be MCP, files, schemas, and docs, not a
framework-specific runtime dependency.

## Testing Architecture

Manual dogfooding through a new aibox project is useful, but it is not
the correctness strategy for v1.0. The core test suite must run against
local fixture projects without requiring aibox and must cover schema
generation, MCP contracts, state machines, index updates, migrations,
and pk-doctor adversarial fixtures. aibox should be tested as an adapter
after the processkit-native suite is green.

See [Test Strategy](./test-strategy.md).
