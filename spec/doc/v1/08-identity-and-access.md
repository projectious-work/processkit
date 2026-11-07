# Identity and access control

One installation can serve people and agents with different rights. Access
control follows the Kubernetes pattern deliberately: pluggable authenticators
turn a request into a principal, and additive role-based rules decide what
the principal may read. processkit adopts the pattern, not Kubernetes itself.

Access control protects confidentiality only on the shared server. Over
stdio the caller already holds the working copy.

- **PK-ACC-001:** in stdio mode processkit MUST NOT present access rules as a
  confidentiality control; the local principal sees every item.

## Identity

processkit consumes identity; it does not manage it. Identity providers,
certificate authorities, and credential issuance belong to the operator's
infrastructure.

| Authenticator | Use | Identity source |
|---|---|---|
| `local` | stdio, the default | the operating-system user that owns the server process |
| `oidc` | people and harnesses using the shared server | bearer token from a configured issuer; user and group claims |
| `x509` | services and automation using the shared server | client certificate from a configured CA; subject CN as user, O as groups |
| `trusted-proxy` | a shared server behind an authenticating reverse proxy | identity headers accepted only from a proxy authenticated by mutual TLS |

- **PK-ACC-010:** processkit MUST NOT store users, passwords, or group
  memberships, and MUST NOT issue, sign, or rotate credentials.
- **PK-ACC-011:** authenticators MUST be configured in operator configuration
  outside repository files. Repository content MUST NOT enable an
  authenticator, trust an issuer or CA, or define a principal.
- **PK-ACC-012:** authenticators MUST run as an ordered chain; the first that
  accepts a request defines the principal, and a request none accepts MUST be
  rejected. Anonymous access MUST be off unless configured, and an anonymous
  principal belongs only to the group `system:unauthenticated`.
- **PK-ACC-013:** `oidc` MUST validate issuer, audience, signature, expiry,
  and not-before, and MUST act as an OAuth protected resource according to
  the MCP authorization specification for the supported MCP version.
- **PK-ACC-014:** `x509` MUST verify the chain, validity, and
  client-authentication usage and MUST support a revocation list. Operators
  SHOULD issue short-lived certificates.
- **PK-ACC-015:** `trusted-proxy` MUST accept identity headers only on
  connections whose peer certificate identifies a configured proxy, and MUST
  strip them from every other connection.
- **PK-ACC-016:** processkit MUST NOT pass a caller's token or certificate to
  another service and MUST redact bearer material from every output.
- **PK-ACC-017:** the principal MUST be an input to every application
  operation; adapters MUST NOT make access decisions themselves.
- **PK-ACC-018:** an Actor or TeamMember item MUST NOT be treated as proof of
  identity. A Binding subject identifies a principal by an identifier the
  authenticator asserts.

## Authorization

Access rules are ordinary ontology content reviewed through Git:

1. A **Role** MAY declare access rules: verbs on kinds, optionally narrowed
   by names or a label selector.
2. A **Binding** with relation type `grants-role` grants one Role. Its
   subject is a user or group principal, its target is the Role, its scope is
   a Container, and its validity bounds the grant in time.

```json
{
  "apiVersion": "processkit.projectious.work/v1",
  "kind": "Role",
  "metadata": { "name": "standards-reader" },
  "spec": {
    "responsibilities": ["Apply company engineering standards"],
    "access": [
      {
        "kinds": ["Standard", "ProcessSpecification", "Skill"],
        "verbs": ["get", "list"],
        "selector": "sensitivity notin (confidential)"
      }
    ]
  }
}
```

```json
{
  "apiVersion": "processkit.projectious.work/v1",
  "kind": "Binding",
  "metadata": { "name": "engineering-reads-standards" },
  "spec": {
    "relation": "grants-role",
    "subject": { "principal": "Group", "name": "engineering@example.com" },
    "target": "Role/standards-reader",
    "scope": "Container/engineering",
    "validity": { "until": "2027-12-31T23:59:59Z" }
  }
}
```

- **PK-ACC-020:** access MUST be denied by default. Rules MUST be additive;
  v1 has no deny rule.
- **PK-ACC-021:** a request is allowed only when a `grants-role` Binding,
  valid at request time and scoped to the item's Container or an ancestor,
  binds the principal, directly or through a group, to a Role with a rule
  matching kind, verb, name, and selector.
- **PK-ACC-022:** verbs are `get` and `list` in v1. Every tool and command
  MUST declare the verb and kinds it requires.
- **PK-ACC-023:** `list`, `get_context`, and the briefing MUST filter before
  ordering, counting, and truncation. A forbidden `get` MUST return the same
  result as a missing item.
- **PK-ACC-024:** a reference from an allowed item to a forbidden one MUST be
  returned as unresolved, without the target's title, labels, or content.
- **PK-ACC-025:** a Binding to an unknown Role, scoped to an unknown
  Container, or with a non-principal subject, and a rule with an invalid
  selector MUST be validation errors and MUST grant nothing.
- **PK-ACC-026:** access decisions MUST be written to the operational log
  with principal, authenticator, verb, kind, namespace, name, outcome, and
  granting Binding. They are not repository content.
- **PK-ACC-027:** `processkit access can-i VERB KIND [NAME] --as USER
  [--as-group G]` MUST report the decision and the granting Binding.
  Impersonation MUST require an explicit grant and MUST be logged.

## Shared server

The shared server runs the application core against one working copy,
usually a checkout of the governing repository's reviewed default branch.

- **PK-ACC-030:** `processkit mcp serve --http --listen ADDRESS` MUST refuse
  to start without TLS and at least one authenticator other than `local`.
- **PK-ACC-031:** the shared server MUST serve exactly one working copy and
  report its revision.
- **PK-ACC-032:** the operator MUST supply TLS keys and certificates.
  processkit MUST NOT create a certificate authority or request certificates.
- **PK-ACC-033:** request limits MUST apply per principal as well as per
  server. The unauthenticated health endpoint MUST NOT reveal item names,
  counts, or rules.
