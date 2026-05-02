---
sidebar_position: 2
title: "Installing"
---

# Installing

processkit is distributed as git tags of the
[projectious-work/processkit](https://github.com/projectious-work/processkit)
repository. The managed path is to install aibox and pin a processkit
tag in your project's `aibox.toml`.

aibox is not required by processkit at runtime. It is the installer and
supervisor for managed projects: it fetches processkit content, writes
provider-specific harness config, and starts the devcontainer. Users who
install the same files by another method can point an MCP-capable
harness directly at processkit's server commands.

## 1. Install aibox

Follow the [aibox installation guide](https://projectious-work.github.io/aibox/docs/getting-started/installation).
You need a recent enough version of aibox to consume processkit — see the
compatibility matrix below.

## 2. Pin a processkit version

In your project's `aibox.toml`:

```toml
[context]
packages = ["managed"]
processkit_version = "v0.18.2"
```

`aibox init` and `aibox sync` will fetch that tag and cache it under
`~/.cache/aibox/processkit/v0.18.2/`.

## 3. Run `aibox init`

```bash
aibox init --name my-project --process managed
```

On first run, aibox fetches processkit at the pinned tag (preferring
the published release-asset tarball, falling back to a git fetch) and
installs the selected package's skills into `context/skills/`, the
shared lib into `context/skills/_lib/processkit/`, primitive schemas
into `context/schemas/`, state machines into `context/state-machines/`,
and process definitions into `context/processes/`. The full upstream
reference templates are copied verbatim to
`context/templates/processkit/<version>/` and `aibox.lock` is written
at the project root.

## 4. Verify

```bash
ls context/skills/
aibox lint   # structural validation of context/
```

If `aibox lint` passes and the `context/skills/` directory contains the
expected skills, you are ready to start working.

## Compatibility matrix

| processkit | aibox (min) | notes                                           |
|------------|-------------|-------------------------------------------------|
| `v0.1.0`   | 0.14.1      | Foundation only — no skills yet                 |
| `v0.7.0`   | 0.17.0      | Full skill catalog + MCP servers                |
| `v0.10.0`  | 0.17.0      | Skills in 7 category subdirectories             |
| `v0.12.0`  | 0.17.12     | artifact-management MCP; processkit/ layout     |
| `v0.13.0`  | 0.17.12     | task-router + skill-finder MCP; route_task()    |
| `v0.14.0`  | 0.17.12     | enforcement Rails 1–4: contract + hooks + ack   |
| `v0.15.0`  | 0.17.12     | team-creator skill; session-orientation wiring  |
| `v0.16.0`  | 0.17.12     | canonical team schema fields; closes aibox #6   |
| `v0.17.0`  | 0.17.12     | 13 /pk-* commands; OpenWeave; Rail 5; contract v2 |
| `v0.18.0`  | 0.18.3      | CapabilityProfileRouting 3-layer models; 26 /pk-*; skill-gate decouple |
| `v0.18.1`  | 0.18.3      | hotfix: src↔context sync; fixes #7 hookEventName in Claude Code 2.1+ |
| `v0.18.2`  | 0.18.3      | fixes #8 mcp-config paths; skip_decision_record + contract v2; drift guard; SnappyTrout |

aibox ships with a default processkit version pin. Overriding it in
`aibox.toml` is how you opt into newer content without upgrading aibox (or
vice versa).

## Community skill packages

Any GitHub repo with a `package.yaml` and a git tag can be installed as a
processkit-compatible skill package:

```bash
aibox process install https://github.com/youruser/your-skills --tag v1.0.0
```

See the [aibox docs](https://projectious-work.github.io/aibox/) for the
full community-package spec.
