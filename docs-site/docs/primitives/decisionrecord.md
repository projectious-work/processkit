---
sidebar_position: 12
title: "DecisionRecord"
---

# DecisionRecord

A significant choice — architectural, product, or process — recorded with
its context, rationale, and alternatives. The ADR (Architecture Decision
Record) pattern as a first-class entity.

| | |
|---|---|
| **ID prefix** | `DEC` |
| **State machine** | `decisionrecord` |
| **MCP server** | `decision-record` |
| **Skill** | `decision-record` (Layer 2) |

## State machine

```
proposed → accepted → superseded
         ↘ rejected
```

`accepted`, `rejected`, and `superseded` are terminal.

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `title` | string (1–200) | Short declarative title |
| `state` | string | Current state |
| `decision` | string | The chosen option, stated clearly |

### Optional

| Field | Type | Description |
|---|---|---|
| `context` | string | Situation that prompted the decision |
| `rationale` | string | Why this option was chosen |
| `alternatives` | object[] | Each with `option` (required) and `rejected_because` (optional) |
| `consequences` | string | Known or expected downstream effects |
| `deciders` | `ACTOR-*[]` | People / agents who made the decision |
| `supersedes` | `DEC-*` | Prior decision this replaces |
| `superseded_by` | `DEC-*` | Later decision that replaces this one |
| `related_workitems` | `BACK-*[]` | Work items that motivated or implement this decision |
| `decided_at` | datetime | When the decision was finalised |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260411_0902-SwiftPeak-sqlite-for-index
  created: '2026-04-11T09:02:00Z'
spec:
  title: Use SQLite as the entity index store
  state: accepted
  decision: Use SQLite with WAL mode as the backing store for the index.
  context: |
    We need a queryable index over all context/ entities that agents can
    use without doing filesystem walks.
  rationale: |
    SQLite is zero-config, ships as a Python built-in, and supports
    full-text search via FTS5. No external service needed.
  alternatives:
    - option: PostgreSQL
      rejected_because: Requires a running service; too heavy for local dev.
    - option: DuckDB
      rejected_because: No built-in full-text search; adds a dependency.
  decided_at: '2026-04-09T12:00:00Z'
---
```

## Notes

- Use `supersede_decision` to create a clean supersession chain when a
  decision changes — the old record stays as history, the new one links
  back via `supersedes`.
- Link decisions to work items with `link_decision_to_workitem` to make
  the "why was this built?" trail queryable.
- `proposed` is the right starting state for decisions that need
  stakeholder sign-off before being acted on.
