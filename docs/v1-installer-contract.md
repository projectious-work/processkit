# v1 installer contract

The standalone installer consumes only a release directory or verified archive
explicitly supplied by its caller. It has no built-in release URL, package
layout, MCP inventory, or harness policy.

The release-owned contract is under `.processkit/installer/`. The first
protocol version supports a deterministic, no-write plan and two closed
operations: `copy/v1` and `preserve-user/v1`. Install, update, and uninstall
will be enabled only after their atomic-apply and recovery contracts ship.

Target-local state belongs in `.processkit/state.json`; it is never copied
back into a release payload. Harness adapters consume the canonical MCP
catalogue and own only their named managed keys.
