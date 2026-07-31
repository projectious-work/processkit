# Issue #135 Implementation Review

> Final requirement review of the Rust CLI and Python MCP product briefing against the v1.x development line.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

This final review compares
[GitHub issue #135](https://github.com/projectious-work/processkit/issues/135)
with the current `v1.x-dev` implementation. It distinguishes implemented alpha
scope from the work still required before a generally available release.

## Summary

The corrected product boundary and trustworthy local lifecycle are
implemented. The Rust executable verifies and transactionally applies an
explicit release; Python remains the MCP runtime; release content stays
visible; and interruption recovery is exercised with real processes.

Issue #135 is therefore complete as the v1.x implementation umbrella and has
been closed after final review. Four remaining GA tracks have been extracted
into focused follow-up issues. Closing the umbrella does **not** declare the
alpha GA-ready or claim that those follow-ups are complete.

## Coverage Matrix

| Requirement cluster | Status | Current evidence or follow-up |
| --- | --- | --- |
| Rust CLI / Python MCP / visible-file boundary | **Implemented** | Rust binary under `installer/`; Python servers ship with skills; release and architecture docs state the fixed boundary |
| `context/` dogfood vs `src/context/` payload | **Implemented** | Release-boundary checks prevent project entities from entering the staged payload |
| Deterministic plan and transactional install/update/recover/uninstall | **Implemented** | `planner.rs`, `transaction.rs`, target lock/staging/journal tests, lifecycle pilot |
| Signed release and native verification | **Implemented** | Ed25519 envelope binds archive, descriptor, provenance, and ARM64 installer |
| Opaque `execute --request` automation contract | **Implemented** | Versioned request/result schemas and golden fixtures |
| Rust modularization and typed failures | **Partial** | Logic moved from the former monolith into focused modules with stable error tests; a separate public library crate and full API docs remain |
| README/help/schema consistency | **Mostly implemented** | Current local-distribution requirements agree; generated help snapshot/release facts automation remains |
| Four native target platforms | **Follow-up** | The release workflow binds a collected four-target matrix; native production and smoke testing remain in [#165](https://github.com/projectious-work/processkit/issues/165) |
| Bootstrap installer | **Partial** | Exact-version, non-root, checksum/signature/fingerprint verification exists; canonical key distribution and immutable online resolution remain in [#165](https://github.com/projectious-work/processkit/issues/165) |
| Human exact-version online resolution | **Follow-up** | Human lifecycle commands still require `--distribution`; exact immutable resolution is tracked in [#165](https://github.com/projectious-work/processkit/issues/165) |
| Python/`uv` runtime contract | **Mostly implemented** | Runtime policy, native diagnosis, dependency-profile preparation, and offline-readiness verification exist; reproducible runtime resolution remains in [#170](https://github.com/projectious-work/processkit/issues/170) |
| Native `processkit doctor` and `processkit mcp` | **Mostly implemented** | Typed read-only doctor plus native MCP verify/serve/proxy supervision exist; broader host-signal acceptance remains in [#170](https://github.com/projectious-work/processkit/issues/170) |
| Extracted-release MCP acceptance | **Implemented** | Package smoke starts the staged gateway and exercises representative tools |
| Repository dogfood update/recovery acceptance | **Implemented** | The release gate combines the full-content lifecycle pilot with a deterministic real-process update interruption, rollback, user-data preservation, retry, and provenance verification |
| v0 migration and aibox parity | **Partial** | Exact fixtures exercise guarded transition, byte-preserving transactional corpus application, persisted loss/provenance evidence, and interruption recovery; mixed-root ownership baselines and aibox parity remain in [#167](https://github.com/projectious-work/processkit/issues/167) |
| Harness projection ownership | **Implemented** | Codex and Claude adapters preserve unrelated keys and have lifecycle tests |
| Stable/prerelease documentation story | **Partial** | Docs separate v0 stable and v1 preview; generated facts/help and public Rust API docs remain in [#168](https://github.com/projectious-work/processkit/issues/168) |

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

## Extracted GA Follow-ups

1. [#165: trusted four-platform release distribution](https://github.com/projectious-work/processkit/issues/165)
2. [#167: v0 mixed-root baselines and CLI/aibox parity](https://github.com/projectious-work/processkit/issues/167)
3. [#168: generated CLI, release, and Rust API documentation](https://github.com/projectious-work/processkit/issues/168)
4. [#170: runtime dependency locking and host-health coverage](https://github.com/projectious-work/processkit/issues/170)

The guiding constraint remains: finish the trustworthy native lifecycle around
visible content and the Python MCP runtime before expanding conceptual breadth.
