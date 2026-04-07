---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-metrics-monitoring
  name: metrics-monitoring
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Application metrics with RED/USE methods, Prometheus types, dashboards, and SLO alerting."
  category: observability
  layer: null
  when_to_use: "Use when instrumenting an application with metrics, designing dashboards, setting up alerting, choosing between metric types, defining SLIs/SLOs, or applying RED, USE, or the four golden signals."
---

# Metrics & Monitoring

## Level 1 — Intro

Metrics turn a running system into numbers you can alert and chart on.
Use the four golden signals (latency, traffic, errors, saturation),
RED for request paths, USE for resources, and Prometheus histograms
for latency. Drive alerting from SLO burn rate, not raw thresholds.

## Level 2 — Overview

### Four golden signals (Google SRE)

These four cover the health of any request-serving system:

1. **Latency** — time to serve a request. Track success and failure
   separately; a fast 500 is not a healthy request.
2. **Traffic** — demand on the system: HTTP req/sec, messages
   consumed/sec, active connections.
3. **Errors** — explicit (HTTP 5xx), implicit (200 with wrong
   content), and policy violations (responses above SLA threshold).
4. **Saturation** — how full the system is: CPU, memory pressure,
   queue depth, thread pool. Useful saturation metrics predict
   exhaustion before it happens.

### RED method (request-driven services)

For APIs, web services, and microservices, track at every boundary:

- **Rate** — requests per second
- **Errors** — failed requests per second (or error percentage)
- **Duration** — latency distribution (p50, p95, p99 — never just the
  average)

### USE method (resources)

For CPU, memory, disk, network, and queues, track at every resource:

- **Utilization** — % of time the resource is busy or % capacity used
- **Saturation** — work queued or waiting (queue depth, swap usage)
- **Errors** — error events (disk errors, NIC drops, OOM kills)

### Prometheus metric types

| Type        | Use For                                    | Example                           |
|-------------|--------------------------------------------|------------------------------------|
| **Counter** | Monotonically increasing values            | `http_requests_total`              |
| **Gauge**   | Values that go up and down                 | `temperature_celsius`              |
| **Histogram**| Distribution of values in buckets         | `http_request_duration_seconds`    |
| **Summary** | Pre-calculated quantiles on the client     | `rpc_duration_seconds`             |

Use counters for anything you'll `rate()` over: requests, errors,
bytes. Use gauges for current state. Prefer histograms over summaries
in almost all cases — histograms aggregate across instances, summaries
do not. Suffix counters with `_total` and use unit suffixes
(`_seconds`, `_bytes`). See `references/metric-types.md` for code
examples and label cardinality guidance.

### Dashboard design

Start every service dashboard with the golden signals. Use p50/p95/p99
for latency, never just averages — p99 is often 10x worse than p50.
Layer dashboards: overview (all services) -> service detail ->
instance detail. Include deployment markers as vertical annotations.
For each downstream dependency, show a RED row so failures attribute
correctly.

## Level 3 — Full reference

### SLIs, SLOs, and SLAs

- **SLI (Service Level Indicator)** — a measure of service quality:
  "proportion of requests served in < 200ms"
- **SLO (Service Level Objective)** — a target for an SLI: "99.9% of
  requests served in < 200ms over 30 days"
- **SLA (Service Level Agreement)** — a contract with consequences for
  missing the SLO: "99.9% availability or customer credit"

Pick 3-5 SLIs reflecting user experience (availability, latency,
correctness). Set targets from user expectations, not system
capability. Track error budgets — if SLO is 99.9% you have 0.1% (43
min/month). When the budget is exhausted, freeze feature work and
focus on reliability.

### Alerting thresholds

1. Alert on **symptoms, not causes** — "error rate > 1%" rather than
   "CPU > 80%"
2. Use **SLO burn-rate** alerting — see the alerting-oncall skill
3. Set thresholds from **2 weeks of baseline** measurement, not guesses
4. Use **multi-window** alerting — fire only when both a short window
   (5 min) and a long window (1 hr) exceed the threshold
5. Avoid static thresholds on gauges — 85% CPU is fine for batch
   workloads and critical for latency-sensitive ones

### Instrumentation checklist

For any new service, instrument at minimum:

- Request rate, error rate, latency at every API endpoint
- Dependency call rate, error rate, latency for each downstream
- Queue depth and processing lag for any async work
- Connection pool utilization (active/idle/max)
- Application-specific business metrics (orders/sec, signups/day)
- Runtime metrics (GC pauses, thread count, heap usage)

### Label cardinality

Keep labels low-cardinality (< 10 values each in practice). Never use
user IDs, email addresses, or full request paths as label values. Use
bounded categories like `status="2xx"` rather than per-status-code.
A metric with 3 labels of 10 values each = 1,000 series; a 4th label
of 100 values = 100,000 series and Prometheus memory pain. See
`references/metric-types.md` for PromQL patterns covering rate,
error %, histogram quantiles, saturation, and burn-rate.
