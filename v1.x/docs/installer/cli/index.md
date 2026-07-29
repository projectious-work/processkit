# CLI and automation interfaces

> Human lifecycle commands and the stable automation protocol.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

processkit has two deliberately separate command interfaces. Human lifecycle
commands optimize for reviewable output and safe project operation. The
machine interface uses a versioned JSON request and result contract for aibox
and other automation.

> **Release and development status:** `v1.0.0-alpha.4` supports the local
> lifecycle commands below except `doctor` and `mcp`. The `v1.x-dev` line adds
> read-only native diagnosis and MCP supervision for the next prerelease.
> Commands in “Target human lifecycle” remain planned unless listed as current.

## Current v1 alpha commands

The current prerelease supports:

```text
processkit plan
processkit install
processkit update
processkit verify
processkit verify-release
processkit doctor
processkit mcp verify
processkit mcp serve --transport stdio
processkit mcp proxy --url http://127.0.0.1:8000/mcp
processkit inspect-compatibility
processkit recover
processkit uninstall
processkit execute --request request.json
```

`plan`, `install`, `update`, and compatibility inspection currently require an
explicit local release directory through `--distribution`. Mutating commands
also require `--yes`. This makes the alpha suitable for offline use and for
callers that already acquire and verify an exact release.

For example:

```sh
processkit plan \
  --root . \
  --distribution /path/to/processkit-v1.0.0-alpha.4 \
  --profile managed \
  --harness codex
```

## Target human lifecycle

The human-facing CLI will grow into these lifecycle groups without changing
the Python implementation of the MCP servers:

```text
processkit init
processkit plan
processkit install
processkit update
processkit verify
processkit inspect
processkit migrate
processkit recover
processkit uninstall
processkit package
processkit harness
processkit mcp
```

Human commands will eventually resolve an exact canonical version and verify
its signed release metadata before planning. `--distribution` will remain the
explicit offline and development override. Moving branches and unverified
`latest` URLs are not release identities.

The Rust `mcp` command will diagnose and supervise the installed Python
gateway. It will not become a second MCP implementation. Direct
`uv run .../server.py` configurations remain supported.

## Stable machine interface

Automation uses:

```sh
processkit execute --request request.json
```

The request and result use the versioned installer schema. The request names
the target root, operation, release input, profiles, harnesses, and mutation
acknowledgement. The command emits one result envelope. Callers must use its
status and the process exit code rather than parse human output.

The `execute` protocol remains the opaque aibox integration boundary. New
human commands may compile their intent into the same internal operations,
but they must not silently change the versioned machine contract.

See the [installer contract](../contract/) for transaction, ownership, and
recovery guarantees and [aibox integration](../aibox-integration/) for the
consumer protocol.
