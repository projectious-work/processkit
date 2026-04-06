---
sidebar_position: 2
title: "minimal"
---

# minimal

**Intended for:** solo developers and small side projects.
**Extends:** — (the base tier)

The lightest footprint package. Just enough structure to track work and
debug effectively — no roles, no scopes, no governance artifacts.

## Included skills

- `event-log` — foundation: probabilistic append-only event log
- `actor-profile` — basic Actor entities
- `workitem-management` — WorkItem creation and transitions
- `git-workflow` — branch/commit/PR conventions
- `debugging` — systematic debug workflow
- `testing-strategy` — unit vs integration vs E2E guidance
- `error-handling` — cross-language patterns

## When to upgrade

- You're joining a team → `managed`
- You need formal decision records, scopes, and process artifacts → `managed`
- You're building production software → `software`
- You're doing data/ML work → `research`
- You need the kitchen sink → `product`

## Source

[`src/packages/minimal.yaml`](https://github.com/projectious-work/processkit/blob/main/src/packages/minimal.yaml)
