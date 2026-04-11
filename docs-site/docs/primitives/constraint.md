---
sidebar_position: 24
title: "Constraint"
---

# Constraint

An explicit rule or limit the project must respect — budget ceiling,
latency SLO, regulatory requirement, team capacity cap. Violations
are LogEntries; constraints themselves do not change when violated.

| | |
|---|---|
| **ID prefix** | `CONST` |
| **State machine** | none |
| **MCP server** | none |
| **Skill** | `constraint-management` (Layer 3) |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `name` | string | Kebab-case identifier |
| `description` | string | One-sentence statement of the constraint |
| `kind` | enum | `budget` · `slo` · `regulatory` · `capacity` · `dependency` · `policy` · `other` |
| `severity` | enum | `hard` · `soft` · `advisory` |

### Optional

| Field | Type | Description |
|---|---|---|
| `measurement` | string | How to determine if the constraint is met |
| `target` | string | Threshold or boundary value |
| `source` | string | Where the constraint comes from (contract, regulation, decision) |
| `active` | boolean | `false` = no longer in effect (default: `true`) |
| `related_decisions` | `DEC-*[]` | Decisions that established or relaxed the constraint |

## Severity levels

| Level | Meaning |
|---|---|
| `hard` | Cannot violate — work stops until resolved |
| `soft` | Flagged and tracked; can be overridden with justification |
| `advisory` | Informational — violation noted but no process impact |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Constraint
metadata:
  id: CONST-20260411_0916-SteadyMoss-api-latency-slo
  created: '2026-04-11T09:16:00Z'
spec:
  name: api-latency-slo
  description: MCP tool round-trip p99 latency must stay below 200ms.
  kind: slo
  severity: hard
  target: "< 200ms p99"
  measurement: |
    Measured via the observability pipeline from tool-call dispatch to
    server response. Alert fires if exceeded for 5 minutes.
  source: Customer SLA — contract clause 4.2
  related_decisions:
    - DEC-20260409_latency-slo-accepted
---
```

## Notes

- Constraint violations are logged via `log_event` with
  `event_type: constraint.violated` — the Constraint entity itself is
  not modified.
- A `hard` constraint violation should surface as a blocked WorkItem or
  an urgent Discussion.
- Bind a Constraint to a Scope via a `constraint-scope` Binding to make
  it scope-specific rather than project-wide.
- Set `active: false` when a constraint is no longer in effect (SLA
  renegotiated, regulatory exemption granted).
