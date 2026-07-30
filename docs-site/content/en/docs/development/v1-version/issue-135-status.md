---
title: "Issue #135 Implementation Review"
description: "Requirement-by-requirement review of the Rust CLI and Python MCP product briefing against v1.0.0-alpha.4."
weight: 2
---

This review compares
[GitHub issue #135](https://github.com/projectious-work/processkit/issues/135)
with `v1.0.0-alpha.4`. It distinguishes shipped evidence from target design.

## Summary

The corrected product boundary is established and the local lifecycle alpha
is substantial. The Rust executable safely verifies and applies an explicitly
provided release; Python remains the MCP runtime; release content remains
visible. The alpha is not yet the complete standalone experience described by
the issue.

| Outcome | Assessment |
| --- | ---: |
| Implemented | 8 requirement clusters |
| Partial | 7 requirement clusters |
| Missing | 1 requirement cluster |

Counts group related criteria so that large prose sections do not outweigh
user journeys.

## Coverage Matrix

| Requirement cluster | Status | Alpha.4 evidence or gap |
| --- | --- | --- |
| Rust CLI / Python MCP / visible-file boundary | **Implemented** | Rust binary under `installer/`; Python servers ship with skills; release and architecture docs state the fixed boundary |
| `context/` dogfood vs `src/context/` payload | **Implemented** | Release-boundary checks prevent project entities from entering the staged payload |
| Deterministic plan and transactional install/update/recover/uninstall | **Implemented** | `planner.rs`, `transaction.rs`, target lock/staging/journal tests, lifecycle pilot |
| Signed release and native verification | **Implemented** | Ed25519 envelope binds archive, descriptor, provenance, and ARM64 installer |
| Opaque `execute --request` automation contract | **Implemented** | Versioned request/result schemas and golden fixtures |
| Rust modularization and typed failures | **Partial** | Logic moved from the former monolith into focused modules with stable error tests; a separate public library crate and full API docs remain |
| README/help/schema consistency | **Mostly implemented** | Current local-distribution requirements agree; generated help snapshot/release facts automation remains |
| Four native target platforms | **Partial** | Alpha.4 publishes only ARM64 Linux; `v1.x-dev` can deterministically bind a collected four-target matrix, but native production/smoke remains |
| Bootstrap installer | **Partial** | `v1.x-dev` adds an exact-version, non-root, checksum/signature/fingerprint-verifying bootstrap; canonical key distribution and four published assets remain |
| Human exact-version online resolution | **Missing** | Human lifecycle commands still require `--distribution` |
| Python/`uv` runtime contract | **Mostly implemented** | Runtime policy, native diagnosis, dependency-profile preparation, and offline-readiness verification exist; resolved versions remain unlocked |
| Native `processkit doctor` and `processkit mcp` | **Mostly implemented** | `v1.x-dev` provides typed read-only doctor plus native MCP verify/serve/proxy supervision; broader host and signal acceptance remains |
| Extracted-release MCP acceptance | **Implemented** | Package smoke starts the staged gateway and exercises representative tools |
| Repository dogfood update/recovery acceptance | **Implemented** | The release gate combines the full-content lifecycle pilot with a deterministic real-process update interruption, rollback, user-data preservation, retry, and provenance verification |
| v0 migration and aibox parity | **Partial** | Exact fixtures exercise guarded transition, byte-preserving transactional corpus application, persisted loss/provenance evidence, and interruption recovery; mixed-root ownership baselines and aibox parity remain |
| Harness projection ownership | **Implemented** | Codex and Claude adapters preserve unrelated keys and have lifecycle tests |
| Stable/prerelease documentation story | **Partial** | Alpha.4 docs now separate v0 stable and v1 preview; generated facts and broader downstream validation remain |

## What Users Can Rely On

- exact local release inputs;
- checksum and Ed25519 verification;
- a non-mutating deterministic plan;
- transactional install and update with persisted ownership;
- recovery after interrupted installer transactions;
- conservative uninstall that preserves changed or user-owned files;
- installed-provenance verification;
- Codex and Claude managed-key projections;
- Python MCP operation from the extracted package; and
- versioned machine request/result envelopes for integrators.

## What Users Must Not Assume

- published support for Linux x86_64 or either macOS architecture;
- a trusted `latest` resolver or canonical release-key distribution;
- native semantic corpus migration, `package`, or `harness` commands;
- removal of Python or `uv` as runtime dependencies;
- safe in-place migration of an existing v0 project; or
- GA stability of alpha contracts.

## Minimum Remaining Path

1. Publish and smoke-test Linux x86_64 and both macOS native assets.
2. Publish a canonical trust root and resolve exact versions for human
   lifecycle commands without accepting a floating `latest`.
3. Add per-release ownership baselines for mixed v0 artifact, binding, role,
   and TeamMember roots.
4. Demonstrate direct-CLI and aibox installed-state parity.
5. Generate release facts and help snapshots as part of release validation.
6. Finish the public Rust library boundary and API documentation.

The guiding constraint remains: finish the trustworthy native lifecycle around
visible content and the Python MCP runtime before expanding conceptual breadth.
