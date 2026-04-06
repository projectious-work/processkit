---
sidebar_position: 2
title: "Installing"
---

# Installing

processkit is distributed as git tags of the
[projectious-work/processkit](https://github.com/projectious-work/processkit)
repository. You do not install it directly — you install aibox and pin a
processkit tag in your project's `aibox.toml`.

## 1. Install aibox

Follow the [aibox installation guide](https://projectious-work.github.io/aibox/docs/getting-started/installation).
You need a recent enough version of aibox to consume processkit — see the
compatibility matrix below.

## 2. Pin a processkit version

In your project's `aibox.toml`:

```toml
[context]
packages = ["managed"]
processkit_version = "v0.2.0"
```

`aibox init` and `aibox sync` will fetch that tag and cache it under
`~/.cache/aibox/processkit/v0.2.0/`.

## 3. Run `aibox init`

```bash
aibox init --name my-project --process managed
```

On first run, aibox clones processkit at the pinned tag and installs the
selected package's skills into `.claude/skills/` and the primitive schemas
into `context/`.

## 4. Verify

```bash
ls .claude/skills/
aibox lint   # structural validation of context/
```

If `aibox lint` passes and the `.claude/skills/` directory contains the
expected skills, you are ready to start working.

## Compatibility matrix

| processkit | aibox (min) | notes                                     |
|------------|-------------|-------------------------------------------|
| `v0.1.0`   | 0.14.1      | Foundation only — no skills yet           |
| `v0.2.0`   | (TBD)       | Full skill catalog; needs aibox Phase 4.2 |
| `v0.3.0`   | (TBD)       | Adds MCP servers; needs aibox Phase 4.3  |

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
