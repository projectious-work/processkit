# Agent protocol and query surface

## MCP role

MCP is processkit's primary agent-facing protocol. The CLI and MCP adapters
invoke the same application services and enforce identical validation,
authority, mutation, event, and recovery semantics.

The MCP server serves one explicitly selected repository root. It may be
launched by Airunner, Tau, another harness, an IDE, or a human-operated shell,
but the launcher does not change repository authority. The reference profile
runs locally inside the contributor's execution environment against that
contributor's working copy.

The runtime exposes one repository's configured capability catalog. It may be
an on-demand stdio process or one long-lived local daemon reused through
direct HTTP clients and lightweight stdio proxies. Both execute the same
application core and enforce the same repository root, policy, locking,
transactions, events, and result contracts.

- **PK-MCP-006:** behavior from the existing gateway and domain tools MAY be
  reused only when new v1 conformance fixtures approve it. Existing tool
  implementations and observed behavior are not normative.
- **PK-MCP-007:** semantics currently distributed across Python per-skill
  servers MUST be consolidated into the shared application core. Legacy
  per-domain servers are migration inputs, not an additional v1 runtime model.

## Discovery

- **PK-MCP-001:** runtime discovery MUST expose tool name, version, description,
  input schema, output schema, side-effect class, owning capability, and
  deprecation state.
- **PK-MCP-002:** discovered schemas MUST match the schemas used for runtime
  validation and generated reference documentation.
- **PK-MCP-003:** tool names MUST be stable and collision-free; aliases MUST
  declare their canonical replacement and removal horizon.
- **PK-MCP-004:** a configured capability absent at runtime is a startup or
  verification failure, not a silently omitted tool.
- **PK-MCP-005:** list/read/search tools MUST be clearly distinguishable from
  project-mutating and externally mutating tools.
- **PK-MCP-008:** discovery MUST expose the selected repository identity,
  context path, working-copy revision, read/write capability, and index
  freshness without exposing ambient credentials.

## Core read surface

The standard profile provides operations equivalent to:

```text
get_entity(id | path)
list_entities(type?, state?, scope?, limit?, cursor?)
search_entities(text, filters?, limit?, cursor?)
semantic_search_entities(text, filters?, limit?, cursor?)
hybrid_search_entities(text, filters?, limit?, cursor?)
query_by_interface(interface, filters?, limit?, cursor?)
traverse_relations(subject, relation?, direction?, depth?)
events_for_subject(subject, after?, limit?, cursor?)
find_skill(task_description)
route_task(task_description, constraints?)
get_effective_configuration()
assemble_context(task, constraints?, token_budget?, provenance?)
```

- **PK-MCP-010:** reads MUST come from canonical files or a verified index
  generation and MUST report index staleness when freshness cannot be proven.
- **PK-MCP-011:** pagination order and cursors MUST be deterministic for a
  stable generation.
- **PK-MCP-012:** search ranking MAY evolve compatibly, but filters, result
  identity, and completeness claims MUST be explicit.
- **PK-MCP-013:** a query MUST not expose private entity bodies or sensitive
  fields beyond the caller's configured local policy.
- **PK-MCP-014:** semantic and hybrid search MUST return canonical entity IDs,
  source digests, ranking method, and index generation. Similarity is a
  retrieval signal, not evidence that a proposition is true or current.
- **PK-MCP-015:** context assembly MUST be bounded by explicit size or token
  limits, preserve source attribution, report omissions and stale indexes, and
  prefer canonical relationships and policy over embedding similarity alone.
- **PK-MCP-016:** every context result MUST remain reproducible enough to fetch
  its canonical source records without relying on an embedding database row.

## Mutation surface

EntityTypes own typed create, update, transition, link, supersede, and archive
operations as applicable.

The generic CLI entity commands and typed MCP tools are projections of these
same operations. The ontology and capability registries, not adapter-specific
hard-coded lists, determine which operations apply to each EntityType.

- **PK-MCP-020:** mutating tools MUST accept structured requests and return a
  versioned result containing outcome, affected IDs, emitted event IDs,
  warnings, and recovery state.
- **PK-MCP-021:** tools MUST re-read and validate relevant state immediately
  before commit; read-time observations are not mutation preconditions unless
  bound by revision or digest.
- **PK-MCP-022:** optimistic concurrency MUST be available through an expected
  revision or content digest.
- **PK-MCP-023:** partial multi-entity success MUST be prohibited unless the
  operation contract explicitly defines partial outcomes and compensation.
- **PK-MCP-024:** idempotency keys SHOULD be supported for operations likely to
  be retried by orchestrators.
- **PK-MCP-025:** authorization is local policy plus host-process authority;
  MCP connectivity alone MUST NOT grant permission to bypass policy.
- **PK-MCP-026:** a successful mutation changes canonical files only in the
  selected working copy. It MUST NOT imply that the change was staged,
  committed, reviewed, merged, pushed, or accepted by another clone.

## Runtime and transports

- **PK-MCP-030:** stdio MUST be supported for local harness integration and
  started with `processkit mcp serve --stdio`.
- **PK-MCP-031:** `processkit mcp serve --http` MAY run as a long-lived daemon
  bound to loopback for exactly one repository root. It MUST require
  per-client authentication, publish health and catalog-generation metadata,
  and reject a request attempting to select another root.
- **PK-MCP-032:** requests MUST have size and concurrency limits, cancellation,
  timeouts, and bounded error payloads.
- **PK-MCP-033:** the server MUST isolate request context and correlation data;
  concurrent responses MUST not leak data or diagnostics between requests.
- **PK-MCP-034:** graceful shutdown MUST stop accepting work, complete or
  cancel active operations according to contract, flush evidence, and release
  locks.
- **PK-MCP-035:** `processkit mcp proxy` MUST be a bounded transport bridge; it
  MUST NOT load tools, reinterpret schemas, weaken authentication, select a
  different root, or acquire independent mutation authority.
- **PK-MCP-036:** daemon reuse MUST invalidate or atomically refresh its
  capability catalog and derived indexes when the installed manifest,
  configuration, canonical generation, or adapter plan changes. A stale
  catalog MUST be reported rather than silently served as current.
- **PK-MCP-037:** processkit provides a foreground daemon process and health
  contract, not a cross-platform service manager. Aibox, an operating-system
  supervisor, or another authorized runtime MAY own start, restart, and stop.

## Cross-repository coordination

- **PK-MCP-040:** processkit MAY expose export/import and external-reference
  operations, but each call remains scoped to one explicitly selected root
  and returns a bundle for transport by Git, a forge, a harness, or Kaits.
- **PK-MCP-041:** a cross-repository handoff MUST identify source repository,
  source revision, owning entity, requested outcome, and sanitized evidence.
- **PK-MCP-042:** receiving a handoff MUST create local project-owned state;
  it MUST NOT mutate the source repository or claim distributed completion.
- **PK-MCP-043:** portfolio orchestration remains a consumer of processkit
  contracts and is outside the processkit agent runtime.
- **PK-MCP-044:** processkit v1 MUST NOT poll repositories, route messages,
  retry remote delivery, manage forge issues or discussions, or run
  cross-repository heartbeats. Those are adapter or orchestration concerns.
