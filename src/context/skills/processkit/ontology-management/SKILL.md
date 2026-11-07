---
name: ontology-management
description: >
  Manage generated v1 ontology entities that do not require a dedicated
  domain server.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-ontology-management
    version: "1.0.0-alpha.3"
    created: 2026-07-27T00:00:00Z
    category: processkit
    layer: 1
    uses:
      - skill: index-management
        purpose: Keep generic ontology reads current.
      - skill: event-log
        purpose: Record validated generic lifecycle changes.
    provides:
      primitives:
        - Location
        - Measurement
        - Archive
        - Service
        - WorkItemTemplate
        - ScopePlan
        - Roadmap
        - ProgramIncrement
        - Iteration
        - Release
        - EvaluationRun
      mcp_tools:
        - create_ontology_entity
        - get_ontology_entity
        - update_ontology_entity
        - transition_ontology_entity
        - list_ontology_entities
---

# Ontology Management

## Intro

Use this server for generated ontology contracts whose mechanics are generic.
Dedicated domain servers remain authoritative where they exist. Every write
validates the generated schema, updates the read index, and emits an event.

## Overview

Callers provide an explicit processkit ID and a schema-valid `spec`; the
server never guesses domain policy or silently introduces fields.

Use `create_ontology_entity`, `get_ontology_entity`,
`update_ontology_entity`, `transition_ontology_entity`, and
`list_ontology_entities`. Kinds with a state machine may transition only
through declared edges.

## Gotchas

- Do not use this generic server when a dedicated domain server owns the kind.
- A kind name, ID prefix, and generated schema must agree.
- Lifecycle transitions require a shipped state-machine definition.

## Full reference

The generated contracts under `context/schemas/_generated/` define fields and
interfaces. Lifecycle definitions under `context/state-machines/` define
allowed states and transitions. Successful writes are indexed and emit a
typed LogEntry.
