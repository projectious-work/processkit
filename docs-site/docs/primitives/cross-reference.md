---
sidebar_position: 26
title: "CrossReference"
---

# CrossReference

A lightweight, frontmatter-embedded relationship between two entities.
CrossReference is not a file — it is a convention for fields in the
`spec` block of any entity.

| | |
|---|---|
| **ID prefix** | — (not a file entity) |
| **State machine** | — |
| **MCP server** | `index-management` (for querying) |
| **Skill** | `cross-reference-management` (Layer 2) |

## When to use a CrossReference vs a Binding

Use a CrossReference when the relationship is:
- **Simple** — no scope, no time bounds, no attributes of its own
- **Directional** — one entity points at another

Use a **Binding** when the relationship has scope, time, or its own
attributes.

| Situation | Use |
|---|---|
| "WorkItem A blocks WorkItem B" | CrossReference (`blocks` field) |
| "Decision D governs WorkItem W" | CrossReference (`related_decisions`) |
| "Alice is tech lead for Q2" | Binding (scoped + time-bounded) |

## Conventional field names

processkit standardises these field names across entity kinds:

| Field | Pattern | Meaning |
|---|---|---|
| `parent` | `BACK-*` / `SCOPE-*` | Hierarchy parent |
| `children` | `BACK-*[]` | Hierarchy children |
| `blocks` | `BACK-*[]` | This item blocks these items |
| `blocked_by` | `BACK-*[]` | These items block this one |
| `supersedes` | `DEC-*` | This decision replaces an older one |
| `superseded_by` | `DEC-*` | This decision was replaced by a newer one |
| `related_decisions` | `DEC-*[]` | Decisions that govern or motivated this item |
| `related_workitems` | `BACK-*[]` | WorkItems that motivated or implement a decision |
| `outcomes` | `DEC-*[]` | DecisionRecords produced by a Discussion |
| `produces_to` | object | For Note promotion: `{kind, id}` |

## Example

```yaml
# WorkItem with CrossReferences in spec
spec:
  title: Implement FTS5 search
  state: in-progress
  parent: BACK-epic-search-improvements
  blocks:
    - BACK-search-ux-polish
  blocked_by:
    - BACK-index-schema-locked
  related_decisions:
    - DEC-sqlite-for-index
```

## Notes

- CrossReferences are queryable via `query_entities` and `search_entities`
  in the index-management MCP server — the SQLite index tracks these
  relationships.
- There is no separate CrossReference entity file. The relationship lives
  in the referring entity's frontmatter.
- When you find yourself wanting attributes on a cross-reference (e.g. "this
  relationship is valid from April to June"), that is the signal to promote
  it to a **Binding**.
