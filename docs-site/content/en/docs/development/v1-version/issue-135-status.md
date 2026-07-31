---
title: "Issue #135 Implementation Review"
description: "Final requirement review of the Rust CLI and Python MCP product briefing against the v1.x development line."
weight: 2
---

This final review compares
[GitHub issue #135](https://github.com/projectious-work/processkit/issues/135)
with the `v1.0.0-alpha.5` implementation and its published release evidence.

## Summary

The corrected product boundary and trustworthy local lifecycle are
implemented. The Rust executable verifies and transactionally applies an
explicit release; Python remains the MCP runtime; release content stays
visible; and interruption recovery is exercised with real processes.

Issue #135 is complete as the v1.x implementation umbrella. Its four extracted
GA tracks are implemented in alpha.5. This closes the identified engineering
gaps without declaring the prerelease API generally available or stable.

## Coverage Matrix

| Requirement cluster | Status | Current evidence or follow-up |
| --- | --- | --- |
| Rust CLI / Python MCP / visible-file boundary | **Implemented** | Rust binary under `installer/`; Python servers ship with skills; release and architecture docs state the fixed boundary |
| `context/` dogfood vs `src/context/` payload | **Implemented** | Release-boundary checks prevent project entities from entering the staged payload |
| Deterministic plan and transactional install/update/recover/uninstall | **Implemented** | `planner.rs`, `transaction.rs`, target lock/staging/journal tests, lifecycle pilot |
| Signed release and native verification | **Implemented** | Ed25519 envelope binds archive, descriptor, provenance, and all four native installers |
| Opaque `execute --request` automation contract | **Implemented** | Versioned request/result schemas and golden fixtures |
| Rust modularization and typed failures | **Implemented** | Focused modules, stable error tests, a public library API, rustdoc, and runnable examples |
| README/help/schema consistency | **Implemented** | Shipped CLI help and release facts are generated and checked in CI |
| Four native target platforms | **Implemented** | [#165](https://github.com/projectious-work/processkit/issues/165) provides target-host builds, smoke evidence, checksums, and provenance |
| Bootstrap installer | **Implemented** | Exact-version, non-root checksum/signature verification uses the canonical fingerprint and fails closed |
| Human exact-version online resolution | **Implemented** | Exact tags resolve to immutable release assets; absent versions fail without fallback |
| Python/`uv` runtime contract | **Implemented** | Every profile uses the shipped universal, hash-locked dependency set, including offline verification |
| Native `processkit doctor` and `processkit mcp` | **Implemented** | Stable runtime, container, and deferred host-only findings include IDs, severity, and remediation |
| Extracted-release MCP acceptance | **Implemented** | Package smoke starts the staged gateway and exercises representative tools |
| Repository dogfood update/recovery acceptance | **Implemented** | The release gate combines the full-content lifecycle pilot with a deterministic real-process update interruption, rollback, user-data preservation, retry, and provenance verification |
| v0 migration and aibox parity | **Implemented** | Versioned ownership baselines cover mixed roots, replay is idempotent, ambiguity blocks safely, and direct/aibox state is identical |
| Harness projection ownership | **Implemented** | Codex and Claude adapters preserve unrelated keys and have lifecycle tests |
| Stable/prerelease documentation story | **Implemented** | Docs separate v0 stable and v1 preview and generate release facts, CLI help, and public Rust API guidance |

## What Users Can Rely On

- exact local and immutable published release inputs;
- checksum and Ed25519 verification;
- a non-mutating deterministic plan;
- transactional install and update with persisted ownership;
- recovery after interrupted installer transactions;
- conservative uninstall that preserves changed or user-owned files;
- installed-provenance verification;
- Codex and Claude managed-key projections;
- Python MCP operation from the extracted package;
- versioned machine request/result envelopes for integrators;
- mixed-root v0 migration with replay-safe evidence; and
- reproducible, hash-locked Python runtime dependencies.

## What Users Must Not Assume

- native semantic corpus migration, `package`, or `harness` commands;
- removal of Python or `uv` as runtime dependencies;
- in-place mutation of an existing v0 source tree; or
- GA stability of alpha contracts.

## Completed GA Follow-ups

1. [#165: trusted four-platform release distribution](https://github.com/projectious-work/processkit/issues/165)
2. [#167: v0 mixed-root baselines and CLI/aibox parity](https://github.com/projectious-work/processkit/issues/167)
3. [#168: generated CLI, release, and Rust API documentation](https://github.com/projectious-work/processkit/issues/168)
4. [#170: runtime dependency locking and host-health coverage](https://github.com/projectious-work/processkit/issues/170)

Alpha.5 completes the trustworthy native lifecycle around visible content and
the Python MCP runtime. Further work can build on that boundary without
changing the fixed Rust/Python product split.
