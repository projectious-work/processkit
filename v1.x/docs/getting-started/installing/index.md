# Installing

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

## v1 alpha

`v1.0.0-alpha.4` is installed with the native Rust lifecycle CLI from an
explicitly downloaded, signed release. The alpha does not yet have an online
version resolver or one-command bootstrap installer.

Use the complete
[v1 alpha installation and first-project tutorial](./v1-alpha-tutorial/).
It verifies the signed envelope, checks both artifact digests, previews the
plan, installs a selected profile, verifies managed state, and connects the
Python MCP gateway.

The current command shape is:

```sh
processkit plan \
  --root /path/to/project \
  --distribution /path/to/processkit-v1.0.0-alpha.4 \
  --profile managed \
  --harness codex

processkit install \
  --root /path/to/project \
  --distribution /path/to/processkit-v1.0.0-alpha.4 \
  --profile managed \
  --harness codex \
  --yes
```

Do not copy the v1 payload by hand. The CLI supplies transaction, ownership,
recovery, and conservative uninstall evidence that manual copying cannot.

## Stable v0 and managed aibox projects

Existing v0 projects remain supported and should stay pinned to their current
stable version until the v1 migration path is complete. aibox remains an
optional downstream installer and integrator; it is not required to build,
test, or run processkit.

See [v0 compatibility](../installer/v0-compatibility/) and
[aibox integration](../installer/aibox-integration/) before changing an
existing project.

## After installation

Python and `uv` remain runtime prerequisites for MCP:

```sh
uv run \
  context/skills/processkit/processkit-gateway/mcp/server.py \
  serve --transport stdio
```

Use MCP tools for entity writes. They validate schemas and transitions and
produce the required audit events.
