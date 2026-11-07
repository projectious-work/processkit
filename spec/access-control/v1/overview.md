# Identity and access control — overview

Non-normative. The requirements are in `requirements.md`; the interface
catalog is `interfaces.yaml`.

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
stdio the caller already holds the working copy, so the local principal
sees everything.

## Boundaries

| Not covered here | Covered by |
|---|---|
| label-selector grammar, Containers, the Container tree, the envelope, typed references, relations | ontology@v1 |
| where Role, Binding, and Container files live | repository-storage@v1 |
| the MCP tools, briefing, context assembly, caching, MCP resources, and per-request runtime limits | mcp-context-serving@v1 |
| command structure, result envelope, exit codes, `validate`, `config show` | cli@v1 |
| upstream access rules, import of upstream Roles and Bindings, restricted inherited items | inheritance@v1 |
| threat model, shared-server transport hardening, configuration layering, log sinks and redaction patterns | security@v1 |

## Governing decisions

- **C7 — Kubernetes-pattern access control with consumed identity:** the
  four authenticators, operator-only configuration, additive deny-by-default
  rules on Roles granted by `grants-role` Bindings scoped to Containers.
- **C8 — Two serving modes, read-only:** stdio for a working copy and a
  TLS-only, authenticated shared server; access control is a shared-server
  concern.
- **C10 — Python, one application core:** the principal is an input to the
  core and the thin CLI and MCP adapters make no access decisions.

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

Gap items carried from the governance draft: none. The governance draft's
field contracts for Role and Binding are not carried; they await an owner
decision and are recorded as open questions.

## Open questions

Mirrors `interfaces.yaml` `open`.

- **OPEN-access-control-01:** operator-configuration keys and format for
  the authenticator chain, issuers, audiences, CAs, revocation lists, proxy
  identities, TLS material, and anonymous access.
- **OPEN-access-control-02:** OIDC user and group claims; the identity the
  `local` authenticator asserts.
- **OPEN-access-control-03:** trusted-proxy header names and proxy
  identification.
- **OPEN-access-control-04:** full Role access-rule schema, including the
  names field and wildcard handling.
- **OPEN-access-control-05:** full Binding schema: subject principal values,
  validity fields, optionality, namespaced references.
- **OPEN-access-control-06:** the verb and kinds each tool and command
  declares.
- **OPEN-access-control-07:** how the impersonation grant is expressed with
  only `get` and `list` verbs, and where `can-i` evaluates.
- **OPEN-access-control-08:** the documented timing bound and its
  measurement.
- **OPEN-access-control-09:** `can-i` result fields and exit code on deny.
- **OPEN-access-control-10:** output and ownership of `access whoami`.
- **OPEN-access-control-11:** diagnostic and exit code when the shared
  server refuses to start.
- **OPEN-access-control-12:** per-principal and per-server limits, defaults,
  and the over-limit response.
- **OPEN-access-control-13:** health endpoint path and response.
- **OPEN-access-control-14:** decision-log field keys and granularity.
- **OPEN-access-control-15:** diagnostic codes of access validation errors.
- **OPEN-access-control-16:** how request-time Binding validity combines
  with time-independent deterministic assembly.
