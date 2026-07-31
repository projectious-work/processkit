# Python MCP runtime contract

> Supported Python, uv, dependency, cache, and transport behavior.

---

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

Python is an intentional processkit runtime dependency. It implements the MCP
servers; it is not required by the Model Context Protocol itself. The native
Rust CLI owns installation and lifecycle safety. Native diagnostics and
process supervision wrap that Python implementation; they do not reimplement
MCP behavior.

## Current alpha requirements

- Python 3.10 or newer must be discoverable by `uv`.
- `uv` must support PEP 723 script metadata.
- The installed gateway script and processkit shared Python library must be
  readable from the selected project root.
- The first preparation may require network access to populate the `uv` cache.
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

The release also installs a universal, hash-checked requirements lock at
`.processkit/runtime/python-requirements.lock`. The policy binds its SHA-256.
Runtime preparation refuses a missing, symlinked, unhashed, or digest-mismatched
lock and passes the lock directly to `uv`.

## Dependency and cache behavior

`uv` resolves PEP 723 dependencies and stores downloaded artifacts and
environments in its user cache. Operators may select a separate cache through
`UV_CACHE_DIR`. The cache must remain outside processkit's managed project
content; normal MCP startup must not modify `context/`, `src/context/`, or
tracked configuration.

Resolved runtime versions and distributions are locked with hashes. A cold
offline installation still requires a prepared cache because wheels are not
embedded in the release. Prepare the locked runtime into the selected cache:

```sh
processkit mcp prepare --root .
processkit mcp prepare --root . --cache-dir /absolute/cache/path
```

Then prove that the same policy is usable without network resolution:

```sh
processkit mcp prepare --root . --offline
processkit mcp prepare --root . \
  --cache-dir /absolute/cache/path \
  --offline \
  --json
```

Offline verification fails if the cache directory is absent, symlinked, or
cannot satisfy any dependency profile. Preparation validates the installed
policy identity, aggregate digest, profile digests, representative server
paths, dependency strings, and Python constraints before invoking `uv`
without a shell.

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

The `v1.x-dev` line also implements the native supervision interface:

```text
processkit mcp verify
processkit mcp prepare
processkit mcp prepare --offline
processkit mcp serve --transport stdio
processkit mcp serve --transport streamable-http
processkit mcp proxy --url http://127.0.0.1:8000/mcp
```

These commands validate a regular, non-symlink gateway path and launch `uv`
with a direct argument vector, without shell interpretation. The child is
scoped to the canonical project root and its exit status is preserved.
Streamable HTTP and proxy URLs are restricted to explicit loopback hosts;
remote exposure remains an operator-owned deployment concern.

## Diagnostic contract

The native doctor preserves Python findings, reports whether it is running on
a local host or in a container, and lists deferred host-only checks with stable
IDs, severity, and remediation. The host-only IDs are
`host.docker-engine`, `host.filesystem-permissions`, and
`host.network-release-access`.

Runtime failures cover:

- missing or unsupported Python;
- missing or incompatible `uv`;
- unreadable gateway or shared-library paths;
- invalid PEP 723 metadata;
- unavailable, unsafe, or incomplete runtime cache;
- gateway initialization or startup timeout;
- invalid harness projection;
- optional semantic-index degradation.

Missing optional `sqlite-vec` acceleration must not be confused with failure
of the canonical file-backed entity operations. Diagnostic output must never
include environment secrets, provider credentials, private signing material,
or private TeamMember memory.
