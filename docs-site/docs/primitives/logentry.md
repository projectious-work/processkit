---
sidebar_position: 11
title: "LogEntry"
---

# LogEntry

An immutable, append-only record of something that happened. The audit
trail primitive — never updated or deleted after creation.

| | |
|---|---|
| **ID prefix** | `LOG` |
| **State machine** | none (immutable) |
| **MCP server** | `event-log` |
| **Skill** | `event-log` (Layer 0) |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `event_type` | string | Machine-readable event type (e.g. `workitem.created`, `gate.passed`) |
| `actor` | string | ID of actor who caused the event |
| `timestamp` | datetime | When the event occurred (ISO 8601 UTC) |

### Optional

| Field | Type | Description |
|---|---|---|
| `subject` | string | ID of the entity the event concerns |
| `subject_kind` | string | Kind of subject entity (fast filtering) |
| `summary` | string | One-line human-readable summary |
| `details` | object | Event-specific structured payload |
| `correlation_id` | string | Links related events (e.g. a workflow run) |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260411_0901-SteadyWren-workitem-transitioned
  created: '2026-04-11T09:01:00Z'
spec:
  event_type: workitem.transitioned
  actor: ACTOR-claude
  timestamp: '2026-04-11T09:01:00Z'
  subject: BACK-20260411_0900-BoldVale-fts5-full-text-search
  subject_kind: WorkItem
  summary: WorkItem transitioned from backlog to in-progress
  details:
    from_state: backlog
    to_state: in-progress
---
```

## Auto-logging

Entity-mutating MCP servers (`create_*`, `transition_*`, `link_*`) append a
LogEntry automatically — callers do not need to call `log_event` separately.

Manual calls to `log_event` are for events that have no MCP server: deploying
a build, running a meeting, making a phone call, completing a manual step in a
process.

## Event type conventions

Use dot-separated `entity.verb` naming:

| Pattern | Examples |
|---|---|
| `<kind>.created` | `workitem.created`, `decision.created` |
| `<kind>.transitioned` | `workitem.transitioned`, `scope.transitioned` |
| `<kind>.linked` | `workitem.linked`, `decision.linked` |
| `gate.passed` / `gate.failed` / `gate.waived` | gate evaluation results |
| `metric.recorded` | individual metric reading |
| `constraint.violated` | constraint breach |
| `session.handover` | end-of-session handover written |

## Notes

- LogEntries are **never** updated or deleted. If an event was logged in
  error, log a corrective entry explaining the error.
- `query_events` and `recent_events` support filtering by subject, actor,
  event_type, and date range.
- Logs are date-sharded: `context/logs/{year}/{month}/`.
