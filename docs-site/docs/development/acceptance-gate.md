---
title: Acceptance Gate
description: Readiness criteria for processkit v1.0 stages.
---

# Acceptance Gate

## Purpose

The acceptance gate keeps the v1.0 rebuild measurable. The RFC's
81-criterion gate is authoritative for final cutover; the staged lists
below are working summaries for alpha-first execution.

## RFC Cutover Gate

| Phase | Criteria | Strict | Soft |
|---|---:|---:|---:|
| P0 - Pre-conditions | 5 | 5 | 0 |
| O1 - Ontology completeness | 11 | 9 | 2 |
| T2 - Tooling parity | 12 | 9 | 3 |
| C3 - Corpus migration | 10 | 10 | 0 |
| S4 - Skills and agents | 8 | 8 | 0 |
| A5 - First-ART validation | 18 | 18 | 0 |
| G6 - Cutover decision point | 8 | 8 | 0 |
| R7 - Post-cutover stabilisation | 9 | 8 | 1 |
| **Total** | **81** | **75** | **6** |

A5 is the proof phase: model a real ART end to end and run one full PI
cycle through planning, execution, demo, and inspect-and-adapt.

## Alpha Gate

Alpha is ready when:

- the alpha ontology subset is documented
- schemas are generated and committed
- MCP create/read/transition paths work for alpha entities
- `query_by_interface` works for at least one shared interface
- strict and tolerant validation modes are observable
- a small v0.x corpus migrates or maps into the alpha model
- processkit-native fixture tests pass without depending on aibox
- one real process cycle runs through the alpha
- OKF export produces a conformant bundle
- docs build locally

## Beta Gate

Beta is ready when:

- the ontology has expanded beyond the alpha subset with migration proof
- all migrated kinds validate strictly
- core MCP tools have stable signatures
- MCP Python signatures match draft-2020-12 JSON Schemas
- docs cover user workflows and architecture
- pk-doctor checks the important invariants
- pk-doctor passes a golden adversarial fixture
- runtime integration examples exist
- OKF import and export are both tested
- human review and approval workflows are represented

## Release Candidate Gate

Release candidate is ready when:

- schema generation is deterministic
- migration tools are repeatable
- acceptance fixtures cover adversarial cases
- docs, examples, and publishing scripts are stable
- a real project has run a full planning and delivery cycle
- package smoke tests pass from release artifacts without aibox
- no known blocker remains for v1.0.0 cutover

## Final Gate

v1.0.0 is ready when:

- the cutover decision is recorded
- the final ontology and migration plan are accepted
- docs are published
- release artifacts are reproducible
- downstream projects have a supported adoption path
- v0.x maintenance and v1.x development boundaries are documented
