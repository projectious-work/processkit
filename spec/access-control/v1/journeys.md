# Identity and access control — acceptance journeys

Each journey runs against the exact release-candidate artifacts in a
temporary Git repository with synthetic content, synthetic identity
infrastructure (a test OIDC issuer, a test certificate authority, and where
needed a test reverse proxy), and no ambient credentials or user
configuration. Operator configuration is a file named with `--config`
(`cli@v1`) that uses the keys of `interfaces.yaml`
(`operator_configuration`). Codes, paths, and fields are those of
`interfaces.yaml` and the schemas in `schemas/`.

Common fixture, used by J1 to J9 and J14 to J16: a governing repository
with Containers `company` (a child of the root Container), `engineering`
(child of `company`), and `finance` (child of `company`); Standards
`eng-std` in `engineering` with label `sensitivity=internal`, `eng-secret`
in `engineering` with label `sensitivity=confidential`, and `fin-std` in
`finance`; `eng-std` references `fin-std`. Role `standards-reader` as in
the baseline example (kinds Standard, ProcessSpecification, Skill; verbs
get, list; selector `sensitivity notin (confidential)`). Binding
`engineering-reads-standards` grants that Role to group
`engineering@example.com`, scoped to `Container/engineering`, valid until a
future time. Binding `ops-reads-all` grants a Role with rules for all three
kinds and no selector to the x509 group `ops`, scoped to
`Container/company`.

Common server configuration, used where a journey says "the shared
server": `tls.certificate` and `tls.private-key` (mode 0600) from the test
CA; `auth.authenticators = ["oidc", "x509"]`; `auth.oidc.issuer` the test
issuer; `auth.oidc.audience = "https://pk.test/mcp"`;
`auth.x509.ca-bundle` the test CA. The server is started with
`processkit mcp serve --http --listen 127.0.0.1:PORT --config FILE`.

## J1 — Two principals receive different, correctly filtered context

Baseline release journey 6. Preconditions: the common fixture and the
shared server.

Steps:

1. Start the shared server; poll `GET /healthz` until it answers.
2. Connect principal A with a valid OIDC token (audience
   `https://pk.test/mcp`) whose `sub` is `alice` and whose `groups` claim
   is `["engineering@example.com"]`; read the briefing; call
   `list(kind=Standard)`, `get(Standard, eng-std)`,
   `get(Standard, eng-secret)`, `get(Standard, fin-std)`, and
   `get_context()`.
3. Connect principal B with a valid client certificate with subject
   `CN=ci-bot, O=ops`; repeat step 2's calls.

Expected results:

- Step 1 starts the server; `/healthz` answers HTTP 200 with
  `{"state": "healthy"}`; tool results report the working-copy revision.
- A: the briefing, `list`, and `get_context` contain `eng-std` only;
  `list` reports one item; `get` of `eng-secret` and `fin-std` returns the
  same result as a missing item; `eng-std`'s reference to `fin-std` is
  unresolved without `fin-std`'s title, labels, or content.
- B: the briefing, `list`, and `get_context` contain all three Standards;
  every `get` succeeds; the reference resolves.
- A's and B's results differ only by the filtered items; both report the
  same revision.

Covers: PK-PROD-011, PK-ACC-012, PK-ACC-013, PK-ACC-014, PK-ACC-021,
PK-ACC-023, PK-ACC-024, PK-ACC-031, PK-ACC-034, PK-ACC-036, PK-ACC-038,
PK-ACC-045

## J2 — OIDC rejects invalid tokens

Preconditions: the shared server with `auth.authenticators = ["oidc"]`,
anonymous access off.

Steps: call `list(kind=Standard)` on `/mcp` with, in turn: no token; an
expired token (expiry more than 60 seconds ago); a token whose not-before
is more than 60 seconds in the future; a token for another audience; a
token from another issuer; a token with an invalid signature; a token
signed with HS256; a token without a `sub` claim; a token whose `groups`
claim is a number. Then `GET /.well-known/oauth-protected-resource/mcp`.
Then send a valid token whose `groups` claim is the string
`engineering@example.com`.

