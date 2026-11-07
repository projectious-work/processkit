# MCP context serving — overview

Non-normative. The requirements are in `requirements.md`.

## Purpose

MCP is processkit's agent interface. A harness connects to the processkit
MCP server and obtains the organization's governance context from it,
instead of from copied instruction and skill files: a bounded level-0
briefing at connection time, then items loaded on demand one level at a time
through six fixed, read-only tools. Context is assembled per request from
the revision, the lock, the caller's access set, and normalized arguments
only, so equal requests give byte-identical, cacheable output.

This specification also adds, beyond the #197 baseline: reporting of items
excluded by profile or applicability (limited to what the caller may read),
the health and diagnostics contract that the baseline's PK-MCP-043 names,
deterministic pagination with documented limits, and serve-time pinned
profiles (issue #204, P1).

A typical project agent uses both serving modes: the project's processkit
over stdio, which inherits upstream content through the lock, or the
company's shared server directly when the project has no processkit
configuration of its own.

## Boundaries

This slug does not cover:

- authenticators, Roles, Bindings, access decisions, the shared server's
  TLS and startup refusal, per-principal limits, and the content limits of
  the unauthenticated health endpoint — `access-control@v1`;
- the content kinds, their schemas, disclosure-level contents, `summary` and
  `triggers`, served-item identity fields, and invalid-item reporting —
  `content-kinds@v1`;
- command syntax, `processkit context` equivalence with `get_context`,
  `--json` envelopes, and exit codes — `cli@v1`;
- the ontology registry served by the `ontology` tool — `ontology@v1`;
- the lock, upstream fetch, overrides, and provenance — `inheritance@v1`;
- threat model, input size limits, configuration layering, and log
  redaction — `security@v1`;
- repository layout and the local cache directory — `repository-storage@v1`.

## Governing decisions

- **C4** MCP is the agent interface: the briefing replaces always-on
  instructions; skills and standards load on demand; no harness outputs.
- **C5** Deterministic, cacheable assembly: revision, lock, access set, and
  normalized arguments only; stable order; shared content first.
- **C6** Inheritance through locked upstreams: the lock is an assembly and
  cache-key input.
- **C7** Kubernetes-pattern access control: the access set is an assembly
  input; excluded-item reports and pinning never reveal or grant access.
- **C8** Two serving modes, read-only: stdio and the shared server; neither
  writes; no daemon or proxy.
- **C9** A catalog of trusted MCP servers, not a gateway: catalogued servers
  are indexed and served, never invoked.
- **C10** Python, one application core: MCP is a thin adapter, equivalent to
  the CLI.

## Provenance

| Baseline (#197) | This slug |
|---|---|
| `spec/doc/v1/07-mcp-and-context-assembly.md` — Serving modes | PK-MCP-001 to 003 |
| 07 — Connection briefing | PK-MCP-010 to 012 |
| 07 — Tools | PK-MCP-020 to 024 |
| 07 — Assembly and caching | PK-MCP-030 to 034 |
| 07 — Runtime | PK-MCP-040 to 043 |
| `11-verification-and-release.md` — Performance | PK-PERF-001 to 003 |
| 11 — Acceptance journeys 5 and 7 | journeys 1 and 2 |
| `01-product-definition.md` — Goals | PK-PROD-004, 006, 007, 008, 014 |
| `01-product-definition.md` — Non-goals | PK-PROD-022, 023, 025 |

Gap items carried from the governance draft (tag
`archive/processkit-v1-governance-standards`):

| New ID | Source | Notes |
|---|---|---|
| PK-MCP-044, 045 | `04-content-packages-and-extensions.md` PK-STD-011; `06-agent-protocol-and-query-surface.md` PK-MCP-053 | generalized from standards to all kinds; restricted to items the caller may read; invalid-item reporting stays in `content-kinds@v1` (PK-CONT-011) |
| PK-MCP-046, 047 | `14-performance-and-operations.md` PK-OPS-002 | `recovery_required` state dropped (no journals or recovery under C1) |
| PK-MCP-048 | `14-performance-and-operations.md` PK-OPS-003 | "optional registered reconciler" dropped for the same reason |
| PK-MCP-049, 050 | `14-performance-and-operations.md` PK-PERF-010; `06-agent-protocol-and-query-surface.md` PK-MCP-011 | limited to `list`, the only paginated tool; draft PK-MCP-011 is unrelated to baseline PK-MCP-011 (briefing budget) |

Owner-accepted proposal carried: issue #204, section P1 (serve-time pinned
profiles) as PK-MCP-051 to 057. PK-MCP-056 is a reconciliation, not proposal
text: PK-MCP-030 forbids any assembly input besides revision, lock, access
set, and normalized arguments, so the pinned set is treated as part of the
normalized arguments. Lesson 1 of #204 (gateway-compatible identity) needs
no change and P2 (catalogue toolkits) is not carried.

Supporting context (not carried as requirements): the disclosure-level table
and PK-CONT-001/003/004 of `04-governance-content.md`; PK-STD-005
(always-on standards); PK-CLI-007 and the `processkit mcp serve` rows of
`06-cli.md`; PK-ACC-023/024/031/033 of `08-identity-and-access.md`;
PK-TEST-004/005 of `11-verification-and-release.md`.

## Open questions

Mirrors `open` in `interfaces.yaml`.

1. OPEN-mcp-context-serving-01 — result field names (basis, cache key,
   revision, excluded items, cursor, cache-hit indicator).
2. OPEN-mcp-context-serving-02 — default `level`; default and maximum
   `list` limit.
3. OPEN-mcp-context-serving-03 — cursor format; stale cursor after a
   generation change.
4. OPEN-mcp-context-serving-04 — briefing budget key, unit, default, and
   summarized form.
5. OPEN-mcp-context-serving-05 — request limit keys, defaults, and the
   over-limit diagnostic.
6. OPEN-mcp-context-serving-06 — how health is exposed over stdio and the
   shared server without a new tool; checks and their mapping to states.
7. OPEN-mcp-context-serving-07 — diagnostic code registry and severity
   values.
8. OPEN-mcp-context-serving-08 — excluded-item reason codes; whether
   pin-excluded items are reported; bounds.
9. OPEN-mcp-context-serving-09 — profile-less items under a pin; unknown
   pinned profile; empty intersection with caller profiles.
10. OPEN-mcp-context-serving-10 — group default pinned profiles: key,
    precedence with `--profile`, multiple groups.
11. OPEN-mcp-context-serving-11 — argument normalization and cache-key
    format.
12. OPEN-mcp-context-serving-12 — `validate` content encoding; prompt name
    form.
13. OPEN-mcp-context-serving-13 — matching free-text `task` to declared
    triggers without lexical ranking; ranking weights.
14. OPEN-mcp-context-serving-14 — reference host and measurement method for
    performance objectives.
15. OPEN-mcp-context-serving-15 — generation reporting and cache change
    detection.
