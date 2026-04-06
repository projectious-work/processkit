---
sidebar_position: 1
title: "Overview"
---

# Getting Started — Overview

processkit is consumed, not run directly. The typical workflow is:

1. Install [aibox](https://projectious-work.github.io/aibox/) — this gives you the
   containerized runtime and the `aibox` CLI.
2. Run `aibox init` in a new or existing project, pinning a processkit tag.
3. Pick a package tier (`minimal`, `managed`, `software`, `research`, `product`).
4. Start working in the dev container — the agent has the skills available immediately.

See [Installing](./installing) for the concrete steps.

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
- `.devcontainer/` — Dockerfile, docker-compose.yml, devcontainer.json
- `CLAUDE.md` — root-level agent guidance
- `context/` — your project's management artifacts (BACKLOG, DECISIONS, ...)
- `.claude/skills/` — the skills from the selected processkit package

From v0.2.0 onwards, the skills come from the processkit tag pinned in
`aibox.toml`, not from aibox itself.

## Requirements

- Docker or OrbStack (for the dev container)
- Python ≥ 3.10 and `uv` (already present inside aibox containers; required by
  the Phase 3 MCP servers)
- A supported AI provider: Claude Code, Aider, Gemini CLI, or Mistral

## Learning path

1. Read [Primitives → Overview](../primitives/overview) to understand the 18 primitives.
2. Read [Primitives → Format](../primitives/format) to learn the entity file shape.
3. Read [Skills → Overview](../skills/overview) to learn what skills do.
4. Pick a package ([Packages → Overview](../packages/overview)).
5. Create your [first entity](./first-entity).
