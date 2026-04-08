---
name: constraint-management
description: |
  Manage Constraint entities — rules and limits the project must respect (budget, latency SLO, team size, compliance). Use when recording a rule, limit, or boundary that affects decisions — budget ceiling, latency SLO, regulatory requirement, team bandwidth.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-constraint-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 3
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
    provides:
      primitives: [Constraint]
      templates: [constraint]
---

# Constraint Management

## Intro

A Constraint is an explicit rule or limit the project must respect: budget
ceilings, latency SLOs, team capacity, compliance requirements, dependency
restrictions. Capturing constraints as first-class entities makes them
referenceable from decisions and visible to trade-off analysis.

## Overview

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Constraint
metadata:
  id: CONST-p99-latency
  created: 2026-04-06T00:00:00Z
spec:
  name: p99-latency
  description: "API p99 latency must stay under 200ms under normal load."
  kind: slo             # budget | slo | regulatory | capacity | dependency | policy | other
  severity: hard        # hard | soft | advisory
  measurement: "p99 of request duration over 5-minute windows"
  target: "< 200ms"
  source: "Customer SLA, signed 2026-01-15"
  active: true
---
```

### Workflow

1. Pick `CONST-<short-name>`.
2. Set `kind` — budget, SLO, regulatory, capacity, dependency, policy, or other.
3. Set `severity`: `hard` (cannot be violated), `soft` (flagged but overridable),
   `advisory` (informational).
4. Describe the `measurement` (how you know if it's met) and the `target`.
5. Record the `source` — where the constraint came from (contract, regulation,
   owner decision).

### Using constraints

- DecisionRecords link via `spec.related_constraints` when a decision was
  shaped by a constraint.
- WorkItems add `labels.constraint` when the work exists because of a constraint.
- Processes reference constraints via Bindings (`type: process-constraint`)
  for scoped constraints.

## Full reference

### Fields

| Field         | Type        | Notes                                                     |
|---------------|-------------|-----------------------------------------------------------|
| `name`        | string      | kebab-case identifier                                     |
| `description` | string      | One sentence                                              |
| `kind`        | enum        | `budget` / `slo` / `regulatory` / `capacity` / `dependency` / `policy` / `other` |
| `severity`    | enum        | `hard` / `soft` / `advisory`                              |
| `measurement` | string      | How the constraint is measured                            |
| `target`      | string      | The threshold or boundary                                 |
| `source`      | string      | Where the constraint comes from                           |
| `active`      | bool        | `false` = no longer in effect                             |
| `violations`  | list        | Log-style list of known violations (optional, prefer LogEntries) |

### Constraint violations

When a hard constraint is violated, write a `constraint.violated` LogEntry
rather than editing the Constraint file. Repeated violations may motivate a
DecisionRecord to relax the constraint or address the underlying cause.

### Retiring a constraint

Set `active: false` and log `constraint.retired`. Do not delete — historical
decisions may reference the constraint as part of their rationale.
