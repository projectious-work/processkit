# Identity and access control — acceptance journeys

Each journey runs against the exact release-candidate artifacts in a
temporary Git repository with synthetic content, synthetic identity
infrastructure (a test OIDC issuer, a test certificate authority, and where
needed a test reverse proxy), and no ambient credentials or user
configuration. Configuration keys, OIDC claim names, proxy header names,
diagnostic codes, the health endpoint path, and the timing bound are open
(see `interfaces.yaml` `open`); until they are fixed, a journey checks the
outcome and the absence or presence of the stated information.

Common fixture, used by J1 to J9: a governing repository with Containers
`company` (root) and `engineering` (child of `company`) and `finance` (child
of `company`); Standards `eng-std` in `engineering` with label
`sensitivity=internal`, `eng-secret` in `engineering` with label
`sensitivity=confidential`, and `fin-std` in `finance`; `eng-std`
references `fin-std`. Role `standards-reader` as in the baseline example
(kinds Standard, ProcessSpecification, Skill; verbs get, list; selector
`sensitivity notin (confidential)`). Binding `engineering-reads-standards`
grants that Role to group `engineering@example.com`, scoped to
`Container/engineering`, valid until a future time. Binding `ops-reads-all`
grants a Role with rules for all three kinds and no selector to the x509
group `ops`, scoped to `Container/company`.

## J1 — Two principals receive different, correctly filtered context

Baseline release journey 6. Preconditions: the common fixture; operator
configuration (outside the repository) enables `oidc` (test issuer,
audience `processkit`) and `x509` (test CA) and TLS with operator-supplied
key and certificate.

Steps:

1. Start `processkit mcp serve --http --listen 127.0.0.1:PORT`.
2. Connect principal A with a valid OIDC token whose group claim is
   `engineering@example.com`; read the briefing; call `list(kind=Standard)`,
   `get(Standard, eng-std)`, `get(Standard, eng-secret)`,
   `get(Standard, fin-std)`, and `get_context()`.
3. Connect principal B with a valid client certificate with subject
   `CN=ci-bot, O=ops`; repeat step 2's calls.

Expected results:

- Step 1 starts the server, which reports the working-copy revision.
- A: the briefing, `list`, and `get_context` contain `eng-std` only;
  `list` reports one item; `get` of `eng-secret` and `fin-std` returns the
  same result as a missing item; `eng-std`'s reference to `fin-std` is
  unresolved without `fin-std`'s title, labels, or content.
- B: the briefing, `list`, and `get_context` contain all three Standards;
  every `get` succeeds; the reference resolves.
- A's and B's results differ only by the filtered items; both report the
  same revision.

Covers: PK-PROD-011, PK-ACC-012, PK-ACC-013, PK-ACC-014, PK-ACC-021,
PK-ACC-023, PK-ACC-024, PK-ACC-031

## J2 — OIDC rejects invalid tokens

Preconditions: J1's server running with `oidc` as the only
non-`local` authenticator in the chain, anonymous access off.

Steps: call `list(kind=Standard)` with, in turn: no token; an expired token;
a token whose not-before is in the future; a token for another audience; a
token from another issuer; a token with an invalid signature. Also request
the server's OAuth protected-resource metadata as defined by the MCP
authorization specification for the supported MCP version.

Expected results:

- Every request is rejected; no request returns item data, item names, or
  counts; the operational log shows no bearer material.
- The protected-resource behavior (metadata and challenge on rejection)
  conforms to the MCP authorization specification.
- A valid token for the same principal is accepted afterwards.

Covers: PK-ACC-012, PK-ACC-013, PK-ACC-016

## J3 — x509 rejects untrusted, expired, and revoked certificates

Preconditions: J1's server with `x509` configured with the test CA and a
revocation list containing certificate R.

Steps: connect with, in turn: a certificate from an untrusted CA; an
expired certificate; a certificate not yet valid; a certificate without
client-authentication usage; certificate R; then a valid certificate.

Expected results:

- The first five connections are rejected without item data.
- The valid certificate is accepted; its principal's user is the subject CN
  and its groups the subject O, as shown by the decision log.

Covers: PK-ACC-012, PK-ACC-014

## J4 — Spoofed proxy identity headers are ignored

Preconditions: the server configured with `trusted-proxy` (accepting proxy
P identified by its client certificate) followed by `oidc`; a test proxy P.

Steps:

1. Through P, send a request whose proxy-supplied identity is principal B.
2. Directly (no client certificate), send a request carrying identity
   headers naming principal B and no token.
3. Directly with a client certificate from the test CA that does not
   identify P, send identity headers naming principal B.
4. Directly, send identity headers naming principal B plus principal A's
   valid OIDC token.

Expected results:

- 1: accepted as principal B.
- 2 and 3: rejected; the headers are not used as identity.
- 4: accepted as principal A, never B; the response is filtered for A.

Covers: PK-ACC-012, PK-ACC-015

## J5 — Anonymous access

Steps:

1. With anonymous access not configured, send an unauthenticated request.
2. Configure anonymous access; add a Binding granting a Role to group
   `system:unauthenticated` for `eng-std` only; restart; send an
   unauthenticated request and call `list(kind=Standard)`.

Expected results:

- 1: rejected.
- 2: accepted; the decision log records a principal whose only group is
  `system:unauthenticated`; only `eng-std` is listed.

Covers: PK-ACC-012, PK-ACC-020, PK-ACC-021

## J6 — Forbidden items do not leak through any surface

Preconditions: J1's server; principal A; additionally `eng-secret` made
invalid in a second run, and a third Standard `aa-secret` in `engineering`
labelled `sensitivity=confidential`, so that it is forbidden to A and would
precede `eng-std` in a name-based stable order.

