# Agent protocol and query surface

## MCP role

MCP is processkit's primary agent-facing protocol. The CLI and MCP adapters
invoke the same application services and enforce identical validation,
authority, mutation, event, and recovery semantics.

The default runtime is a single local process exposing a configured capability
catalog. Per-domain servers can be supported for isolation or debugging, but
do not define competing behavior.

- **PK-MCP-006:** behavior from the existing gateway and domain tools MAY be
  reused only when new v1 conformance fixtures approve it. Existing tool
  implementations and observed behavior are not normative.
- **PK-MCP-007:** semantics currently distributed across Python per-skill
  servers MUST be consolidated into the shared application core. Per-domain
  or per-skill servers MAY remain as thin protocol adapters with no independent
  validation, mutation, lifecycle, or event authority.

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

## Core read surface

The managed profile provides operations equivalent to:

```text
get_entity(id | path)
list_entities(type?, state?, scope?, limit?, cursor?)
search_entities(text, filters?, limit?, cursor?)
query_by_interface(interface, filters?, limit?, cursor?)
traverse_relations(subject, relation?, direction?, depth?)
events_for_subject(subject, after?, limit?, cursor?)
find_skill(task_description)
route_task(task_description, constraints?)
get_effective_configuration()
```

- **PK-MCP-010:** reads MUST come from canonical files or a verified index
  generation and MUST report index staleness when freshness cannot be proven.
- **PK-MCP-011:** pagination order and cursors MUST be deterministic for a
  stable generation.
- **PK-MCP-012:** search ranking MAY evolve compatibly, but filters, result
  identity, and completeness claims MUST be explicit.
- **PK-MCP-013:** a query MUST not expose private entity bodies or sensitive
  fields beyond the caller's configured local policy.

## Mutation surface

EntityTypes own typed create, update, transition, link, supersede, and archive
operations as applicable.

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

## Runtime and transports

- **PK-MCP-030:** stdio MUST be supported for local harness integration.
- **PK-MCP-031:** streamable HTTP MAY be supported only on loopback by default;
  non-loopback binding requires explicit authorization and an authentication
  and transport-security profile.
- **PK-MCP-032:** requests MUST have size and concurrency limits, cancellation,
  timeouts, and bounded error payloads.
- **PK-MCP-033:** the server MUST isolate request context and correlation data;
  concurrent responses MUST not leak data or diagnostics between requests.
- **PK-MCP-034:** graceful shutdown MUST stop accepting work, complete or
  cancel active operations according to contract, flush evidence, and release
  locks.

## Cross-repository coordination

- **PK-MCP-040:** processkit MAY expose export/import and external-reference
  operations, but each call remains scoped to one explicitly selected root.
- **PK-MCP-041:** a cross-repository handoff MUST identify source repository,
  source revision, owning entity, requested outcome, and sanitized evidence.
- **PK-MCP-042:** receiving a handoff MUST create local project-owned state;
  it MUST NOT mutate the source repository or claim distributed completion.
- **PK-MCP-043:** portfolio orchestration remains a consumer of processkit
  contracts and is outside the processkit agent runtime.
