# Security — overview

Non-normative. The requirements are in `requirements.md`.

## Purpose

processkit serves content that agents treat as instructions, so its
security rests on keeping that content in the role of data: it is labelled
with kind and provenance, never executed or followed, and cannot change
tools, configuration, or access. This specification also fixes the
baseline defenses that span every feature: input size limits and bounded
failure on malformed input, no network or telemetry by default, signed
releases with verified installation, dependency hygiene, and defect
handling. It adds hardening for the one network transport, the read-only
shared server: Origin and request-isolation checks, no credentials in
command arguments or discovery responses, owner-only credential files, and
limits that project configuration cannot loosen. It spans the CLI
(PK1-P2), stdio serving (PK1-P3), and the shared server (PK1-P5).

## Boundaries

This slug does not cover:

- authenticators, TLS and authenticator prerequisites of the shared server,
  Roles, Bindings, deny-by-default authorization, filter-before-rank, and
  token pass-through — `access-control@v1`;
- configuration layering, closed configuration schemas, what project
  configuration may not configure (PK-CONFIG-002), result envelopes, logs,
  and redaction (PK-OUT-004) — `cli@v1`;
- repository paths, path containment (PK-STORE-013), the safe YAML subset
  and front matter contract (PK-STORE-012) — `repository-storage@v1`;
- MCP tool definitions fixed by the release (PK-MCP-024), request size,
  concurrency, and time limits (PK-MCP-040), and per-request isolation of
  results (PK-MCP-041) — `mcp-context-serving@v1`;
- locked commits, digests, and explicit fetch — `inheritance@v1`;
- skill scripts as labelled content (PK-SKILL-003) and credential values in
  catalog entries (PK-CAT-003) — `content-kinds@v1`.

## Governing decisions

- **C4** MCP is the agent interface: tool definitions are fixed by the
  release, so content cannot add or change tools.
- **C6** Inheritance through locked upstreams: upstream content is pinned
  by commit and digest, and fetching is explicit, the only network access
  outside the shared server.
- **C7** Consumed identity: processkit holds no identity and handles
  operator credentials only as files it reads, never as arguments.
- **C8** Two serving modes, read-only: stdio plus a TLS-only shared server;
  hardening targets only that HTTP transport.
- **C9** Catalog, not gateway: processkit never connects to catalogued
  servers or follows URLs in content.

## Provenance

| Baseline (#197) | This slug |
|---|---|
| `spec/doc/v1/09-security-configuration-and-output.md` — Threat model | threat table, PK-SEC-001 to 005 |
| 09 — Release trust | PK-SEC-010 to 012 |
| `11-verification-and-release.md` — PK-TEST-007 | basis of journeys 1 to 5 (PK-TEST-007 stays in documentation) |

PK-CONFIG-* and PK-OUT-* of chapter 09 are carried by `cli@v1`.

Gap items carried from the governance draft (tag
`archive/processkit-v1-governance-standards`):

| New ID | Source | Adaptation |
|---|---|---|
| PK-SEC-013 | `08-security-and-trust.md` PK-SEC-020 | Origin part only; TLS and authentication of every client are PK-ACC-030/011 in `access-control@v1`; accepted origins are OPEN-security-02 |
| PK-SEC-014 | 08 PK-SEC-020 | request-isolation part, made observable as "session identifier is not identity"; whether sessions exist is OPEN-security-03 |
| PK-SEC-015 | 08 PK-SEC-028 | command arguments and MCP discovery responses kept; repository configuration already covered by PK-CONFIG-002; "generated skill projections" dropped (C4: no generated harness outputs); redaction already PK-OUT-004 |
| PK-SEC-016 | 08 PK-SEC-028 | owner-only credential files; refusal and report made explicit as the observable effect |
| PK-SEC-017 | `14-performance-and-operations.md` PK-PERF-015 | "system/user authority" read as operator configuration and the invocation layer; "project policy" read as project configuration and repository content |

## Open questions

Mirrors `open` in `interfaces.yaml`.

1. OPEN-security-01 — default size limits, configuration keys, maximum
   diagnostic size.
2. OPEN-security-02 — accepted Origin values, requests without Origin,
   rejection response.
3. OPEN-security-03 — whether the shared server uses MCP sessions and how
   they bind to a principal.
4. OPEN-security-04 — signing scheme, trust anchor, installation command.
5. OPEN-security-05 — dependency record location and lockfile format.
6. OPEN-security-06 — which files are credential files; directory and group
   permissions.
7. OPEN-security-07 — diagnostic and exit codes of security failures.
8. OPEN-security-08 — whether `processkit lock` may use the network
   (baseline tension between PK-SEC-005 and PK-INH-002).
9. OPEN-security-09 — whether project configuration may tighten limits;
   release-defined hard ceilings.
10. OPEN-security-10 — definition of a credential value; how fetch passes
    upstream credentials to Git without arguments.
