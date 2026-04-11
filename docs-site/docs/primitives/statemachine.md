---
sidebar_position: 29
title: "StateMachine"
---

# StateMachine

A state/transition graph that defines valid lifecycle states and allowed
transitions for a primitive kind. processkit ships default state machines
for WorkItem, DecisionRecord, Migration, Scope, Discussion, and Note.
Projects can override or extend them.

| | |
|---|---|
| **ID prefix** | `SM` |
| **State machine** | none (meta-primitive) |
| **MCP server** | none |
| **Skill** | `state-machine-management` (Layer 3) |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `description` | string | What this state machine governs |
| `initial` | string | Starting state for new entities |
| `states` | object | Map of state name → `{description, transitions[]}` |

### Optional

| Field | Type | Description |
|---|---|---|
| `terminal` | string[] | States with no outgoing transitions |

### Transition fields (within each state)

| Field | Type | Description |
|---|---|---|
| `to` | string | Target state |
| `guard` | string | Prose description of when this transition is allowed |
| `on_enter` | string | Side effect description when entering target state |
| `required_role` | string | Role required to make this transition |

## Default state machines shipped by processkit

| Primitive | States |
|---|---|
| WorkItem | `backlog → in-progress → review → done` (+ `blocked`, `cancelled`) |
| DecisionRecord | `proposed → accepted / rejected → superseded` |
| Migration | `pending → in-progress → applied / rejected` |
| Scope | `planned → active → completed / cancelled` |
| Discussion | `active → resolved / closed` |
| Note | `fleeting → insight / promoted / archived` |

## Example — custom state machine

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: StateMachine
metadata:
  id: SM-20260411_0919-ClearRidge-rfc-lifecycle
  created: '2026-04-11T09:19:00Z'
spec:
  description: RFC lifecycle for architecture proposals.
  initial: draft
  terminal: [accepted, withdrawn]
  states:
    draft:
      description: Being written — not ready for review.
      transitions:
        - to: in-review
          guard: Author marks RFC ready.
    in-review:
      description: Open for comments from stakeholders.
      transitions:
        - to: accepted
          required_role: tech-lead
        - to: draft
          guard: Major revision needed.
        - to: withdrawn
          guard: Author withdraws.
    accepted:
      description: Accepted — implementation may proceed.
    withdrawn:
      description: RFC withdrawn by author.
---
```

## Notes

- State machine definitions live in `context/state-machines/` as YAML
  files indexed by the SQLite index.
- MCP servers load the state machine for a given `kind` and enforce
  valid transitions — invalid transition attempts return a structured error.
- To override a default state machine, create a new StateMachine entity
  with the same `kind` name as the primitive and reference it in your
  project config.
