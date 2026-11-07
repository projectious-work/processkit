# PK1-P0 — Accept the v1 context-framework baseline

## Scope and status

Done. The normative v1 baseline in `spec/doc/v1/` defines processkit as a
provider-neutral context framework. It was accepted by the owner and merged
into `v1.x-dev` through #197 (`03b7eddb`).

## What was decided

- processkit manages organizational context, not memory (decision C1): it
  stores and serves standards, process specifications, skills, trusted MCP
  server entries, decision records, and documents. Events, logs, work-item
  instances, sessions, and agent memories are out of scope.
- The full 90-concept ontology is the definition language (C2); decision
  records stay as reviewed documents (C3).
- MCP is the only agent interface, with a connection briefing and on-demand
  loading; no vendor-specific outputs (C4). Assembly is deterministic and
  cacheable (C5).
- Inheritance through locked upstream repositories (C6), Kubernetes-pattern
  access control with consumed identity (C7), stdio plus a read-only shared
  server (C8), an MCP server catalog instead of a gateway (C9), and one
  Python application core (C10).

## Alternatives and deviations

- The earlier memory-oriented v1 draft (#182) and its governance extension
  (#196) were closed as superseded. They remain readable on their branches.
- An MCP gateway, vendor-channel exports, and a local loopback daemon were
  considered and rejected; see C4, C8, and C9.
- The decision `DEC-20260807_1559-BraveFern`, which defined processkit as
  context and memory infrastructure, is superseded by C1.

## Validation

- `scripts/validate-v1-spec.py` passes: 198 normative requirements, no
  duplicate IDs, no broken local links, valid roadmap.
- `standard.template.json` and `mcp-server.template.json` validate against
  their schemas with `resource-metadata.schema.json`.
- No implementation exists yet; conformance is measured from PK1-P1 onward.

## Consequences

- No code from v0 or the v1 alpha is carried over without a requirement or
  black-box fixture (PK-ARCH-002).
- `README.md` and the documentation site still describe v0. They are
  rewritten when v1 behavior exists, following the documentation standard.

## Follow-up

- PK1-P1 starts with the ontology registry: classifying all 90 concepts as
  definition or instance.
