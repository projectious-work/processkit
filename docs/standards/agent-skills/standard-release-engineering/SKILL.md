---
name: standard-release-engineering
description: Company verification and release-engineering standards, including human-controlled host phases. Use when defining test layers or verification gates, preparing or publishing a release, building release artifacts and provenance, or running release work that needs the host outside the dev container.
---

# standard-release-engineering

Binding company standard. The rules below are the summary; the linked file is authoritative. Read only the section the task needs.

## Software verification and release-engineering standard

Branch promotion moves an already proven commit. Select checks by product
profile and change risk, verify exact candidate artifacts, and independently
verify what was published.

Full standard: `docs/standards/software-verification-and-release-engineering.md`. Sections:

- Purpose and relationship to branching
- Release identity and chain of custody
- Test layers
- Verification gates
- Implementation integrity
- Regression, isolation, and reliability
- Release artifacts and provenance
- Release record

## Human-controlled host-phase execution standard

Prepare immutable candidates in the restricted environment, cross the host
boundary through a portable versioned handover, validate without credentials,
and publish only from finalized evidence through narrowly bounded authority.

Full standard: `docs/standards/human-controlled-host-phase-execution.md`. Sections:

- Purpose and applicability
- Normative security boundary
- Producer/verifier protocol
- Lifecycle and storage classes
- Bootstrap and executable resolution
- Capability adapters
- Validation and publication
- Operator contract
- Coverage, vulnerabilities, and caches
- Conformance

## Host-gated release conformance

Implementations of host-phase execution pass every applicable mandatory case group (handover and lifecycle, bootstrap and environment, capability adapters, validation and publication). Record candidate identity, platform, adapter, outcome, evidence paths, and a reason for every skip. Negative cases pass only when the gate refuses safely with the expected failure evidence.

Full standard: `docs/standards/host-gated-release-conformance.md`. Sections:

- Purpose
- Mandatory case groups
- Reference profiles
