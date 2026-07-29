# Python MCP runtime contract

> Supported Python, uv, dependency, cache, and transport behavior.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

Python is an intentional processkit runtime dependency. It implements the MCP
servers; it is not required by the Model Context Protocol itself. The native
Rust CLI owns installation and lifecycle safety. Native diagnostics and
optional process supervision are planned and will not reimplement MCP
behavior.

## Current alpha requirements

- Python 3.10 or newer must be discoverable by `uv`.
- `uv` must support PEP 723 script metadata.
- The installed gateway script and processkit shared Python library must be
  readable from the selected project root.
- The first dependency resolution may require network access.
- Direct `uv run` startup remains a supported compatibility and development
  interface.

Every shipped MCP entry point declares its Python constraint and dependencies
in a PEP 723 block. The gateway currently declares:

```toml
requires-python = ">=3.10"
dependencies = [
  "mcp[cli]>=1.0,<2.0",
  "pyyaml>=6.0",
  "jsonschema>=4.0",
  "jinja2>=3.1",
  "httpx>=0.27",
  "sqlite-vec>=0.1.0",
]
```

The release manifest records a digest of every server dependency header.
Changing a header requires regenerating that manifest and restarting the
server.

The release also ships
`.processkit/installer/runtime/python-uv.json`. This deterministic policy is
generated exclusively from the MCP servers under the release's
`src/context/` producer tree. It records each server header, its dependency
profile, and an aggregate digest. Installed projects receive it as
`.processkit/runtime/python-uv.json`.

The policy is declarative evidence, not a dependency lock. It deliberately
does not claim resolved package versions or cold offline readiness.

## Dependency and cache behavior

`uv` resolves PEP 723 dependencies and stores downloaded artifacts and
environments in its user cache. Operators may select a separate cache through
`UV_CACHE_DIR`. The cache must remain outside processkit's managed project
content; normal MCP startup must not modify `context/`, `src/context/`, or
tracked configuration.

The current alpha uses compatible lower bounds rather than a fully locked
runtime set. Consequently, a cold offline installation is not yet a supported
guarantee. An offline run requires a cache prepared for the same platform,
Python version, and dependency set. A later lifecycle command will make that
preparation explicit and verify it before declaring a project offline-ready.

## Startup and transport

Direct gateway startup is:

```sh
uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  serve --transport stdio
```

The gateway also supports streamable HTTP on loopback and a stdio proxy. A
non-loopback HTTP listener requires an explicit deployment security layer;
processkit does not expose it remotely by default.

The `v1.x-dev` line implements the first read-only native diagnostic:

```sh
processkit doctor --root . --json
processkit doctor --root . --category drift
```

It validates the project root and doctor script, probes `uv`, launches the
authoritative Python doctor without a shell, and wraps its structured result
in `processkit.projectious.work/runtime/v1alpha1`. It intentionally exposes no
fix flags.

The remaining target Rust interface is:

```text
processkit mcp verify
processkit mcp serve --transport stdio
processkit mcp serve --transport streamable-http
processkit mcp proxy --url http://127.0.0.1:8000/mcp
```

The `processkit mcp` commands are not part of the current alpha binary. When
implemented,
they will construct a direct `uv` argument vector without shell
interpretation, scope the child to the selected project, preserve exit and
signal behavior, and redact secrets from diagnostics.

## Diagnostic contract

The native doctor currently preserves Python doctor findings and reports
runtime launch failures without exposing fix behavior. Future static checks
will add stable codes and actionable remediation for:

- missing or unsupported Python;
- missing or incompatible `uv`;
- unreadable gateway or shared-library paths;
- invalid PEP 723 metadata;
- unavailable or unwritable runtime cache;
- dependency preparation failure;
- gateway initialization or startup timeout;
- invalid harness projection;
- optional semantic-index degradation.

Missing optional `sqlite-vec` acceleration must not be confused with failure
of the canonical file-backed entity operations. Diagnostic output must never
include environment secrets, provider credentials, private signing material,
or private TeamMember memory.
