---
name: category-management
description: |
  Manage Category entities — taxonomies and classification schemes that group other entities by type, area, tier, etc. Use when defining a new classification axis (priority levels, bug severity, feature tier, product area) that other entities will be tagged with.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-category-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 2
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
    provides:
      primitives: [Category]
      templates: [category]
---

# Category Management

## Intro

A Category is a named classification — a list of possible values for a
labeling axis. Examples: priority (critical/high/medium/low), bug severity
(sev1/sev2/sev3), feature tier (core/enhancement/experiment), product area
(frontend/backend/infra).

## Overview

### When to create a Category

Create a Category when:
- A labeling axis is used across many entities
- The values are constrained to a specific set
- The set is worth documenting (meanings, SLAs per value)

Don't create a Category for one-off tags or freeform labels.

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Category
metadata:
  id: CAT-priority
  created: 2026-04-06T00:00:00Z
spec:
  name: priority
  description: "Business priority for work items."
  axis: priority
  values:
    - name: critical
      description: "Drop everything. Affects production or blocks a release."
    - name: high
      description: "Top of the queue. Assigned this sprint."
    - name: medium
      description: "Important but schedulable."
    - name: low
      description: "Nice to have. Pick up when capacity allows."
  applies_to: [WorkItem]
---
```

### Using a category

Entities tag themselves via `metadata.labels.<axis>: <value>` or
`spec.<axis>: <value>`. The index MCP server validates that the value is
one of the category's defined values.

### Workflow

1. Pick `CAT-<axis>` where axis is the labeling dimension.
2. List `values` with clear, non-overlapping definitions.
3. Declare which primitive `kinds` this category `applies_to`.
4. Save to `context/categories/`.
5. When you add a new value, write a `category.value_added` LogEntry so
   the change is traceable.

## Full reference

### Fields

| Field         | Type           | Notes                                                  |
|---------------|----------------|--------------------------------------------------------|
| `name`        | string         | Category name                                          |
| `description` | string         | What this axis categorizes                             |
| `axis`        | string         | The label key used on entities (e.g. `priority`)       |
| `values`      | list[object]   | `{name, description, optional metadata}`               |
| `applies_to`  | list[string]   | Primitive kinds this category applies to               |
| `default`     | string         | Optional. Default value if unspecified.                |
| `multi`       | bool           | Can an entity have multiple values? Default false.     |

### Hierarchical categories

A category value may have its own `children` for nested taxonomies:

```yaml
values:
  - name: backend
    children:
      - name: backend-api
      - name: backend-db
      - name: backend-queue
  - name: frontend
    children:
      - name: frontend-web
      - name: frontend-mobile
```

The validator accepts any leaf or any intermediate name.

### Retiring a value

Set `deprecated: true` on a value rather than removing it — existing entities
still reference it, and removing it would invalidate them.

### Categories vs Labels vs Roles

- **Category**: defined set of values for a classification axis.
- **Labels**: freeform key/value tags. No schema.
- **Roles**: named sets of responsibilities actors fill.

Categories are for closed sets. If the set is open and changes often, use
labels. If it's about who does things, it's a role.
