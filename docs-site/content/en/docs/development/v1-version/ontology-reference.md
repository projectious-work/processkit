---
title: Ontology Reference
description: T/P/D/C ontology baseline for processkit v1.0.
---

# Ontology Reference

`processkit-v1.0-rfc-draft.md` is the leading document for the v1.0
ontology. When older analysis conflicts with this page, the RFC and this
page win.

## T/P/D/C Classes

The RFC names four implementation classes. If a note says `TCDP`, read it
as the same four classes, with the RFC's canonical order written as
`T/P/D/C`.

| Class | Meaning | Description |
|---|---|---|
| `T` | Terminology / foundational fragment | A concept, slot, or meta-mechanic that has no independent entity lifecycle. T concepts are reused in schemas, state machines, constraints, and generated fragments. |
| `P` | Primitive | An atomic persistent entity kind with its own schema, lifecycle, ID policy, validation contract, and storage path. P concepts can be composed into C concepts. |
| `D` | Discriminator | A typed variant of a parent primitive, usually represented by `kind:` or an equivalent closed enum. D concepts inherit the parent schema and lifecycle. |
| `C` | Composition | A named kind assembled from primitives plus T fragments. C concepts can have their own lifecycle, but their schema is built from composed parts. |

## Counts

The v1.0 target is 89 ontology concepts.

| Class | Count | Rule |
|---|---:|---|
| `T` | 19 | Reusable vocabulary and schema mechanics; no independent persistence. |
| `P` | 22 | Atomic persisted entity families with schemas and state machines. |
| `D` | 24 | Parent-primitive variants with inherited lifecycle. |
| `C` | 24 | Generated composed kinds assembled from P and T parts. |
| **Total** | **89** | The RFC count is the release target. |

## Full Working Inventory

This inventory makes the RFC's count concrete for implementation
planning. It preserves the RFC settlements: `Location` and `Skill` are
primitives, `Service` and `TeamMember` are compositions, `Position` is a
role-slot Binding discriminator, and `Hierarchy` is a named
parent-child Binding discriminator.

### T: Foundational Concepts

| Concept | Description |
|---|---|
| State | A named condition within a lifecycle, such as `open`, `accepted`, `done`, or `archived`. |
| Transition | A valid movement between states, including required actors, guards, and event emission. |
| StateMachine | The complete lifecycle graph for a kind, discriminator, or composition. |
| Lifecycle | The operational meaning of a state machine, including terminal states and audit expectations. |
| Constraint | A rule that restricts valid data, links, transitions, or composition. |
| Guard | A precondition checked before a transition, command, or write-side tool action runs. |
| Identity | The stable identity contract for an entity, including ID format, aliases, and lookup rules. |
| Versioning | The version contract for schemas, entities, generated files, and release artifacts. |
| Ownership | The accountable actor, role, or team responsible for an entity or process surface. |
| Immutability | The rule that some evidence, event, hash, or historical decision must not be rewritten. |
| Schema | The structured validation contract for an entity or fragment. |
| Composition | The build-time assembly of fragments and primitives into a generated runtime schema. |
| Inheritance | The explicit reuse of a parent schema or fragment by a child composition. |
| Uniqueness | A rule that one value, relation, or role-slot can exist only once in a defined scope. |
| Interface | A shared query surface declared by schemas, such as `Record` or `Versioned`. |
| ValidationMode | The per-kind mode that decides whether validation is strict or tolerant during migration. |
| Provenance | The source and transformation trail for content, decisions, generated schemas, and migrations. |
| Visibility | The audience and disclosure boundary for an entity or generated export. |
| Cardinality | The allowed count for fields, relations, owners, children, or bindings. |

### P: Atomic Primitives

| Primitive | Description |
|---|---|
| Actor | A human, agent, service account, organization, or other participant that can own, perform, or be assigned work. |
| Artifact | A durable evidence object such as a design, report, release note, analysis, fixture, or generated output. |
| Binding | A typed relation between entities, actors, roles, containers, or claims. |
| Capability | A durable ability or capacity that an actor, system, role, or service can provide. |
| Channel | A communication or handoff surface, including chat, queue-like inboxes, issue streams, and runtime buses. |
| Command | An intended action issued by a human, agent, hook, or process. |
| Container | A structural grouping boundary such as a portfolio, ART, team, project, scope, or repository area. |
| Event | A recorded occurrence in the system, including transitions, tool calls, releases, and external signals. |
| Gate | A decision or policy checkpoint that must pass before a process can continue. |
| Location | A spatial, site, coordinate, logical-region, or timezone anchor. |
| Note | Captured knowledge that may be fleeting, promoted, linked, or archived. |
| Outcome | A result, effect, delivery state, metric result, or observed consequence. |
| Policy | A governing rule, standard, permission, or organizational constraint. |
| Proposition | A claim about the world, work, risk, belief, forecast, or estimate. |
| Queue | An ordered or claimable work intake, handoff, or processing surface. |
| Record | A durable process record family for decisions, logs, measurements, approvals, and historical evidence. |
| Recurrence | A repeating schedule, cadence, ritual, or trigger rule. |
| Resource | A consumed or governed asset, including budget, compute, environment, credential, material, or tool capacity. |
| Role | A reusable responsibility bundle that can be assigned to actors or team members. |
| Skill | A first-class processkit capability package with its own schema, lifecycle, triggers, and tooling. |
| Specification | A formal description of a schema, process, role, gate, service, goal, schedule, channel, queue, or test. |
| WorkItem | A unit of requested or planned work with acceptance criteria, state, and evidence. |

