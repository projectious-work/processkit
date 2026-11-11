# Identity and access control — overview

Non-normative. The requirements are in `requirements.md`; the interface
catalog is `interfaces.yaml`; document shapes are in `schemas/`.

## Owner goal

The owner wants one processkit installation to serve a company's governing
repository to many people and agents with different rights (product
definition, "Repository roles" and "Users"; C7). Identity stays in the
organization's existing identity provider and certificate authority, so
processkit adds no identity system to run or secure. Who may read what is
ordinary content that is reviewed through Git, like every other rule. The
shared server must never reveal what a caller may not read, and stdio must
not pretend to protect anything (C8).

## Purpose

One processkit installation can serve people and agents with different
rights. Access control follows the Kubernetes pattern deliberately, without
depending on Kubernetes: pluggable authenticators turn a request into a
principal, and additive, deny-by-default rules decide what that principal
may read. Identity is consumed, never managed: identity providers,
certificate authorities, and credential issuance stay in the operator's
infrastructure, and authenticators are configured only by the operator.

Access rules are ordinary ontology content reviewed through Git. A Role
declares rules (verbs on kinds, optionally narrowed by names or a label
selector); a `grants-role` Binding grants one Role to a user or group
principal, scoped to a Container (and its descendants) and bounded in time.
Every read surface on the shared server filters before ordering, counting,
and truncation, so forbidden items are indistinguishable from missing ones.

Access control protects confidentiality only on the shared server. Over
stdio and in the CLI the caller already holds the working copy, so the
local principal sees everything.

## Boundaries

| Not covered here | Covered by |
|---|---|
| label-selector grammar, Containers, the Container tree, the envelope, typed references, relation types and their endpoint checks | ontology@v1 |
| where Role, Binding, and Container files live; serialization | repository-storage@v1 |
| the MCP tools, briefing, context assembly, caching, MCP resources, health states and checks, and per-request size, concurrency, and time limits | mcp-context-serving@v1 |
| command structure, result envelope, diagnostics, exit codes, configuration layering, `validate`, `config show`, log records, redaction | cli@v1 |
| upstream access rules, import of upstream Roles and Bindings, restricted inherited items | inheritance@v1 |
| threat model, transport hardening and its check order, credential files, limit configuration rules | security@v1 |

## Governing decisions

- **C7 — Kubernetes-pattern access control with consumed identity:** the
  four authenticators, operator-only configuration, additive deny-by-default
  rules on Roles granted by `grants-role` Bindings scoped to Containers.
- **C8 — Two serving modes, read-only:** stdio for a working copy and a
  TLS-only, authenticated shared server; access control is a shared-server
  concern.
- **C10 — Python, one application core:** the principal is an input to the
  core and the thin CLI and MCP adapters make no access decisions.
- **Owner decision #213 finding 5:** the Role and Binding JSON Schemas live
  here (`schemas/role.schema.json`, `schemas/binding.schema.json`). As
  ontology@v1 decided, a Binding keeps `spec.relation`, `subject`,
  `target`, `scope`, and `validity` for every relation type; scope is
  allowed only on `grants-role`; a Binding scoped to the root Container
  names `Container/root` (PK-ACC-041).

## Provenance

