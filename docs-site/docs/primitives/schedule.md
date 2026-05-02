---
sidebar_position: 23
title: "Schedule"
---

# Schedule

Legacy v1 time-based trigger or recurring cadence. In the
SmoothTiger/SmoothRiver v2 direction, processkit no longer presents
`Schedule` as a first-class shipped entity surface. Use
`Binding(type=time-window)` with `conditions.recurrence_rule` for the
durable contract; an external runner still performs execution.

| | |
|---|---|
| **ID prefix** | `SCHED` (legacy v1) |
| **State machine** | none |
| **MCP server** | none |
| **Skill** | `schedule-management` (legacy authoring guidance) |

## v2 replacement

Use the `binding-management` server's `create_time_window` path for
time windows. `pk-doctor`'s `v2_contracts` check requires
`Binding(type=time-window)` records to include
`conditions.recurrence_rule`.

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `name` | string | Kebab-case identifier |
| `description` | string | Human-readable summary |
| `cadence` | enum | `daily` · `weekly` · `monthly` · `quarterly` · `adhoc` · `custom` |

### Optional

| Field | Type | Description |
|---|---|---|
| `cron` | string | Standard cron expression for machine scheduling |
| `timezone` | string | IANA timezone name (e.g. `Europe/Berlin`) |
| `triggers` | object[] | What this schedule fires (processes, reminders, events) |
| `active` | boolean | `false` = suspended (default: `true`) |
| `last_run` | datetime | Advisory — set by whoever runs the schedule |
| `next_run` | datetime | Advisory — set by runner |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Schedule
metadata:
  id: SCHED-20260411_0915-CalmGlen-weekly-standup
  created: '2026-04-11T09:15:00Z'
spec:
  name: weekly-standup
  description: Fire the standup-context skill every Monday morning.
  cadence: weekly
  cron: "0 9 * * 1"
  timezone: Europe/London
  triggers:
    - kind: skill
      skill: standup-context
  active: true
---
```

## Notes

- Legacy v1 Schedule records are documentation for migration only. In
  v2, an external runner reads `Binding(type=time-window)` records and
  fires the target at the right time.
- `last_run` and `next_run` are advisory fields set by the runner — not
  enforced by processkit on legacy records.
- Scope a recurring cadence by binding the governed WorkItem, Artifact,
  or Scope through `type: time-window`; do not create new
  `schedule-scope` Bindings.
