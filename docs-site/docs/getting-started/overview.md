---
sidebar_position: 1
title: "Overview"
---

# Getting Started — Overview

processkit is consumed by agent harnesses and project tooling. The
typical managed workflow is:

1. Install [aibox](https://projectious-work.github.io/aibox/) — this gives you the
   containerized runtime and the `aibox` CLI.
2. Run `aibox init` in a new or existing project, pinning a processkit tag.
3. Pick a package tier (`minimal`, `managed`, `software`, `research`, `product`).
4. Start working in the dev container — the agent has the skills available immediately.

See [Installing](./installing) for the concrete steps.

aibox is optional infrastructure, not a runtime dependency of
processkit. The same installed `context/skills` tree can be used by
Claude Code, Codex, OpenCode, Hermes, Aider integrations, or a custom
MCP client when those tools are configured directly.

## What aibox init actually does

For a new project:

```bash
aibox init \
  --name my-project \
  --process managed \
  --ai claude \
  --addons python
```

produces:

- `aibox.toml` — aibox configuration, pinning aibox and processkit versions
- `aibox.lock` — Cargo-style lockfile pinning the resolved processkit
  source URL, version, and commit
- `.devcontainer/` — Dockerfile, docker-compose.yml, devcontainer.json
- `AGENTS.md` — root-level agent entry point (provider-neutral); a thin
  `CLAUDE.md` (or other provider-specific file) points at it
- `context/` — your project's management artifacts and the installed
  processkit content:
  - `context/skills/<name>/` — installed processkit skills
    (provider-neutral path; nothing lands under `.claude/`)
  - `context/skills/_lib/processkit/` — the shared lib for MCP servers
  - `context/schemas/`, `context/state-machines/`, `context/processes/`
    — installed primitives and process definitions
  - `context/templates/processkit/<version>/` — verbatim reference
    copies of every shipped file (used for `aibox sync` diffs)
  - `context/workitems/`, `decisions/`, `logs/`, ... — your project's
    own entity files

From v0.2.0 onwards, the skills come from the processkit tag pinned in
`aibox.toml`, not from aibox itself.

## Requirements

- Docker or OrbStack (for the dev container)
- Python ≥ 3.10 and `uv` (already present inside aibox containers; required by
  the Phase 3 MCP servers)
- A supported AI provider: Claude Code, Aider, Gemini CLI, or Mistral

## Learning path

1. Read [Primitives → Overview](../primitives/overview) to understand
   the 19 primitives.
2. Read [Primitives → Format](../primitives/format) to learn the entity file shape.
3. Read [Skills → Overview](../skills/overview) to learn what skills do.
4. Pick a package ([Packages → Overview](../packages/overview)).
5. Create your [first entity](./first-entity).
