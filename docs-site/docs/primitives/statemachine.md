---
sidebar_position: 29
title: "StateMachine"
---

# StateMachine

Legacy v1 state/transition graph entity. In the SmoothTiger/SmoothRiver
v2 direction, processkit no longer presents `StateMachine` as a
first-class shipped entity surface. State machines still exist as
validation machinery used by MCP servers, but users should not model
new workflow records as StateMachine entities.

| | |
|---|---|
| **ID prefix** | `SM` (legacy v1) |
| **State machine** | none (meta-primitive) |
| **MCP server** | none |
| **Skill** | `state-machine-management` (legacy authoring guidance) |

## v2 replacement

Use the owning MCP server for lifecycle transitions. It loads the
appropriate implementation contract and returns structured errors for
invalid transitions. Project workflows should be expressed with
WorkItems, Artifacts, Gates, and Bindings rather than new
StateMachine records.

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

- Legacy state machine definitions may exist in `context/state-machines/`
  during v1 migration, but they are not first-class v2 entities.
- MCP servers load the state machine for a given `kind` and enforce
  valid transitions — invalid transition attempts return a structured error.
- For v2, change lifecycle behavior in the owning MCP server or a
  reviewed implementation contract, then migrate affected records
  explicitly. Do not create new StateMachine records.
