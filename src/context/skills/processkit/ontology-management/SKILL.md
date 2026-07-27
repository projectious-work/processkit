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

Use this server for generated ontology contracts whose mechanics are generic.
Dedicated domain servers remain authoritative where they exist. Every write
validates the generated schema, updates the read index, and emits an event.

Callers provide an explicit processkit ID and a schema-valid `spec`; the
server never guesses domain policy or silently introduces fields.
