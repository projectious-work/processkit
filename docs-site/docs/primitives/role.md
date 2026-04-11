---
sidebar_position: 16
title: "Role"
---

# Role

A named set of responsibilities. Roles are descriptive — they document
who is expected to do what, but do not enforce access control.

| | |
|---|---|
| **ID prefix** | `ROLE` |
| **State machine** | none |
| **MCP server** | `role-management` |
| **Skill** | `role-management` (Layer 1) |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `name` | string (1–100) | Kebab-case identifier matching the `metadata.id` suffix |
| `description` | string | One-sentence purpose statement |

### Optional

| Field | Type | Description |
|---|---|---|
| `responsibilities` | string[] | Imperative bullet points — concrete, not vague |
| `skills_required` | string[] | Skill IDs or names (advisory, not enforced) |
| `default_scope` | enum | `project` · `sprint` · `permanent` — assumed scope when binding without an explicit one |
| `supersedes` | `ROLE-*` | Role ID this one replaces |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Role
metadata:
  id: ROLE-20260411_0907-ClearOak-tech-lead
  created: '2026-04-11T09:07:00Z'
spec:
  name: tech-lead
  description: Owns technical direction and architecture decisions.
  responsibilities:
    - Review and approve architectural decisions (DEC)
    - Unblock teammates on technical questions within 24 hours
    - Run weekly engineering sync
  skills_required: [software-architecture, code-review, decision-record]
  default_scope: project
---
```

## Notes

- Roles describe responsibilities, not permissions. processkit does not
  enforce RBAC.
- A global, unscoped assignment can use the Actor's `roles` field
  directly. For a scoped or time-bounded assignment ("Alice is tech lead
  on Project X for Q2"), create a **Binding** instead.
- `link_role_to_actor` creates the shortcut entry on the Actor entity.
