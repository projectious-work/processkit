# Security — overview

Non-normative. The requirements are in `requirements.md`.

## Owner goal

The owner wants organizations to trust processkit with the rules their
agents follow (product definition, "Purpose"; C4). That trust holds only
if served content stays data that cannot change tools, configuration,
or access, and only if processkit adds no new way to leak credentials or
reach the network. The owner also wants the one network transport, the read-only
shared server (C8), to be safe to expose with fixed, testable defaults
that a repository cannot weaken, and wants every release to be verifiable
before installation.

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
  catalog entries (PK-CAT-003) — `content-kinds@v1`;
- an instruction or reference trust tag on served content —
  `mcp-context-serving@v1`.

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
- **Owner decision #213 finding 3 (2026-11-08)** "fetch, then lock":
  `processkit lock` uses no network (PK-SEC-018); recorded in
  `docs/adr/0002-lock-resolves-from-fetched-data.md`.
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
| PK-SEC-013 | `08-security-and-trust.md` PK-SEC-020 | Origin part only; TLS and authentication of every client are PK-ACC-030/011 in `access-control@v1`; accepted origins are PK-SEC-023 |
| PK-SEC-014 | 08 PK-SEC-020 | request-isolation part, made observable as "session identifier is not identity"; the stateless transport is PK-SEC-024 |
| PK-SEC-015 | 08 PK-SEC-028 | command arguments and MCP discovery responses kept; repository configuration already covered by PK-CONFIG-002; "generated skill projections" dropped (C4: no generated harness outputs); redaction already PK-OUT-004 |
| PK-SEC-016 | 08 PK-SEC-028 | owner-only credential files; refusal and report made explicit as the observable effect |
| PK-SEC-017 | `14-performance-and-operations.md` PK-PERF-015 | "system/user authority" read as operator configuration and the invocation layer; "project policy" read as project configuration and repository content |

## Resolved open items

| Item | Resolution | Basis |
|---|---|---|
| OPEN-security-01 | Parser limits `limits.file-bytes` 1 MiB, `limits.nesting-depth` 64, `limits.collection-items` 10 000, `limits.string-bytes` 256 KiB; configuration files fixed at 1 MiB; transport limits `transport.max-header-bytes` 16 KiB, `transport.header-timeout-seconds` 10, `transport.idle-timeout-seconds` 60, `transport.max-connections` 256; operator configuration only; a bounded diagnostic is one per input, quotes no input, and is at most 4096 bytes (PK-SEC-019 to 022, PK-SEC-025). MCP request limits stay with `mcp-context-serving@v1`. | agent proposal |
| OPEN-security-02 | Requests without `Origin` are accepted; listed origins in `transport.allowed-origins` (default empty) are accepted; others get HTTP 403 `security.origin-rejected` before authentication; no CORS; fixed response headers; JSON-RPC rejection body (PK-SEC-023, PK-SEC-026, `schemas/http-rejection.schema.json`). | standard: agent-native-product-interfaces.md#Transport and deployment; agent proposal |
| OPEN-security-03 | Stateless Streamable HTTP: no `Mcp-Session-Id` is issued; a request carrying one gets HTTP 404 `security.session-rejected`; non-POST gets 405 (PK-SEC-024). | agent proposal |
| OPEN-security-04 | Sigstore keyless bundles per artifact, identity of the `release.yml` workflow at the release tag, issuer GitHub Actions; documented installation verifies with `sigstore verify identity` before `uv tool install` (PK-SEC-030). | standard: security-and-software-supply-chain.md#Release supply chain; agent proposal |
| OPEN-security-05 | `uv.lock` committed and checked with `uv lock --check`; dependency record in `docs/dependencies.md` (PK-SEC-031). | standard: security-and-software-supply-chain.md#Dependency policy; agent proposal |
| OPEN-security-06 | Credential files are operator-named files with secret material (v1: the TLS private key); refused if any group or other read or write bit is set, after following links; directory not checked; `security.credential-file-permissions`, exit 3 (PK-SEC-029). | agent proposal |
| OPEN-security-07 | `security.limit-exceeded` and `security.malformed-input` (validation, exit 1), `security.credential-file-permissions` (environment, exit 3), HTTP rejection codes with fixed statuses; reuse of `cli.config-*` and `cli.upstream-not-fetched`; release verification failure is the verifier's exit status (`interfaces.yaml` `errors`). | agent proposal |
| OPEN-security-08 | `processkit lock` uses no network and resolves only from the local cache (PK-SEC-018, `cli@v1` PK-CLI-044); PK-SEC-005 unchanged; ADR `docs/adr/0002-lock-resolves-from-fetched-data.md`. | owner decision: #213 finding 3 (2026-11-08) |
| OPEN-security-09 | Project configuration may not set a limit, also not a lower one (`cli.config-forbidden-key`); each limit has a release ceiling; values outside 1..ceiling fail with `cli.config-invalid-value`, never clamped (PK-SEC-019, PK-SEC-020). | standard: application-configuration.md#Authority is separate from precedence; agent proposal |
| OPEN-security-10 | Credential value defined in `interfaces.yaml` (`credentials.credential_value`); bearer credentials only in the `Authorization` header, `access_token` query rejected (PK-SEC-027); processkit passes no credentials to Git, Git uses its own credential configuration; URL user information in an upstream source is `cli.config-forbidden-key` (PK-SEC-028). | agent proposal |
