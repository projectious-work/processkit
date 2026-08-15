# Conceptual model and ontology

## Design rule

The complete v1 ontology is a primary product capability, not an experiment or
optional extension. processkit v0 already demonstrated that a smaller
Git-native process model and validated agent operations work in principle.
v1 adds the semantic breadth required to express processes, organizations,
evidence, plans, communication, resources, and agentic work without forcing
unrelated concepts into generic tags or records.

The ontology remains framework-neutral. Domain packages may compose and extend
it, but MUST NOT redefine its canonical concepts or their class semantics.

The ontology is applied recursively at different organizational levels. A
deliverable repository may use it to govern product work, while a coordinating
repository may use the same concepts for strategy, portfolio goals, standards,
or cross-project decisions. This semantic consistency does not create a global
database: each repository remains authoritative only for the entities it owns.

## T/P/D/C class system

| Class | Count | Contract |
|---|---:|---|
| T — foundational concept | 19 | Reusable schema and lifecycle mechanic without independent persistence. |
| P — primitive | 22 | Atomic persistent entity family with identity, schema, storage, lifecycle, and interfaces. |
| D — discriminator | 24 | Closed typed variant of a parent primitive that inherits its storage and lifecycle. |
| C — composition | 24 | Named concept assembled from primitives and foundational fragments, with a generated schema and declared lifecycle. |
| **Total** | **89** | Complete mandatory v1 ontology. |

- **PK-MODEL-000:** the v1 ontology MUST contain exactly the 89 canonical
  concepts named below: 19 T, 22 P, 24 D, and 24 C concepts.
- **PK-MODEL-008:** a product profile MAY expose a smaller operational tool
  surface, but the standard v1 distribution MUST install and validate the
  complete ontology. Profile selection MUST NOT change concept meaning.

## Canonical ontology inventory

### T — foundational concepts (19)

State, Transition, StateMachine, Lifecycle, Constraint, Guard, Identity,
Versioning, Ownership, Immutability, Schema, Composition, Inheritance,
Uniqueness, Interface, ValidationMode, Provenance, Visibility, and
Cardinality.

### P — atomic primitives (22)

Actor, Artifact, Binding, Capability, Channel, Command, Container, Event,
Gate, Location, Note, Outcome, Policy, Proposition, Queue, Record, Recurrence,
Resource, Role, Skill, Specification, and WorkItem.

### D — discriminator variants (24)

| Parent primitive | Discriminators |
|---|---|
| Proposition | Risk, Belief, WorldFact, WSJFEstimate, Assumption |
| Location | GeographicRegion, Site, Coordinate, LogicalRegion, Timezone |
| Capability | Disposition |
| Container | Portfolio, ValueStream, ART, Team, Project, Scope |
| Binding | Hierarchy, Position, ProvenanceLink, Correlation, Dependency, OwnershipLink, RelatedTo |

### C — compositions (24)

TeamMember, DecisionRecord, LogEntry, Measurement, Archive,
ProcessSpecification, GoalSpecification, Service, RoleSpecification,
GateSpecification, SchemaSpecification, ScheduleSpecification,
TestSpecification, ChannelSpecification, QueueSpecification, WorkItemTemplate,
Migration, ScopePlan, Roadmap, ProgramIncrement, Iteration, Release,
Discussion, and EvaluationRun.

- **PK-MODEL-009:** canonical names, classes, parent primitives, and
  composition membership MUST be represented in one versioned ontology
  registry from which schemas, references, query metadata, and coverage
  reports are generated or mechanically checked.

## Common envelope

- **PK-MODEL-001:** every entity MUST declare a contract version, entity type,
  stable ID, creation time, and typed specification.
- **PK-MODEL-002:** mutable entities SHOULD declare an update time and MUST
  declare lifecycle state when their EntityType has a state machine.
- **PK-MODEL-003:** unknown fields MUST fail strict validation unless the
  owning schema explicitly declares an extension map.
- **PK-MODEL-004:** extension fields MUST be namespaced and MUST NOT redefine
  kernel or EntityType fields.
- **PK-MODEL-005:** IDs MUST be unique within a repository context and remain
  stable across path changes.
- **PK-MODEL-006:** references MUST use typed IDs or declared external
  references; filenames and Markdown links alone are not durable identity.
- **PK-MODEL-007:** a schema MUST distinguish absent, null, empty, and default
  values whenever they have different semantics.

## Lifecycle and mutation

- **PK-MODEL-010:** every state transition MUST name its source, destination,
  applicable guards, authority requirement, and emitted event.
- **PK-MODEL-011:** terminal-state mutation MUST be prohibited unless the
  EntityType defines an explicit correction or supersession operation.
- **PK-MODEL-012:** historical decisions and events MUST be superseded or
  corrected through traceable records, not silently rewritten.
- **PK-MODEL-013:** mutating operations MUST validate the complete resulting
  entity before replacing canonical state.
- **PK-MODEL-014:** successful mutations MUST emit their required domain event
  in the same operation boundary.
- **PK-MODEL-015:** failed validation or authorization MUST leave canonical
  files and derived indexes unchanged.

## Relations and interfaces

- **PK-MODEL-020:** relations MUST declare type, subject, target, and optional
  scope or validity bounds.
- **PK-MODEL-021:** relation types MUST define direction, cardinality,
  endpoint constraints, inverse behavior, and deletion semantics.
- **PK-MODEL-022:** interfaces MAY group EntityTypes by capability, such as
  `Record`, `Assignable`, or `Versioned`, but MUST NOT hide incompatible
  lifecycle semantics.
- **PK-MODEL-023:** querying by interface MUST return the concrete EntityType
  and contract version of every result.
- **PK-MODEL-024:** cross-repository references MUST carry repository identity,
  object identity, and observed revision where reproducibility matters.
- **PK-MODEL-025:** unresolved external references MUST remain visible and
  MUST NOT be treated as validated local relations.
- **PK-MODEL-027:** every persistent entity MUST have exactly one authoritative
  repository context. Other contexts MUST use qualified references, imported
  evidence, or explicitly non-authoritative projections rather than competing
  writable copies.
- **PK-MODEL-028:** authority MUST be scoped to a decision surface. A
  coordinating repository MAY own broader intent, policy, dependencies, and
  coordination processes, but MUST NOT thereby acquire implicit write
  authority over participant repositories.
- **PK-MODEL-029:** organizational structure MAY form a multi-level graph of
  coordinating and participating repositories. Where authority overlaps, the
  applicable contract MUST define precedence or require explicit resolution.

## Events

- **PK-MODEL-030:** LogEntry is the canonical append-only event record.
- **PK-MODEL-031:** an event MUST identify event type, time, actor or system
  authority, subject, outcome, and structured details appropriate to its type.
- **PK-MODEL-032:** event vocabulary and detail schemas MUST be versioned.
- **PK-MODEL-033:** operational logs MUST NOT be inserted into the domain
  event stream merely because they are available.
- **PK-MODEL-034:** corrections append new evidence and preserve original
  content or its cryptographic digest according to retention policy.

## Extensibility test

- **PK-MODEL-026:** additions beyond the canonical 89-concept v1 ontology MUST
  demonstrate reusable meaning across at least two unrelated product domains,
  declare whether they are T, P, D, or C, and provide compatibility and
  migration treatment. Otherwise they belong in a package or project
  namespace.
