---
sidebar_position: 3
title: "Version Migration"
---

# Version Migration

processkit is distributed as git tags. Upgrading pinned versions is
deliberate — neither aibox nor processkit follows the other automatically.

## When to upgrade processkit

- A new processkit tag ships skills, schemas, or MCP servers you want
- A security fix lands
- You're starting a new project and want the latest

## How to upgrade

```toml
# aibox.toml
[context]
processkit_version = "v0.2.0"   # was: "v0.1.0"
```

Then:

```bash
aibox sync        # refetches processkit, reinstalls skills
aibox migrate     # reviews template diffs (v0.1.0 → v0.2.0)
aibox lint        # structural validation
```

`aibox migrate` (from aibox Phase 4.7) diffs the template snapshot stored
in `context/.aibox/templates/v0.1.0/` against the new snapshot and
produces migration prompts for the agent. The agent reviews each change
and applies it with human approval. **No automatic in-place patching.**

## What gets updated

Upgrading processkit affects:

- **Skills** in `.claude/skills/` — re-installed from the new tag
- **Primitive schemas** in `context/.aibox/schemas/` — refreshed
- **State machines** in `context/.aibox/state-machines/` — refreshed
- **Package definitions** — refreshed
- **MCP configs** — refreshed

It does **not** touch:

- Your `context/workitems/`, `context/decisions/`, `context/logs/`, etc.
- Any files you have manually edited outside `.aibox/` scaffolding
- Your `aibox.toml` (except `processkit_version` which you set)

## Breaking changes

If the new processkit tag introduces a new `apiVersion` (e.g. `v1 → v2`),
`aibox migrate` produces a more detailed migration prompt including
schema-level changes. The agent walks the project's existing entities and
upgrades them with human approval.

See [apiVersion Policy](./apiversion-policy) for what counts as breaking.

## Downgrading

Downgrading is supported but discouraged. To downgrade:

```toml
[context]
processkit_version = "v0.1.0"   # was: "v0.2.0"
```

then `aibox sync`. If the downgrade skips past a schema `apiVersion` bump,
existing entities may become incompatible with the older schemas.
`aibox lint` will flag the failures. You may need to manually edit or
delete incompatible entities.
