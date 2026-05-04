# processkit

**Provider-neutral process memory, skills, and MCP tools for agentic
software projects.**

processkit gives AI coding agents a structured project context they can
read and write through validated tools instead of ad hoc Markdown,
untracked scratch files, or provider-specific conventions.

It ships as a versioned content and runtime layer that can be used
directly with MCP-capable harnesses, installed manually into an existing
repository, or wired by an external environment manager.

## Highlights

- **140 skills** for software delivery, product work, research,
  documentation, data, design, devops, and processkit operations.
- **25 MCP server entry points** for validated reads, writes, discovery,
  routing, release checks, and gateway access.
- **16 project-memory schemas** covering WorkItems, Decisions,
  Artifacts, Notes, Logs, Migrations, Actors, Roles, Bindings, Scopes,
  Gates, Discussions, and related primitives.
- **5 package tiers** so projects can choose a small bootstrap context
  or a fuller managed workspace.
- **One-process MCP gateway** for low-memory environments, plus
  per-skill MCP servers for granular compatibility.
- **Provider-neutral by design**: Claude, Codex, OpenCode, Hermes, Aider,
  and other harnesses are integration targets, not dependencies.

## Why processkit?

Most agent setups start with prompts and loose files. That works until a
project needs durable decisions, repeatable migrations, stable handovers,
auditable release checks, or multiple agents working from the same
context.

processkit provides the missing process layer:

- Schemas define the shape of project memory.
- Skills describe repeatable workflows.
- MCP tools enforce validation and state transitions.
- Indexes make the context searchable without raw filesystem scraping.
- Release packaging keeps the shipped `src/context/` deliverable
  separate from this repository's local dogfooding `context/`.

The goal is not to replace your harness. The goal is to give any harness
the same reliable process surface.

## What Ships

| Area | Includes |
| --- | --- |
| Process primitives | WorkItems, DecisionRecords, Artifacts, Notes, Logs, Migrations, Actors, Roles, Bindings, Scopes, Gates, Discussions |
| Skills | Engineering, product, research, design, data, documents, devops, release, team, and processkit workflows |
| MCP runtime | Per-skill servers, legacy aggregate MCP, and the current `processkit-gateway` |
| Packaging | Minimal, managed, product, research, and software context packages |
| Docs and checks | Documentation source, smoke tests, release audit helpers, drift checks, and tarball packaging scripts |

## Manual Use

Download a release tarball and copy the shipped context into your
project:

```sh
curl -L \
  https://github.com/projectious-work/processkit/releases/download/v0.25.5/processkit-v0.25.5.tar.gz \
  -o processkit-v0.25.5.tar.gz
tar -xzf processkit-v0.25.5.tar.gz

cp -a processkit-v0.25.5/context ./context
cp -a processkit-v0.25.5/.processkit ./.processkit
cp processkit-v0.25.5/AGENTS.md ./AGENTS.md
```

Then point your harness at the gateway MCP server. For stdio-based MCP:

```json
{
  "mcpServers": {
    "processkit-gateway": {
      "command": "uv",
      "args": [
        "run",
        "context/skills/processkit/processkit-gateway/mcp/server.py",
        "serve",
        "--transport",
        "stdio"
      ]
    }
  }
}
```

For a long-running local daemon:

```sh
uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  serve --transport streamable-http --host 127.0.0.1 --port 8000 --path /mcp
```

Harnesses that only support stdio can connect to that daemon through the
included proxy:

```sh
uv run context/skills/processkit/processkit-gateway/mcp/server.py \
  stdio-proxy --url http://127.0.0.1:8000/mcp
```

You can also run individual MCP servers when you want a smaller,
explicit tool surface:

```sh
uv run context/skills/processkit/workitem-management/mcp/server.py
uv run context/skills/processkit/decision-record/mcp/server.py
uv run context/skills/processkit/index-management/mcp/server.py
```

## MCP Layouts

processkit supports three MCP layouts:

- **Gateway**: the preferred provider-neutral entry point. It exposes
  processkit tools through stdio or streamable HTTP and can reduce idle
  memory by replacing many Python server processes with one runtime.
- **Per-skill servers**: one MCP server per capability area. This is
  useful for harnesses with strict allowlists or incremental adoption.
- **Aggregate MCP**: the legacy compatibility bridge retained for older
  integrations.

The gateway does not call model-provider APIs, store provider-specific
state, or know model names. Harness-specific concerns stay outside
processkit in thin config adapters.

## Optional aibox Integration

[aibox](https://github.com/projectious-work/aibox) can install and wire
processkit automatically for devcontainers:

```toml
[processkit]
source = "https://github.com/projectious-work/processkit.git"
version = "v0.25.5"

[context]
packages = ["managed"]
```

That integration is convenient, but not required. processkit remains the
standalone source of the schemas, skills, packages, and MCP runtime.

## Documentation

- [Documentation](https://projectious-work.github.io/processkit/docs/)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [License](LICENSE)

## Status

processkit is currently pre-1.0. Breaking changes can still land in
minor releases, and release notes call them out explicitly.

`v0.25.5` is the current patch release. It keeps the v0.25.0 gateway
and v2 deliverable boundary, adds active interlocutor runtime mismatch
reporting, and keeps role/team model routing portable across harnesses.

## Development

Common local checks:

```sh
npm --prefix docs-site run build
uv run scripts/smoke-test-servers.py
```

Release docs publishing is manual:

```sh
scripts/publish-docs-gh-pages.sh vX.Y.Z
```

Release packaging is guarded by:

```sh
scripts/check-src-context-drift.sh --release-deliverable
scripts/build-release-tarball.sh vX.Y.Z
```
