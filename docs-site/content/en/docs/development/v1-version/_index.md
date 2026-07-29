---
title: v1.x Version
description: Architecture, implementation status, and evidence for the processkit v1 line.
---

The v1 line is an active prerelease, not only a design proposal.
`v1.0.0-alpha.4` supplies a native Rust lifecycle CLI, a signed release
contract, generated schemas, and the Python MCP runtime as visible project
content.

The RFC and planning pages in this section remain useful design history.
Statements written as future requirements are not evidence that a feature is
implemented. Use the implementation review for the current truth.

## Current Status

- [Issue #135 Implementation Review](./issue-135-status.md)
- [Alpha.4 Release Facts](../../reference/v1-alpha-release-facts.md)
- [Install and Use the v1 Alpha](../../getting-started/v1-alpha-tutorial.md)

The fixed architecture is:

- Rust owns release trust and project-content lifecycle.
- Python remains the authoritative MCP implementation.
- skills, schemas, processes, state machines, and entities remain files.
- `context/` is dogfood consumer state; `src/context/` is the release
  producer payload.
- the supported v0 line remains the default while v1 is exact-pin alpha.

## Design and Evidence Documents

- [Product Specification](./product-specification.md)
- [Architecture Specification](./architecture-specification.md)
- [Ontology Reference](./ontology-reference.md)
- [Tooling Architecture](./tooling-architecture.md)
- [Test Strategy](./test-strategy.md)
- [Alpha Scope](./alpha-scope.md)
- [Alpha Release Testing](./alpha-release-testing.md)
- [v0 Reconciliation](./v0-reconciliation.md)
- [Beta Ontology Plan](./beta-ontology-plan.md)
- [Branch Start Work Plan](./branch-start-work-plan.md)
- [Landscape Note](./landscape-note.md)
- [Acceptance Gate](./acceptance-gate.md)
- [Issue #135 Implementation Review](./issue-135-status.md)

## Supporting Analysis

- [Base Context](./analysis/base-context.md)
- [Concept Mapping Briefing Analysis][concept-mapping-analysis]
- [processkit v1.0 RFC Analysis](./analysis/processkit-v1-rfc-analysis.md)
- [OKF Compatibility Analysis](./analysis/okf-compatibility-analysis.md)
- [Start Assessment](./analysis/processkit-v1-start-assessment.md)

[concept-mapping-analysis]: ./analysis/concept-mapping-briefing-analysis.md

## Branch Contract

The v1 development line is isolated from v0 maintenance:

- schema source and generated schema machinery
- v1.0 ontology and migration adapters
- MCP gateway, helper, and index changes required by the RFC
- automated fixture suites and first-ART validation evidence
- docs and acceptance-gate updates for the v1 line

| Purpose | Branch | Tag policy |
| --- | --- | --- |
| v0 maintenance development | `v0.x-dev` | never tag |
| v0 integration | `v0.x-release` | stable v0 tags only |
| v1 development | `v1.x-dev` | never tag |
| v1 prerelease integration | `v1.x-pre-release` | v1 alpha, beta, and RC tags only |
| v1 GA integration | `v1.x-release` | stable v1 tags only |
| published history | `main` | contains every stable tagged release |

`v1.x-dev` merges to `v1.x-pre-release` for each prerelease. At general
availability, create `v1.x-release` from the selected prerelease state,
validate and tag there, then merge it into `main`. v0 follows the same
development-to-release-to-main pattern. Security fixes and dependency
bumps may flow between lines when needed; feature work does not
automatically backport.

## Historical-page convention

Every page below this section is reviewed against alpha.4, but several pages
describe a target gate or the reasoning that preceded implementation. Treat
the labels as follows:

- **Implemented** means executable code and release evidence exist.
- **Partial** means a safe subset exists and the remaining behavior is named.
- **Planned** means the page is a design contract, not a supported command.
- **Historical** means the page records an earlier alpha planning stage.
