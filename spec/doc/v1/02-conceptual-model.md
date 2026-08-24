# Conceptual model and ontology

## Design rule

Processkit v1 has a small repository-memory kernel and optional semantic
packages. The kernel contains only concepts needed to install, operate,
validate, query, migrate, and hand off durable project memory. Organizational,
scaling-framework, communication, location, scheduling, portfolio, and
evaluation concepts are not universal merely because projectious.work uses
them.

The existing 89-concept inventory is retained as design input for package
disposition, not as mandatory core or a v1.0.0 release gate. A concept may be
retained in the kernel, moved to an optional first-party package, aligned with
an established term, redesigned, or removed.

Packages may compose and extend kernel concepts, but MUST NOT redefine their
canonical semantics. Each repository remains authoritative only for the
entities it owns.

## T/P/D/C class system

| Class | Contract |
|---|---|
| T — foundational concept | Reusable schema and lifecycle mechanic without independent persistence. |
| P — primitive | Atomic persistent entity family with identity, schema, storage, lifecycle, and interfaces. |
| D — discriminator | Closed typed variant of a parent primitive that inherits its storage and lifecycle. |
| C — composition | Named concept assembled from primitives and foundational fragments, with a generated schema and declared lifecycle. |

- **PK-MODEL-000:** the v1 kernel MUST contain only the T/P/D/C concepts
  required by the mandatory repository-memory journeys. Optional packages MAY
  add concepts through the same registry and validation machinery.
- **PK-MODEL-008:** profile and package selection MUST NOT change the meaning
  of an installed concept.

## Provisional kernel inventory

The baseline kernel contains:

- the foundational schema, identity, versioning, ownership, lifecycle,
  validation, visibility, provenance, relation, and cardinality mechanics;
- the persistent primitives Actor, Artifact, Binding, Event, Note, Policy,
  Record, Role, Skill, Specification, and WorkItem; and
- the compositions DecisionRecord, Discussion, LogEntry, and Migration.

This is the maximum initial kernel, not a minimum quota. Phase 0 may remove or
merge a concept when the mandatory journeys remain explicit and type-safe.

- **PK-MODEL-040:** every kernel concept MUST be justified by at least one
  mandatory v1 user journey and MUST NOT exist only to support an optional
  package.
- **PK-MODEL-041:** optional concepts MUST remain absent from a core-only
  installation rather than appearing as empty schemas or disabled tools.

## Existing 89-concept candidate inventory

The following inventory is retained for the required disposition review. Its
presence in this chapter does not make a concept mandatory.

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

- **PK-MODEL-009:** installed canonical names, classes, parent primitives,
  package ownership, and composition membership MUST be represented in one
  versioned ontology registry from which schemas, references, query metadata,
  and coverage reports are generated or mechanically checked.

## Minimal standards reuse

Processkit keeps YAML or JSON Git files, published JSON Schemas, and explicit
state machines as its operational contracts. It does not make RDF, RDFS, OWL,
SHACL, JSON-LD, Wikidata, DBpedia, or another knowledge graph a runtime
dependency.

The initial semantic reuse assessment is deliberately narrow:

- use Dublin Core Terms as the reference semantics for generic descriptive
  metadata where the meaning fits exactly;
- use the W3C PROV model as the reference semantics for entity, activity,
  agent, plan, generation, derivation, association, attribution, and
  delegation concepts where the meaning fits; and
- evaluate other vocabularies only when a concrete kernel or optional-package
  requirement cannot be expressed cleanly with these foundations.

- **PK-MODEL-042:** reuse MUST be documented in a versioned concept
  disposition matrix as exact reuse, specialization, informative alignment,
  processkit-specific semantics, optional-package semantics, or removal.
- **PK-MODEL-043:** semantic alignment MUST NOT weaken processkit's
  closed-world schema validation, state-machine rules, repository authority,
  or deterministic mutation behavior.
- **PK-MODEL-044:** general semantic-web export and inference are future work
  and MUST NOT enter the v1 critical path.

## Canonical and derived graphs

The canonical entities and typed relations already form a graph-shaped domain
model. Graph storage is not another source of truth: it is a query projection
over exact entity identities, revisions, relation types, scopes, and validity
bounds.

- **PK-MODEL-045:** an explicit relation recorded by a validated Processkit
  operation is canonical according to its owning repository and contract.
- **PK-MODEL-046:** a relation inferred from prose, embeddings, model output,
  clustering, or another probabilistic method MUST remain derived retrieval
  evidence and MUST NOT establish truth, instruction trust, lifecycle,
  ownership, completion, or mutation authority.
- **PK-MODEL-047:** every inferred edge MUST identify its canonical sources
  and revisions or digests, extraction method and version, index generation,
  time, and confidence or equivalent uncertainty metadata.
- **PK-MODEL-048:** rebuilding or deleting a graph projection MUST NOT create,
  remove, or modify canonical entities or relations.

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

- **PK-MODEL-026:** additions to the kernel MUST demonstrate necessity across
  at least two unrelated product domains, declare whether they are T, P, D, or
  C, and provide compatibility and migration treatment. Otherwise they belong
  in an optional package or project namespace.
