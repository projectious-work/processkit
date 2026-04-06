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
| 0     | Foundation                | `event-log`                                                                                            |
| 1     | Primitive management      | `role-management`, `actor-profile`                                                                     |
| 2     | Core entities             | `workitem-management`, `decision-record`, `scope-management`, `category-management`, `cross-reference-management`, `binding-management` |
| 3     | Process orchestration     | `process-management`, `state-machine-management`, `gate-management`, `schedule-management`, `constraint-management` |
| 4     | Cross-cutting             | `discussion-management`, `metrics-management`                                                          |

## What the layers mean

- **Layer 0** — the single foundation skill all other process skills
  depend on. `event-log` sits here because everything should log.
- **Layer 1** — management for the "participants" of processes: Actors
  (who does things) and Roles (what things they do).
- **Layer 2** — management for the primary work artifacts: WorkItems,
  DecisionRecords, Scopes. Depends on Layers 0–1.
- **Layer 3** — the orchestration layer: Processes, Gates, Schedules,
  Constraints, StateMachines. These tie Layer 2 entities together.
- **Layer 4** — cross-cutting concerns that reference everything:
  Discussions (which produce decisions, reference work items) and Metrics
  (which measure anything).

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
