---
name: capability-management
description: >
  Manage versioned Capability entities and their governed lifecycle.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-capability-management
    version: "1.0.0-alpha.1"
    created: 2026-07-23T00:00:00Z
    category: processkit
    layer: 1
    uses:
      - skill: event-log
        purpose: Record capability lifecycle changes.
      - skill: index-management
        purpose: Keep capability reads and interface queries current.
    provides:
      primitives: [Capability]
      mcp_tools:
        - create_capability
        - get_capability
        - update_capability
        - transition_capability
        - list_capabilities
---

# Capability Management

## Intro

Capability management owns the v1 Capability primitive: an ability that an
actor, team, skill, or system can provide or consume.

## Overview

Create capabilities in `draft`, enrich their providers, consumers, inputs,
outputs, constraints, and evidence, then transition them through the generated
Capability state machine. All writes validate against the generated schema,
update the index, and emit a declared lifecycle event.

## Gotchas

- **Do not model a skill package as a Capability.** Skills may provide
  capabilities, but remain separately versioned packages.
- **Do not edit lifecycle state through update.** Use
  `transition_capability` so invalid edges are rejected.
- **Do not invent provider-specific capability kinds.** Alpha uses the
  ontology's `ability` kind.
- **Do not skip interface indexing.** Capability queries depend on the
  generated `Capability` interface rather than filename guessing.
- **Do not report logging as successful without an event ID.** Tool responses
  expose event status so callers can detect audit drift.

## Full reference

`create_capability` requires a name and description. `update_capability`
changes descriptive and relation fields only. `transition_capability` follows
`draft → active → deprecated|retired`, with supported reactivation from
`deprecated`.

Anti-patterns:

- Encoding executable implementation details in the capability description.
- Deleting retired capabilities that remain referenced by historical work.
- Treating provider and consumer lists as authorization policy.
