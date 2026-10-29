# Resources, identity, and access control

processkit serves one repository's governance content to people and agents:
standards, documents, skills, trusted MCP server entries, and other entities.
This chapter defines how that content is addressed and filtered as resources,
how callers are identified without processkit managing identity, and how
access to individual resources is granted.

The model follows the Kubernetes pattern deliberately: typed resources with
namespaces, labels, and selectors; pluggable authenticators that turn a
request into a principal; and additive role-based access control. processkit
adopts the pattern, not Kubernetes itself, and has no Kubernetes dependency.

## Resource model

Every served object is a resource with this envelope:

```json
{
  "apiVersion": "processkit.projectious.work/v1",
  "kind": "Standard",
  "metadata": {
    "name": "git-branching",
    "namespace": "engineering",
    "labels": { "area": "delivery", "sensitivity": "internal" },
    "annotations": { "example.com/review-cycle": "yearly" }
  },
  "spec": { "...": "kind-specific authored content" }
}
```

The shared metadata shape is published as
[`resource-metadata.schema.json`](../../schemas/v1/resource-metadata.schema.json).

- **PK-RES-001:** every served resource MUST be addressable by kind,
  namespace, and name, and MUST be retrievable as an MCP resource at
  `processkit://<namespace>/<kind>/<name>`.
- **PK-RES-002:** `metadata.labels` MUST be selectable key/value pairs with
  bounded key and value syntax and a bounded count. `metadata.annotations`
  MUST NOT be selectable and MUST NOT influence authorization.
- **PK-RES-003:** the label and annotation key prefix
  `processkit.projectious.work/` is reserved for processkit. Authored content
  MUST NOT set reserved keys; processkit MAY set them only on derived status.
- **PK-RES-004:** authored content lives in `spec`. Validation result,
  content digest, source path, index freshness, and other derived facts MUST
  be reported as `status` and MUST NOT be authored.
- **PK-RES-005:** label selectors MUST support equality (`key=value`,
  `key!=value`), set membership (`key in (a,b)`, `key notin (a,b)`), and
  existence (`key`, `!key`), combined by comma as logical AND. CLI and MCP
  MUST parse one grammar and reject invalid selectors with the exact position.
- **PK-RES-006:** generic read operations MUST be available for every served
  kind: `list_resources(kind, namespace?, selector?, limit?, cursor?)` and
  `get_resource(kind, namespace, name, level?)`. Kind-specific operations,
  such as the standards tools, MAY add disclosure levels and ranking but MUST
  apply the same selectors and access decisions.
- **PK-RES-007:** visibility restrictions MUST be expressed through labels and
  access policy. processkit MUST NOT add a separate taint-like mechanism that
  hides resources outside access control.

### Served kinds

