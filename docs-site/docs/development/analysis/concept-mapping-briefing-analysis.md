---
title: Concept Mapping Briefing Analysis
description: Historical concept-mapping analysis for processkit v1.0.
---

# Concept Mapping Briefing Analysis

Source: `concept-mapping-2026-05-16.md`

Analyzed: 2026-07-04

Supersession note: `processkit-v1.0-rfc-draft.md` is now the guiding
briefing for processkit v1.0. Where this analysis conflicts with the
[processkit v1.0 RFC analysis](./processkit-v1-rfc-analysis.md), the
RFC analysis wins. Keep this file as historical interpretation of the
earlier concept-mapping input, not as current implementation guidance.

The filename dates the briefing to 2026-05-16, but the document itself
continues through Round 17 on 2026-05-20. Treat it as a mid-May design
snapshot, roughly six to seven weeks old as of this analysis.

## Executive Read

The document starts as a reconciliation exercise: preserve processkit's
closed primitive set and map missing concepts onto fields, sub-kinds, or
Binding types. It does not stay there.

By the later rounds, the recommendation has shifted to a greenfield
ontology for a new processkit version:

- keep the processkit target from the v0.x line
- replace the old "small closed primitive set plus many special cases"
  model with a richer orthogonal ontology
- promote several abstract parents to first-class atomic primitives
- model domain terms through discriminators and compositions
- support large agent-heavy organizations by making vocabulary explicit
  enough for agents to reason over

The most important sentence operationally is in Round 16: for a
10-human, many-agent company doing roughly 500-person work, the document
recommends going full greenfield.

## Relationship To Base Context

The briefing preserves these base-context invariants:

- processkit remains provider-neutral and harness-neutral
- project memory remains structured, versioned, and agent-readable
- repository-local process data remains the source of truth
- migrations remain explicit
- rich skills and MCP tooling remain part of the product
- old `context/` dogfood history is evidence, not a payload to ship

It challenges these base-context assumptions:

- the current v0.x primitive set is no longer treated as the likely target
- current schemas are evidence, not constraints
- "no new primitives" is rejected by later rounds
- `kind=` discriminators alone are insufficient for the greenfield model
- composition support becomes load-bearing

The base context says "do not change the product target." This briefing
does not change the target. It changes the ontology and implementation
strategy for reaching that target.

## Evolution Inside The Document

The early section says:

- zero new primitives required
- keep the closed primitive set
- add fields, `known_kinds`, `known_types`, and Binding kinds
- use an editorial Content / Structure / Governance framing

The middle rounds add:

- a fourth level: Specification / Type / Meta
- a cross-cutting Relation stratum
- explicit Definition / Instance / Record thinking, then later simplify
  back to level-only organization
- a class column:
  - `T`: terminology only
  - `P`: primitive
  - `D`: discriminator on a parent primitive
  - `C`: composed schema

The late rounds settle on a greenfield-corrected cut:

- parent concepts such as `Record`, `Specification`, `Container`,
  `Policy`, `Event`, and `Capability` become atomic primitives
- children such as `DecisionRecord` and `LogEntry` become compositions
  under `Record`
- some grammar-level concepts are dropped as too low-level
- the greenfield model is judged sufficient for SAFe-style scaling

This means the final recommendation should be read from Rounds 13-17,
not from the opening "zero new primitives" finding.

## Final Ontology Shape

The final stable shape in the document has five levels:

- Specification / Type / Meta
- Content
- Structure
- Governance
- Relation

It classifies concepts by four implementation classes:

- `T`: concept only, no schema
- `P`: atomic primitive with its own YAML schema
- `D`: discriminator variant on a parent primitive
- `C`: composed schema assembled from primitive blocks

Round 14/15 reports:

- 35 foundational concepts
- 47 specifics
- 82 concepts total
- 21 primitives
- 19 discriminators
- 23 compositions
- 19 terminology concepts

The very last delta table also says Round 14 drops from 87 to 81
concepts after removing six grammar-leak concepts. This conflicts with
the Round 14/15 total of 82 because Round 15 adds `Uniqueness`. For
future work, treat the effective final count as 82 unless newer input
clarifies otherwise.

The RFC is that newer input. The current processkit v1.0 target is 89
concepts: 19 T, 22 P, 24 D, and 24 C.

## Candidate Atomic Primitives

The greenfield model's important `P` candidates are:

Specification / Type / Meta:

- `Specification`

Content:

- `Artifact`
- `Capability`
- `Command`
- `Discussion`
- `Message`
- `Note`
- `Proposition`
- `Queue`
- `Record`
- `Resource`
- `Token`
- `WorkItem`

Structure:

- `Actor`
- `Channel`
- `Container`
- `Role`

Governance:

- `Event`
- `Gate`
- `Policy`

Relation:

- `Binding`

Some of these overlap with old processkit primitives. Others are new or
promoted from concepts previously represented by fields, sub-kinds, or
runtime behavior.

## Major Reclassifications

The biggest conceptual shift is parent promotion:

- `Record` becomes primitive; `DecisionRecord`, `LogEntry`,
  `Measurement`, `Outcome`, and `Archive` become Record-derived forms.
- `Container` becomes primitive; `Scope` becomes a composition or
  specific container form.
- `Specification` becomes primitive; schema, process, role, gate,
  schedule, goal, service, channel, queue, and test specifications become
  composed specifications.
- `Policy` becomes primitive instead of being represented only through
  Artifact + Binding + Gate composition.
- `Event` becomes primitive and pairs with `Command`.
- `Proposition` becomes primitive and absorbs `Belief`, `WorldFact`,
  and `Risk` as discriminator variants.
