# processkit

**Primitives, skills, and process templates for AI-assisted work environments.**

processkit is the content layer for [aibox](https://github.com/projectious-work/aibox).
aibox provides the containerized development environment; processkit provides
the skills, process primitives, and MCP servers that run inside it.

## What's inside

```
src/                   ← content shipped to consumers (treat like source code)
  primitives/
    FORMAT.md          ← entity file format spec (apiVersion/kind/metadata/spec)
    schemas/           ← YAML schemas for the 18 process primitives
    state-machines/    ← default state machine definitions
  skills/              ← multi-artifact skill packages (SKILL.md + examples + templates + mcp)
  processes/           ← process definitions (code-review, release, incident-response, ...)
  packages/            ← skill/process bundles (minimal, managed, software, research, product)

docs-site/             ← user-facing documentation (Docusaurus)
.devcontainer/         ← this repo's own dev environment (dogfooded via aibox)
context/               ← this repo's own project management artifacts
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
| Release mechanism      | GHCR images + CLI binary                    | Git tags                                  |

`aibox init` consumes a specific processkit git tag and installs its skills +
process templates into the target project. Users can add more skills from any
git repo using the same `git-tag` release pattern.

## Dogfooding and the bootstrap loop

processkit is itself scaffolded and developed using aibox — opening this repo
in a dev container gives you all the aibox tooling. This creates an intentional
loop: aibox depends on processkit for content; processkit depends on aibox for
its dev environment.

The loop is resolved by **version pinning**:

- `aibox.toml` in this repo pins the aibox version used to generate
  `.devcontainer/` (currently `0.14.1`).
- aibox (starting with the version that adds processkit consumption) pins a
  processkit tag in its own defaults and in generated project `aibox.toml`.
- Neither side follows the other automatically. Upgrades happen deliberately
  via `aibox migrate`, which generates a diff against the pinned version.

**Why this works during bootstrap:** The aibox version currently pinned here
(0.14.1) still ships embedded skills — it does not yet consume processkit.
So this repo can be developed today with aibox's own tooling while processkit
itself is being built. Once processkit reaches a consumable state (tag
`v0.2.0` onwards) and aibox ships the consumer logic, the loop closes, but
each side still pins a specific counterpart version.

## Status

Phase 1 (foundation) — in progress. See [context/DISCUSSIONS](context/) and
the aibox repo's DISC-002 for the full plan.

## License

MIT — see [LICENSE](LICENSE).
