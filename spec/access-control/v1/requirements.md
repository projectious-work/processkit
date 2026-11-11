# Identity and access control — requirements

This specification defines how processkit identifies callers and decides
what each caller may read: the operator-configured authenticator chain
(`local`, `oidc`, `x509`, `trusted-proxy`) that turns a request into a
principal, the additive, deny-by-default access rules declared on Roles and
granted by `grants-role` Bindings scoped to Containers, how access
decisions filter every read surface, the `processkit auth can-i` command,
the decision log, and the start-up and operating conditions of the shared
server. processkit consumes identity; it never manages it. Label selectors
and Containers are defined by ontology@v1, context assembly and the MCP
tools by mcp-context-serving@v1, inherited access rules by inheritance@v1,
and the threat model and transport hardening by security@v1; this
specification uses them.

Conventions: requirements use EARS; "shall" is mandatory, "should"
recommended, "may" optional; IDs are stable and never reused.

## Purpose and serving modes

- **PK-PROD-011:** The shared server shall serve each caller only the
  content the caller's access grants allow.
- **PK-ACC-001:** While processkit serves over stdio, processkit shall not
  present access rules as a confidentiality control, and the local principal
  shall see every item.

## Identity

- **PK-ACC-010:** processkit shall not store users, passwords, or group
  memberships, and shall not issue, sign, or rotate credentials.
- **PK-ACC-011:** processkit shall accept authenticator configuration only
  from operator configuration outside repository files. Repository content
  shall not enable an authenticator, trust an issuer or certificate
  authority, or define a principal.
- **PK-ACC-012:** processkit shall run the configured authenticators as an
  ordered chain, and the first authenticator that accepts a request shall
  define the principal. If no authenticator accepts a request, then
  processkit shall reject the request. Anonymous access shall be off unless
  configured. Where anonymous access is configured, an anonymous principal
  shall belong only to the group `system:unauthenticated`.
- **PK-ACC-013:** The `oidc` authenticator shall validate the issuer,
  audience, signature, expiry, and not-before of a bearer token, and shall
  act as an OAuth protected resource according to the MCP authorization
  specification for the supported MCP version.
- **PK-ACC-014:** The `x509` authenticator shall verify the certificate
  chain, validity, and client-authentication usage of a client certificate,
  and shall support a revocation list. Operators should issue short-lived
  certificates.
- **PK-ACC-015:** The `trusted-proxy` authenticator shall accept identity
  headers only on connections whose peer certificate identifies a
  configured proxy, and shall strip identity headers from every other
  connection.
- **PK-ACC-016:** processkit shall not pass a caller's token or certificate
  to another service, and shall redact bearer material from every output.
- **PK-ACC-017:** processkit shall pass the principal as an input to every
  application operation. The CLI and MCP adapters shall not make access
  decisions themselves.
- **PK-ACC-018:** processkit shall not treat an Actor or TeamMember item as
  proof of identity. A Binding subject shall identify a principal by an
  identifier that the authenticator asserts.
- **PK-ACC-034:** processkit shall read the shared-server configuration
  only from the operator keys in `interfaces.yaml` (`operator_configuration`),
  with the types and defaults listed there. The key `tls.private-key` shall
  name a credential file (`security@v1` PK-SEC-029). The limit keys shall
  follow `security@v1` PK-SEC-019 and PK-SEC-020.
  <!-- agent proposal: OPEN-access-control-01 -->
- **PK-ACC-035:** For each request, each authenticator in the chain shall
  accept the request, reject it, or abstain. An authenticator shall abstain
  when the request carries no credential of its type. processkit shall run
  the authenticators in the order of `auth.authenticators`. The first
  authenticator that accepts shall define the principal. If no
  authenticator accepts and at least one rejects, then processkit shall
  reject the request. If every authenticator abstains, then processkit
  shall use the anonymous principal where `auth.anonymous` is `true`, and
  shall reject the request otherwise.
  <!-- agent proposal: OPEN-access-control-01 -->
