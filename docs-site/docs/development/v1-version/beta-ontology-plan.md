---
title: Beta Ontology Plan
description: Dependency-aware target for processkit v1.0 beta coverage.
---

# Beta Ontology Plan

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
  passing in CI
