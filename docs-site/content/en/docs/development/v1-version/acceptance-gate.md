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

## Detailed RFC Criteria

The detailed list below expands the RFC gate into checkable criteria for
planning and implementation. Criteria marked `soft` may be waived with a
recorded rationale. All other criteria are strict.

### P0 - Pre-conditions

| ID | Criterion |
|---|---|
| P0.1 | Upstream agrees to host the `v1.0` feature branch or records an explicit alternative branch/repository model. |
| P0.2 | The RFC is accepted as the leading document for ontology, release, validation, indexing, and cutover planning. |
| P0.3 | A named maintainer contact or owner exists for reviewing v1.0 changes. |
| P0.4 | The v0.x maintenance boundary and backport policy are documented before v1.0 feature work begins. |
| P0.5 | The baseline corpus, migration source, and release-gate evidence locations are frozen for Phase 1. |

### O1 - Ontology Completeness

| ID | Criterion |
|---|---|
| O1.1 | The 89-concept T/P/D/C ontology inventory is documented with 19 T, 22 P, 24 D, and 24 C entries. |
| O1.2 | Each concept has a canonical name, class, description, and migration note from the v0.x model where applicable. |
| O1.3 | The grammar-leak concepts rejected by the RFC are excluded from the entity layer. |
| O1.4 | `Location` is modeled as a primitive with geographic-region, site, coordinate, logical-region, and timezone variants. |
| O1.5 | `Skill` is modeled as a primitive with its own schema and lifecycle, distinct from `Capability`. |
| O1.6 | `TeamMember` is modeled as a composition of Actor, calendar, capabilities, persona, skill-list, and journal. |
| O1.7 | `Service` is modeled as `S(Capability)/C`, not as a primitive. |
| O1.8 | `Proposition` is modeled as the parent for risk, belief, world-fact, WSJF estimate, and related epistemic content. |
| O1.9 | `Hierarchy` and `Position` are represented through Binding variants, including nullable role-slot subject support. |
| O1.10 | Soft: each ontology concept has at least one concrete example from a SAFe or agentic software workflow. |
| O1.11 | Soft: human-facing glossary language is reviewed for non-specialist readability. |

### T2 - Tooling Parity

| ID | Criterion |
|---|---|
| T2.1 | Jinja + YAML schema sources ship under `context/schemas/src/`. |
| T2.2 | Generated flat schemas are committed under `context/schemas/_generated/` and consumed by runtime tooling. |
| T2.3 | Composition supports `extends`, `{% include %}`, and `__merge: replace|concat|name-merge`. |
| T2.4 | The MCP endpoint `regenerate_schemas(kinds: list \| None) -> {rebuilt, unchanged, errors}` exists. |
| T2.5 | Full and partial schema regeneration are both deterministic and test-covered. |
| T2.6 | Per-kind validation mode is observable through MCP. |
| T2.7 | Strict validation fails invalid migrated entities; tolerant validation warns for kinds still being migrated. |
| T2.8 | MCP create/read/update/transition paths exist for the alpha entity set, use generated schemas, and expose typed doctor remediation dispositions. |
| T2.9 | Entity and remediation writes emit required events and update the read index or report index drift. |
| T2.10 | Search includes FTS5 plus interface grouping; the canned-query set is signed off before rc. |
| T2.11 | All MCP tools have valid Python type signatures and matching draft-2020-12 JSON Schemas; every doctor-declared remediation tool exists in the gateway catalog with compatible arguments. |
| T2.12 | Soft: local developer commands make schema rebuild, validation, and MCP smoke tests easy to run. |

### C3 - Corpus Migration

| ID | Criterion |
|---|---|
| C3.1 | A migration plan maps every v0.x entity kind to a v1.0 primitive, discriminator, composition, archive, or explicit rejection. |
| C3.2 | Declarative migration planning and execution run repeatably from a clean checkout, enforce expected source hashes, and record source/target processkit versions. |
| C3.3 | Migrated entities preserve stable IDs or record durable predecessor/successor links and aliases that the read index resolves. |
| C3.4 | Field loss is measured and stays within the RFC's maximum 5 percent ceiling. |
| C3.5 | Unknown fields are preserved, transformed, or reported; they are not silently dropped. |
| C3.6 | LogEntry hash and append-only invariants are checked during migration; history rewrites require explicit policy, source hashes, and archived originals. |
| C3.7 | Orphaned entities, broken required links, and invalid required owners hard-fail the migration. |
| C3.8 | Migrated strict kinds pass generated-schema validation. |
| C3.9 | Migration reports include counts, warnings, failures, typed remediation guidance, and doctor recheck results. |
| C3.10 | A representative v0.x fixture corpus is detected, planned, migrated, and rechecked with documented local commands without aibox. |

### S4 - Skills And Agents