Expected results:

- Every invalid request gets HTTP 401 with a body valid against
  `schemas/access-rejection.schema.json` and `data.code`
  `access.unauthenticated`; all nine bodies are identical; no response
  carries item data, item names, or counts.
- Each 401 carries `WWW-Authenticate: Bearer` with `resource_metadata`
  set to `https://pk.test/.well-known/oauth-protected-resource/mcp`; the
  responses to presented tokens also carry `error="invalid_token"`.
- The metadata response is RFC 9728 metadata with `resource`
  `https://pk.test/mcp` and `authorization_servers` the test issuer.
- Each rejection writes one log record with event
  `access.unauthenticated` and a `fields.reason`; no log record contains
  bearer material.
- The token with a string `groups` claim is accepted with that one group.

Covers: PK-ACC-012, PK-ACC-013, PK-ACC-016, PK-ACC-036, PK-ACC-055

## J3 — x509 rejects untrusted, expired, and revoked certificates

Preconditions: the shared server with `auth.x509.revocation-list`
containing certificate R.

Steps: connect with, in turn: a certificate from an untrusted CA; an
expired certificate; a certificate not yet valid; a certificate without
client-authentication usage; certificate R; a certificate from the test CA
with two subject CN values; then a valid certificate with subject
`CN=ci-bot, O=ops, O=release`.

Expected results:

- The first five connections fail in the TLS handshake; no HTTP response
  is sent; each writes a log record with event
  `access.certificate-rejected` and the matching `fields.reason`.
- The certificate with two CN values gets HTTP 401 `access.unauthenticated`.
- The valid certificate is accepted; the decision log shows the principal
  `{"user": "ci-bot", "groups": ["ops", "release"], "authenticator":
  "x509"}`.

Covers: PK-ACC-012, PK-ACC-014, PK-ACC-038

## J4 — Spoofed proxy identity headers are ignored

Preconditions: the shared server with `auth.authenticators =
["trusted-proxy", "oidc"]`, `auth.trusted-proxy.ca-bundle` the test CA, and
`auth.trusted-proxy.allowed-names = ["proxy-p"]`; a test proxy P whose
client certificate has subject `CN=proxy-p`.

Steps:

1. Through P, send a request with `X-Remote-User: ci-bot` and
   `X-Remote-Group: ops`.
2. Directly (no client certificate), send a request carrying the same
   headers and no token.
3. Directly with a client certificate from the test CA with subject
   `CN=other`, send the same headers.
4. Directly, send the same headers plus principal A's valid OIDC token.
5. Through P, send a request without `X-Remote-User`.

Expected results:

- 1: accepted as principal `ci-bot` with group `ops`.
- 2 and 3: HTTP 401 `access.unauthenticated`; the headers are not used as
  identity.
- 4: accepted as principal A, never `ci-bot`; the response is filtered
  for A.
- 5: HTTP 401 `access.unauthenticated`.

Covers: PK-ACC-012, PK-ACC-015, PK-ACC-035, PK-ACC-039

## J5 — Anonymous access

Steps:

1. With `auth.anonymous` absent, send a request without credentials.
2. Set `auth.anonymous = true`; add a Binding granting a Role to group
   `system:unauthenticated` for `eng-std` only (rule `names: ["eng-std"]`);
   restart; send a request without credentials and call
   `list(kind=Standard)`.
3. With the same configuration, send a request with an expired token.

Expected results:

- 1: HTTP 401 `access.unauthenticated`.
- 2: accepted; the decision log records the principal
  `{"user": "system:anonymous", "groups": ["system:unauthenticated"],
  "authenticator": "anonymous"}`; only `eng-std` is listed.
- 3: HTTP 401 `access.unauthenticated`; the request is not served as
  anonymous.

Covers: PK-ACC-012, PK-ACC-020, PK-ACC-021, PK-ACC-035, PK-ACC-037

## J6 — Forbidden items do not leak through any surface

Preconditions: the shared server; principal A; additionally `eng-secret`
made invalid in a second run, and a third Standard `aa-secret` in
`engineering` labelled `sensitivity=confidential`, so that it is forbidden
to A and would precede `eng-std` in a name-based stable order.

