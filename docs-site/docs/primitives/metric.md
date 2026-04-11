---
sidebar_position: 22
title: "Metric"
---

# Metric

A definition of something the project measures — latency, velocity,
error rate, coverage. Individual readings are LogEntries, not updates
to the Metric entity itself.

| | |
|---|---|
| **ID prefix** | `METRIC` |
| **State machine** | none |
| **MCP server** | none |
| **Skill** | `metrics-management` (Layer 4) |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `name` | string | Kebab-case identifier |
| `description` | string | What this metric measures |
| `unit` | string | Unit of measurement (`ms`, `%`, `count`, `points`, …) |
| `direction` | enum | `higher-is-better` · `lower-is-better` · `target` |

### Optional

| Field | Type | Description |
|---|---|---|
| `measurement` | string | How to compute the value (prose recipe) |
| `target` | number or string | Desired value (e.g. `"< 200ms"`) |
| `tolerance` | string | Acceptable deviation (e.g. `"±20%"`) |
| `cadence` | string | How often measured (`continuous`, `daily`, `sprint`, `monthly`, …) |
| `owner` | `ACTOR-*` | Actor responsible for this metric |
| `active` | boolean | `false` = no longer tracked (default: `true`) |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Metric
metadata:
  id: METRIC-20260411_0914-SwiftTide-mcp-p99-latency
  created: '2026-04-11T09:14:00Z'
spec:
  name: mcp-p99-latency
  description: 99th-percentile round-trip latency for MCP tool calls.
  unit: ms
  direction: lower-is-better
  target: "< 200ms"
  tolerance: "±20%"
  cadence: continuous
  measurement: |
    Measured from client tool-call dispatch to server response receipt.
    Sampled from production traffic via the observability pipeline.
  owner: ACTOR-platform-team
---
```

## Notes

- The Metric entity is a **definition** — it describes what to measure
  and what good looks like.
- Individual readings are logged via `log_event` with
  `event_type: metric.recorded` and a `details` payload containing
  `{metric_id, value, timestamp}`.
- For time-series storage, connect to an external system (Prometheus,
  InfluxDB); processkit records definitions and alerts, not raw series.
