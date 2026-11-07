# Identity and access control — requirements

This specification defines how processkit identifies callers and decides
what each caller may read: the operator-configured authenticator chain
(`local`, `oidc`, `x509`, `trusted-proxy`) that turns a request into a
principal, the additive, deny-by-default access rules declared on Roles and
granted by `grants-role` Bindings scoped to Containers, how access
decisions filter every read surface, the `processkit access can-i` command,
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
- **PK-ACC-027:** `processkit access can-i VERB KIND [NAME] --as USER
  [--as-group G]` shall report the decision and the granting Binding.
  Impersonation shall require an explicit grant and shall be logged.

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
