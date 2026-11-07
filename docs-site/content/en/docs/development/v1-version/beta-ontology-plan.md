---
title: Beta Ontology Plan
description: Dependency-aware target for processkit v1.0 beta coverage.
---

> **Alpha.4 documentation review:** This page records design or historical
> planning. For shipped behavior and current gaps, use the
> [issue #135 implementation review](./issue-135-status.md).

## Target

The beta target is 62 of the ontology's 89 concepts, or 69.7%. This keeps the
accepted goal inside the 60–70% range while leaving room to validate the model
through real workflows before completing the long tail.

Coverage is counted by ontology category:

| Category | Beta target |
|---|---:|
| Terminology | 19 |
| Primitives | 22 |
| Discriminators | 8 |
| Compositions | 13 |
| **Total** | **62** |

The alpha's 18 generated contracts are the first dependency-complete slice of
this target.

## Implementation Status

The beta inventory is now frozen in
`src/context/schemas/src/registry.yaml` and contains exactly 62 unique
concepts:

- all 19 foundational terminology concepts
- all 22 atomic primitives
- the 8 selected discriminators
- the 13 selected compositions

The executable portion produces 43 generated schema contracts. The difference
between 62 concepts and 43 schemas is intentional: terminology concepts are
reusable schema and lifecycle mechanics rather than independently persisted
entity kinds. A contract test enforces the four category counts, uniqueness,
and presence of every generated output.

## Selected Discriminators

The beta discriminator set is:

- Risk
- Belief
- WorldFact
- WSJFEstimate
- Assumption
- Scope
- Hierarchy
- Position

## Selected Compositions

The beta composition set is:

- TeamMember
- DecisionRecord
- LogEntry
- Migration
- ProcessSpecification
- GoalSpecification
- RoleSpecification
- GateSpecification
- SchemaSpecification
- ScheduleSpecification
- TestSpecification
- ChannelSpecification
- QueueSpecification

## Selection Rules

Concepts enter the beta set when they support a real processkit workflow,
unlock another selected concept, or provide interoperability value. Parent
concepts count independently because their contracts are generated and tested.
Variants are represented as discriminators rather than false top-level kinds.

The 27 concepts outside the beta target remain valid ontology candidates; they
are deferred, not rejected.

## Promotion Gates

Beta promotion requires:

- a stable, dependency-closed list of exactly 62 implemented concepts
- generated schemas and state machines for every selected executable concept
- MCP create, transition, query, and relation coverage where the concept owns
  lifecycle behavior
- representative migration from a v0.x corpus
- OKF export and import conformance
- at least one end-to-end process cycle using the beta model
- deterministic generation, fixture, package, docs, and release-audit checks
  passing through the local release gate
