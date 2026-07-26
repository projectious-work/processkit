# processkit

**A provider-neutral process and project-memory layer for agentic software
projects.**

processkit gives coding agents a shared, versioned project state they can read
and change through validated tools. Work, decisions, migrations, and audit
events remain explicit instead of disappearing into prompts, scratch files,
or provider-specific conventions.

> **Maturity: usable project in active development; pre-1.0.**
> Current prereleases support end-to-end local installation and validated MCP
> workflows, but contracts may still change between prereleases. Pin exact
> versions, read the release notes before updating, and test upgrades against
> a disposable copy of your project.

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
| MCP runtime | One-process gateway and per-skill servers | Aggregate server retained for older integrations | Additional harness-specific transport validation |
| Project memory | Validated entities, state transitions, indexing, events, migrations | Explicit v0-to-v1 compatibility manifests | Further v1 vocabulary stabilization |
| Installer | Local `plan`, `install`, `update`, `verify`, recovery, and conservative `uninstall` | Selected v0 layouts detected from explicit evidence | More platform release assets and successive prerelease upgrade coverage |
| Harness projections | Canonical MCP catalog with Codex and Claude adapters | Existing user-owned configuration is preserved or reported as a conflict | Broader first-class harness acceptance |
| Packages and profiles | Release-owned distribution manifest and managed profile | Manual archive copying remains documented for older releases | Profile contract stabilization before v1 GA |

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

The v1 prerelease includes a local standalone installer. Download the release
archive and its matching installer asset, verify the published checksums and
trust material, then plan before applying:

```sh
processkit plan --root . --profile managed --harness codex
processkit install --root . --profile managed --harness codex
processkit verify --root .
```

Updates are three-way reconciled against target-side provenance; user changes
are preserved or surfaced as conflicts. Uninstall removes only unchanged paths
whose ownership processkit can prove. See the
[installer contract](docs-site/content/en/docs/installer/contract.md),
[local release and verification workflow](docs-site/content/en/docs/installer/local-release.md),
and [threat model](docs-site/content/en/docs/installer/threat-model.md).

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
version = "v0.27.1"

[context]
packages = ["managed"]
```

That integration is convenient, but not required. processkit remains the
standalone source of the schemas, skills, packages, and MCP runtime.

## Documentation

- [Documentation](docs-site/content/en/docs/_index.md)
- [Changelog](CHANGELOG.md)
- [Contributing](CONTRIBUTING.md)
- [License](LICENSE)

## License

processkit is distributed under the MIT License. Unless a file states
otherwise, the project maintainers intend the MIT License in this
repository to apply retroactively to all historical commits, tags, and
release artifacts for this repository.

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
The repository does not use GitHub Actions; maintainers run and report these
checks locally before merging or releasing.

Release packaging is guarded by:

```sh
scripts/check-src-context-drift.sh --release-deliverable
scripts/test-installer-local.sh
scripts/release-local.sh vX.Y.Z <private-key.pem> <public-key.pem>
```

See [Local release operation](docs-site/content/en/docs/installer/local-release.md)
for the agent-first, human-operable signing and verification workflow.
