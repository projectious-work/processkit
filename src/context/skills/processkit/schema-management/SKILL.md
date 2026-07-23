---
name: schema-management
description: >
  Manage generated processkit schema contracts through deterministic MCP
  rebuild and inspection workflows.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-schema-management
    version: "1.0.0-alpha.1"
    created: 2026-07-22T00:00:00Z
    category: processkit
    layer: 0
    provides:
      primitives: []
      mcp_tools:
        - regenerate_schemas
        - get_schema_contract
        - get_validation_mode
---

# Schema Management

## Intro

Schema management exposes the committed build-time schema generator and
runtime contract metadata through MCP. Use it to rebuild all or selected
generated schemas and to inspect the contract or validation mode for a kind.

## Overview

Use `regenerate_schemas` after changing canonical sources under
`context/schemas/src/`. A full rebuild accepts no kind filter; a partial
rebuild accepts registry selectors such as `workitem` or `decisionrecord`.
The result always has `rebuilt`, `unchanged`, and `errors` fields.

Use `get_schema_contract` to retrieve the runtime Schema `spec`, including
interfaces, validation mode, vocabularies, generation metadata, and the
draft-2020-12 entity-spec schema. Pass a discriminator such as `risk` to
inspect an overlay. Use `get_validation_mode` for the smaller strict/tolerant
routing decision.

The source tree is canonical. Generated files are committed derived output;
never edit them directly.

## Gotchas

- **Rebuilding without reviewing the scope.** Regeneration overwrites committed
  derived files. Inspect the requested kinds and current diff first when the
  user has not already authorized a rebuild.
- **Editing generated YAML directly.** Regeneration overwrites such edits.
  Change the source fragment, primitive, discriminator, or composition.
- **Confusing product and schema versions.** Product v1.x uses entity API v2,
  while each Schema has its own compatibility version.
- **Passing entity IDs as selectors.** Partial generation accepts registry
  kind selectors, not entity IDs or schema filenames.
- **Assuming every MCP process shares caches.** Regeneration clears the cache
  in its own process. Restart or call existing reload tools in other granular
  MCP processes when they must observe changed contracts immediately.
- **Treating tolerant validation as valid data.** Tolerant mode supports
  migration; it does not waive schema findings or release gates.
- **Ignoring an `errors` mapping.** Generation is atomic. Any reported error
  means no planned output from that call was written.
- **Promising a rebuild without running it.** When regeneration is requested,
  call `regenerate_schemas` in the same turn and report its actual result.

## Full reference

`regenerate_schemas(kinds=None)` renders the registry in deterministic order.
Kind names are normalized to lowercase registry selectors. Unknown selectors,
inheritance failures, invalid merge strategies, and unsafe output paths appear
under `errors`.

`get_schema_contract(kind, discriminator=None)` returns the selected contract.
The contract is the Schema entity's `spec` block because that is the runtime
surface consumed by processkit servers.

`get_validation_mode(kind, discriminator=None)` returns the selected mode.
Missing schemas return a structured error instead of silently choosing a mode.

Anti-patterns:

- Hand-editing `_generated/` output.
- Rebuilding schemas from an installed tree that lacks canonical sources.
- Using schema regeneration as a substitute for an entity-data migration.
- Converting a discriminator variant into a false top-level entity kind.
