# v1.0 Version

> Planning hub for the processkit v1.0 rebuild.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

The v1.0 version is the planned greenfield rebuild described by
`processkit-v1.0-rfc-draft.md`. It keeps the processkit product promise
but replaces the current v0 ontology and tooling internals with an
89-concept T/P/D/C model, generated schemas, stronger MCP contracts, and
automated validation.

This section is the working design package for the v1 development line.

## Core Documents

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

---

Section pages:

- [Acceptance Gate](/processkit/v1.x/docs/development/v1-version/acceptance-gate/): Readiness criteria for processkit v1.0 stages.
- [Alpha Release Testing](/processkit/v1.x/docs/development/v1-version/alpha-release-testing/): Publish and consume an explicit v1 prerelease safely.
- [Alpha Scope](/processkit/v1.x/docs/development/v1-version/alpha-scope/): First buildable vertical slice for processkit v1.0.
- [Alpha.3 Closure Plan](/processkit/v1.x/docs/development/v1-version/alpha3-closure-plan/): Feature-completion gates for the final pre-cutover alpha.
- [Analysis Archive](/processkit/v1.x/docs/development/v1-version/analysis/): Supporting analysis used to shape the processkit v1.0 plan.
- [Architecture Specification](/processkit/v1.x/docs/development/v1-version/architecture-specification/): Architectural direction for processkit v1.0.
- [Beta Ontology Plan](/processkit/v1.x/docs/development/v1-version/beta-ontology-plan/): Dependency-aware target for processkit v1.0 beta coverage.
- [Branch Start Work Plan](/processkit/v1.x/docs/development/v1-version/branch-start-work-plan/): Phase plan for beginning the processkit v1.0 branch.
- [Landscape Note](/processkit/v1.x/docs/development/v1-version/landscape-note/): Adjacent projects and concepts processkit should learn from.
- [Ontology Reference](/processkit/v1.x/docs/development/v1-version/ontology-reference/): T/P/D/C ontology baseline for processkit v1.0.
- [Product Specification](/processkit/v1.x/docs/development/v1-version/product-specification/): Product definition for processkit v1.0.
- [Test Strategy](/processkit/v1.x/docs/development/v1-version/test-strategy/): Automated testing strategy for processkit v1.0.
- [Tooling Architecture](/processkit/v1.x/docs/development/v1-version/tooling-architecture/): MCP, schema, and index architecture for processkit v1.0.
- [v0 Reconciliation](/processkit/v1.x/docs/development/v1-version/v0-reconciliation/): Controlled carry-over from the supported v0 line into v1.
