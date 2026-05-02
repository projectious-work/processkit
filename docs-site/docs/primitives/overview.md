---
sidebar_position: 1
title: "Overview"
---

# Primitives — Overview

processkit provides a compact set of process primitives as universal
building blocks. The v2 direction keeps durable project facts in the
entity layer and moves workflow definitions, schedules, runtime model
data, and lifecycle implementation details to narrower surfaces.

## Registry and legacy schemas

| Primitive         | Purpose                                                           | Prefix |
|-------------------|-------------------------------------------------------------------|--------|
| **WorkItem**      | Unit of work (task, story, bug, epic, spike, chore)              | BACK   |
| **LogEntry**      | Immutable record of something that happened                      | LOG    |
| **DecisionRecord**| A choice with rationale (ADR pattern)                            | DEC    |
| **Migration**     | Pending/in-progress/applied transition between upstream versions | MIG    |
| **Artifact**      | Completed deliverable (document, dataset, build, URL)            | ART    |
| **Note**          | Zettelkasten capture layer (fleeting, insight, reference)        | NOTE   |
| **Actor**         | Person or agent (humans, AI, services)                           | ACTOR  |
| **Role**          | Named set of responsibilities                                    | ROLE   |
| **Binding**       | Scoped/temporal relationship between two entities (generalized RoleBinding) | BIND |
| **Scope**         | Bounded container (sprint, milestone, project, quarter, release) | SCOPE  |
| **Category**      | Classification axis with defined values                          | CAT    |
| **CrossReference**| Lightweight frontmatter relationship (not a file)                | —      |
| **Gate**          | Validation checkpoint                                             | GATE   |
| **Schedule**      | Legacy v1 time trigger; v2 uses `Binding(type=time-window)`      | SCHED  |
| **Constraint**    | Rule or limit the project must respect                          | CONST  |
| **Context**       | Ambient knowledge and environment                                 | CTX    |
| **Discussion**    | Multi-turn exploratory conversation                               | DISC   |
| **Process**       | Legacy v1 workflow entity; v2 uses process-instance WorkItems plus definition Artifacts | PROC |
| **StateMachine**  | Legacy v1 lifecycle entity; v2 treats state machines as implementation contracts | SM |

`Metric`, `Model`, `Process`, `Schedule`, and `StateMachine` are not
first-class shipped entity surfaces in the SmoothTiger/SmoothRiver v2
direction. Metric and policy definitions become artifact-backed
specifications; readings and events are LogEntries or external time
series. Model data belongs to model-recommender roster/configuration
surfaces. Processes are represented by process-instance WorkItems with
definition Artifacts. Schedules are represented by time-window Bindings.
State machines remain validation machinery, not author-facing workflow
records.

## Layered relationships

Primitives depend on each other through the skill hierarchy:

```
Layer 0: index (infrastructure), id (infrastructure), LogEntry (event-log)
Layer 1: Actor (actor-profile), Role (role-management)
Layer 2: WorkItem, DecisionRecord, Scope, Category, Binding, CrossReference
Layer 3: Gate, Constraint, Migration, workflow/projection skills
Layer 4: Discussion, metrics-management, Owner profile (owner-profiling), Context grooming
```

Lower layers never depend on higher layers. The management skill for a
primitive follows the same layer (e.g. `workitem-management` is Layer 2 and
depends on `event-log` at Layer 0 and `actor-profile` at Layer 1).

## Cross-references vs Bindings

**Rule:** if a relationship has scope, time, or its own attributes → use a
Binding entity. Otherwise → use a cross-reference field in frontmatter.

| Situation                                            | Use         |
|------------------------------------------------------|-------------|
| "A blocks B"                                         | cross-ref   |
| "Alice is a developer" (globally)                    | cross-ref   |
| "Alice is tech lead on project X for 2026"           | **Binding** |
| "Security gate applies to release process on main"   | **Binding** |

See [Primitives → Relationships](./relationships) for details.

## Schema coverage

The current schema tree includes these authoritative YAML schema files under
[`src/context/schemas/`](https://github.com/projectious-work/processkit/tree/main/src/context/schemas/).
The schemas define the `spec` fields, required vs optional, and enum
constraints. MCP servers validate against the schema on every write call —
schema errors surface as structured tool errors rather than silent bad data.

`aibox lint` validates `apiVersion`, `kind`, and `metadata.id` structurally
without requiring MCP servers — useful in CI or offline environments.

## Next

- [Format](./format) — the `apiVersion/kind/metadata/spec` contract.
- [State Machines](./state-machines) — default machines and how to override.
- [Relationships](./relationships) — cross-references and Bindings.