| ID | Criterion |
|---|---|
| S4.1 | Skill metadata and routing instructions use the v1.0 ontology names and storage semantics. |
| S4.2 | Skills that write process entities call MCP tools instead of hand-editing canonical context files. |
| S4.3 | Skill examples demonstrate query-by-interface and typed relation lookup where appropriate. |
| S4.4 | Multi-persona and harness prompts are updated to prevent v0.x primitive assumptions. |
| S4.5 | Agent handoff, role, TeamMember, and model-routing documentation reflects the v1.0 TeamMember composition. |
| S4.6 | At least 20 canned agent scenarios exercise work, decisions, gates, risks, roles, skills, and artifacts. |
| S4.7 | Scenario runs keep malformed entity output below 0.1 percent. |
| S4.8 | Skills and agent docs include transition guidance for v0.x adopters. |

### A5 - First-ART Validation

| ID | Criterion |
|---|---|
| A5.1 | A real or production-shaped ART is modeled with Portfolio, ValueStream, ART, Team, Scope, and RoleSlot structure. |
| A5.2 | PI planning creates objectives, risks, dependencies, capacity assumptions, and committed WorkItems. |
| A5.3 | Execution moves work through state machines using MCP transition tools. |
| A5.4 | Decisions, assumptions, risks, and world facts are recorded as the correct Record/Proposition shapes. |
| A5.5 | Gates represent approval, policy, evaluation, and release checks with required evidence. |
| A5.6 | TeamMember, Role, Skill, Capability, and Binding data support realistic task routing. |
| A5.7 | Channels and queues capture handoffs, intake, or asynchronous coordination. |
| A5.8 | Resources, constraints, and ownership are queryable for the ART. |
| A5.9 | Demo evidence is captured as Artifacts, Measurements, Outcomes, or related Records. |
| A5.10 | Inspect-and-adapt produces follow-up WorkItems, Decisions, and retrospective evidence. |
| A5.11 | Interface queries retrieve mixed-kind records without concrete-kind guessing. |
| A5.12 | Relation traversal answers dependency, provenance, ownership, and hierarchy questions. |
| A5.13 | Generated schemas validate all strict entities created during the cycle. |
| A5.14 | pk-doctor reports no blocking errors on the ART fixture or pilot corpus. |
| A5.15 | Human reviewers can inspect the same state through files and documentation. |
| A5.16 | Runtime-specific integrations are examples only; the ART proof does not require one agent framework. |
| A5.17 | The pilot records friction, interpretation drift, and missing tool affordances as tracked issues. |
| A5.18 | The first-ART result is reviewed and accepted before rc promotion. |

### G6 - Cutover Decision Point

| ID | Criterion |
|---|---|
| G6.1 | Phases P0 through A5 are green except for explicitly accepted soft criteria. |
| G6.2 | The final ontology and migration plan are accepted by the named maintainer/owner. |
| G6.3 | The cutover DecisionRecord or equivalent release decision is recorded. |
| G6.4 | Release artifacts are reproducible from a clean checkout. |
| G6.5 | Documentation for install, migration, MCP tooling, schemas, indexes, and testing is published. |
| G6.6 | Downstream adoption paths are documented for production, alpha/beta/rc, and final v1.0 pins. |
| G6.7 | v0.x maintenance, LTS, and feature-backport boundaries are documented. |
| G6.8 | No known blocker remains for merging `v1.0` to `main` and tagging `v1.0.0`. |

### R7 - Post-cutover Stabilisation

| ID | Criterion |
|---|---|
| R7.1 | A minimum 14-day post-cutover stabilisation window is observed. |
| R7.2 | Critical regressions have documented owner, status, and remediation path. |
| R7.3 | Migration support handles at least one downstream adopter from v0.x to v1.0. |
| R7.4 | Release integrity checks verify tags, tarballs, checksums, provenance, and docs publication. |
| R7.5 | Index rebuild and drift-recovery procedures are exercised after cutover. |
| R7.6 | MCP gateway and per-domain MCP tools pass smoke tests in a clean fixture project. |
| R7.7 | Sensitive-data, privacy, and publication checks run on the shipped docs and release artifacts. |
| R7.8 | Soft: v0.x LTS guidance is validated with at least one slow-adopter scenario. |
| R7.9 | New pk-doctor checks pass a golden adversarial fixture containing deliberately invalid entities. |

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

- the implemented beta inventory targets approximately 60-70% of the
  89-concept ontology (roughly 54-62 concepts), with explicit exclusions;
  this directional coverage target complements rather than replaces the
  capability and evidence criteria below
- the ontology has expanded beyond the alpha subset with migration proof
- all migrated kinds validate strictly
- core MCP tools have stable signatures
- MCP Python signatures match draft-2020-12 JSON Schemas
- docs cover user workflows and architecture
- pk-doctor checks the important invariants
- pk-doctor passes a golden adversarial fixture
- each actionable finding names an installed tool with compatible arguments
  or a recognized policy, migration, archive, or external disposition
- runtime integration examples exist
- OKF import and export are both tested
- human review and approval workflows are represented

## Release Candidate Gate

Release candidate is ready when:

- schema generation is deterministic
- migration tools are repeatable
- doctor remediations execute through the shipped gateway and recheck cleanly
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