Steps: as principal A, call `list(kind=Standard, limit=1)` and follow the
cursor; `list` with a selector matching only forbidden items; `get` of a
forbidden item and of a never-existing name (compare byte for byte apart
from the requested name); read the forbidden item's MCP resource URI;
`get_context` with arguments that would rank the forbidden item first;
read the briefing; trigger a validation report on the invalid forbidden
item through a list that would include it; measure latency as
`interfaces.yaml` (`filtering.timing.measurement`) states.

Expected results:

- `list` with `limit=1` returns `eng-std` first, and no page, count, total,
  or cursor reflects forbidden items; the forbidden-only selector returns
  an empty result identical to one for a non-matching selector.
- Forbidden `get` and resource reads are indistinguishable from missing
  ones in outcome, diagnostics, and error text.
- `get_context` and the briefing omit the forbidden items, including from
  kind and label summary counts.
- No diagnostic names or describes the invalid forbidden item.
- The medians of forbidden and missing `get` latency differ by at most
  2 ms.

Covers: PK-PROD-011, PK-ACC-021, PK-ACC-023, PK-ACC-024, PK-ACC-049

## J7 — Invalid access content grants nothing

Steps: add, one at a time, a Binding naming `Role/unknown`; a Binding
scoped to `Container/unknown`; a `grants-role` Binding whose subject is
`Actor/alice`; a `grants-role` Binding without `spec.scope`; a Binding with
`validity.from` equal to `validity.until`; a Role without
`spec.responsibilities`; a Role rule with selector `sensitivity in (`,
next to a second, valid rule of the same Role that grants `get` on
`fin-std` by name, the Role bound to principal A scoped to
`Container/company`. Run `processkit validate --json`, then restart
the server and call `list(kind=Standard)` and `get(Standard, fin-std)` as
A. Then add an Actor item named `alice` and a Binding naming that Actor as
subject.

Expected results:

- `processkit validate` exits 1 and reports, in this order of additions:
  `ontology.unresolved-reference` (pointer `/spec/target`),
  `ontology.unresolved-reference` (pointer `/spec/scope`),
  `ontology.relation-endpoint` (pointer `/spec/subject`),
  `ontology.missing-field`, `access.invalid-validity`,
  `ontology.missing-field`, and `ontology.invalid-selector` with the file
  and pointer `/spec/access/0/selector`.
- A's visible set is unchanged by each invalid Binding and by the invalid
  rule; the valid second rule still grants `get` on `fin-std`.
- The Actor item does not make the Binding grant anything.

Covers: PK-ACC-018, PK-ACC-020, PK-ACC-025, PK-ACC-040, PK-ACC-041,
PK-ACC-054

## J8 — Scope, validity, and request time

Steps:

1. Add a Binding granting principal A `get` on Standards scoped to
   `Container/company` with `validity.until` two minutes ahead; call
   `get(Standard, fin-std)` as A; call `get_context()` twice, 30 seconds
   apart.
2. After the validity ends, repeat `get` and `get_context()`.
3. Rescope the Binding to `Container/engineering`; call `get` again.
4. Scope it to `Container/root` without validity; call `get` again.
5. Set `validity.from` one minute ahead; call `get`; call again after that
   time.

Expected results:

- 1: allowed (scope is an ancestor of `finance`); both `get_context`
  results are byte-identical and report the same cache key.
- 2: `get` returns the same result as a missing item; `get_context`
  reports a different cache key from step 1.
- 3: same result as a missing item (scope is not `finance` or an
  ancestor).
- 4: allowed.
- 5: missing before `from`, allowed after it.

Covers: PK-ACC-020, PK-ACC-021, PK-ACC-041, PK-ACC-043, PK-ACC-044

## J9 — can-i and impersonation

Preconditions: the common fixture in a local working copy; an operator
configuration file without `access.impersonators`, and a second one with
`access.impersonators` set to the login name of the test user.

Steps:

1. With the first file, run `processkit access can-i get Standard eng-std
   --namespace engineering --as alice --as-group engineering@example.com
   --json`.
