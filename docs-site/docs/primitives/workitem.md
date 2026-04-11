---
sidebar_position: 10
title: "WorkItem"
---

# WorkItem

A unit of work — task, story, bug, epic, spike, or chore. The primary
work-tracking primitive in processkit.

| | |
|---|---|
| **ID prefix** | `BACK` |
| **State machine** | `workitem` |
| **MCP server** | `workitem-management` |
| **Skill** | `workitem-management` (Layer 2) |

## State machine

```
backlog → in-progress → review → done
              ↕
           blocked
```

All states can transition to `cancelled`. `done` and `cancelled` are
terminal.

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `title` | string (1–200) | Short, actionable title |
| `state` | string | Current state |

### Optional

| Field | Type | Description |
|---|---|---|
| `description` | string | Long-form description, acceptance criteria |
| `type` | enum | `task` · `story` · `bug` · `epic` · `spike` · `chore` (default: `task`) |
| `priority` | enum | `critical` · `high` · `medium` · `low` |
| `assignee` | `ACTOR-*` | Responsible actor |
| `parent` | `BACK-*` | Parent work item (for subtasks / epics) |
| `children` | `BACK-*[]` | Child work item IDs |
| `blocks` | `BACK-*[]` | Items this one blocks |
| `blocked_by` | `BACK-*[]` | Items blocking this one |
| `related_decisions` | `DEC-*[]` | Decisions that motivated or govern this item |
| `scope` | string | Scope ID (sprint, milestone, release) |
| `estimate` | object | Freeform effort estimate |
| `started_at` | datetime | Set automatically on first `in-progress` transition |
| `completed_at` | datetime | Set automatically on `done` or `cancelled` |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260411_0900-BoldVale-fts5-full-text-search
  created: '2026-04-11T09:00:00Z'
spec:
  title: Add FTS5 full-text search to SQLite index
  state: backlog
  type: story
  priority: medium
  description: |
    Implement FTS5 trigram tokeniser in index.py so agents can search
    entity body text, not just frontmatter fields.
  related_decisions:
    - DEC-20260409_1200-SwiftPeak-sqlite-for-index
---
```

## Notes

- All state transitions are auto-logged via `event-log` — no manual log
  call needed.
- Use `parent` / `children` to model epics and subtasks; keep the epic
  type `epic` and subtask types `task` or `story`.
- `scope` is a free string; bind to a Scope entity via `binding-management`
  when you need richer scope tracking (dates, goals, state).
- Query by state, type, priority, or assignee via `query_workitems`.
