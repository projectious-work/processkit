---
sidebar_position: 23
title: "Schedule"
---

# Schedule

A time-based trigger or recurring cadence. processkit defines Schedules;
an external runner (aibox, cron, CI) reads them and fires the trigger.

| | |
|---|---|
| **ID prefix** | `SCHED` |
| **State machine** | none |
| **MCP server** | none |
| **Skill** | `schedule-management` (Layer 3) |

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

- processkit **defines** schedules but does **not execute** them. The
  consumer (aibox, CI, cron daemon) is responsible for reading the
  Schedule and firing the trigger at the right time.
- `last_run` and `next_run` are advisory fields set by the runner — not
  enforced by processkit.
- Bind a Schedule to a Scope via a `schedule-scope` Binding to associate
  it with a sprint or milestone.
