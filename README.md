# processkit

**Primitives, skills, and process templates for AI-assisted work environments.**

processkit is the content layer for [aibox](https://github.com/projectious-work/aibox).
aibox provides the containerized development environment; processkit provides
the skills, process primitives, and MCP servers that run inside it.

**Latest tag:** v0.4.0 — Migration primitive, owner-profiling, context-grooming,
configurable upstream source URL, and the PROVENANCE.toml + diff script that
power version migrations across forks. See
[docs](https://projectious-work.github.io/processkit/) and
[docs/reference/migration](https://projectious-work.github.io/processkit/docs/reference/migration).

## What's inside

```
src/                       ← content shipped to consumers (treat like source code)
  PROVENANCE.toml          ← maps every shipped file to its last-changed tag (v0.4.0+)
  primitives/              ← 19 process primitives
    FORMAT.md              ← entity file format spec (apiVersion/kind/metadata/spec + privacy)
    schemas/               ← YAML JSON Schemas
    state-machines/        ← default state machine definitions
  skills/                  ← 106 multi-artifact skill packages (SKILL.md + examples + templates + mcp)
  processes/               ← process definitions (code-review, release, incident-response, ...)
  packages/                ← 5 tier definitions (minimal, managed, software, research, product)
  lib/                     ← shared Python library used by MCP servers (not a primitive — internal infra)

scripts/                   ← release tooling
  stamp-provenance.sh      ← regenerates src/PROVENANCE.toml at release time
  processkit-diff.sh       ← generic diff between two tags (consumed by aibox sync)
  smoke-test-servers.py    ← end-to-end test of all MCP servers

docs-site/                 ← user-facing documentation (Docusaurus)
.devcontainer/             ← this repo's own dev environment (dogfooded via aibox)
context/                   ← this repo's own project management artifacts
```

**Rule:** everything under `src/` is shipped content; everything else is about
*this repo itself*. When `aibox init` installs processkit into a project, it
reads from `src/`.

## How it relates to aibox

| Concern                | aibox                                       | processkit                                |
|------------------------|---------------------------------------------|-------------------------------------------|
| Containers & toolchain | Yes — CLI, images, devcontainer scaffolding | No                                        |
| Skills & process       | No (consumes from processkit)               | Yes — all skills, primitives, MCP servers |
| CLI surface            | `aibox init`, `aibox start`, ...            | None (consumed, not run)                  |
| Release mechanism      | GHCR images + CLI binary                    | Git tags + tarballs                       |

`aibox init` reads `[processkit] source` and `[processkit] version` from your
project's `aibox.toml`, fetches that source at that tag, and installs the
selected package's content into the project. The default source is
`https://github.com/projectious-work/processkit.git` but any git URL works
— see [Configurable upstream source](#configurable-upstream-source) below.

## Configurable upstream source

`aibox.toml` in a consuming project pins both the source URL and the version:

```toml
[processkit]
source   = "https://github.com/projectious-work/processkit.git"   # default upstream
version  = "v0.4.0"
src_path = "src"   # optional — defaults to "src", set to "" if your fork has no src/ wrapper
# branch = "main"  # optional — for tracking a moving branch (discouraged for production)
```

**Use case: company forks.** ACME Corp clones `processkit` into
`gitlab.acme.com/platform/processkit-acme`, makes ACME-specific
customizations to the release process, drops a few skills they don't need,
and tags `v0.4.0-acme.1`. ACME's projects pin:

```toml
[processkit]
source  = "https://gitlab.acme.com/platform/processkit-acme.git"
version = "v0.4.0-acme.1"
```

The fork is a self-contained processkit-compatible source. The diff script
and migration model work identically — they just see the fork's tags instead
of upstream's. ACME can sync from upstream periodically using
`scripts/processkit-diff.sh`.

## Dogfooding and the bootstrap loop

processkit is itself scaffolded and developed using aibox — opening this
repo in a dev container gives you all the aibox tooling. This creates an
intentional loop: aibox depends on processkit for content; processkit
depends on aibox for its dev environment.

The loop is resolved by **version pinning**:

- `aibox.toml` in this repo pins the aibox version used to generate
  `.devcontainer/` (currently `0.14.1`). Bumping to a newer pure-bug-fix
  aibox (e.g. 0.14.4) is technically safe but currently a deferred decision —
  the bump should be coordinated with the in-flight aibox-side processkit
  consumption work.
- aibox (starting with the version that adds processkit consumption,
  planned for aibox 0.15+) pins a processkit tag in its own defaults
  and in generated project `aibox.toml`.
- Neither side follows the other automatically. Upgrades happen
  deliberately via `aibox sync` + `aibox migrate`, which generates a
  Migration entity for the agent and user to walk through.

**Why this works during bootstrap:** The aibox version currently pinned
here (0.14.1) still ships embedded skills — it does not yet consume
processkit. So this repo can be developed today with aibox's own tooling
while processkit itself is being built. Once aibox ships the consumer
logic, the loop closes, but each side still pins a specific counterpart
version.

## Provenance and migrations (v0.4.0+)

processkit ships a **single-file provenance map** at `src/PROVENANCE.toml`
mapping every shipped file to the git tag in which it last changed. The
release process regenerates it via `scripts/stamp-provenance.sh
<next-version>` before tagging.

The generic diff script `scripts/processkit-diff.sh` reads
`src/PROVENANCE.toml` at two tags and emits a structured diff (added,
removed, changed, unchanged) in text, TOML, or JSON. Tools like aibox sync
consume this to produce per-project Migration briefings.

Forks can use the same scripts against their own tags. The
`[source].project` field in `PROVENANCE.toml` identifies which fork the
provenance belongs to.

## Status

| Tag    | Theme                                                          |
|--------|----------------------------------------------------------------|
| v0.1.0 | Foundation — entity format spec, 3 schemas, 2 state machines   |
| v0.2.0 | Skill migration — 101 skills, 5 packages, docs-site bootstrap  |
| v0.3.0 | MCP servers — 6 servers, shared lib, smoke tests               |
| v0.4.0 | **Current** — Migration primitive, owner-profiling, context-grooming, PROVENANCE.toml, configurable upstream source, privacy tiers |
| v1.0.0 | First stable release — not yet scheduled                       |

See [docs](https://projectious-work.github.io/processkit/) for the full
story.

## Documentation

- **User docs:** https://projectious-work.github.io/processkit/
- **Format spec:** [`src/primitives/FORMAT.md`](src/primitives/FORMAT.md)
- **Skill format:** [`src/skills/FORMAT.md`](src/skills/FORMAT.md)
- **Operating manual:** [`CONTRIBUTING.md`](CONTRIBUTING.md)
- **Handover briefing for next agent:** [`context/HANDOVER.md`](context/HANDOVER.md)
- **Backlog (deferred items):** [`context/BACKLOG.md`](context/BACKLOG.md)

## License

MIT — see [LICENSE](LICENSE).