- **PK-ACC-036:** The `oidc` authenticator shall read a bearer token from
  the `Authorization` header. It shall take the user identifier from the
  claim that `auth.oidc.user-claim` names (default `sub`) and the groups
  from the claim that `auth.oidc.groups-claim` names (default `groups`). It
  shall get the issuer's signing keys through OpenID Connect discovery of
  `auth.oidc.issuer`. It shall accept only the signature algorithms listed
  in `interfaces.yaml` and shall allow 60 seconds of clock skew for expiry
  and not-before. The value of `auth.oidc.audience` shall be the protected
  resource identifier of the shared server.
  <!-- agent proposal: OPEN-access-control-02 -->
- **PK-ACC-037:** The `local` authenticator shall assert the login name of
  the effective operating-system user of the processkit process as the user
  identifier, and no groups. The anonymous principal shall have the user
  identifier `system:anonymous`. Every principal shall have its groups
  without duplicates, sorted by Unicode code point.
  <!-- agent proposal: OPEN-access-control-02 -->
- **PK-ACC-038:** The shared server shall request, but not require, a client
  certificate in the TLS handshake. If a client presents a certificate that
  is not trusted by `auth.x509.ca-bundle` or `auth.trusted-proxy.ca-bundle`,
  is expired or not yet valid, lacks client-authentication usage, or is
  listed in `auth.x509.revocation-list`, then the shared server shall fail
  the TLS handshake. The `x509` authenticator shall accept a certificate
  that chains to `auth.x509.ca-bundle` and shall use its only subject CN as
  the user identifier and every subject O as a group.
  <!-- agent proposal: OPEN-access-control-01 -->
- **PK-ACC-039:** The `trusted-proxy` authenticator shall treat a connection
  as coming from a configured proxy only when its client certificate chains
  to `auth.trusted-proxy.ca-bundle` and its subject CN is listed in
  `auth.trusted-proxy.allowed-names`. It shall read the user identifier
  from the header that `auth.trusted-proxy.user-header` names (default
  `X-Remote-User`) and one group from each header that
  `auth.trusted-proxy.group-header` names (default `X-Remote-Group`). On
  every other connection, processkit shall remove both headers before any
  authenticator runs.
  <!-- agent proposal: OPEN-access-control-03 -->

## Authorization

- **PK-ACC-020:** processkit shall deny access by default. Access rules
  shall be additive; v1 shall have no deny rule.
- **PK-ACC-021:** processkit shall allow a request only when a `grants-role`
  Binding that is valid at request time and scoped to the item's Container
  or an ancestor of that Container binds the principal, directly or through
  a group, to a Role with a rule matching the item's kind, the requested
  verb, the item's name, and the rule's selector.
- **PK-ACC-022:** The access verbs in v1 shall be `get` and `list`. Every
  tool and command shall declare the verb and kinds it requires.
- **PK-ACC-023:** `list`, `get_context`, and the briefing shall filter items
  by access before ordering, counting, and truncation. If a `get` is
  forbidden, then processkit shall return the same result as for a missing
  item.
- **PK-ACC-024:** If an allowed item references a forbidden item, then
  processkit shall return the reference as unresolved, without the target's
  title, labels, or content.
- **PK-ACC-025:** If a Binding names an unknown Role, is scoped to an
  unknown Container, or has a non-principal subject, or a Role rule has an
  invalid selector, then processkit shall report a validation error, and
  that Binding or rule shall grant nothing.
- **PK-ACC-026:** processkit shall write every access decision to the
  operational log with the principal, authenticator, verb, kind, namespace,
  name, outcome, and granting Binding. Access decisions shall not be
  repository content.
