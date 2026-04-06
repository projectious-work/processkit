---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-event-log
  name: event-log
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Append-only event log — the probabilistic record of everything that happened in the project."
  category: process
  layer: 0
  uses: [index-management, id-management]
  provides:
    primitives: [LogEntry]
    mcp_tools: [log_event, query_events, recent_events]
    templates: [logentry]
  when_to_use: "Use whenever something notable happens that the project should remember — work items created/transitioned, decisions recorded, bindings changed, incidents occurred, releases shipped."
---

# Event Log

## Level 1 — Intro

The event log is the project's append-only history of significant events. Every
time a work item changes state, a decision is recorded, an actor is assigned,
or an incident occurs, a `LogEntry` file captures what happened, when, and
who caused it. LogEntries are never edited — corrections are added as new
entries.

## Level 2 — Overview

### When to write a LogEntry

Write a LogEntry whenever you do something the project should be able to
reconstruct later. Typical triggers:

- A WorkItem was created, transitioned, reassigned, or completed
- A DecisionRecord was proposed, accepted, or superseded
- A Binding was created or ended (role changed, scope reassigned)
- An external event was observed (deploy, incident, outage, release)
- A process step began or completed
- An automated check passed or failed at a gate

If you are asking "should I log this?", the answer is almost always yes.
Over-logging is cheap; under-logging erases history.

### Shape of a LogEntry

Every LogEntry is a YAML-frontmatter Markdown file:

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-<generated-id>
  created: <now>
spec:
  event_type: workitem.transitioned
  timestamp: <when-it-happened>
  actor: ACTOR-alice
  subject: BACK-calm-fox
  subject_kind: WorkItem
  summary: "Moved BACK-calm-fox from in-progress to review"
  details:
    from_state: in-progress
    to_state: review
---

Optional body: human-readable narrative, context, links.
```

### Workflow

1. Decide on `event_type`. Use dotted lowercase: `workitem.created`,
   `decision.accepted`, `binding.ended`, `incident.started`. Conventions emerge
   per project — write new types freely; the index MCP server (Phase 3) will
   surface them.
2. Fill in `actor` (who), `subject` + `subject_kind` (what it affected),
   `timestamp` (when the event occurred — distinct from `metadata.created`
   which is when the log file was written).
3. Write a one-line `summary`. This is what appears in timelines and queries.
4. Put anything structured in `details`. Freeform object.
5. Save the file to `context/logs/` (or whatever directory the project uses).

### Never edit a LogEntry

If you realize a LogEntry was wrong, do not edit it. Write a new LogEntry with
`event_type: logentry.corrected` and reference the original in `details.corrects`.
The original stays as historical record.

## Level 3 — Full reference

### event_type conventions

Use dotted, lowercase, `<subject>.<verb-past>` names. Examples that are already
well-established:

| event_type                | When to emit                                                 |
|---------------------------|--------------------------------------------------------------|
| `workitem.created`        | New WorkItem file written                                    |
| `workitem.transitioned`   | WorkItem state changed; include `from_state`/`to_state`      |
| `workitem.assigned`       | WorkItem assignee changed                                    |
| `workitem.linked`         | Cross-reference or parent/child relationship added           |
| `workitem.completed`      | WorkItem reached a terminal state (done/cancelled)           |
| `decision.proposed`       | New DecisionRecord in `proposed` state                       |
| `decision.accepted`       | DecisionRecord transitioned to `accepted`                    |
| `decision.superseded`     | DecisionRecord transitioned to `superseded`                  |
| `binding.created`         | New Binding written                                          |
| `binding.ended`           | Binding `valid_until` reached or Binding deleted             |
| `process.step.started`    | A step in a declared process began                           |
| `process.step.completed`  | A step in a declared process ended                           |
| `gate.passed` / `gate.failed` | A gate validation result                                 |
| `incident.started` / `incident.resolved` | Incident lifecycle                            |
| `release.shipped`         | A release was published                                      |
| `logentry.corrected`      | Correction of an earlier LogEntry (referenced in details)    |

### Fields

- `event_type` (required): See above.
- `timestamp` (required): ISO 8601 UTC. When the event *occurred*, not when
  it was *logged*. If the agent is logging retroactively, use the original
  event time and set `details.logged_late: true`.
- `actor` (required): `ACTOR-<id>` for a processkit Actor; raw string for
  external agents (`"github-actions"`, `"claude-cli"`, `"alice@example.com"`).
- `subject` (optional): ID of the entity the event concerns. Omit for
  project-level events.
- `subject_kind` (optional): The `kind` of the subject entity, for fast
  filtering in queries.
- `summary` (required): One line. Human-readable. Appears in timelines.
- `details` (optional): Structured object with event-specific fields.
- `correlation_id` (optional): Links related events across a workflow run.

### Directory layout

Default: `context/logs/` flat. Projects may shard by date in `aibox.toml`:

```toml
[context.sharding.LogEntry]
scheme = "date"
pattern = "context/logs/{year}/{month}/"
```

When sharded, the index MCP server still sees the full log; only the filesystem
layout differs.

### File naming

Default: `LOG-<generated-id>.md` where the ID format follows the project's
`aibox.toml` setting. With date-sharded storage, consider including a time
prefix in the ID (`LOG-2026-04-06T10-30-00-calm-owl.md`) so chronological
sort matches filesystem order.

### Interaction with the index MCP server

In Phase 3, the `index-management` MCP server reads all LogEntries into a
SQLite `events` table and exposes:

- `query_events(event_type?, actor?, subject?, since?, until?)`
- `recent_events(limit)`
- `events_for_entity(subject_id)`
- `timeline(start, end, filters)`

Until the MCP server exists, agents query by reading files directly — filesystem
glob + grep is adequate for small projects.

### Relationship to deterministic logging

Per DISC-002, processkit's event log is **all probabilistic** — it is written
by agents via this skill, not by instrumentation. If an enterprise deployment
needs tamper-evident event logs for audit or compliance, that is a governance
platform's responsibility, not processkit's. Do not build a second, deterministic
event source here.
