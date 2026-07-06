---
title: processkit v1.0 RFC Analysis
description: Analysis of the guiding RFC for the processkit v1.0 redesign.
---

# processkit v1.0 RFC Analysis

Source: `processkit-v1.0-rfc-draft.md`

Analyzed: 2026-07-04

Status for this project: guiding briefing. Where this RFC conflicts with
`concept-mapping-2026-05-16.md` or
[concept-mapping-briefing-analysis.md](./concept-mapping-briefing-analysis.md),
this RFC wins.

## Executive Read

The RFC turns the earlier concept-mapping work into an implementation
and release proposal. It is no longer just an ontology discussion. It
asks upstream processkit maintainers to host a full v1.0 greenfield
rebuild on a parallel `v1.0` branch while `main` continues v0.x
maintenance.

The product target from the base context remains intact: processkit is
still provider-neutral process memory, skills, and MCP tooling for
agentic software projects. The RFC changes the model and build plan used
to reach that target.

The RFC's operational direction is:

- full greenfield ontology rebuild
- 89 concepts in T/P/D/C classes
- Jinja + YAML schema composition
- committed build-time `_generated/` schemas
- new `regenerate_schemas` MCP endpoint
- interface-aware polymorphic queries
- strict/tolerant per-kind validation during migration
- 9-12 month rebuild on a `v1.0` branch
- alpha, beta, rc, final pre-release progression
- 81-criterion cutover gate before `v1.0.0`

## Authority And Evidence

The RFC cites:

- `DEC-DeepTide`: rebuild authorization
- `DEC-BraveAtlas`: 81-criterion cutover gate
- `DISC-BriskWillow`: 20-round ontology discussion
- upstream issues `#74` and `#75` as pk-doctor reliability evidence

Those DEC/DISC entities are not indexed in this new repository, so they
were not locally verifiable through processkit MCP.

I also checked the private `projectious-work/internal` repository as an
external evidence source:

- `origin/main`
  `44704b451d4baa53d04eb0e53c1bc01a41f6627e`
  (`2026-05-16T20:18:07+02:00`)
- `origin/policy-primitive-trigger-reeval-2026-06-29`
  `8197000d5951ae5e5303e6f2ca868d9f7b4e9ad9`
  (`2026-06-29T07:05:29Z`)

That repository verifies `DISC-BriskWillow` at
`context/discussions/`
`DISC-20260515_1955-BriskWillow-is-hierarchy-a-primitive-are-higher.md`.
The discussion is active, supersedes the earlier `DISC-OpenPanda`
record, and carries forward the hierarchy / abstraction-level question.
It also says the proposed decision was leaning toward editorial
three-level framing without new primitives or schema migration, with
hierarchy remaining composable through existing parent / Scope / Role /
Binding shapes.

The same internal repository did not contain `DEC-DeepTide` or
`DEC-BraveAtlas` by filename, ID token, or all-history search on the
available branches. The June branch only adds
`tmp/policy-primitive-trigger-reeval-2026-06-29.md`, which corroborates
that `DISC-BriskWillow` is a live non-Policy primitive-admission
question but does not provide the missing RFC decision records.

Treat the RFC as the authority because the user explicitly selected it
as the guiding document. Treat `DEC-DeepTide` and `DEC-BraveAtlas` as
unresolved external provenance to be imported, recreated, or replaced by
new local decision records before irreversible implementation cutover.

## What Supersedes The Earlier Concept Mapping

The earlier analysis treated Round 14/15 as the likely baseline and
noted open questions. The RFC closes or changes several of those points.

The RFC now says:

- final ontology count is 89 concepts, not 81/82
- `Location` is a new primitive
- `Skill` is a primitive, not a composition
- `TeamMember` is a composition, not `Actor{kind=team-member}`
- `Service` is `S(Capability)/C`, not a primitive
- `Position` is `Binding{kind=role-slot}` with nullable subject
- `Location` has five discriminator variants
- `Capability{kind=disposition}` settles the disposition question
- build-time Jinja + YAML composition is the preferred mechanism
- `_generated/` output is committed
- processkit v1.0 should be built upstream on a `v1.0` branch, not only
  in this derived repo

Any earlier note saying "confirm this later" should be read as resolved
when the RFC makes a concrete settlement.

## Ontology Direction

The current v0.x 13-primitive ontology is rejected as insufficient. The
RFC says it cannot cleanly model AI-first SAFe execution at 100x5000
scale without both:

- missing first-class concepts, and
- grammar concepts leaking into the entity layer

The intended v1.0 ontology uses four concept classes:

- `T`: foundational terminology or meta-mechanic, no own lifecycle
- `P`: atomic primitive with schema, lifecycle, and persistence
- `D`: discriminator variant of a primitive
- `C`: composition of primitives and terminology fragments

Final RFC counts:

- `T`: 19
- `P`: 22
- `D`: 24
- `C`: 24
- total: 89

## Key Primitive Settlements

The RFC explicitly calls out these settlements:

- `Proposition` is a new primitive. It is the parent for Belief, Risk,
  WorldFact, WSJF-estimate, and related epistemic content.
- `Location` is a new primitive, with discriminator variants for
  geographic region, site, coordinate, logical region, and timezone.
- `Skill` is a primitive with its own schema and lifecycle, distinct
  from Capability.
- `Capability` remains a primitive; `Service` is composed from
  Capability.
- `TeamMember` becomes a composition of Actor plus calendar,
  capabilities, persona, skill list, and journal.
