<div align="center">

<img src="docs-site/static/logo/processkit-light.svg" alt="processkit" width="96" height="96">

# processkit

**Provider-neutral process memory, skills, and MCP tools for agentic software projects.**

[![Lifecycle: stable](https://img.shields.io/badge/lifecycle-stable-1d3352)](SECURITY.md)
[![Status: pre-1.0](https://img.shields.io/badge/status-pre--1.0-E05232)](https://github.com/projectious-work/processkit/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-1d3352)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-projectious--work.github.io-1d3352)](https://projectious-work.github.io/processkit/)

</div>

---

> [!NOTE]
> **This is the released `v0.x` line** — the version that ships in release
> tarballs and is dogfooded in this repository. Maintained by projectious-work
> for teams building provider-neutral agent workflows; support and security
> reports go through [SECURITY.md](SECURITY.md).
>
> processkit is pre-1.0: breaking changes can still land in minor releases, and
> the release notes call them out explicitly. The v1.0 rebuild is developed on
> `v1.x-dev` and documented separately in the
> [v1.x preview](https://projectious-work.github.io/processkit/v1.x/).

---

## What this is

AI coding agents are good at writing code and bad at remembering why. Ask one to
resume work after a context reset and it re-derives decisions that were already
made, re-opens questions that were already settled, and writes its findings into
whatever scratch file it invented that session.

processkit gives AI coding agents a structured project context they read and
write through validated tools instead of ad hoc Markdown, untracked scratch
files, or provider-specific conventions. It ships as a versioned content and
runtime layer usable directly with MCP-capable harnesses, installed manually
into an existing repository, or wired by an external environment manager.

## What this is not

- Not a harness, and not a replacement for one. processkit gives any harness the
  same process surface; it does not run models or manage conversations.
- Not stable in the semver sense yet. Pre-1.0 means minor releases can break
  you — read the changelog before upgrading.
- Not a dependency on aibox. aibox can install and wire processkit for you, but
  processkit is the standalone source of the schemas, skills, packages, and MCP
  runtime.

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
  https://github.com/projectious-work/processkit/releases/download/v0.28.4/processkit-v0.28.4.tar.gz \
  -o processkit-v0.28.4.tar.gz
tar -xzf processkit-v0.28.4.tar.gz

cp -a processkit-v0.28.4/context ./context
cp -a processkit-v0.28.4/.processkit ./.processkit
cp processkit-v0.28.4/AGENTS.md ./AGENTS.md
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
version = "v0.28.4"

[context]
packages = ["managed"]
```

That integration is convenient, but not required. processkit remains the
standalone source of the schemas, skills, packages, and MCP runtime.

## Documentation

Full documentation lives at
**[projectious-work.github.io/processkit](https://projectious-work.github.io/processkit/)**
— this released v0.x line at the root, the v1.0 preview under
[`/v1.x/`](https://projectious-work.github.io/processkit/v1.x/).

| Section | Contents |
|---------|----------|
| [Getting Started](https://projectious-work.github.io/processkit/docs/getting-started/) | Manual and managed install paths, first entity |
| [Primitives](https://projectious-work.github.io/processkit/docs/primitives/) | The entity model, formats, state machines, relationships |
| [Skills](https://projectious-work.github.io/processkit/docs/skills/) | Skill package format, hierarchy, and the full catalog |
| [Packages](https://projectious-work.github.io/processkit/docs/packages/) | The five tiers, from minimal bootstrap to managed workspace |
| [MCP Servers](https://projectious-work.github.io/processkit/docs/mcp-servers/) | Gateway, daemon, stdio-proxy, aggregate, per-skill layouts |
| [Reference](https://projectious-work.github.io/processkit/docs/reference/) | apiVersion policy, ID formats, migration, privacy, v2 contracts |
| [Development](https://projectious-work.github.io/processkit/docs/development/) | Planning documents for the v1.0 rebuild |

Preview locally with `./scripts/serve-docs-local.sh` (Hugo + Docsy, port 1315);
validate with `./scripts/check-docs-local.sh`.

- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [License](LICENSE)

## Contributing

Issues and pull requests are welcome. Start with
[CONTRIBUTING.md](CONTRIBUTING.md) for the branch model, the skill and
primitive checklists, and the release procedure — and note that this
repository runs its checks locally rather than in CI, so a PR should say which
ones you ran.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
Security issues go through [SECURITY.md](SECURITY.md), not the issue tracker.

## License

[MIT](LICENSE). Unless a file states otherwise, the project maintainers intend
the MIT License in this repository to apply retroactively to all historical
commits, tags, and release artifacts for this repository.

Brand and design system © [projectious.work](https://github.com/projectious-work/brand).
The processkit mark is derived from that system.

## Status

processkit is currently pre-1.0. Breaking changes can still land in
minor releases, and release notes call them out explicitly.

`v0.28.4` is the current patch release. It keeps the v2 deliverable
boundary and closes derived-project doctor remediation and policy
false-positive gaps.

## Development

Common local checks:

```sh
./scripts/check-docs-local.sh
uv run scripts/smoke-test-servers.py
```

The repository does not use GitHub Actions; maintainers run and report these
checks locally before merging or releasing.

Documentation publishing is also manual:

```sh
scripts/publish-docs-gh-pages.sh
```

Release packaging is guarded by:

```sh
scripts/check-src-context-drift.sh --release-deliverable
scripts/build-release-tarball.sh vX.Y.Z
```
