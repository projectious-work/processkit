# Installer Contract

> Trust, ownership, transaction, and automation guarantees for the v1 lifecycle CLI.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

> **Alpha.4 status:** Implemented for explicit local distributions and signed
> local releases. Canonical online release acquisition is not implemented.

The standalone installer consumes only a release directory or verified archive
explicitly supplied by its caller. It has no built-in release URL, package
layout, MCP inventory, or harness policy.

The release-owned contract is under `.processkit/installer/`. Protocol
`processkit.projectious.work/installer/v1alpha1` supports deterministic
planning plus transactional install, update, uninstall, and recovery.
`copy/v1` and `preserve-user/v1` are the closed payload operations.

Consumers invoke the opaque request/result boundary:

```sh
processkit execute --request installer-request.json
```

The request selects an operation, arbitrary target root, release directory,
profiles, harness intent, and explicit mutation acknowledgement. The command
prints exactly one JSON result. A non-zero exit and `status: invalid` indicate
an unsuccessful request.

Target-local state belongs in `.processkit/state.json`; it is never copied
back into a release payload. Every mutation uses a target-local lock, staging
tree, backups, and persisted action journal. After interruption, a caller
runs a `recover` request; recovery either rolls back the old state or
finalizes the new state and refuses ambiguous evidence.

Harness adapters consume the canonical MCP catalogue and own only their named
managed keys. Existing unrelated JSON keys survive install and uninstall.

Release creation and verification are local operations. Repository scripts
run the authoritative tests, build the archive, sign a release envelope with a
locally held Ed25519 key, and verify it against a local trust-store document.
The Rust executable verifies the exact signed envelope bytes and archive
digest natively. Updates reject downgrades and same-version equivocation.
No hosted CI or publication service is part of the contract.

The authoritative local gate is:

```sh
scripts/test-installer-local.sh
```

It includes Rust formatting, Clippy, unit/integration tests, signature and
tamper tests, an arbitrary-directory lifecycle pilot, contract validation,
package smoke testing, and the derived-project health check.

The implementation is split across focused release, request, planning,
transaction, state, compatibility, output, and typed-error modules. A
separate reusable Rust library crate and fully documented public API remain
future refactoring work.