- `Capability` becomes primitive and absorbs `Skill`, `Authority`, and
  `Service` as specific forms.
- `Binding` remains primitive, but `Hierarchy`, `Position`,
  `Correlation`, and `Provenance` become Binding variants.

These changes are incompatible with simply importing v0.27.1 schemas.
They require a deliberate model redesign.

## Load-Bearing Design Decisions

The document creates several decisions that should be confirmed before
implementation:

1. Adopt full greenfield ontology rather than incremental v0.27.x
   evolution.
2. Treat Round 14/15 as the baseline cut, subject to newer inputs.
3. Use 5 levels: Specification / Content / Structure / Governance /
   Relation.
4. Use T/P/D/C classification to decide storage shape.
5. Promote `Record`, `Specification`, `Container`, `Event`, `Policy`,
   `Capability`, `Proposition`, `Command`, `Message`, `Queue`,
   `Resource`, `Token`, and `Channel`.
6. Demote old first-class children such as `DecisionRecord` and
   `LogEntry` to composed Record forms in the greenfield model.
7. Keep `Binding` as the relation primitive and express hierarchy,
   provenance, position, and correlation as Binding variants.
8. Use `Proposition` as the shared parent for belief, fact, and risk.
9. Demote Service to a Capability-specific composition, unless newer
   SOA-oriented input reverses that.
10. Keep spatial/location and BFO disposition out of the core model.

The RFC supersedes item 10: `Location` is now a primitive and
`Capability{kind=disposition}` is explicitly included.

None of these should be silently encoded as implementation work without
a current confirmation pass, because the briefing is dated.

## Composition Strategy

The document rejects a false binary between duplicated flat schemas and
runtime `$ref`.

Recommended path:

1. Start with Option 8: runtime-only composition.
   Schemas may duplicate initially, while tests and polymorphic query
   behavior enforce shared interfaces.
2. Evolve toward Option 3: build-time generation.
   Source uses composition; generated runtime schemas are flat YAML.
3. Keep Option 7 available: `extends:` annotation with a lightweight
   loader.

The RFC supersedes this staged path. processkit v1.0 should use
build-time Jinja + YAML schema generation from the start, with committed
`_generated/*.yaml` output.

## Scaling Argument

The document tests the model against:

- 10 humans plus agents doing roughly 500-person work
- 100 humans plus agents doing roughly 5000-person work
- SAFe / ART / portfolio structures

Its conclusion:

- today's model is too weak for this
- a reduced model improves agentic workflows but under-models cadence,
  channel, policy, and goal vocabulary
- the greenfield model reaches near-complete SAFe modelling capability
- further 10x scale does not require new concepts

The remaining scale problems are engineering and governance:

- composition tooling
- indexing and search
- federation
- throughput
- bulk operations
- interpretation drift
- agent training on canonical meanings

This strongly implies that processkit v1.0 should invest early in
indexing, composition tests, and canonical ontology documentation.

## Questions Resolved By The RFC

The document left these unresolved or only implicitly resolved. The RFC
now settles them for processkit v1.0:

- Position is `Binding{kind=role-slot}` with nullable subject.
- Belief, WorldFact, Risk, and WSJF-estimate sit under Proposition.
- Service is `S(Capability)/C`, not a primitive.
- Hierarchy remains a named concept implemented as
  `Binding{kind=parent-child}`.
- Location is a primitive with five discriminator variants.
- `Capability{kind=disposition}` is included.
- The final concept count is 89, not 81 or 82.
- The RFC supersedes Round 14/15 where they conflict.

## Implications For processkit v1.0 Build-Up

The new project should not start by copying the old `src/context/`
schemas wholesale. The better path is:

1. Preserve the product target and release discipline from the first
   version.
2. Treat old schemas, skills, and MCP servers as implementation evidence.
3. Define the greenfield ontology contract first.
4. Decide the first-phase primitive set and class assignment.
5. Create schema-generation or runtime-composition policy.
6. Build minimal tooling around the new primitives:
   - ID generation
   - schema validation
   - state transitions
   - entity index
   - relation queries
   - migrations
7. Port or rewrite skills after the new ontology is stable.
8. Use migration adapters to ingest old-processkit context where needed.

The first implementation milestone should be a thin vertical slice, not
the whole ontology:

- one or two Specification forms
- `Record`
- `WorkItem`
- `Binding`
- `Container` or `Scope`
- `Event` / `Command`
- index and validation support

Then expand through compositions and discriminators.

## Risks

- The document is internally inconsistent because it records an evolving
  discussion, not a single final spec.
- It references companion Notes and Decisions that are not present in
  this new repository.
- It was produced before later project learning, so its final
  recommendation may be superseded.
- Going full greenfield creates a migration burden from processkit v0.x.
- Composition tooling can become a project inside the project.
- Agents may benefit from rich vocabulary, but humans may find the
  ontology too abstract without good docs and examples.

## What The RFC Resolves

The later RFC answers the briefing's implementation questions:

- The intended baseline is the RFC's 89-concept T/P/D/C ontology.
- v1.0 is a greenfield rebuild with migration/import bridges from v0.x.
- The composition mechanism is build-time Jinja + YAML generation.
- SAFe / many-agent scaling remains the main ontology pressure.
- The first deliverable is a phase-gated alpha built around ontology
  completeness and tooling parity.

## Working Interpretation

Until newer input says otherwise, use this as the working direction:

processkit v1.0 should preserve processkit's product promise but rebuild
the core model around the RFC's greenfield 89-concept ontology. The old
project is evidence and migration source, not a schema constraint.
Implementation should follow the RFC's build-time schema generation,
interface-aware indexing, and 81-criterion gate.
