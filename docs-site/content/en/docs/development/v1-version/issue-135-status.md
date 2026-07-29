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
| Implemented | 7 requirement clusters |
| Partial | 5 requirement clusters |
| Missing | 4 requirement clusters |

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
| Four native target platforms | **Missing** | Alpha.4 publishes only `aarch64-unknown-linux-gnu` |
| Bootstrap installer | **Missing** | Users manually download and install the native executable |
| Human exact-version online resolution | **Missing** | Human lifecycle commands still require `--distribution` |
| Python/`uv` runtime contract | **Partial** | Runtime manifest and documentation exist; offline preparation and native diagnosis are incomplete |
| Native `processkit doctor` and `processkit mcp` | **Missing** | `pk-doctor` and direct Python gateway operation exist, but no native command groups |
| Extracted-release MCP acceptance | **Implemented** | Package smoke starts the staged gateway and exercises representative tools |
| Repository dogfood update/recovery acceptance | **Partial** | Release boundary is checked; full disposable-repository update/interruption recovery is not yet a release gate |
| v0 migration and aibox parity | **Partial** | Compatibility inspection and explicit dispositions exist; no in-place native migration or complete parity proof |
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

- support for Linux x86_64 or either macOS architecture;
- a trusted `latest` resolver or bootstrap script;
- native `doctor`, `migrate`, `package`, `harness`, or `mcp` commands;
- removal of Python or `uv` as runtime dependencies;
- safe in-place migration of an existing v0 project; or
- GA stability of alpha contracts.

## Minimum Remaining Path

1. Publish and smoke-test Linux x86_64 and both macOS native assets.
2. Add a checksum-verifying, non-root bootstrap installer.
3. Resolve exact canonical versions and trust roots for human commands.
4. Implement native runtime diagnosis before native MCP supervision.
5. Exercise dogfood update/recovery and v0 migration against disposable
   repositories.
6. Demonstrate direct-CLI and aibox installed-state parity.
7. Generate release facts and help snapshots as part of release validation.

The guiding constraint remains: finish the trustworthy native lifecycle around
visible content and the Python MCP runtime before expanding conceptual breadth.
