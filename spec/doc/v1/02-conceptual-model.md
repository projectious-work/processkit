# Conceptual model

## Design rule

The core model is deliberately small. A concept belongs in the v1 kernel only
when processkit must validate its lifecycle or relationships consistently
across unrelated projects. Domain taxonomies belong in packages or project
extensions.

The earlier 89-concept T/P/D/C model is useful research, but breadth is not a
v1 success criterion. The clean v1 model optimizes for coherent invariants,
composability, and migration rather than maximum vocabulary coverage.

## Kernel concepts

| Concept | Purpose |
|---|---|
| Entity | Persisted typed project record with identity and version. |
| EntityType | Schema, lifecycle, storage, and interface declaration. |
| StateMachine | Allowed states, transitions, guards, and terminal states. |
| Relation | Typed edge between addressable subjects. |
| Event | Append-only fact describing an observed process change. |
| Policy | Project-owned rule controlling authority or validation. |
| Package | Versioned set of content and compatibility declarations. |
| Capability | Discoverable operation or knowledge surface. |
| ProcessDefinition | Reusable ordered or branching workflow contract. |
| ProcessRun | Project-owned execution state and evidence for a definition. |

## Standard entity types

- **PK-MODEL-000:** the managed profile MUST include these standard
  EntityTypes:

- WorkItem;
- DecisionRecord;
- Discussion;
- Note;
- Artifact;
- Actor;
- Role;
- TeamMember;
- Binding;
- Scope;
- Gate;
- Migration;
- LogEntry; and
- ProcessRun.

- **PK-MODEL-008:** profiles MAY omit EntityTypes they do not expose, but
  installed schemas and tools MUST agree exactly.

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

- **PK-MODEL-026:** a proposed new kernel concept MUST demonstrate at least two
  unrelated product domains, lifecycle semantics that packages cannot express
  safely, and a migration path. Otherwise it belongs in a package or project
  namespace.
