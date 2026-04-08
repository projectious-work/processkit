---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-metrics-management
  name: metrics-management
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Manage Metric entities — quantified observations the project cares about (velocity, error rates, lead time, NPS)."
  category: process
  layer: 4
  uses: [event-log]
  provides:
    primitives: [Metric]
    templates: [metric]
  when_to_use: "Use when defining or recording a quantitative measure — team velocity, error rate, lead time, customer satisfaction score."
---

# Metrics Management

## Level 1 — Intro

A Metric is a named, quantified observation — something the project measures
and cares about. Examples: team velocity per sprint, p99 latency, release
frequency, error rate, customer NPS.

## Level 2 — Overview

### Metric vs observation

The Metric primitive defines *what is measured*. Individual readings of the
metric are LogEntries (`event_type: metric.recorded`) or external time-series
data. processkit stores the definition, not the time series.

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Metric
metadata:
  id: METRIC-velocity
  created: 2026-04-06T00:00:00Z
spec:
  name: velocity
  description: "Story points completed per sprint."
  unit: points
  direction: higher-is-better
  measurement: "Sum of spec.estimate.value for WorkItems with spec.state=done in the sprint's SCOPE."
  target: 40
  tolerance: "±20%"
  cadence: sprint
  owner: ACTOR-tech-lead
---
```

### Recording observations

Individual measurements are LogEntries:

```yaml
kind: LogEntry
spec:
  event_type: metric.recorded
  timestamp: 2026-04-14T17:00:00Z
  actor: ACTOR-claude
  subject: METRIC-velocity
  subject_kind: Metric
  summary: "Sprint 42 velocity: 38 points"
  details:
    value: 38
    scope: SCOPE-sprint-42
```

The index MCP server (Phase 3) joins Metric definitions with their LogEntry
observations to produce time series.

## Level 3 — Full reference

### Fields

| Field         | Type     | Notes                                               |
|---------------|----------|-----------------------------------------------------|
| `name`        | string   | kebab-case identifier                               |
| `description` | string   | What this metric measures                           |
| `unit`        | string   | `points` / `ms` / `%` / `count` / etc.              |
| `direction`   | enum     | `higher-is-better` / `lower-is-better` / `target`   |
| `measurement` | string   | How to compute the value                            |
| `target`      | any      | Desired value (number or string)                    |
| `tolerance`   | string   | Acceptable deviation from target                    |
| `cadence`     | string   | How often it's measured                             |
| `owner`       | string   | Actor ID responsible for the metric                 |
| `active`      | bool     | `false` = no longer tracked                         |

### Vanity metrics

Avoid metrics that always trend up just by activity (commits per week, lines
of code) — they reward effort, not outcome. Favor metrics that can get
worse when the project is unhealthy: lead time, defect rate, customer
satisfaction, mean-time-to-recovery.

### Metrics vs goals

A goal is a desired future state recorded in a Scope's `spec.goals`. A Metric
is the quantitative thing the goal is measured by. One goal may reference
multiple metrics; one metric may inform multiple goals.
