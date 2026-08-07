# Ontology contracts

This chapter refines high-use ontology concepts and defines the conformance
contract for the complete inventory in the conceptual-model chapter. The
named refinements below do not reduce v1 scope: every one of the 89 canonical
concepts is a release requirement.

## Complete-ontology requirements

- **PK-ENTITY-000:** the release MUST publish a machine-readable ontology
  registry containing every canonical concept, its T/P/D/C class, description,
  owner, interfaces, dependencies, and schema or fragment location.
- **PK-ENTITY-004:** every P primitive and C composition MUST have a closed
  entity schema, storage declaration, identity policy, interface metadata,
  lifecycle declaration where mutable, and positive and negative fixtures.
- **PK-ENTITY-005:** every D discriminator MUST be a closed variant of its
  declared parent P schema, inherit the parent's lifecycle and storage rules,
  and publish fixtures proving both valid specialization and invalid mixing.
- **PK-ENTITY-006:** every T foundational concept MUST have one canonical
  schema fragment or registry contract and MUST be exercised by at least one
  generated P or C schema.
- **PK-ENTITY-007:** ontology generation MUST fail on an unknown class,
  duplicate canonical name, missing parent, dependency cycle, unconsumed T
  concept, uncovered discriminator, or composition with unresolved parts.
- **PK-ENTITY-008:** a release coverage report MUST prove 19/19 T, 22/22 P,
  24/24 D, and 24/24 C concepts complete. Partial ontology coverage prevents
  v1.0.0 release.

## Work and reasoning

### WorkItem

- **PK-ENTITY-001:** WorkItem MUST record title, type, lifecycle state,
  priority, description or acceptance outcome, and optional assignee, parent,
  scope, dependencies, blockers, and governing decisions.
- **PK-ENTITY-002:** standard WorkItem types are `task`, `story`, `bug`,
  `epic`, `spike`, and `chore`; extensions use namespaced values.
- **PK-ENTITY-003:** the default lifecycle is
  `backlog → in_progress → review → done`, with explicit `blocked`,
  `cancelled`, reopen, and correction paths. Terminal completion records
  completion time and evidence where required.

### DecisionRecord

- **PK-ENTITY-010:** DecisionRecord MUST contain title, state, context,
  decision, rationale, alternatives, consequences, deciders, and decision time
  when accepted.
- **PK-ENTITY-011:** its lifecycle is `proposed → accepted → superseded` or
  `proposed → rejected`; accepted history is not edited to represent a new
  decision.
- **PK-ENTITY-012:** supersession MUST link both records and preserve the old
  rationale independently of the new record.

### Discussion

- **PK-ENTITY-020:** Discussion MUST contain a driving question, state,
  participants or audience, related subjects, and chronological contributions
  or a durable body representing the inquiry.
- **PK-ENTITY-021:** discussion outcomes reference accepted DecisionRecords,
  created WorkItems, promoted Artifacts, or an explicit no-decision result.
- **PK-ENTITY-022:** closing a Discussion MUST NOT imply agreement unless an
  accepted outcome says so.

### Note

- **PK-ENTITY-030:** Note captures bounded uncommitted information as one of
  `fleeting`, `insight`, `question`, or `reference`, with title, body, source,
  tags, and optional review time.
- **PK-ENTITY-031:** promotion creates or links a durable target; it does not
  silently mutate a Note into a different EntityType.

## Evidence and governance

### Artifact

- **PK-ENTITY-040:** Artifact identifies a durable deliverable or external
  pointer with name, kind, location or body, format, version, ownership,
  producer, digest where reproducibility matters, and related subjects.
- **PK-ENTITY-041:** registration does not assert that an external location is
  available or trusted; verification state and observed revision remain
  explicit.

### Gate

- **PK-ENTITY-050:** Gate defines a stable check with description, kind,
  validator contract, required authority, blocking behavior, and evidence
  requirement.
- **PK-ENTITY-051:** evaluations are append-only events referencing the Gate;
  a Gate definition MUST NOT be mutated after evaluation history in a way that
  changes the meaning of past results.
- **PK-ENTITY-052:** outcomes are `passed`, `failed`, or `waived`; waiver
  requires authority, reason, scope, and expiry or review condition.

### Scope

- **PK-ENTITY-060:** Scope defines a bounded project, release, milestone,
  sprint, quarter, or namespaced interval with goals, optional parent, time
  bounds, and lifecycle.
- **PK-ENTITY-061:** closing Scope MUST evaluate required completion gates and
  record unresolved owned work rather than implying it disappeared.

### Migration

- **PK-ENTITY-070:** Migration records source/target contracts, state,
  preconditions, operations, affected paths or entities, evidence, progress,
  and applied or rejection outcome.
- **PK-ENTITY-071:** migration lifecycle and semantics follow the migration
  requirements in the compatibility chapter and cannot embed arbitrary code.

### LogEntry

- **PK-ENTITY-080:** LogEntry uses the event contract from the conceptual model
  and is append-only after successful creation.
- **PK-ENTITY-081:** event types have a registered owner and schema; unknown
  event details MUST NOT be interpreted as a known event type.

## People, teams, and relations

### Actor

- **PK-ENTITY-090:** Actor represents a human, AI agent, service, or
  organization with display identity, active status, optional contact or
  handle, declared capabilities, and privacy classification.
- **PK-ENTITY-091:** provider credentials, secret model identifiers, and
  mutable runtime session state MUST NOT be stored in ordinary Actor entities.

### Role

- **PK-ENTITY-100:** Role defines provider-neutral responsibilities, required
  capabilities or skills, and default scope; a Role is not a person or model.
- **PK-ENTITY-101:** changing the meaning of a Role with historical bindings
  requires versioning or supersession rather than silent reinterpretation.

### TeamMember

- **PK-ENTITY-110:** TeamMember composes an Actor identity with team-facing
  role defaults, persona, capability references, and bounded memory locations.
- **PK-ENTITY-111:** private memory, credentials, and runtime working state use
  separately classified storage and are excluded from exports by default.
- **PK-ENTITY-112:** TeamMember identity remains provider-neutral; runtime
  model selection is a policy or Binding resolved at invocation time.

### Binding

- **PK-ENTITY-120:** Binding is the canonical scoped or time-bounded relation
  entity and contains relation type, subject, target, optional scope,
  validity, conditions, and description.
- **PK-ENTITY-121:** Binding validation enforces the relation registry's
  endpoint, cardinality, inverse, and temporal rules.

## Durable execution record

- **PK-ENTITY-130:** a durable execution record binds an exact
  ProcessSpecification version to a project root, Scope, initiator, inputs,
  ordered state, produced entities, evidence, and completion or recovery
  Outcome.
- **PK-ENTITY-131:** a durable execution record MUST expose the current
  actionable step and MUST distinguish waiting, blocked, failed, cancelled,
  and completed.
- **PK-ENTITY-132:** process execution may coordinate external work but records
  observed handoffs and results; it MUST NOT claim external completion without
  evidence from the owning system or repository.

## Schema acceptance

- **PK-ENTITY-140:** every persistent P or C concept MUST publish a closed
  schema, state machine where applicable, storage declaration, relation
  constraints, event vocabulary, and valid/invalid fixtures.
- **PK-ENTITY-141:** schemas MUST reuse one versioned common envelope and
  fragments without generating divergent copies of shared semantics.
- **PK-ENTITY-142:** generated schemas are release artifacts and MUST match
  generator inputs byte-for-byte under the deterministic generation command.
