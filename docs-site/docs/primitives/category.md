---
sidebar_position: 25
title: "Category"
---

# Category

A classification axis with a closed set of allowed values — priority
levels, bug severity tiers, product areas. Use Category when the valid
values are defined and enforced; use freeform labels for open-ended
tagging.

| | |
|---|---|
| **ID prefix** | `CAT` |
| **State machine** | none |
| **MCP server** | none |
| **Skill** | `category-management` (Layer 2) |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `name` | string (1–100) | Category name (kebab-case) |
| `description` | string | What this axis classifies |
| `axis` | string | Label key used on entities (e.g. `priority`, `severity`) |
| `values` | object[] | Allowed values — each with `name` (required), `description`, `deprecated`, `children` (optional) |

### Optional

| Field | Type | Description |
|---|---|---|
| `applies_to` | string[] | Primitive kinds this applies to; empty = applies anywhere |
| `default` | string | Default value when unspecified |
| `multi` | boolean | `true` = entity can carry multiple values (default: `false`) |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Category
metadata:
  id: CAT-20260411_0917-BrightFern-workitem-priority
  created: '2026-04-11T09:17:00Z'
spec:
  name: workitem-priority
  description: Business priority for work items.
  axis: priority
  applies_to: [WorkItem]
  default: medium
  values:
    - name: critical
      description: Blocks a release or customer. Drop everything.
    - name: high
      description: Important this sprint. Do before medium items.
    - name: medium
      description: Normal priority. Default.
    - name: low
      description: Nice to have. Defer if sprint is full.
---
```

## Notes

- Categories complement the `type` and `priority` fields already on
  WorkItem — use Category when you need a *custom* classification axis
  beyond the built-in enums.
- `deprecated: true` on a value signals it should no longer be used on
  new entities, but keeps old entities valid.
- Hierarchical value sets use the `children` field to model tree-shaped
  taxonomies (e.g. product area → sub-area).