- `Position` is a Binding variant with nullable subject.
- `Hierarchy` remains named for mental anchoring but is implemented as
  `Binding{kind=parent-child}`.

These are guiding decisions for processkit v1.0 unless later input
supersedes the RFC.

## Implementation Mechanics

The RFC rejects runtime `$ref` as the main solution and chooses
build-time generation:

- schema sources live under `schemas/src/`
- Jinja templates render into flat `_generated/*.yaml`
- runtime tools consume `_generated/`
- `_generated/` is committed to git
- composition uses `extends: parent.yaml`
- templates use `{% include %}` for T fragments
- merge behavior uses `__merge: replace|concat|name-merge`

This is more specific than the earlier "Option 8 first, Option 3 later"
guidance. The RFC chooses the build-time path directly.

Required MCP endpoint:

```python
regenerate_schemas(kinds: list | None) -> {rebuilt, unchanged, errors}
```

The same endpoint handles full and partial rebuilds. `aibox apply`
triggers full rebuilds by default, with opt-out for fast iteration.

## Validation And Indexing

Validation is phase-gated:

- migrated kinds: strict validation
- kinds still migrating: tolerant validation, warn but pass
- per-kind validation mode must be observable through MCP

Indexing extends the existing FTS5 surface rather than replacing it.
Schemas declare interfaces:

```yaml
interfaces: [Record, Versioned]
```

The required new query capability is:

```text
query_by_interface(Record, ...)
```

This is load-bearing. The RFC identifies it as the fix for agent routing
failures where agents have to choose between WorkItem, DecisionRecord,
Artifact, LogEntry, and similar concrete kinds.

## Branch And Release Model

The RFC proposes an upstream `v1.0` feature branch:

- `main` continues v0.x.y maintenance
- `v1.0` receives all greenfield rebuild work
- alpha, beta, rc, and final tags are cut from `v1.0`
- final cutover merges `v1.0` into `main` and tags `v1.0.0`
- derived projects opt in by pinning `aibox.toml` to alpha/beta/rc tags

Backport policy:

- security fixes flow both ways
- dependency bumps flow at maintainer discretion
- feature work does not backport either way

This keeps the 9-12 month divergence bounded.

## Cutover Gate

The RFC adopts an 81-criterion acceptance gate:

- 75 strict criteria
- 6 soft criteria
- 8 phases

Phases:

- P0: pre-conditions
- O1: ontology completeness
- T2: tooling parity
- C3: corpus migration
- S4: skills and agents
- A5: first-ART validation
- G6: cutover decision point
- R7: post-cutover stabilization

The most important proof phase is A5: model a real ART end to end and
run one full PI cycle in the new ontology.

The RFC highlights these specific acceptance constraints:

- `regenerate_schemas(kinds: list | None)` MCP endpoint is required
- search must include FTS5 plus interface grouping
- canned query set must be signed off before rc
- all MCP tools need valid Python type signatures and matching
  draft-2020-12 JSON Schemas
- pk-doctor must pass a golden adversarial fixture

## Upstream Asks

The RFC asks upstream maintainers for:

1. host the `v1.0` feature branch upstream
2. endorse merge-to-main and `v1.0.0` release model
3. accept the backport policy
4. name an upstream owner/contact
5. adopt DEC-BraveAtlas or counter-propose a release gate

It explicitly does not ask upstream for engineering capacity.

## Timeline

Indicative timeline:

- months 1-2: composition tooling and first alpha
- months 3-4: parent promotion and migration scripts
- months 5-6: specification compositions plus Channel, Queue, Resource,
  Container; beta begins
- months 7-9: skills, MCP tools, doctor, indexer; beta to rc
- months 10-12: cutover and first ART on v1.0
- post-cutover: at least 14 days stabilization

The gate, not the calendar, decides release progress.

## Risks

The RFC's main risks:

- upstream rejects branch model
- single derived-project decider bottlenecks sign-off
- pk-doctor bugs hide failures
- corpus migration loses data
- agents drift into non-canonical interpretations
- long-lived `main` / `v1.0` divergence becomes hard to merge

The RFC mitigates these through the RFC itself, DEC-BraveAtlas tracking,
adversarial doctor fixtures, migration loss ceilings, agent scenario
tests, and strict backport policy.

## Implications For This Repository

For processkit v1.0, this RFC should become the primary planning
baseline:

- do not build from the old v0.27.1 schema set
- do not follow the earlier 81/82-concept Round 14/15 interpretation
- use the RFC's 89-concept shape as current guidance
- plan schema tooling before broad schema migration
- make interface-aware indexing a first-class requirement
- design validation modes before migrating live corpora
- treat pk-doctor rewrite/hardening as part of v1.0, not afterthought
- prepare for upstream-branch workflow or a fork fallback

The first concrete work products should be:

1. local copy of the RFC analysis and conflict rules
2. ontology inventory derived from the 89-concept RFC
3. phase-zero work plan for composition tooling
4. local representation of the 81-criterion gate
5. decision record for processkit v1.0 adopting this RFC as guidance

The fifth item should be recorded through processkit DecisionRecord MCP
only after explicit acceptance, or when the user asks us to start
planning work items.

## Conflict Rule

If `processkit-v1.0-rfc-draft.md` conflicts with
`concept-mapping-2026-05-16.md`, the RFC wins.

If the RFC conflicts with old processkit v0.27.1 implementation, the RFC
wins for processkit v1.0 design, while v0.27.1 remains migration-source
evidence.

If later user-provided input conflicts with the RFC, analyze that input
explicitly and decide whether it supersedes this RFC.
