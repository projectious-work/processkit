---
sidebar_position: 18
title: "Scope"
---

# Scope

A bounded container for work — sprint, milestone, quarter, release, or
project. Scopes give WorkItems, Processes, and Constraints a shared
time and goal boundary.

| | |
|---|---|
| **ID prefix** | `SCOPE` |
| **State machine** | `scope` |
| **MCP server** | `scope-management` |
| **Skill** | `scope-management` (Layer 2) |

## State machine

```
planned → active → completed
        ↘ cancelled
```

`completed` and `cancelled` are terminal.

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `name` | string (1–200) | Human-readable name |
| `kind` | enum | `sprint` · `milestone` · `quarter` · `project` · `release` · `other` |
| `state` | string | Current state |

### Optional

| Field | Type | Description |
|---|---|---|
| `starts_at` | date | Start date |
| `ends_at` | date | End date |
| `goals` | string[] | Concrete, testable outcomes |
| `description` | string | Longer context |
| `parent` | `SCOPE-*` | Parent scope (a quarter contains sprints) |
| `related_decisions` | `DEC-*[]` | Planning or retro decisions for this scope |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Scope
metadata:
  id: SCOPE-20260411_0909-BrightElm-sprint-7
  created: '2026-04-11T09:09:00Z'
spec:
  name: Sprint 7 — WildButter docs push
  kind: sprint
  state: active
  starts_at: '2026-04-11'
  ends_at: '2026-04-25'
  goals:
    - All primitive reference pages published
    - Docusaurus build green on 3.8.x
    - First public deploy complete
  parent: SCOPE-20260410_q2-2026
---
```

## Notes

- Attach WorkItems to a Scope via a `scope` field on the WorkItem, or
  via a `work-assignment` Binding when richer tracking is needed.
- Scope hierarchy (quarter → sprint) is modelled via the `parent` field.
- `transition_scope` to `active` when work begins; to `completed` when
  the scope closes — this timestamps the lifecycle automatically.