### D: Discriminator Variants

| Discriminator | Parent | Description |
|---|---|---|
| Risk | Proposition | A claim about uncertainty, impact, probability, mitigation, and ownership. |
| Belief | Proposition | A held assumption or judgment that may need evidence or revision. |
| WorldFact | Proposition | A factual claim treated as externally true until contradicted. |
| WSJFEstimate | Proposition | A weighted shortest-job-first estimate or related prioritization claim. |
| Assumption | Proposition | A premise accepted temporarily to enable planning or execution. |
| GeographicRegion | Location | A country, region, market, jurisdiction, or other broad geographic area. |
| Site | Location | A physical office, facility, datacenter, or operating site. |
| Coordinate | Location | A precise coordinate or geospatial point. |
| LogicalRegion | Location | A logical deployment, business, data, or governance region. |
| Timezone | Location | A timezone anchor for schedules, teams, or operational windows. |
| Disposition | Capability | A tendency, affordance, or BFO-style disposition exposed as capability vocabulary. |
| Portfolio | Container | A strategic investment or governance container above programs and ARTs. |
| ValueStream | Container | A flow of value across products, teams, systems, and delivery steps. |
| ART | Container | An Agile Release Train or equivalent multi-team delivery container. |
| Team | Container | A small delivery or operating group. |
| Project | Container | A bounded initiative, repository, product effort, or implementation scope. |
| Scope | Container | A bounded area of authority, work, release, or applicability. |
| Hierarchy | Binding | A named parent-child relation used as the canonical hierarchy anchor. |
| Position | Binding | A role-slot relation with nullable subject until a TeamMember or Actor fills it. |
| ProvenanceLink | Binding | A relation from a derived entity to its source, import, generator, or evidence. |
| Correlation | Binding | A relation stating that two entities refer to related or equivalent concerns. |
| Dependency | Binding | A relation stating that one entity depends on another. |
| OwnershipLink | Binding | A relation assigning accountability or stewardship. |
| RelatedTo | Binding | A low-specificity relation used only when no stronger binding type applies. |

### C: Compositions

| Composition | Description |
|---|---|
| TeamMember | `C(Actor + calendar + capabilities + persona + skill-list + journal)`. |
| DecisionRecord | `C(Record + Proposition + alternatives + consequences + lifecycle)`. |
| LogEntry | `C(Record + Event + immutable timestamp + actor + subject)`. |
| Measurement | `C(Record + metric definition + observed value + provenance)`. |
| Archive | `C(Record + retention policy + source hash + location)`. |
| ProcessSpecification | `C(Specification + states + transitions + guards + commands)`. |
| GoalSpecification | `C(Specification + desired outcomes + measures + owners)`. |
| Service | `S(Capability)/C`: a provided capability with interface, owner, SLOs, and resources. |
| RoleSpecification | `C(Specification + responsibilities + authority + expected skills)`. |
| GateSpecification | `C(Specification + policy + required evidence + pass/fail semantics)`. |
| SchemaSpecification | `C(Specification + YAML schema + interfaces + validation mode)`. |
| ScheduleSpecification | `C(Specification + recurrence + timezone + calendar constraints)`. |
| TestSpecification | `C(Specification + fixture + expected result + acceptance signal)`. |
| ChannelSpecification | `C(Specification + channel protocol + participants + retention rules)`. |
| QueueSpecification | `C(Specification + queue discipline + claim rules + retry policy)`. |
| WorkItemTemplate | `C(WorkItem + reusable acceptance criteria + default bindings)`. |
| Migration | `C(Command + Event + source schema + target schema + validation evidence)`. |
| ScopePlan | `C(Container + WorkItem set + owners + acceptance gate)`. |
| Roadmap | `C(Container + GoalSpecification + sequencing + milestones)`. |
| ProgramIncrement | `C(Container + cadence + objectives + risks + demo evidence)`. |
| Iteration | `C(Container + cadence + committed work + review evidence)`. |
| Release | `C(Container + Gate + Artifact bundle + provenance + versioning)`. |
| Discussion | `C(Record + Channel + Proposition thread + outcome capture)`. |
| EvaluationRun | `C(Command + TestSpecification + Event + Measurement + Artifact evidence)`. |
