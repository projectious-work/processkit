---
title: Alpha Scope
description: First buildable vertical slice for processkit v1.0.
---

# Alpha Scope

## Purpose

The alpha proves that the v1.0 model improves real agentic project work
before the project implements the full 89-concept ontology.

The alpha is a vertical slice, not a miniature final release.

## Scope

The alpha product slice is frozen to these 14 high-value concepts:

- WorkItem
- DecisionRecord
- Artifact
- LogEntry
- Binding
- Gate
- Role
- TeamMember
- Skill
- Capability
- Proposition
- Risk
- Scope
- Migration

Four prerequisite parent concepts are required to model that slice honestly:
`Actor` for `TeamMember`, `Container` for `Scope`, and `Command` plus `Event`
for `Migration`. The generated alpha contract therefore covers 18 of the
ontology's 89 concepts while preserving the 14-concept product scope.

All 18 schemas are generated from the registry. `Risk` and `Scope` are
discriminator overlays, while `TeamMember` and `Migration` are compositions
of their prerequisite interfaces.

## Required Capabilities

- Generate schemas for the alpha kinds.
- Create and transition entities through MCP tools.
- Query entities by ID, text, relation, and interface.
- Preserve structured LogEntries.
- Migrate a small v0.x corpus.
- Export a conformant OKF bundle.
- Publish the docs site locally and through GitHub Pages.
- Run automated fixture tests without requiring aibox.
- Run one real process cycle through the new model.

## Out Of Scope

- Full 89-concept implementation.
- Complete migration of every historical entity.
- Runtime-specific orchestration.
- Vector database integration.
- Public package stability guarantees.

## Alpha Proof

The alpha is successful when:

- a real work item moves from capture to completion
- at least one decision is recorded and linked
- artifacts and notes are attached as supporting evidence
- a gate or approval is represented
- event history is queryable
- an agent can retrieve the relevant context through MCP
- OKF export passes v0.1 conformance
- processkit-native tests pass without aibox
- a human can inspect the same state in files and docs

## Promotion Gates

Alpha promotion additionally requires:

- deterministic regeneration produces no diff
- every generated schema is valid JSON Schema draft 2020-12
- the representative fixture validates and indexes all declared interfaces
- discriminator identity survives indexing
- source and packaged context trees remain in sync
- the docs site, server smoke suite, and release audit pass