Baseline (`spec/doc/v1`, #197):

- `08-identity-and-access.md`, all sections (introduction, Identity,
  Authorization, Shared server): PK-ACC-001, PK-ACC-010 to PK-ACC-018,
  PK-ACC-020 to PK-ACC-027, PK-ACC-030 to PK-ACC-033. The authenticator
  table and the Role and Binding JSON examples are carried into
  `interfaces.yaml`.
- `01-product-definition.md`: PK-PROD-011.
- `11-verification-and-release.md`: release journey 6 is J1; the negative
  cases of PK-TEST-006 are J2 to J6 (PK-TEST-006 itself stays in the
  verification documentation).
- `06-cli.md`: the `access whoami|can-i` and `mcp serve --http` command rows
  (also in cli@v1).

Gap row 8 from the governance draft (tag
`archive/processkit-v1-governance-standards`,
`13-standard-entity-types.md`), carried as agent proposals and accepted by
owner decision 2026-11-11 (#212):

| Source | Carried as | Not carried, and why |
|---|---|---|
| PK-ENTITY-100 (Role: responsibilities, required capabilities or skills, default scope) | `spec.responsibilities` required; `spec.capabilities` (informational references to Capability or Skill) — PK-ACC-040 | default scope: ontology@v1 and finding 5 make scope explicit on every `grants-role` Binding |
| PK-ENTITY-101 (supersession instead of silent reinterpretation) | — | v1 evaluates the Roles of the served Git revision; Git history is the version record |
| PK-ENTITY-120 (Binding: relation type, subject, target, optional scope, validity, conditions, description) | `spec.description`; `spec.validity.from` next to `until` — PK-ACC-041 | conditions: v1 has no condition language and keeps rules additive |
| PK-ENTITY-121 (registry endpoint, cardinality, inverse, temporal rules) | temporal rule `from` before `until` (`access.invalid-validity`); endpoint and cardinality stay ontology@v1 PK-MODEL-070 | inverse: derived from the registry, never stored |

## Resolved contradictions

**Impersonation versus the v1 verbs (PK-ACC-027 and PK-ACC-022).**
`can-i --as` needs an explicit grant, but Role rules can grant only `get`
and `list`. Resolution (agent proposal, PK-ACC-042): impersonation is a
separate privilege, logged with the verb `impersonate`. Only the operator
key `access.impersonators` grants it; no Role can. `can-i` runs locally, so
the operator configuration named by `--config` is the grant. Alternative:
add `impersonate` as a third Role verb, Kubernetes style, with a rule form
that names users and groups instead of kinds. It is not chosen because it
changes PK-ACC-022, needs a second rule shape, and lets repository content
decide who may act as another identity, which PK-ACC-011 keeps with the
operator.

**Request-time validity versus deterministic assembly (PK-ACC-021 and
mcp-context-serving@v1 PK-MCP-030).** Resolution (agent proposal,
PK-ACC-043, PK-ACC-044): processkit reads the clock once per request when
authorization runs, before assembly. The request time decides token and
Binding validity and so the access set. Assembly and the cache key use the
access set and its digest, never the time. Two requests at different times
with the same access set are byte-identical; a Binding that expires changes
the access set, and so the cache key. Alternative: snapshot validity per
served generation and start a new generation at each validity boundary. It
is not chosen because it makes generations depend on the clock.

mcp-context-serving@v1 needs to state, for wave 3:

1. PK-MCP-030: "the caller's access set" is the access set of
   access-control@v1 (`access_set`, PK-ACC-044), computed once per request
   before assembly; the request time is an authorization input only and is
   not an assembly input.
2. PK-MCP-032: the access-set digest in the cache key is the digest of
   access-control@v1 `access_set.digest`.
3. One request uses one access set from start to end, as it uses one
   generation (PK-MCP-042).
4. The health states and checks behind `GET /healthz` (PK-ACC-052,
   `schemas/health.schema.json`) are those of PK-MCP-046 and PK-MCP-047;
   the shared server serves MCP at `/mcp` (PK-ACC-055).
5. Its request limits (PK-MCP-040) run after authentication and the
   access limits (`http_endpoints.request_order`).
6. "Readable" in PK-MCP-045 means the verb of
   `authorization.operation_declarations` for the reporting operation.

## Resolved open items

| Item | Resolution | Basis |
|---|---|---|
| OPEN-access-control-01 | Operator keys `tls.*`, `auth.*`, `access.impersonators`, `limits.principal-*`, `limits.server-requests-per-minute` (`interfaces.yaml` `operator_configuration`); `tls.private-key` is a credential file (PK-SEC-029); limit keys follow PK-SEC-019 and PK-SEC-020; chain with accept, reject, abstain, and anonymous only when all abstain; invalid client certificates fail the TLS handshake; `/mcp`, `/healthz`, RFC 9728 metadata, HTTP 401 `access.unauthenticated` (PK-ACC-034, PK-ACC-035, PK-ACC-038, PK-ACC-055). | agent proposal |
| OPEN-access-control-02 | OIDC user claim `sub`, groups claim `groups`, both configurable; discovery for keys; asymmetric algorithms only; 60 s skew; audience is the resource identifier. `local` asserts the login name and no groups; anonymous is `system:anonymous` (PK-ACC-036, PK-ACC-037). | agent proposal |
| OPEN-access-control-03 | Headers `X-Remote-User` and `X-Remote-Group` (configurable); a proxy is a client certificate from `auth.trusted-proxy.ca-bundle` with a CN in `auth.trusted-proxy.allowed-names` (PK-ACC-039). | agent proposal |
| OPEN-access-control-04 | `schemas/role.schema.json`: `names` narrows a rule; kinds, verbs, names, and selector combine by AND; no wildcards (PK-ACC-040). | agent proposal; gap row 8 accepted by owner 2026-11-11 (#212) |
| OPEN-access-control-05 | `schemas/binding.schema.json`: subject `User` or `Group`; validity optional with `from` (inclusive) and `until` (exclusive); scope required on `grants-role`; target and scope accept the typed-reference forms of ontology@v1 (PK-ACC-041). | owner decision: #213 finding 5; agent proposal; gap row 8 accepted by owner 2026-11-11 (#212) |
| OPEN-access-control-06 | Verb per tool, resource and prompt operation, briefing part, and command (`authorization.operation_declarations`, PK-ACC-045). | agent proposal |
| OPEN-access-control-07 | Separate `impersonate` privilege from `access.impersonators` (PK-ACC-042); `can-i` evaluates the local working copy (PK-ACC-047); the local principal is never evaluated (PK-ACC-046). | agent proposal |
| OPEN-access-control-08 | `get` resolves against the access set; medians of forbidden and missing differ by at most 2 ms over 1000 interleaved requests (PK-ACC-049). | agent proposal |
| OPEN-access-control-09 | `schemas/can-i-result.schema.json`; exit 0 for allow and deny (PK-ACC-047). | agent proposal |
| OPEN-access-control-10 | In scope: `whoami` reports `schemas/principal.schema.json`; in the CLI always the local principal (PK-ACC-048). | agent proposal |
| OPEN-access-control-11 | Ordered start-up checks with `access.tls-not-configured`, `access.no-authenticator`, `access.config-missing-key` (exit 1), `security.credential-file-permissions`, `access.file-unusable`, `access.oidc-unavailable`, `access.listen-failed` (exit 3) (PK-ACC-050). | agent proposal |
| OPEN-access-control-12 | Per-principal rate (600/min) and concurrency (8), per-server rate (6000/min); HTTP 429 `access.principal-limit` or `access.server-limit` with `Retry-After` (PK-ACC-051). | agent proposal |
| OPEN-access-control-13 | `GET /healthz`, body `{"status": ...}` only, 200 or 503 (PK-ACC-052). | agent proposal |
| OPEN-access-control-14 | `schemas/access-log-record.schema.json`; events `access.decision` (one per item and verb decided) and `access.impersonation`; outcome `allow` or `deny`; not filtered by log level (PK-ACC-053). | agent proposal |
| OPEN-access-control-15 | Reuse `ontology.unresolved-reference`, `ontology.relation-endpoint`, `ontology.invalid-selector`; add `access.invalid-validity` and `access.schema-violation` (PK-ACC-054). | agent proposal |
| OPEN-access-control-16 | Clock read once per request at authorization; time decides the access set, not assembly; access-set digest defined (PK-ACC-043, PK-ACC-044). | agent proposal |

## Notes for review

- User and group names are matched without the authenticator. An operator
  who trusts several authenticators should keep their identifier spaces
  apart (for example e-mail addresses in OIDC and service names in x509).
- One decision record per item and verb is verbose for `list` and
  `get_context`. The alternative, one record per request, does not fit the
  single `name` and granting Binding that PK-ACC-026 requires.
- `can-i` answers `deny` with exit 0. `kubectl auth can-i` exits 1 instead,
  but cli@v1 reserves exit 1 for validation failures.
