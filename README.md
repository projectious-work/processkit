# processkit

Provider-neutral process primitives, skills, and MCP servers for
AI-assisted work environments.

processkit is the content layer for
[aibox](https://github.com/projectious-work/aibox): a versioned library
of process primitives, domain skills, and MCP servers that helps agents
work with project memory through validated tools instead of ad hoc file
edits.

## What It Ships

- **Process primitives** for durable project memory, including
  WorkItems, Decisions, Artifacts, Notes, Logs, Migrations, Actors,
  Roles, Bindings, Scopes, Gates, Discussions, and related schemas.
- **Domain skills** for engineering, product, data, design, documents,
  devops, and processkit operations.
- **MCP servers** that validate entity writes, enforce state machines,
  maintain indexes, and expose processkit tools to agent harnesses.
- **A provider-neutral gateway** that can expose processkit through a
  single MCP entry point instead of many per-skill server processes.

## How It Fits With aibox

processkit owns the process semantics and shipped content. aibox owns
installation, devcontainer wiring, harness configuration, and lifecycle
management.

Projects usually consume processkit through `aibox.toml`:

```toml
[processkit]
source = "https://github.com/projectious-work/processkit.git"
version = "v0.25.0"

[context]
packages = ["managed"]
```

aibox then installs the selected package into the project `context/`
tree, merges MCP configuration for the chosen harness, and records the
resolved source in `aibox.lock`.

## MCP Entry Points

processkit supports both granular and one-process MCP layouts:

- Per-skill MCP servers for fine-grained compatibility.
- `aggregate-mcp` as the legacy one-process compatibility bridge.
- `processkit-gateway` as the current provider-neutral gateway, with
  direct stdio, streamable HTTP daemon, stdio proxy, and lazy catalog
  modes.

The gateway is not tied to Claude, Codex, OpenCode, Hermes, Aider, or
any other harness. Harness-specific behavior belongs in thin installer
and configuration adapters.

## Current Status

The current release line is pre-1.0. Breaking changes may still land in
minor releases, and release notes call those out explicitly.

`v0.25.0` is a breaking pre-1.0 release focused on the v2 deliverable
boundary, demotion of legacy first-class primitives from shipped
`src/context/`, and the new `processkit-gateway` MCP surface.

## Documentation

- [Documentation site](https://projectious-work.github.io/processkit/)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [License](LICENSE)

## Development

Common local checks:

```sh
npm --prefix docs-site run build
uv run scripts/smoke-test-servers.py
```

Release packaging is guarded by:

```sh
scripts/check-src-context-drift.sh --release-deliverable
scripts/build-release-tarball.sh vX.Y.Z
```