Steps: as principal A, call `list(kind=Standard, limit=1)` and follow the
cursor; `list` with a selector matching only forbidden items; `get` of a
forbidden item and of a never-existing name (compare byte for byte apart
from the requested name); read the forbidden item's MCP resource URI;
`get_context` with arguments that would rank the forbidden item first;
read the briefing; trigger a validation report on the invalid forbidden
item through a list that would include it; repeat each forbidden and
missing `get` many times and compare latency distributions.

Expected results:

- `list` with `limit=1` returns `eng-std` first, and no page, count, total,
  or cursor reflects forbidden items; the forbidden-only selector returns
  an empty result identical to one for a non-matching selector.
- Forbidden `get` and resource reads are indistinguishable from missing
  ones in outcome, diagnostics, and error text.
- `get_context` and the briefing omit the forbidden items, including from
  kind and label summary counts.
- No diagnostic names or describes the invalid forbidden item.
- The latency difference between forbidden and missing stays within the
  documented bound (OPEN-access-control-08).

Covers: PK-PROD-011, PK-ACC-021, PK-ACC-023, PK-ACC-024

## J7 — Invalid access content grants nothing

Steps: add, one at a time, a Binding naming `Role/unknown`; a Binding
scoped to `Container/unknown`; a Binding whose subject is not a principal
(for example an Actor item); a Role rule with selector `sensitivity in (`
bound to principal A. Run `processkit validate`, then restart the server and
call `list(kind=Standard)` as A; then add an Actor item named after A's
user identifier and a Binding naming that Actor as subject.

Expected results:

- `processkit validate` reports a validation error for each item.
- A's visible set is unchanged by each invalid Binding or rule.
- The Actor item does not make the Binding grant anything.

Covers: PK-ACC-018, PK-ACC-020, PK-ACC-025

## J8 — Scope and validity bound a grant

Steps:

1. Add a Binding granting principal A access to `fin-std`'s kind scoped to
   `Container/company` with validity until a time two minutes ahead; call
   `get(Standard, fin-std)` as A.
2. After the validity ends, repeat the call.
3. Rescope the Binding to `Container/engineering`; call again.

Expected results:

- 1: allowed (scope is an ancestor of `finance`).
- 2: same result as a missing item.
- 3: same result as a missing item (scope is not `finance` or an ancestor).

Covers: PK-ACC-020, PK-ACC-021

## J9 — can-i and impersonation

Preconditions: the common fixture in a local working copy.

Steps:

1. Without any impersonation grant, run `processkit access can-i get
   Standard eng-std --as alice --as-group engineering@example.com --json`.
2. With an explicit impersonation grant for the caller, repeat step 1; then
   run it for `eng-secret` and `fin-std`; then run `can-i list Standard
   --as carol`.
3. Inspect the operational log.

Expected results:

- 1: refused for lack of an impersonation grant.
- 2: `eng-std` allowed with granting Binding `engineering-reads-standards`;
  `eng-secret` and `fin-std` denied with no granting Binding; `carol`
  denied.
- 3: every decision and every impersonation is logged with principal,
  authenticator, verb, kind, namespace, name, outcome, and granting
  Binding; the repository working tree is unchanged.

Covers: PK-ACC-022, PK-ACC-026, PK-ACC-027

## J10 — Shared server start-up conditions

Steps:

1. Run `processkit mcp serve --http --listen 127.0.0.1:PORT` with no TLS
   configured.
2. Run it with TLS but only the `local` authenticator.
3. Run it with no operator-supplied certificate or key at all, and inspect
   the filesystem and network for created CA material or certificate
   requests.
4. Put an authenticator definition, a trusted issuer, and a principal
   definition into repository files (including project configuration) and
   start with TLS but no operator authenticator.
5. Start correctly configured; request the health endpoint without
   credentials; call any tool and inspect the revision.

Expected results:

- 1 to 4: the server refuses to start with a diagnostic; no CA,
  certificate, or certificate request is created; repository-supplied
  authenticator, issuer, or principal definitions are not used.
- 5: the health endpoint answers without item names, counts, or rules;
  results report the revision of the single served working copy.

Covers: PK-ACC-011, PK-ACC-030, PK-ACC-031, PK-ACC-032, PK-ACC-033

## J11 — Per-principal limits

Preconditions: J1's server with a low per-principal request limit and a
higher per-server limit.

Steps: principal A sends requests beyond its limit while principal B sends
requests within its limit.

Expected results: A's excess requests are limited; B's requests are served;
exceeding the per-server limit limits both.

Covers: PK-ACC-033

## J12 — Credentials stay private

Steps: run J2's and J3's requests with debug logging, provoke an error
response for an authenticated request, and capture all server output,
results, diagnostics, and outbound network connections.

Expected results: no bearer token or client certificate appears in any
output; the server opens no outbound connection carrying the caller's
token or certificate; processkit stores no users, passwords, or group
memberships in the working copy or its cache.

Covers: PK-ACC-010, PK-ACC-016

## J13 — stdio makes no confidentiality claim

Steps: in the common fixture, start `processkit mcp serve --stdio` as the
working-copy owner and call `list(kind=Standard)` and `get` on every item;
read the briefing and `processkit mcp serve --help`.

Expected results: every valid item is returned regardless of Roles and
Bindings; nothing in the output presents access rules as protecting
confidentiality in stdio mode.

Covers: PK-ACC-001

## Verified by component tests only

- **PK-ACC-017** — that the principal is an input to every application
  operation and that adapters decide nothing is an architecture property;
  verified by core-level tests and a dependency check that adapters do not
  call the access evaluator, and indirectly by CLI–MCP equivalence (cli@v1).
- **PK-ACC-022** (declaration part) — that every tool and command declares
  its verb and kinds is checked by a registry test over all operations;
  J9 covers the v1 verb set.
