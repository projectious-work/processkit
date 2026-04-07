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

- **19 process primitives** — WorkItem, LogEntry, DecisionRecord, Migration *(new in v0.4.0)*,
  Actor, Role, Binding, Scope, Category, Constraint, Gate, Schedule, Process, StateMachine,
  Metric, Discussion, Artifact, Context, CrossReference. Framework-agnostic building blocks.
- **106 skills** — 85 technical and language skills migrated from aibox, plus 21 new
  process-primitive skills (`event-log`, `workitem-management`, `decision-record`,
  `owner-profiling`, `context-grooming`, `migration-management`, ...) that wrap the
  primitives.
- **5 package tiers** — `minimal`, `managed`, `software`, `research`, `product` — curated
  bundles of skills for common use cases.
- **Python MCP servers** (from v0.3.0) — mechanical-correctness tools for foundation skills,
  delivered via the official MCP SDK with PEP 723 inline dependencies.
- **Configurable upstream + diff script** *(new in v0.4.0)* — `[processkit] source` in
  `aibox.toml` accepts any git URL (GitHub, GitLab, Gitea, self-hosted), so companies
  can fork processkit, customize it, and have their projects consume the fork.
  `scripts/processkit-diff.sh` is the generic version-comparison tool that drives
  migration generation.

## How it's used

A consumer selects a processkit source and version in their `aibox.toml`:

```toml
[processkit]
source  = "https://github.com/projectious-work/processkit.git"
version = "v0.4.0"

[context]
packages = ["managed"]
```

`aibox init` fetches that tag and installs the selected package's
skills, primitives, and process templates into the project's `context/`
directory (provider-neutral — nothing lands under `.claude/`). The
project gets `aibox.lock` at the repository root (Cargo-style, pinning
the resolved source URL + version + commit) and a verbatim reference
copy of every shipped file at
`context/templates/processkit/<version>/`. A future `aibox sync` reads
SHAs from those reference templates on the fly to classify what's been
changed locally vs upstream — no separate manifest file is needed.

Users can add more skills from any GitHub repo using the same pattern.

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
- [Primitives](./primitives/overview) — the 19 building blocks and the entity file format
- [Skills](./skills/overview) — the skill package format and the catalog
- [Packages](./packages/overview) — the five tiers and how to pick one
- [Reference → Privacy Tiers](./reference/privacy) — public, project-private, user-private
- [Reference → Migration](./reference/migration) — the v0.4.0 migration model

## Status

- **v0.1.0** — foundation (entity format, three primitives, two state machines)
- **v0.2.0** — skill migration (85 + 16 skills, packages, this docs site)
- **v0.3.0** — MCP servers (six servers, shared lib, smoke tests)
- **v0.4.0** *(current)* — Migration primitive, owner-profiling, context-grooming,
  PROVENANCE.toml + diff script, configurable upstream source URL, privacy tiers
- **v1.0.0** — first stable release (not yet scheduled)
