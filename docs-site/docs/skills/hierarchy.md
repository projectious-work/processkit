---
sidebar_position: 3
title: "Skill Hierarchy"
---

# Skill Hierarchy

Process-primitive skills form a strict layered DAG. A skill's `spec.uses`
field may only reference skills in **lower** layers. Cycles are validation
errors.

## The layers

| Layer | Role                      | Skills                                                                                                 |
|-------|---------------------------|--------------------------------------------------------------------------------------------------------|
| 0     | Foundation                | `index-management`, `id-management`, `event-log`                                                       |
| 1     | Primitive management      | `role-management`, `actor-profile`                                                                     |
| 2     | Core entities             | `workitem-management`, `decision-record`, `scope-management`, `category-management`, `cross-reference-management`, `binding-management` |
| 3     | Workflow policy           | `gate-management`, `constraint-management`; legacy/migration guidance for `process-management`, `state-machine-management`, `schedule-management` |
| 4     | Cross-cutting             | `discussion-management`, `metrics-management`                                                          |

> **Layer 0 has three skills with one intra-layer edge.** `index-management`
> and `id-management` are the absolute foundation — they depend on nothing.
> `event-log` is also Layer 0 but `uses: [index-management, id-management]`,
> so it conceptually sits "atop" them. This is the only intra-layer edge in
> the entire hierarchy. The strict-downward rule applies to Layers 1+ unchanged.

## What the layers mean

- **Layer 0** — the foundation that every entity-creating skill depends
  on. `index-management` provides the read side (look up entities by ID,
  kind, state, text). `id-management` provides the write side (allocate
  unique IDs in the configured format). `event-log` is also at Layer 0
  but uses both — the only intra-layer edge in the hierarchy.
- **Layer 1** — management for the "participants" of processes: Actors
  (who does things) and Roles (what things they do).
- **Layer 2** — management for the primary work artifacts: WorkItems,
  DecisionRecords, Scopes. Depends on Layers 0–1.
- **Layer 3** — workflow policy: Gates and Constraints tie Layer 2
  entities together. Process, Schedule, and StateMachine skills remain
  as legacy/migration guidance; v2 expresses runs as WorkItems,
  definitions as Artifacts, recurrence as `time-window` Bindings, and
  lifecycle enforcement through MCP server contracts.
- **Layer 4** — cross-cutting concerns that reference everything:
  Discussions produce decisions and reference work items; metrics-management
  records metric specifications as artifacts and observations as LogEntries.
  This is a skill-layer placement, not a Metric primitive.

## Technical/language skills are unlayered

Skills in categories like `language`, `framework`, `infrastructure`,
`database`, `data`, `ai`, `security`, `observability`, `performance`,
`design` are `layer: null`. They don't fit the layered hierarchy — they
describe how to do engineering things, not how to manage process artifacts.
Such skills can still use `spec.uses` for *other* technical skills
(e.g. `fastapi-patterns` uses `python-best-practices`).

## Validation

Phase 5 of the DISC-002 plan adds DAG validation to the index MCP server:

- Every `spec.uses` entry must reference an existing skill.
- For process-primitive skills, each referenced skill's `spec.layer` must be
  strictly less than the referencing skill's `spec.layer`.
- No cycles are permitted.
