---
argument-hint: "[--category=...] [--fix=... | --fix-all] [--since=<ref>] [--yes]"
allowed-tools: []
---

Use the pk-doctor skill to run the aggregator health check and print a
single report. Detect-only by default; `--fix=<cat>` or `--fix-all`
opts in to scoped repairs. After the run, emit one `doctor.report`
LogEntry via the event-log MCP tool.
