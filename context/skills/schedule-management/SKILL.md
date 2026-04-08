---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-schedule-management
  name: schedule-management
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Manage Schedule entities — time-based triggers and recurring cadences (daily standup, weekly review, monthly retro)."
  category: process
  layer: 3
  uses: [event-log]
  provides:
    primitives: [Schedule]
    templates: [schedule]
  when_to_use: "Use when defining a recurring cadence — daily/weekly/monthly — that triggers a process or reminder."
---

# Schedule Management

## Level 1 — Intro

A Schedule is a time-based trigger describing when a process should run or
a reminder should fire — daily standups, weekly retros, monthly ops reviews,
quarterly planning.

## Level 2 — Overview

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Schedule
metadata:
  id: SCHED-daily-standup
  created: 2026-04-06T00:00:00Z
spec:
  name: daily-standup
  description: "Daily async standup at 09:00 local time."
  cadence: daily
  cron: "0 9 * * 1-5"
  timezone: Europe/Berlin
  triggers:
    - process: standup
  active: true
---
```

### Workflow

1. Pick `SCHED-<name>`.
2. Set a human `cadence` (`daily`/`weekly`/`monthly`/`quarterly`/`adhoc`/`custom`).
3. For machine-readable scheduling, set `cron` + `timezone`.
4. Link what it `triggers` — a process name, a reminder text, etc.
5. Use Bindings to scope a schedule to a specific team or project.

## Level 3 — Full reference

### Fields

| Field       | Type         | Notes                                              |
|-------------|--------------|----------------------------------------------------|
| `name`      | string       | Kebab-case identifier                              |
| `description` | string     | Human-readable                                     |
| `cadence`   | enum         | `daily`/`weekly`/`monthly`/`quarterly`/`adhoc`/`custom` |
| `cron`      | string       | Standard cron expression                           |
| `timezone`  | string       | IANA timezone name                                 |
| `triggers`  | list[object] | What fires: processes, reminders, events           |
| `active`    | bool         | `false` = suspended                                |
| `last_run`  | datetime     | Advisory — set by whoever runs the schedule        |
| `next_run`  | datetime     | Advisory                                           |

### Execution

processkit does NOT execute schedules. It describes them. An external
runner (GitHub Actions, cron, a human, an agent on a loop) reads the
Schedule and fires the trigger at the right time. The `triggers` field is
the contract between the Schedule definition and whoever runs it.

### Scoped schedules

A daily standup runs in one scope, not globally. Use a Binding:

```yaml
kind: Binding
spec:
  type: schedule-scope
  subject: SCHED-daily-standup
  target: SCOPE-project-x
```

Then the runner fetches all schedules bound to the scope it's acting on.
