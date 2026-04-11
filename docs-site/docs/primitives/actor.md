---
sidebar_position: 15
title: "Actor"
---

# Actor

A participant in the project — human, AI agent, or automated service.
Actors are assigned to WorkItems, named in DecisionRecords, and bound
to Roles.

| | |
|---|---|
| **ID prefix** | `ACTOR` |
| **State machine** | none |
| **MCP server** | `actor-profile` |
| **Skill** | `actor-profile` (Layer 1) |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `type` | enum | `human` · `ai-agent` · `service` |
| `name` | string (1–200) | Display name (for AI agents: model name + version) |

### Optional

| Field | Type | Description |
|---|---|---|
| `email` | email | Humans only |
| `handle` | string | GitHub handle, Slack user, etc. |
| `expertise` | string[] | Tags used by assignment-suggestion logic |
| `roles` | `ROLE-*[]` | Shortcut for unscoped role assignment |
| `preferences` | object | Freeform (commit style, timezone, review style, …) |
| `active` | boolean | `false` = actor has left, no new work assigned (default: `true`) |
| `joined_at` | datetime | When actor became part of the project |
| `left_at` | datetime | When actor stopped |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Actor
metadata:
  id: ACTOR-20260411_0906-SteadyWren-claude
  created: '2026-04-11T09:06:00Z'
spec:
  type: ai-agent
  name: Claude Sonnet 4.6
  handle: claude
  expertise: [python, typescript, processkit, documentation]
  active: true
  preferences:
    commit_style: conventional-commits
    timezone: UTC
---
```

## Notes

- Roles are descriptive, not restrictive — processkit does not enforce
  RBAC. Use `roles` for assignment-suggestion only.
- Use `deactivate_actor` (not manual editing) to mark an actor as
  `active: false`; it keeps the index consistent.
- For scoped or time-bounded role assignments, use a **Binding** instead
  of the `roles` shortcut field.
