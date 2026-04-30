---
apiVersion: processkit.projectious.work/v2
kind: Discussion
metadata:
  id: DISC-20260424_0101-DaringBird-how-should-mcp-servers
  created: '2026-04-24T01:01:25+00:00'
  updated: '2026-04-24T01:29:05+00:00'
spec:
  question: How should MCP servers pick up schema / PEP 723 dep changes without a
    full harness restart — watchdog hot-reload, an admin reload_schemas tool, both,
    or neither?
  state: resolved
  opened_at: '2026-04-24T01:01:25+00:00'
  participants:
  - TEAMMEMBER-cora
  outcomes:
  - DEC-20260424_0127-QuickPine-split-sharpbrook-ship-schema
  closed_at: '2026-04-24T01:29:05+00:00'
---

## Context

During the v0.19.2 cycle, each schema edit under `context/schemas/` and each PEP 723 dep edit under `context/skills/**/mcp/server.py` required a full harness restart before taking effect. Measured cost: one restart each for SteadyCedar (pyyaml dep) and BraveDove (5-schema alternation widening). DX impact: the feedback loop grew from <10s (offline test) to minutes (harness cycle), and stacked restart risk (each restart briefly drops MCP availability across all agents).

Scope: WorkItem BACK-20260424_0037-SharpBrook-mcp-servers-cache-schemas.

## Options under consideration

1. **Watchdog-based hot-reload** — each MCP server subscribes (via `watchdog` or inotify) to its schema dir and re-reads on change. Zero admin action needed. Risks: race with in-flight requests, partial-write visibility, silent reload failures.
2. **`reload_schemas` MCP tool** — explicit admin-invoked tool (callable from any agent session with permission) that re-reads schemas and re-executes the PEP 723 resolver. Predictable; serializable; requires an explicit call.
3. **PEP 723 dep re-resolve on dep-set delta** — server detects a header-hash change and re-invokes its own uv env before serving the next request. Narrower scope than (1): only addresses dep changes, not schema edits.
4. **Combination** — (2) as the near-term fix; (1) as a v0.next nice-to-have once reload semantics are proven safe.

## Key questions

- Who owns the reload invariant — each individual skill server, or a dedicated admin server?
- What happens to in-flight requests during a reload? Are they drained, retried, or rejected?
- How do we surface reload failures (partial reload) — a log event, a tool error, a health flag?
- Does the fix need to cover both dogfood (processkit) and consumer (derived projects via aibox) cycles, or only dogfood?
- What's the test strategy — can we exercise reload semantics under concurrent load in CI?

## Done when

Discussion emits one or more outcomes that scope the v0.21.0 implementation of SharpBrook concretely.
