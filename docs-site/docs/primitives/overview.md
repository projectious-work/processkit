---
sidebar_position: 1
title: "Overview"
---

# Primitives — Overview

processkit provides **20 process primitives** as universal building blocks.
They are framework-agnostic — they appear in every serious process methodology
(SAFe, PMBOK, CMMI, Scrum, Kanban). processkit ships their schemas, default
state machines, and management skills, but does not impose a methodology on
top of them.

## The 20 primitives

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
| **Metric**        | Quantified observation                                            | METRIC |
| **Schedule**      | Time-based trigger / cadence                                     | SCHED  |
| **Constraint**    | Rule or limit the project must respect                          | CONST  |
| **Context**       | Ambient knowledge and environment                                 | CTX    |
| **Discussion**    | Multi-turn exploratory conversation                               | DISC   |
| **Process**       | Declarative workflow definition                                  | PROC   |
| **StateMachine**  | State/transition graph for lifecycle primitives                  | SM     |

## Layered relationships

Primitives depend on each other through the skill hierarchy:

```
Layer 0: index (infrastructure), id (infrastructure), LogEntry (event-log)
Layer 1: Actor (actor-profile), Role (role-management)
Layer 2: WorkItem, DecisionRecord, Scope, Category, Binding, CrossReference
Layer 3: Process, StateMachine, Gate, Schedule, Constraint, Migration
Layer 4: Discussion, Metric, Owner profile (owner-profiling), Context grooming
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

All 20 primitives ship with authoritative YAML schema files under
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
