# Ontology

## Role of the ontology

The ontology is the common language in which an organization defines how it
works. processkit publishes it complete and versioned, uses it for its own
content kinds, and lets authors use any of its concepts inside their
standards and process definitions.

The ontology describes both definitions and instances. processkit stores and
serves definitions only. Instance concepts remain part of the vocabulary so a
definition can talk about them: a ticket-handling ProcessSpecification names
the WorkItem type it governs, its StateMachine, its Roles, and its Gates, but
no ticket is ever stored by processkit.

| Side | Examples | processkit |
|---|---|---|
| Definition | Policy, Specification, ProcessSpecification, StateMachine, RoleSpecification, GateSpecification, WorkItemTemplate, Skill, Service, Role, Container, Binding, DecisionRecord | stores, validates, composes, serves |
| Instance | WorkItem, Event, LogEntry, Outcome, Measurement, EvaluationRun, Iteration | vocabulary inside definitions only |

- **PK-MODEL-001:** processkit MUST publish one versioned ontology registry
  containing every concept with its class, side, description, parent
  primitive where applicable, relations, and schema or fragment location.
- **PK-MODEL-002:** every concept MUST be classified as definition or
  instance. A concept used both ways MUST be split or documented with the
  rule that decides which use is stored.
- **PK-MODEL-003:** processkit MUST NOT persist, serve, or validate content
  whose kind is an instance concept. Definitions MAY reference instance
  concepts by name as vocabulary.
- **PK-MODEL-004:** the registry, schemas, and generated reference
  documentation MUST be produced from one source and checked for drift.

## T/P/D/C class system

| Class | Contract |
|---|---|
| T — foundational concept | Reusable schema or mechanic without independent persistence. |
| P — primitive | Atomic concept with identity, schema, and relations. |
| D — discriminator | Closed typed variant of a parent primitive. |
| C — composition | Named concept assembled from primitives and foundational fragments. |

## Inventory

The v1 ontology contains 90 concepts: the 89-concept inventory of earlier
processkit work plus Labeling.

### T — foundational concepts (20)

State, Transition, StateMachine, Lifecycle, Constraint, Guard, Identity,
Versioning, Ownership, Immutability, Schema, Composition, Inheritance,
Uniqueness, Interface, ValidationMode, Provenance, Visibility, Cardinality,
and Labeling.

### P — primitives (22)

Actor, Artifact, Binding, Capability, Channel, Command, Container, Event,
Gate, Location, Note, Outcome, Policy, Proposition, Queue, Record, Recurrence,
Resource, Role, Skill, Specification, and WorkItem.

### D — discriminators (24)

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

- **PK-MODEL-005:** every concept in the inventory MUST be present in the
  published registry with a definition-or-instance classification and a
  schema or fragment. Coverage of the full inventory is a release gate.
- **PK-MODEL-006:** concepts from scaling frameworks, such as ART,
  ValueStream, ProgramIncrement, and WSJFEstimate, MUST be usable but MUST NOT
  be required by any processkit content kind or default.

## Common envelope

Every stored item uses one envelope. The metadata shape is published as
[`resource-metadata.schema.json`](../../schemas/v1/resource-metadata.schema.json).

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

- **PK-MODEL-010:** every item MUST declare `apiVersion`, `kind`,
  `metadata.name`, and `spec`. `metadata.name` MUST be unique per kind within
  its namespace and stable across file moves.
- **PK-MODEL-011:** `metadata.namespace` MUST name a Container; omitted means
  the repository's root Container. Containers form a tree through the
  Hierarchy relation; cycles and unknown parents are validation errors.
- **PK-MODEL-012:** `metadata.labels` MUST be selectable key/value pairs with
  bounded key and value syntax and a bounded count. `metadata.annotations`
  MUST NOT be selectable and MUST NOT influence access decisions.
- **PK-MODEL-013:** the key prefix `processkit.projectious.work/` is reserved.
  Authored content MUST NOT set reserved keys.
- **PK-MODEL-014:** authored content lives in `spec`. Validation result,
  content digest, source path, provenance, and other derived facts MUST be
  reported as `status` and MUST NOT be authored.
- **PK-MODEL-015:** unknown fields MUST fail validation unless the owning
  schema declares an extension map. Extension fields MUST be namespaced and
  MUST NOT redefine ontology fields.
- **PK-MODEL-016:** a schema MUST distinguish absent, null, empty, and default
  values whenever they have different semantics.

## Relations

- **PK-MODEL-020:** relations MUST declare type, subject, target, and optional
  scope or validity bounds. Relation types MUST define direction,
  cardinality, endpoint constraints, and inverse.
- **PK-MODEL-021:** references MUST use typed names, `<kind>/<name>` or
  `<kind>/<namespace>/<name>`. Filenames and Markdown links are not identity.
- **PK-MODEL-022:** a reference to an inherited item MUST resolve through the
  inheritance lock and MUST carry the upstream identity in results.
- **PK-MODEL-023:** an unresolved reference MUST remain visible as unresolved
  and MUST fail validation where the owning schema requires it.

## Standards reuse

processkit keeps JSON files and published JSON Schemas as its contracts. It
does not make RDF, OWL, SHACL, JSON-LD, or another knowledge graph a runtime
dependency.

- **PK-MODEL-030:** generic descriptive metadata SHOULD follow Dublin Core
  Terms where the meaning fits exactly, and provenance SHOULD follow the W3C
  PROV model where the meaning fits.
- **PK-MODEL-031:** an exported JSON-LD or other semantic-web projection MAY
  be offered later; it MUST be generated from the registry and MUST NOT become
  a second source.

## Extensions

- **PK-MODEL-040:** a repository MAY add namespaced concepts, discriminators,
  relation types, and content kinds. They MUST validate against published
  extension metaschemas and declare their namespace owner.
- **PK-MODEL-041:** extensions MUST NOT redefine published concepts.
  Inherited repositories MAY use an upstream extension; its namespace owner
  remains the upstream repository.
- **PK-MODEL-042:** an addition to the published ontology MUST demonstrate
  need across at least two unrelated domains, declare its class and side,
  and provide compatibility and migration treatment.
- **PK-MODEL-043:** processkit's own repositories MUST use the published
  ontology and schemas only and MUST NOT define private concepts.
