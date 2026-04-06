# aibox Configuration Notes — processkit

**Project:** processkit — content layer for aibox (primitives, skills, processes, MCP servers).

## Bootstrap version pinning

This repo pins **aibox 0.14.1** in `aibox.toml`. That version still ships embedded
skills and does not yet consume processkit, which is what makes the dogfooding loop
safe during bootstrap:

- aibox 0.14.1 scaffolds `.devcontainer/` and `context/` for this repo.
- processkit builds v0.1.0..v0.3.0 in parallel.
- aibox Phase 4.2 adds processkit consumption logic (targeting processkit ≥ v0.2.0).
- Only then is it safe to bump aibox in this repo — and the upgrade should be
  coordinated with a processkit tag the new aibox knows about.

**Rule:** do not upgrade `[aibox] version` in `aibox.toml` here until
(a) aibox ≥ X consumes processkit, and (b) processkit has a tag ≥ Y that X knows about.

## The skills in `.claude/skills/` vs `skills/` top level

- `.claude/skills/` — 6 skills aibox 0.14.1 deployed for the agent working on this repo
  (agent-management, estimation-planning, fastapi-patterns, pandas-polars,
  python-best-practices, retrospective). These are for agents working ON processkit.
- `skills/` (top level, currently empty) — the multi-artifact skill packages this repo
  ships TO consumers. Populated in Phase 2.

See CLAUDE.md for the full disambiguation.

## Status

Phase 1 (foundation) — v0.1.0:
- [x] Repo scaffolding (primitives/, skills/, processes/, packages/, INDEX.md files)
- [x] Entity file format spec (primitives/FORMAT.md)
- [x] Schemas for WorkItem, LogEntry, DecisionRecord
- [x] State machines for WorkItem, DecisionRecord
- [ ] Tag v0.1.0

See aibox's `context/discussions/DISC-002-aibox-refocus.md` for the full plan.
