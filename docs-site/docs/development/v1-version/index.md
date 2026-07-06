---
title: v1.0 Version
description: Planning hub for the processkit v1.0 rebuild.
---

# v1.0 Version

The v1.0 version is the planned greenfield rebuild described by
`processkit-v1.0-rfc-draft.md`. It keeps the processkit product promise
but replaces the current v0 ontology and tooling internals with an
89-concept T/P/D/C model, generated schemas, stronger MCP contracts, and
automated validation.

This section is the working design package for the `v1.0` development
branch.

## Core Documents

- [Product Specification](./product-specification.md)
- [Architecture Specification](./architecture-specification.md)
- [Ontology Reference](./ontology-reference.md)
- [Tooling Architecture](./tooling-architecture.md)
- [Test Strategy](./test-strategy.md)
- [Alpha Scope](./alpha-scope.md)
- [Branch Start Work Plan](./branch-start-work-plan.md)
- [Landscape Note](./landscape-note.md)
- [Acceptance Gate](./acceptance-gate.md)

## Supporting Analysis

- [Base Context](./analysis/base-context.md)
- [Concept Mapping Briefing Analysis][concept-mapping-analysis]
- [processkit v1.0 RFC Analysis](./analysis/processkit-v1-rfc-analysis.md)
- [OKF Compatibility Analysis](./analysis/okf-compatibility-analysis.md)
- [Start Assessment](./analysis/processkit-v1-start-assessment.md)

[concept-mapping-analysis]: ./analysis/concept-mapping-briefing-analysis.md

## Branch Contract

The `v1.0` branch is for the rebuild line only:

- schema source and generated schema machinery
- v1.0 ontology and migration adapters
- MCP gateway, helper, and index changes required by the RFC
- automated fixture suites and first-ART validation evidence
- docs and acceptance-gate updates for the v1.0 line

v0.x maintenance continues on `main` until the final cutover decision.
Security fixes and dependency bumps may flow both ways; feature work does
not automatically backport.

