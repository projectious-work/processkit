# MCP context serving — overview

Non-normative. The requirements are in `requirements.md`.

## Owner goal

The owner wants agents to get an organization's governance context from
one vendor-neutral place instead of copied instruction and skill files
(product definition; C4). The context must be small at connection time and
loadable on demand, so it does not crowd the agent's window. It must be
deterministic and cacheable, so personalization does not destroy server,
harness, or model caching (C5). It must stay read-only and filtered by
access, so one shared server can serve many readers safely (C7, C8).

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
- the ontology registry served by the `ontology` tool, and `status` —
  `ontology@v1`;
- the shared server's paths `/mcp` and `/healthz`, the access set and its
  digest, per-principal limits, and which verb each operation needs —
  `access-control@v1`;
- the lock, upstream fetch, overrides, and provenance — `inheritance@v1`;
- threat model, input size limits, configuration layering, and log
  redaction — `security@v1`;
- repository layout, the local cache directory, and the revision object —
  `repository-storage@v1`;
- catalogue entries that name a product toolkit profile — not in v1,
  pending owner decision on #204 P2.

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
profiles) as PK-MCP-051 to 057. PK-MCP-056 (the pinned profile set counts
as a normalized argument) is confirmed by owner decision #213 finding 1.
Lesson 1 of #204 (gateway-compatible identity) needs no change. P2
(catalogue toolkits) is not carried.

Owner decision #213 finding 2 changed PK-MCP-044: items that only a pin
leaves out are counted with a stable reference and listed only on request
(argument `excluded`, PK-MCP-072).

Gap row 5 (instruction versus reference trust on served content, governance
draft `16-agent-native-posture.md` PK-AGENT-020, 023, 024) is drafted as
PK-MCP-087. The owner has not decided it. It fits C4 and C5 because the
class is derived from kind and validation outcome only, and it fits the
prompt and tool injection rule of `agent-native-product-interfaces.md`
because content is instruction only after review and grants no authority.

Supporting context (not carried as requirements): the disclosure-level table
and PK-CONT-001/003/004 of `04-governance-content.md`; PK-STD-005
(always-on standards); PK-CLI-007 and the `processkit mcp serve` rows of
`06-cli.md`; PK-ACC-023/024/031/033 of `08-identity-and-access.md`;
PK-TEST-004/005 of `11-verification-and-release.md`.

## Resolved open items

| Item | Resolution | Basis |
|---|---|---|
| OPEN-mcp-context-serving-01 | Tool result envelope `schemas/tool-result.schema.json` (`apiVersion` `mcp.processkit.projectious.work/v1`, `revision`, `generation`, `data`, `diagnostics`), RFC 8785 text, `isError` on error diagnostics; `data.cacheKey`, `items[].basis`, `excluded`, `nextCursor`; entries carry `status` as ontology@v1 `listStatus`; cache hit and miss are log events only, so repeat results stay byte-identical; explain `applicability`; protocol versions and annotations (PK-MCP-058 to 060, 065, 066, 086). | agent proposal |
| OPEN-mcp-context-serving-02 | `get_context` level 0 or 1, default 0; `get` default 1, or 2 with `section`; `list` default limit 50, maximum `mcp.list-max-items` (default 200); out of range is `mcp-context-serving.invalid-argument`, never clamped (PK-MCP-061, 062). | agent proposal |
| OPEN-mcp-context-serving-03 | Opaque deterministic cursor bound to generation, access set, and arguments other than `limit`; earlier generation gives `cursor-stale`, other mismatch `cursor-invalid` (PK-MCP-063). | agent proposal |
| OPEN-mcp-context-serving-04 | `briefing.budget-bytes` in `processkit.toml`, UTF-8 bytes, default 16384, range 4096 to 1048576; fixed full, summarized, and fallback text forms (PK-MCP-069, 070). | agent proposal |
| OPEN-mcp-context-serving-05 | Operator keys `mcp.max-request-bytes`, `mcp.max-concurrent-requests`, `mcp.request-timeout-seconds`, `mcp.list-max-items`, each with default and ceiling; checked after authentication and access-control limits; JSON-RPC error with one diagnostic, at most 8192 bytes (PK-MCP-071, 081). | standard: security-and-software-supply-chain.md; agent proposal |
| OPEN-mcp-context-serving-06 | Resource `processkit:health` on both transports (no new tool); `GET /healthz` of access-control@v1 carries the same state; five checks with blocking or degrading effect; unavailable never passes (PK-MCP-088, 089). | agent proposal |
| OPEN-mcp-context-serving-07 | cli@v1 diagnostic shape and severities; `mcp-context-serving.*` code registry in `interfaces.yaml` `errors`; same codes as the CLI (PK-MCP-085). | agent proposal |
| OPEN-mcp-context-serving-08 | Pin exclusions: count and pinned-set digest, list only with `excluded` true; other exclusions listed with reason `profile`; unreadable items never reported; with `excluded` true, `list` pages exclusions with items against `limit` (PK-MCP-044, 072, 073, 091). | owner decision: #213 finding 2; agent proposal |
| OPEN-mcp-context-serving-09 | Items without declared profiles and `*` items are within any pin; unknown `--profile` refuses to start, unknown `profiles` argument fails; caller profiles outside the pin narrow to nothing with a warning; `profiles` key in `processkit.toml` (PK-MCP-074 to 076, 090). | agent proposal |
| OPEN-mcp-context-serving-10 | Operator key `mcp.group-profiles`; `--profile` replaces group defaults; several groups give the union; stdio ignores it (PK-MCP-077). | agent proposal |
| OPEN-mcp-context-serving-11 | Normalization rules (task as sorted word set, sorted profiles, paths, kinds, defaults filled, pinned set added); cache key `sha256:` over the RFC 8785 preimage; access set and its digest from access-control@v1, request time not an input (PK-MCP-078 to 080). | agent proposal |
| OPEN-mcp-context-serving-12 | `validate` `content` is the complete draft text; prompt names use the ontology@v1 reference form; resources return the level-1 `get` data (PK-MCP-064, 067, 068). | agent proposal |
| OPEN-mcp-context-serving-13 | Declared word-subset matching of triggers and label values against the task, profile, path (local source path), and always-on bases; order by basis tier, kind, namespace, name; no scores (PK-MCP-082 to 084). | agent proposal |
| OPEN-mcp-context-serving-14 | Reference host, seeded corpus, and percentile method in `performance.method`; results in release evidence (PK-PERF-004). | agent proposal |
| OPEN-mcp-context-serving-15 | Per-request change check; every result carries `generation`, a content-derived digest (PK-MCP-092). | agent proposal |