| Kind | Source | Phase |
|---|---|---|
| `Standard` | `standards/<name>.json`, see [governance standards](04-content-packages-and-extensions.md#governance-standards) | PK1-P3 |
| `MCPServer` | `mcp-servers/<name>.json`, see [trusted MCP server catalog](#trusted-mcp-server-catalog) | PK1-P3 |
| `Document` | Markdown files matched by a declared document source | PK1-P3 |
| `Skill` and other entities | Installed packages and canonical entities | PK1-P4 |
| `Role`, `RoleBinding` | `access/roles/` and `access/bindings/` | PK1-P6 |

- **PK-RES-010:** a document source MUST be declared in project configuration
  with a repository-relative path pattern, a namespace, and labels applied to
  every matched file. processkit MUST NOT serve Markdown that no declared
  source matches.
- **PK-RES-011:** a `Document` MUST be served with progressive disclosure:
  level 0 is title, path, labels, and heading index; level 2 is one heading
  section. A document has no level-1 rule set and no lifecycle semantics.

### Namespaces

A namespace is an organizational scope inside one installation, such as a
company, a team, or a project area. Namespaces form a tree declared in
project configuration. A repository that declares none has one implicit root
namespace.

- **PK-RES-020:** namespaces MUST be declared with a name and an optional
  parent; cycles, undeclared parents, and duplicate names are verification
  errors.
- **PK-RES-021:** a resource without `metadata.namespace` MUST belong to the
  root namespace. A resource naming an undeclared namespace MUST fail
  validation and MUST NOT be served.
- **PK-RES-022:** namespace membership MUST NOT change authored content or
  semantics; it scopes naming, selection, and access only.

## Trusted MCP server catalog

A governing repository can publish the MCP servers it trusts, including an
external MCP gateway that fronts them. processkit serves those entries as
resources so agents and people can discover what to connect to. processkit is
not a gateway: it never connects to, proxies, or invokes a catalogued server.

Entries follow [`mcp-server.schema.json`](../../schemas/v1/mcp-server.schema.json)
and start from
[`mcp-server.template.json`](../../templates/v1/mcp-server.template.json).
A pointer to a company gateway may also be stated as a rule in an ordinary
governance standard.

- **PK-CAT-001:** processkit MUST NOT forward, proxy, aggregate, or invoke
  tools of a catalogued MCP server, and MUST NOT write harness MCP
  configuration from a catalog entry without a reviewed plan.
- **PK-CAT-002:** an entry MUST declare a pinned version, transport, highest
  side-effect class, owner, lifecycle status, and authentication mode. Remote
  transports MUST use HTTPS. Stdio entries MUST name a package coordinate,
  never a shell command line.
- **PK-CAT-003:** entries MUST NOT contain credential values. Verification
  MUST fail on fields that match configured secret patterns.
- **PK-CAT-004:** an entry with role `gateway` MAY list the catalogued
  servers it fronts. processkit MUST validate those names and MUST NOT infer
  trust in a server from its presence behind a gateway.
- **PK-CAT-005:** `processkit catalog export --format FORMAT` MAY render the
  catalog for an external gateway or harness. Export is a read-only machine
  result and MUST apply the caller's access decisions.

## Identity

processkit consumes identity; it does not manage it. An authenticator turns a
request into a principal: a user identifier, a set of groups, and the name of
the authenticator that asserted them. Identity providers, certificate
authorities, and credential issuance belong to the operator's infrastructure,
for example a company identity provider or the projectious.work infrastructure
product.

| Authenticator | Use | Identity source |
|---|---|---|
| `local` | stdio and loopback daemon, the default | the operating-system user that owns the server process |
| `oidc` | AI harnesses and people over HTTPS | bearer token from a configured issuer; user and group claims |
| `x509` | services, CI, and machine clients over mutual TLS | client certificate from a configured CA; subject CN as user, O as groups |
| `trusted-proxy` | deployments behind an authenticating reverse proxy | identity headers accepted only from a proxy authenticated by mutual TLS |

- **PK-ACC-001:** processkit MUST NOT store users, passwords, or group
  memberships, and MUST NOT issue, sign, or rotate credentials.
- **PK-ACC-002:** authenticators MUST be configured in operator runtime
  configuration outside project-controlled files. Repository content MUST NOT
  enable an authenticator, trust an issuer or CA, or define a principal.
- **PK-ACC-003:** authenticators MUST run as an ordered chain. The first
  authenticator that accepts the request defines the principal; a request no
  authenticator accepts MUST be rejected. Anonymous access MUST be disabled
  unless the operator configures it explicitly, and an anonymous principal
  belongs only to the group `system:unauthenticated`.
- **PK-ACC-004:** the `oidc` authenticator MUST validate issuer, audience,
  signature, expiry, and not-before, and MUST act as an OAuth protected
  resource according to the MCP authorization specification in force for the
  supported MCP version.
- **PK-ACC-005:** the `x509` authenticator MUST verify the chain against the
  configured CA bundle, validity period, and client-authentication usage, and
  MUST support a configured revocation list. Operators SHOULD issue
  short-lived client certificates.
- **PK-ACC-006:** the `trusted-proxy` authenticator MUST accept identity
  headers only on connections whose peer certificate identifies a configured
  proxy, and MUST strip those headers from every other connection.
- **PK-ACC-007:** processkit MUST NOT pass a caller's token or certificate to
  another service and MUST redact bearer material from every output channel.
- **PK-ACC-008:** a principal MUST be available to the application core as an
  input to every operation. MCP, CLI, and daemon adapters MUST NOT make access
  decisions themselves.

## Authorization

Access policy is ordinary repository content reviewed through Git. A `Role`
lists permitted verbs on kinds, optionally narrowed by names or a label
selector. A `RoleBinding` grants one role to users or groups in a namespace.
Schemas: [`role.schema.json`](../../schemas/v1/role.schema.json) and
[`role-binding.schema.json`](../../schemas/v1/role-binding.schema.json).

```json
{
  "apiVersion": "processkit.projectious.work/v1",
  "kind": "Role",
  "metadata": { "name": "standards-reader" },
  "spec": {
    "rules": [
      {
        "kinds": ["Standard", "Document"],
        "verbs": ["get", "list", "search"],
        "selector": "sensitivity notin (confidential)"
      }
    ]
  }
}
```

- **PK-ACC-010:** access MUST be denied by default. Rules MUST be additive
  only; v1 has no deny rule.
- **PK-ACC-011:** a request is allowed only when a RoleBinding in the
  resource's namespace or an ancestor namespace binds the principal, directly
  or through a group, to a Role with a rule matching kind, verb, name, and
  label selector.
- **PK-ACC-012:** verbs MUST be `get`, `list`, `search`, `create`, `update`,
  `transition`, and `delete`. Each MCP tool and CLI command MUST declare the
  verb and kind it requires, and discovery MUST show only tools the principal
  can use at least once.
- **PK-ACC-013:** when no access policy exists and the principal comes from
  the `local` authenticator, the principal MUST hold every verb in the
  installation. This preserves single-user local behavior without policy files.
- **PK-ACC-014:** `list` and `search` MUST filter before pagination, counting,
  and ranking. A forbidden `get` MUST return the same not-found result as a
  missing resource.
- **PK-ACC-015:** lexical, semantic, and hybrid retrieval and context assembly
  MUST exclude unauthorized resources before ranking and MUST NOT return
  their snippets, embeddings, or derived summaries.
- **PK-ACC-016:** a reference from an authorized resource to an unauthorized
  one MUST be returned as an unresolved reference without the target's title,
  labels, or content.
- **PK-ACC-017:** a RoleBinding referring to an undefined Role, a Role rule
  with an invalid selector, and a binding in an undeclared namespace MUST be
  verification errors. An invalid policy file MUST grant nothing.
- **PK-ACC-018:** access decisions MUST be recorded in the operational log
  with principal, authenticator, verb, kind, namespace, name, outcome, and
  the matching binding. They MUST NOT be written as canonical events.
- **PK-ACC-019:** `processkit access whoami` MUST report the current
  principal, and `processkit access can-i VERB KIND [NAME]` MUST report the
  decision and the granting binding. Impersonation through `--as` and
  `--as-group` MUST itself require an explicit grant and MUST be logged.

## Shared serving

A governing repository is usually served to many people from one host. The
shared mode runs the ordinary application core against one working copy,
typically a checkout of the reviewed default branch, and listens on a network
address.

- **PK-ACC-030:** `processkit mcp serve --http --listen ADDRESS` with a
  non-loopback address MUST refuse to start unless TLS is configured and at
  least one authenticator other than `local` is enabled.
- **PK-ACC-031:** a shared server MUST be read-only in v1: it MUST NOT expose
  project-mutating or externally mutating tools. Changes to served content
  remain local operations followed by Git review.
- **PK-ACC-032:** a shared server MUST serve exactly one working copy, report
  its revision in discovery, and refresh its catalog and access policy
  according to the daemon refresh requirement in
  [Agent protocol](06-agent-protocol-and-query-surface.md#runtime-and-transports).
- **PK-ACC-033:** the operator MUST supply TLS keys and certificates.
  processkit MUST NOT create a certificate authority or request certificates.
- **PK-ACC-034:** request limits MUST apply per principal as well as per
  server, and the unauthenticated health endpoint MUST NOT reveal resource
  names, counts, or policy.

## Verification

- **PK-ACC-040:** the release suite MUST include negative cases for every
  authenticator: expired, not-yet-valid, wrong-audience, and wrong-issuer
  tokens; untrusted, expired, and revoked certificates; spoofed proxy headers;
  and anonymous access when disabled.
- **PK-ACC-041:** authorization tests MUST prove that unauthorized resources
  do not appear through list, get, search, semantic retrieval, context
  assembly, references, counts, catalog export, error messages, or timing
  differences beyond a documented bound.
- **PK-ACC-042:** CLI and MCP MUST produce the same access decision for the
  same principal, verb, and resource.
