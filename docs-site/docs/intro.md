---
sidebar_position: 1
title: "Introduction"
slug: /
---

# processkit

**processkit is the content layer for [aibox](https://github.com/projectious-work/aibox).**
Where aibox provides the containerized runtime for AI-assisted development, processkit
provides everything that runs inside it: process primitives, skills, process templates,
and Model Context Protocol (MCP) servers.

## The analogy

- `aibox` is to AI work environments as `uv` is to Python environments — it sets up the box.
- `processkit` is what goes *in* the box.

## What processkit ships

- **18 process primitives** — WorkItem, LogEntry, DecisionRecord, Actor, Role, Binding,
  Scope, Category, Constraint, Gate, Schedule, Process, StateMachine, Metric, Discussion,
  Artifact, Context, CrossReference. Framework-agnostic building blocks.
- **101 skills** — 85 technical and language skills migrated from aibox, plus 16 new
  process-primitive skills (`event-log`, `workitem-management`, `decision-record`, ...)
  that wrap the 18 primitives.
- **5 package tiers** — `minimal`, `managed`, `software`, `research`, `product` — curated
  bundles of skills for common use cases.
- **Python MCP servers** (from v0.3.0) — mechanical-correctness tools for foundation skills,
  delivered via the official MCP SDK with PEP 723 inline dependencies.

## How it's used

A consumer selects a processkit tag in their `aibox.toml`:

```toml
[context]
packages = ["managed"]
processkit_version = "v0.2.0"
```

`aibox init` fetches that tag and installs the selected package's skills, primitives,
and process templates into the project's `context/` and `.claude/` directories. Users
can add more skills from any GitHub repo using the same pattern.

## The two repos

| Concern                | aibox                                       | processkit                                |
|------------------------|---------------------------------------------|-------------------------------------------|
| Containers & toolchain | Yes — CLI, images, devcontainer scaffolding | No                                        |
| Skills & process       | No (consumes from processkit)               | Yes — skills, primitives, MCP servers     |
| CLI surface            | `aibox init`, `aibox start`, ...            | None (consumed, not run)                  |
| Release mechanism      | GHCR images + CLI binary                    | Git tags                                  |

Splitting content from infrastructure lets both sides evolve at their natural pace.

## Where to go next

- [Getting Started](./getting-started/overview) — install aibox, consume processkit, create your first entity
- [Primitives](./primitives/overview) — the 18 building blocks and the entity file format
- [Skills](./skills/overview) — the skill package format and the catalog
- [Packages](./packages/overview) — the five tiers and how to pick one

## Status

processkit is early. v0.1.0 was the foundation; **v0.2.0** ships the skill migration,
package tiers, and this documentation site. **v0.3.0** will ship working MCP servers
and the SQLite index. **v1.0.0** will be the first stable release.