2. With the second file, repeat step 1; then run it for `eng-secret`,
   for `fin-std` with `--namespace finance`, and for the never-existing
   name `nope`; then run `can-i list Standard --namespace engineering --as
   carol` and `can-i list Standard --namespace engineering --as bob
   --as-group engineering@example.com`.
3. Run `can-i get Standard eng-std` without `--as`, and `can-i delete
   Standard eng-std --as alice`.
4. Inspect the operational log, written with `--log-level error`.

Expected results:

- 1: exit 3, `access.impersonation-denied`, `data` null.
- 2: every run exits 0 with data valid against
  `schemas/can-i-result.schema.json`; `eng-std` is `allow` with
  `grantedBy` `{"binding": "Binding/engineering-reads-standards", "role":
  "Role/standards-reader", "rule": 0}`; `eng-secret`, `fin-std`, and
  `nope` are `deny` with `grantedBy` null; `carol` is `deny`; `bob` with
  the group is `allow`.
- 3: exit 2 with `cli.missing-argument` and `access.unknown-verb`.
- 4: each run of steps 1 and 2 wrote one `access.impersonation` record
  (outcome `deny` for step 1, `allow` for step 2), and each run of step 2
  one `access.decision` record with `fields.impersonator`, all valid
  against `schemas/access-log-record.schema.json`, although the log level
  was `error`; the repository working tree is unchanged.

Covers: PK-ACC-022, PK-ACC-026, PK-ACC-027, PK-ACC-042, PK-ACC-047,
PK-ACC-053

## J10 — Shared server start-up conditions

Steps:

1. Start `processkit mcp serve --http --listen 127.0.0.1:PORT` with no
   TLS keys.
2. Start it with TLS keys but `auth.authenticators` absent.
3. Start it with `auth.authenticators = ["oidc"]` and no
   `auth.oidc.audience`.
4. Start it with the common server configuration and `tls.private-key` at
   mode 0644.
5. Start it with `tls.private-key` naming a file that is not a PEM key.
6. Start it with `auth.oidc.issuer` naming an unreachable URL.
7. Start it with no operator-supplied certificate or key at all, and
   inspect the filesystem and network for created CA material or
   certificate requests.
8. Put `[auth]`, `[tls]`, and `[auth.oidc]` tables into `processkit.toml`
   and start with TLS but no operator authenticator.
9. Start with the common server configuration; request `GET /healthz`
   without credentials, `GET /unknown`, and call any tool.

Expected results:

- 1: exit 1, `access.tls-not-configured`; 2: exit 1,
  `access.no-authenticator`; 3: exit 1, `access.config-missing-key` with
  `evidence.key` `auth.oidc.audience`; 4: exit 3,
  `security.credential-file-permissions`; 5: exit 3,
  `access.file-unusable`; 6: exit 3, `access.oidc-unavailable`; 7: exit 1,
  `access.tls-not-configured`; 8: exit 1, `cli.config-forbidden-key`. In
  1 to 8 nothing listens on PORT and no CA, certificate, or certificate
  request is created.
- 9: `/healthz` answers HTTP 200 with exactly `{"state": "healthy"}`,
  without item names, counts, or rules; `/unknown` answers HTTP 404 with
  `access.unknown-path`; results report the revision of the single served
  working copy.

Covers: PK-ACC-011, PK-ACC-030, PK-ACC-031, PK-ACC-032, PK-ACC-033,
PK-ACC-034, PK-ACC-050, PK-ACC-052, PK-ACC-055

## J11 — Per-principal and per-server limits

Preconditions: the shared server with
`limits.principal-requests-per-minute = 5` and
`limits.server-requests-per-minute = 8`.

Steps: within one minute, principal A sends 7 requests; principal B sends
2; then B sends 2 more. Repeat with `limits.principal-concurrent-requests
= 1` and two concurrent slow requests of A. Put `[limits]
principal-requests-per-minute = 1` into `processkit.toml` and start again.

Expected results:

