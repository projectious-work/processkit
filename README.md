<div align="center">

<img src="docs-site/static/logo/processkit-light.svg" alt="processkit" width="96" height="96">

# processkit

**A provider-neutral process and project-memory layer for agentic software projects.**

[![Status: alpha project](https://img.shields.io/badge/status-alpha%20project-1d3352)](MAINTENANCE.md)
[![License: MIT](https://img.shields.io/badge/license-MIT-1d3352)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-projectious--work.github.io-1d3352)](https://projectious-work.github.io/processkit/)

</div>

---

> [!NOTE]
> **Maturity:** alpha project — active development.
>
> The maintained v0.x line is the supported/default release. The independent
> v1.x line supports end-to-end local installation and validated MCP workflows
> as an exact-pin preview, but contracts may change between prereleases.
> Linux ARM64 GNU is the only native v1 target currently published. See
> [MAINTENANCE.md](MAINTENANCE.md) and [SECURITY.md](SECURITY.md).
>
> The released line is `v0.x`. Documentation for the two lines is published
> separately: the [v0.x docs](https://projectious-work.github.io/processkit/)
> are the default, and the
> [v1.x preview](https://projectious-work.github.io/processkit/v1.x/) tracks
> this branch.
>
> The current v1 release is `v1.0.0-alpha.5`. Its published native executable
> supports Linux ARM64 GNU only.

---

## What this is

AI coding agents are good at writing code and bad at remembering why. Ask one to
resume work after a context reset and it re-derives decisions that were already
made, re-opens questions that were already settled, and writes its findings into
whatever scratch file it invented that session.

processkit gives coding agents a shared, versioned project state they can read
and change through validated tools. Work, decisions, migrations, and audit
events remain explicit instead of disappearing into prompts, scratch files,
or provider-specific conventions.

## What this is not

- Not a harness, and not a replacement for one. processkit gives any harness the
  same process surface; it does not run models or manage conversations.
- Not stable yet. Pre-1.0 means contracts can change between prereleases.
- Not a dependency on aibox. aibox can install and wire processkit for you, but
  processkit is the standalone source of the schemas, skills, packages, and MCP
  runtime.

## See the process, not just the prompt

A minimal processkit workflow creates a typed WorkItem, moves it through a
validated state transition, and reads back the resulting state and event:

```text
create_workitem(
  title="Add release verification",
  type="story",
  priority="high"
)
transition_workitem(id="<returned-id>", to_state="in-progress")
get_workitem(id="<returned-id>")
events_for_subject(subject="<returned-id>")
```

These are MCP tool calls, so the same workflow is available to any configured
MCP client. Invalid transitions are rejected before the entity changes, while
successful transitions write both the new state and an auditable LogEntry.
The extracted-package smoke test executes this workflow in a disposable
project and verifies the resulting entities and events:
[`scripts/smoke-test-package.py`](scripts/smoke-test-package.py).

## Capability status

| Surface | Implemented now | Compatibility | Planned or stabilizing |
| --- | --- | --- | --- |
| MCP runtime | Native preparation/verification/supervision, one-process gateway, and per-skill servers | Aggregate server retained for older integrations | Additional harness-specific transport validation |
| Project memory | Validated entities, state transitions, indexing, events, migrations | Explicit v0-to-v1 compatibility manifests | Further v1 vocabulary stabilization |
| Installer | Local `plan`, `install`, `update`, `verify`, read-only `doctor`, recovery, and conservative `uninstall` | Selected v0 layouts detected from explicit evidence | More platform release assets and successive prerelease upgrade coverage |
| Harness projections | Canonical MCP catalog with Codex and Claude adapters | Existing user-owned configuration is preserved or reported as a conflict | Broader first-class harness acceptance |
| Packages and profiles | Release-owned distribution manifest and managed profile | Manual archive copying remains documented for older releases | Profile contract stabilization before v1 GA |

For the complete requirement review, see the
[issue #135 implementation status][issue-135-status].

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

## Standalone installation

The v1 prerelease includes a local standalone installer. Download and extract
the release archive, download its matching installer asset, and verify the
published checksums and trust material. The current alpha requires the
extracted release directory through `--distribution`:

```sh
processkit plan \
  --root . \
  --distribution /path/to/processkit-v1.0.0-alpha.5 \
  --profile managed \
  --harness codex
processkit install \
  --root . \
  --distribution /path/to/processkit-v1.0.0-alpha.5 \
  --profile managed \
  --harness codex \
  --yes
processkit verify --root .
```

Updates are three-way reconciled against target-side provenance; user changes
are preserved or surfaced as conflicts. Uninstall removes only unchanged paths
whose ownership processkit can prove. See the
[installer contract](docs-site/content/en/docs/installer/contract.md),
[local release and verification workflow](docs-site/content/en/docs/installer/local-release.md),
and [threat model](docs-site/content/en/docs/installer/threat-model.md).

For exact downloads, signature verification, local CLI installation, project
creation, MCP startup, first use, update, recovery, and uninstall, follow the
[step-by-step v1 alpha tutorial][v1-alpha-tutorial].

For releases that publish your native target, the exact-version non-root
bootstrap verifies the checksum, signed release envelope, and an independently
trusted Ed25519 key fingerprint before installing:

```sh
scripts/install-processkit.sh v1.0.0-alpha.5 \
  --key-sha256 <trusted-public-key-fingerprint>
```

`--distribution` is intentionally explicit for the alpha's offline and
machine-facing contract. A future human-facing command will resolve an exact
canonical release version, while `processkit execute --request <path>` remains
the opaque, versioned integration boundary for aibox and other automation.

## Quick Start

After installing and verifying an exact v1 distribution:

```sh
mkdir processkit-demo && cd processkit-demo
git init

processkit plan \
  --root . \
  --distribution /path/to/processkit-v1.0.0-alpha.5 \
  --profile managed \
  --harness codex \
  --format human

processkit install \
  --root . \
  --distribution /path/to/processkit-v1.0.0-alpha.5 \
  --profile managed \
  --harness codex \
  --yes

processkit verify --root .
```

Restart the selected harness, then ask it to create and read a WorkItem
through processkit. The
[v1 tutorial][v1-alpha-tutorial] covers signature verification, trust-store
creation, first MCP use, updates, recovery, and uninstall.

### Manual compatibility path

Older v0 releases do not contain the standalone installer. Their manual,
version-pinned archive path remains:

```sh
curl -L \
  https://github.com/projectious-work/processkit/releases/download/v0.27.1/processkit-v0.27.1.tar.gz \
  -o processkit-v0.27.1.tar.gz
tar -xzf processkit-v0.27.1.tar.gz

cp -a processkit-v0.27.1/context ./context
cp -a processkit-v0.27.1/.processkit ./.processkit
cp processkit-v0.27.1/AGENTS.md ./AGENTS.md
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
processkit mcp serve --root . \
  --transport streamable-http \
  --host 127.0.0.1 \
  --port 8000 \
  --path /mcp
```

Harnesses that only support stdio can connect to that daemon through the
included proxy:

```sh
processkit mcp proxy --root . --url http://127.0.0.1:8000/mcp
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
version = "v0.27.1"

[context]
packages = ["managed"]
```

That integration is convenient, but not required. processkit remains the
standalone source of the schemas, skills, packages, and MCP runtime.

## Documentation

Full documentation lives at
**[projectious-work.github.io/processkit](https://projectious-work.github.io/processkit/)**
— the v0.x line at the root, this v1.0 preview line under
[`/v1.x/`](https://projectious-work.github.io/processkit/v1.x/).

| Section | Contents |
|---------|----------|
| [Getting Started](https://projectious-work.github.io/processkit/v1.x/docs/getting-started/) | Manual and managed install paths, first entity |
| [Installer](https://projectious-work.github.io/processkit/v1.x/docs/installer/) | Contract, local release, threat model, v0 compatibility |
| [Primitives](https://projectious-work.github.io/processkit/v1.x/docs/primitives/) | The entity model, formats, state machines, relationships |
| [Skills](https://projectious-work.github.io/processkit/v1.x/docs/skills/) | Skill package format, hierarchy, and the full catalog |
| [Packages](https://projectious-work.github.io/processkit/v1.x/docs/packages/) | The five tiers, from minimal bootstrap to managed workspace |
| [MCP Servers](https://projectious-work.github.io/processkit/v1.x/docs/mcp-servers/) | Gateway, daemon, stdio-proxy, aggregate, per-skill layouts |
| [Reference](https://projectious-work.github.io/processkit/v1.x/docs/reference/) | apiVersion policy, ID formats, migration, privacy, v2 contracts |
| [Development](https://projectious-work.github.io/processkit/v1.x/docs/development/) | The v0 prototype line and the v1.0 rebuild, planned in the open |

Build and preview locally with `./scripts/serve-docs-local.sh` (Hugo + Docsy,
port 1313); validate with `./scripts/check-docs-local.sh`.

- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [License](LICENSE)

## Current release facts

The repository is on the v1 prerelease line. Counts such as skill, schema, and
tool totals are generated release facts rather than maturity claims; run the
package smoke test to print the current extracted-release tool count. Exact
support and compatibility changes are recorded in the
[changelog](CHANGELOG.md) and each GitHub release.

processkit's operating-model direction and architectural boundaries are owned
by the project maintainer. AI agents assist with research, implementation,
testing, and documentation under the repository's review, decision-record,
and local release gates.

## Development

Common local checks:

```sh
scripts/check-docs-local.sh
uv run scripts/generate-v1-schemas.py --check
uv run scripts/smoke-test-servers.py
uv run scripts/smoke-test-package.py
uv run --with pytest --with jinja2 --with pyyaml --with jsonschema \
  pytest -p no:cacheprovider tests/schema_generation \
  scripts/test_processkit_diff.py
```

The smoke tests create provider-neutral temporary projects and do not install
or invoke aibox. `smoke-test-package.py` stages and extracts `src/` before
running the MCP workflow, so repository imports cannot hide missing package
content.
All validation, native artifact production, generated-document checks, and
documentation deployment run from repository scripts on maintainer-controlled
machines. This repository deliberately has no GitHub Actions workflows.

Release packaging is guarded by:

```sh
scripts/check-src-context-drift.sh --release-deliverable
scripts/test-installer-local.sh
scripts/release-local.sh vX.Y.Z <private-key.pem> <public-key.pem>
```

See [Local release operation](docs-site/content/en/docs/installer/local-release.md)
for the agent-first, human-operable signing and verification workflow.

## Contributing

Issues and pull requests are welcome. Start with
[CONTRIBUTING.md](CONTRIBUTING.md) for the branch model, the skill and
primitive checklists, and the release procedure — and note that this
repository runs its checks locally rather than in CI, so a PR should say which
ones you ran.

By participating you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).
Security issues go through [SECURITY.md](SECURITY.md), not the issue tracker.

## Maintenance and Support

- [MAINTENANCE.md](MAINTENANCE.md) defines supported lines, branch authority,
  and the evidence-bound release process.
- [SUPPORT.md](SUPPORT.md) explains what to collect before requesting help.
- [SECURITY.md](SECURITY.md) defines private vulnerability reporting and
  support boundaries.
- [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) sets community expectations.
- [CONTRIBUTING.md](CONTRIBUTING.md) covers development and pull requests.

All build, test, documentation, signing, and publication gates run locally.
Maintainers release through
`./scripts/maintain.sh release <version>`.

## License

[MIT](LICENSE). Unless a file states otherwise, the project maintainers intend
the MIT License in this repository to apply retroactively to all historical
commits, tags, and release artifacts for this repository.

Brand and design system © [projectious.work](https://github.com/projectious-work/brand).
The processkit mark is derived from that system.

[issue-135-status]: docs-site/content/en/docs/development/v1-version/issue-135-status.md
[v1-alpha-tutorial]: docs-site/content/en/docs/getting-started/v1-alpha-tutorial.md
