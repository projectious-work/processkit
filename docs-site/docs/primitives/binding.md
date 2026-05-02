---
sidebar_position: 17
title: "Binding"
---

# Binding

A scoped or time-bounded relationship between two entities — the
junction-table pattern promoted to a first-class primitive. Use when a
relationship has scope, time, or its own attributes; use a frontmatter
cross-reference field otherwise.

| | |
|---|---|
| **ID prefix** | `BIND` |
| **State machine** | none |
| **MCP server** | `binding-management` |
| **Skill** | `binding-management` (Layer 2) |

## When to use a Binding vs a cross-reference

| Situation | Use |
|---|---|
| "A blocks B" | frontmatter `blocks: [BACK-...]` |
| "Alice is a developer" (globally) | Actor's `roles: [ROLE-...]` |
| "Alice is tech lead on Project X for Q2 2026" | **Binding** |
| "Security gate applies to this release WorkItem on main" | **Binding** |
| "Sprint 7 scopes these work items for Apr 1-14" | **Binding** |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `type` | string | Freeform binding type (see conventions below) |
| `subject` | string | Entity on the "from" side |
| `target` | string | Entity on the "to" side |

### Optional

| Field | Type | Description |
|---|---|---|
| `subject_kind` | string | Primitive kind of subject |
| `target_kind` | string | Primitive kind of target |
| `scope` | `SCOPE-*` | Scope within which the binding applies |
| `valid_from` | string | When binding starts (date or ISO 8601 datetime) |
| `valid_until` | string | When binding stops |
| `conditions` | object | Freeform constraints attached to binding |
| `description` | string | One-line human-readable summary |

## Type conventions

| Type | Meaning |
|---|---|
| `role-assignment` | Actor → Role (scoped) |
| `work-assignment` | Actor → WorkItem (assigned to sprint/scope) |
| `workitem-gate` | WorkItem → Gate (this gate guards this run or task) |
| `scope-gate` | Scope → Gate (this gate applies within this scope) |
| `time-window` | Entity → Artifact/Scope (time or recurrence contract) |
| `budget-application` | Artifact → WorkItem/Scope (cost policy applies here) |
| `constraint-scope` | Constraint → Scope (constraint applies in this scope) |
| `category-assignment` | Entity → Category value |

Process and Schedule are not v2 Binding endpoints. Legacy
`process-gate`, `process-scope`, and `schedule-scope` records should be
migrated to concrete WorkItem, Scope, Artifact, Gate, or time-window
relationships.

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Binding
metadata:
  id: BIND-20260411_0908-WarmOak-alice-techlead-q2
  created: '2026-04-11T09:08:00Z'
spec:
  type: role-assignment
  subject: ACTOR-20260411_0906-alice
  target: ROLE-20260411_0907-ClearOak-tech-lead
  scope: SCOPE-20260410_q2-2026
  valid_from: '2026-04-01'
  valid_until: '2026-06-30'
  description: Alice is tech lead on the processkit project for Q2 2026
---
```

## Notes

- `end_binding` closes a binding by setting `valid_until` to the current
  datetime — use this rather than deleting the entity.
- `resolve_bindings_for` returns all active bindings for a given subject,
  useful for "who is currently assigned to what" queries.
