---
name: logging-strategy
description: |
  Structured logging strategy — levels, correlation IDs, context propagation, PII avoidance. Use when designing a logging approach, reviewing log statements, setting up log aggregation (ELK, Loki, CloudWatch), adding correlation IDs to a distributed system, or deciding what to log and what to keep out.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-logging-strategy
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: observability
---

# Logging Strategy

## Intro

Good logs are structured, leveled, correlated, and free of secrets.
Pick a JSON logger, generate a `request_id` at every system boundary,
and propagate it through every downstream call. The cost of bad
logging is cost itself — most overspend comes from a few noisy
endpoints logged at INFO.

## Overview

### Log levels

Use levels intentionally. The semantic ladder:

1. **TRACE** — fine-grained diagnostic detail (loop iterations).
   Never on in production.
2. **DEBUG** — useful during development (SQL queries, cache hits,
   loaded config). Off by default in production.
3. **INFO** — normal operational events (service started, request
   handled, job completed). The default production level.
4. **WARN** — unexpected but recoverable (retry succeeded, deprecated
   API called, approaching rate limit). Not page-worthy.
5. **ERROR** — a failure that prevented an operation from completing.
   Should trigger an alert or ticket.
6. **FATAL** — process cannot continue (missing required config, port
   bound, unrecoverable state). Extremely rare.

When unsure between two levels, pick the lower one. Over-logging at
DEBUG is better than missing context at ERROR.

### Structured over unstructured

Always prefer structured logging (JSON or key-value pairs). Structured
logs are machine-parseable, searchable, and survive message format
changes. Every log line should include `timestamp` (ISO 8601 UTC),
`level`, `service`, `message`, and a `request_id` or `trace_id`. See
`references/structured-logging.md` for language-specific libraries.

### Correlation and context propagation

Generate a unique `request_id` (UUID or ULID) at the system boundary —
API gateway, message consumer, scheduled job. Propagate it through
every downstream call via headers (`X-Request-ID`) or message
metadata. Include it in every log line so you can correlate. In
distributed systems, also propagate `trace_id` and `span_id` (W3C
Trace Context). Use MDC or contextvars to avoid threading IDs through
every function signature.

### What to log

Request and response summaries (method, path, status, duration);
state transitions (order placed, payment processed); decision points
(why a branch was taken, which cache was hit); error details with
stack trace and the input that caused the failure; performance data
(query duration, queue depth); lifecycle events (start, config load,
graceful shutdown); retry attempts with attempt number and backoff;
external calls with downstream service, latency, and status.

### What NOT to log

- **PII**: names, emails, phone numbers, addresses, IP addresses
  (unless legally required and compliant)
- **Secrets**: passwords, API keys, tokens, session IDs, card numbers
- **Sensitive business data**: salary, health records, financial
  details
- **High-cardinality user input**: full request bodies — log a hash or
  a truncation instead
- When in doubt, mask: `email=b***@example.com`, `card=****1234`

## Full reference

### Common fields for every entry

| Field        | Description                          | Example                            |
|--------------|--------------------------------------|------------------------------------|
| `timestamp`  | ISO 8601 with timezone               | `2026-03-22T14:30:00.123Z`         |
| `level`      | Log severity                         | `info`, `error`, `debug`           |
| `service`    | Service or application name          | `order-service`                    |
| `message`    | Human-readable description           | `Order created successfully`       |
| `trace_id`   | Distributed trace identifier         | `4bf92f3577b34da6a3ce929d0e0e4736` |
| `span_id`    | Span within the trace                | `00f067aa0ba902b7`                 |
| `request_id` | Unique ID for the incoming request   | `req_01HXYZ...`                    |
| `duration_ms`| Operation duration in milliseconds   | `142`                              |
| `error`      | Error type or message (if applicable)| `ConnectionTimeout`                |

### Event naming convention

Use dot-delimited event names so logs are easy to filter:
`http.request.received`, `http.response.sent`, `db.query.executed`,
`cache.hit`, `cache.miss`, `order.created`, `order.cancelled`,
`auth.login.success`, `auth.login.failed`,
`queue.message.published`, `queue.message.consumed`. See
`references/structured-logging.md` for full language patterns
(structlog, pino, slog, tracing) and ELK/Loki ingestion examples.

### Aggregation and rotation

Ship logs to a centralized system (ELK, Grafana Loki, CloudWatch
Logs). Use JSON for ingestion and avoid multi-line messages where
possible. Set tiered retention: hot (7-30 days searchable), warm
(90 days), cold archive (1+ year if regulated). In containers, log to
stdout/stderr and let the orchestrator collect — never write to local
files. For VMs, rotate by size (100MB) or daily to prevent disk
exhaustion.

### Performance considerations

Logging has real cost — I/O, serialization, allocation. Use lazy
evaluation for expensive log arguments so debug strings are not built
when DEBUG is off. Avoid logging inside tight loops; aggregate counts
and log a summary after. Sample high-volume logs (e.g. 1 in 100 health
checks). Use async appenders so log I/O does not block requests.

### Anti-patterns

- **Log and throw** — logs the error, then logs it again at every
  caller. Choose one place to log
- **Everything at INFO** — buries the events that matter
- **String concatenation in log calls** — wastes CPU when level is
  off; use parameterized messages
- **`"Error occurred"`** with no context about what, where, or why
- **Mixing structured and unstructured** within the same service
- **Logging in a loop** — aggregate and log a summary
- **Timestamps without timezone** — always UTC, ISO 8601
- **Swallowing exceptions** — catching then logging only a generic
  message loses the stack trace