- **PK-ACC-027:** `processkit auth can-i VERB TYPE [NAME] --as USER
  [--as-group G]` shall report the decision and the granting Binding.
  Impersonation shall require an explicit grant and shall be logged.
  <!-- changed by owner decision: 2026-11-11 (#212), CLI style B -->

### Access content

- **PK-ACC-040:** A Role shall have the shape of `schemas/role.schema.json`.
  An access rule shall match a request only when the item's kind is in
  `kinds`, the verb is in `verbs`, the item's name is in `names` where
  `names` is present, and the item's labels match `selector` where
  `selector` is present. Kinds and verbs shall have no wildcard. The
  references in `spec.capabilities` shall not change any access decision.
  <!-- agent proposal: OPEN-access-control-04 -->
  <!-- agent proposal: gap row 8, accepted by owner 2026-11-11 (#212) -->
- **PK-ACC-041:** A Binding shall have the shape of
  `schemas/binding.schema.json` for every relation type. A `grants-role`
  Binding shall have a principal subject (`User` or `Group`), a Role target,
  and a Container scope. A Binding scoped to the root Container shall name
  `Container/root`. A Binding shall be valid at time t when t is not before
  `spec.validity.from` and is before `spec.validity.until`; an absent bound
  shall not limit it. If `from` is not before `until`, then processkit
  shall report `access.invalid-validity`, and the Binding shall grant
  nothing.
  <!-- owner decision: #213 finding 5 (fields, scope only on grants-role,
       Container/root) -->
  <!-- agent proposal: OPEN-access-control-05 -->
  <!-- agent proposal: gap row 8, accepted by owner 2026-11-11 (#212) -->
- **PK-ACC-054:** processkit shall report the conditions of PK-ACC-025 with
  the codes in `interfaces.yaml` (`validation_errors`). A Role or Binding
  with any other validation error of severity error shall grant nothing. An
  invalid selector shall make only its own rule grant nothing.
  <!-- agent proposal: OPEN-access-control-15 -->

### Decisions and request time

- **PK-ACC-043:** For each request, processkit shall read the clock once,
  when authorization runs and before context assembly starts. processkit
  shall use that request time for token validation and Binding validity.
  The request time shall be an input of the authorization decision only. It
  shall not be an assembly input or a part of a cache key
  (`mcp-context-serving@v1` PK-MCP-030, PK-MCP-032).
  <!-- agent proposal: OPEN-access-control-16 -->
- **PK-ACC-044:** The result of authorization for one request shall be the
  access set: every (verb, kind, namespace, name) that the principal may
  read at the request time. processkit shall compute the access set once
  per request and shall use it for the whole request. The access-set digest
  shall be computed as `interfaces.yaml` (`access_set`) states.
  <!-- agent proposal: OPEN-access-control-16 -->
- **PK-ACC-045:** Each tool, resource operation, prompt operation, the
  briefing, and each command shall require the verb listed for it in
  `interfaces.yaml` (`authorization.operation_declarations`). An item shall
  be readable by an operation only when the principal holds that verb on
  the item.
  <!-- agent proposal: OPEN-access-control-06 -->
- **PK-ACC-046:** While the principal is the `local` principal, processkit
  shall allow `get` and `list` on every item without evaluating Roles and
  Bindings, and shall write no access decision record.
  <!-- agent proposal: OPEN-access-control-07 -->
- **PK-ACC-049:** processkit shall resolve a `get` against the request's
  access set, so that a forbidden item and a missing item take the same
  path. The difference between the median response times of forbidden and
  missing `get` requests shall stay within the bound in `interfaces.yaml`
  (`filtering.timing`).
  <!-- agent proposal: OPEN-access-control-08 -->
- **PK-ACC-053:** processkit shall write one access decision record per
  item and verb that a request decides, in the shape of
  `schemas/access-log-record.schema.json`, with the event `access.decision`.
  If several Bindings grant, then the record shall name the first by
  Unicode code-point order of its typed reference. processkit shall write
  access decision and impersonation records whatever the configured log
  level is.
  <!-- agent proposal: OPEN-access-control-14 -->

### Commands

- **PK-ACC-042:** Impersonation shall be a separate privilege. It shall be
  recorded with the verb `impersonate` and shall not be an access verb of a
  Role rule. processkit shall grant it only to a user identifier listed in
  the operator key `access.impersonators`. If `processkit auth can-i` is
  run by a principal without this privilege, then processkit shall report
  `access.impersonation-denied` as an environment failure and shall
  evaluate nothing. processkit shall log every impersonation attempt with
  the event `access.impersonation`.
  <!-- agent proposal: OPEN-access-control-07; changed by owner decision:
       2026-11-11 (#212), CLI style B -->
- **PK-ACC-047:** `processkit auth can-i` shall evaluate the Roles and
  Bindings of the selected working copy at its revision, without network
  access. The option `--as` shall be required, `--as-group` shall be
  repeatable, and `-n N` shall select the item's Container (default
  `root`). TYPE shall be resolved as in `cli@v1` PK-CLI-049. Without NAME,
  a rule shall match on kind and verb alone. With NAME, if no such item
  exists, then the decision shall be `deny`. The result data shall have
  the shape of `schemas/can-i-result.schema.json`. The exit code shall be
  0 for both decisions.
  <!-- agent proposal: OPEN-access-control-09; changed by owner decision:
       2026-11-11 (#212), CLI style B -->
- **PK-ACC-048:** `processkit auth whoami` shall report the principal of
  the invocation in the shape of `schemas/principal.schema.json`. The
  command shall write nothing.
  <!-- agent proposal: OPEN-access-control-10; changed by owner decision:
       2026-11-11 (#212), CLI style B -->

## Shared server

- **PK-ACC-030:** If `processkit mcp serve --http --listen ADDRESS` is
  started without TLS or without at least one authenticator other than
  `local`, then the processkit CLI shall refuse to start the shared server.
- **PK-ACC-031:** The shared server shall serve exactly one working copy and
  shall report its revision.
- **PK-ACC-032:** The shared server shall use TLS keys and certificates
  supplied by the operator. processkit shall not create a certificate
  authority or request certificates.
- **PK-ACC-033:** The shared server shall apply request limits per principal
  as well as per server. The unauthenticated health endpoint shall not
  reveal item names, counts, or rules.
- **PK-ACC-050:** Before it listens, `processkit mcp serve --http` shall
  run the start-up checks in the order of `interfaces.yaml`
  (`commands`, `mcp serve --http`, `startup_checks`). At the first failing
  check, the processkit CLI shall report that check's code, shall exit with
  the code of its category (`cli@v1`), and shall not listen.
  <!-- agent proposal: OPEN-access-control-11 -->
- **PK-ACC-051:** The shared server shall apply the limits
  `limits.principal-requests-per-minute`,
  `limits.principal-concurrent-requests`, and
  `limits.server-requests-per-minute` after authentication. A principal
  shall be identified for limits by its authenticator and user identifier.
  If a request exceeds a per-principal limit, then the shared server shall
  respond with HTTP status 429 and `access.principal-limit`. If it exceeds
  the per-server limit, then the shared server shall respond with HTTP
  status 429 and `access.server-limit`. Both responses shall carry a
  `Retry-After` header. A rejected request shall not count against a limit.
  <!-- agent proposal: OPEN-access-control-12 -->
- **PK-ACC-052:** The shared server shall answer `GET /healthz` without
  authentication, with the body of `schemas/health.schema.json`. It shall
  use HTTP status 200 for `healthy` and `degraded` and 503 for `blocked`.
  <!-- agent proposal: OPEN-access-control-13 -->
- **PK-ACC-055:** The shared server shall serve MCP at the path `/mcp` and,
  while `oidc` is in the chain, the OAuth protected-resource metadata at
  the path that RFC 9728 derives from `auth.oidc.audience`. If
  authentication rejects a request, then the shared server shall respond
  with HTTP status 401, the body of `schemas/access-rejection.schema.json`
  with `access.unauthenticated`, and, while `oidc` is in the chain, a
  `WWW-Authenticate` challenge that names that metadata URL. The response
  shall be the same for every reason of rejection. For any other path, the
  shared server shall respond with HTTP status 404 and
  `access.unknown-path`.
  <!-- agent proposal: OPEN-access-control-01 -->
