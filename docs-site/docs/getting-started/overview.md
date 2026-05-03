---
sidebar_position: 1
title: "Overview"
---

# Getting Started — Overview

processkit is consumed by agent harnesses and project tooling. You can
install it manually from a release tarball, or let an installer such as
aibox do the copying and harness wiring for you.

The minimal workflow is:

1. Install a processkit release into your project's `context/` tree.
2. Pick a package tier (`minimal`, `managed`, `software`, `research`,
   or `product`).
3. Register `processkit-gateway` with your MCP-capable harness.
4. Use MCP tools for entity reads and writes instead of editing project
   memory by hand.

See [Installing](./installing) for concrete commands.

## What gets installed

A processkit release contains:

- `context/skills/` — the shipped skill catalog and per-skill MCP
  servers.
- `context/skills/_lib/processkit/` — shared Python runtime helpers used
  by the MCP servers and gateway.
- `context/schemas/` — the 16 shipped v2 project-memory schemas.
- `context/state-machines/` — implementation contracts used by entity
  management tools.
- `.processkit/` — package tier metadata and release metadata.
- `AGENTS.md` — a provider-neutral agent entry point.

Your project then owns its local memory under directories such as
`context/workitems/`, `context/decisions/`, `context/artifacts/`,
`context/notes/`, and `context/logs/`.

## Managed install path

Managed installers can add devcontainer lifecycle, harness config, and
upgrade handling. aibox is the reference managed integration today: it
can fetch a pinned processkit release, choose a package tier, write MCP
config for the selected harness, and optionally supervise the gateway
daemon.

That is convenience infrastructure. The same installed processkit files
can also be used directly by Claude Code, Codex, OpenCode, Hermes, Aider
integrations, or a custom MCP client when those tools are configured
manually.

## Requirements

- Python 3.10 or newer.
- `uv`, used to run the Python MCP server scripts and resolve their
  inline PEP 723 dependencies.
- An MCP-capable harness if you want tool access. You can still read the
  skills and schemas directly without MCP.
- Docker or OrbStack only if your chosen environment manager uses a
  devcontainer.

## Learning path

1. Read [Primitives → Overview](../primitives/overview) to understand
   the durable entity model.
2. Read [Primitives → Format](../primitives/format) to learn the entity file shape.
3. Read [Skills → Overview](../skills/overview) to learn what skills do.
4. Pick a package ([Packages → Overview](../packages/overview)).
5. Create your [first entity](./first-entity).