- A's 6th and 7th requests get HTTP 429 with `access.principal-limit` and
  a `Retry-After` header of at least 1; B's first 2 are served; then the
  server has accepted 7 requests, so B's next request is served and the
  one after gets HTTP 429 with `access.server-limit`.
- With the concurrency limit, the second concurrent request of A gets HTTP
  429 `access.principal-limit`.
- `GET /healthz` is answered throughout.
- The project configuration fails with `cli.config-unknown-key`.

Covers: PK-ACC-033, PK-ACC-034, PK-ACC-051

## J12 — Credentials stay private

Steps: run J2's and J3's requests with debug logging, provoke an error
response for an authenticated request, and capture all server output,
results, diagnostics, and outbound network connections.

Expected results: no bearer token or client certificate appears in any
output; the only outbound connections go to the test issuer's discovery
and key URLs and carry no caller token or certificate; processkit stores
no users, passwords, or group memberships in the working copy or its
cache.

Covers: PK-ACC-010, PK-ACC-016

## J13 — stdio makes no confidentiality claim

Steps: in the common fixture, start `processkit mcp serve --stdio` as the
working-copy owner with `--log-level debug` and call `list(kind=Standard)`
and `get` on every item; read the briefing and `processkit mcp serve
--help`.

Expected results: every valid item is returned regardless of Roles and
Bindings; nothing in the output presents access rules as protecting
confidentiality in stdio mode; no `access.decision` record is written.

Covers: PK-ACC-001, PK-ACC-046

## J14 — whoami

Steps: run `processkit access whoami --json` in the common fixture, and
outside any repository.

Expected results: both exit 0 with `data` equal to `{"user": <login name
of the test user>, "groups": [], "authenticator": "local"}`; nothing is
written.

Covers: PK-ACC-037, PK-ACC-048

## J15 — Rule narrowing and operation verbs

Preconditions: the shared server; replace `standards-reader` with two
Roles bound to A: `lister` with rule `{"kinds": ["Standard"], "verbs":
["list"], "names": ["eng-std", "fin-std"]}` scoped to `Container/company`,
and `getter` with rule `{"kinds": ["Standard"], "verbs": ["get"],
"selector": "sensitivity=confidential"}` scoped to `Container/engineering`.

Steps: as A, call `list(kind=Standard)`, `get` on each Standard,
`get_context()`, `resources/list`, and `resources/read` for `eng-secret`.

Expected results:

- `list` and `resources/list` contain `eng-std` and `fin-std` only.
- `get` of `eng-secret` succeeds; `get` of `eng-std` and `fin-std` returns
  the missing-item result.
- `get_context` contains `eng-secret` only; `resources/read` of
  `eng-secret` succeeds.

Covers: PK-ACC-021, PK-ACC-040, PK-ACC-045

## J16 — Decision records on the shared server

Preconditions: the shared server started with `--log-level error`.

Steps: as A, call `get(Standard, eng-std)`, `get(Standard, nope)`, and
`list(kind=Standard)`.

Expected results: the log holds, valid against
`schemas/access-log-record.schema.json`: one `access.decision` record with
outcome `allow` and `binding` `Binding/engineering-reads-standards` for the
first call; one with outcome `deny`, `name` `nope`, and `binding` null for
the second; and one record per Standard for the `list`, with outcome
`allow` only for `eng-std`. No record contains bearer material.

Covers: PK-ACC-016, PK-ACC-026, PK-ACC-053

## Verified by component tests only

- **PK-ACC-017** — that the principal is an input to every application
  operation and that adapters decide nothing is an architecture property;
  verified by core-level tests and a dependency check that adapters do not
  call the access evaluator, and indirectly by CLI–MCP equivalence (cli@v1).
- **PK-ACC-022** (declaration part) and **PK-ACC-045** (declaration part)
  — that every tool and command declares its verb and kinds, matching
  `interfaces.yaml` (`authorization.operation_declarations`), is checked
  by a registry test over all operations; J9 and J15 cover the v1 verbs.
- **PK-ACC-044** (digest computation) — the access-set digest is checked
  against hand-computed RFC 8785 serializations for fixed access sets;
  J8 covers its observable effect on the cache key.
