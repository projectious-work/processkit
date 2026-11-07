# Decisions

These decisions define the v1 context-framework baseline. They supersede the
review decisions D1 to D20 of the earlier memory-oriented v1 draft and the
repository decision `DEC-20260807_1559-BraveFern`, which defined processkit
as agent context and memory infrastructure.

## C1 — Context, not memory

**Accepted:** processkit manages an organization's governance context:
standards, process definitions, skills, trusted MCP servers, decision
records, and documents. It does not record events, logs, work-item
instances, sessions, or agent memories.

**Reason:** an event log duplicated the harness's own memory without being
the memory agents use, and high-churn operational records caused merge
conflicts as soon as several people worked in one repository. Issue
trackers, forges, harnesses, and Git history already hold that information.

**Impact:** journals, transactions, recovery, idempotency keys, event
emission, and memory retrieval leave the product. Content is reviewed files
edited with ordinary tools.

## C2 — The full ontology is the definition language

**Accepted:** the complete 90-concept ontology is published and versioned.
Every concept is classified as definition or instance. processkit stores
definitions only; instance concepts remain vocabulary inside definitions.

**Reason:** the ontology gives organizations a common language for defining
any process, such as ticket handling, without processkit having to track the
process. A smaller ontology would push every organization to invent its own
vocabulary.

**Impact:** registry coverage of the full inventory is a release gate.
processkit's own repositories use only the published ontology.

## C3 — Decision records stay

**Accepted:** decision records are low-volume, reviewed governance documents
linked from the standards and processes they justify.

**Reason:** a rule without its reason ages badly, and decisions change rarely
enough that a merge conflict on one signals a real disagreement.

## C4 — MCP is the agent interface

**Accepted:** agents obtain governance context only over MCP. processkit does
not generate harness instruction files, skill directories, plugins, or
vendor rule formats. The connection briefing replaces the always-on part of
instruction files; skills and standards load on demand.

**Reason:** MCP is vendor-neutral and lets the caller pass arguments that
personalize the result. Per-vendor outputs would multiply formats and tie
processkit to each vendor's release cycle.

**Impact:** harnesses keep system-prompt assembly, memory, conversation
history, code-base context, hooks, and permission settings. Loading skills
over MCP depends on the agent calling `get_context`; the acceptance journeys
measure this.

## C5 — Deterministic, cacheable assembly

**Accepted:** context is assembled per request from the revision, the lock,
the access set, and normalized arguments only, with stable ordering and
shared content before caller-specific content.

**Reason:** personalization must not destroy caching in the server, the
harness, or the model provider.

## C6 — Inheritance through locked upstream repositories

**Accepted:** repositories inherit from pinned upstream governing
repositories through a lockfile, with explicit overrides, final items, and
provenance on every served item. Fetching is explicit.

**Reason:** organizations govern in levels, and reproducible results need
exact upstream versions.

## C7 — Kubernetes-pattern access control with consumed identity

**Accepted:** authenticators (`local`, `oidc`, `x509`, `trusted-proxy`) are
configured by the operator; processkit never manages identity. Access rules
are additive and deny-by-default, declared on Roles and granted by
`grants-role` Bindings scoped to Containers.

**Reason:** one installation serves callers with different rights. Identity
providers and certificate authorities already exist in organizations, and
certificates alone would exclude MCP clients that authenticate with OAuth.

## C8 — Two serving modes, read-only

**Accepted:** stdio for a working copy and a TLS-only, authenticated shared
server for a governing repository. Neither writes content. There is no local
daemon or proxy.

**Reason:** writes are reviewed file changes, and a read-only server is much
simpler to secure.

## C9 — A catalog of trusted MCP servers, not a gateway

**Accepted:** processkit serves MCP server entries, including one for an
external gateway, and never connects to or proxies them.

**Reason:** gateways already exist; processkit's value is the reviewed,
access-controlled statement of which servers an organization trusts.

## C10 — Python, one application core

**Accepted:** one Python implementation with thin CLI and MCP adapters over
one application core.

**Reason:** processkit is a content and protocol product with modest,
IO-bound performance needs; Python has the strongest schema and MCP tooling.
