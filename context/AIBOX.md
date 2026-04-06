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

## The skills in `.claude/skills/` vs `src/skills/`

- `.claude/skills/` — 6 skills aibox 0.14.1 deployed for the agent working on this repo
  (agent-management, estimation-planning, fastapi-patterns, pandas-polars,
  python-best-practices, retrospective). These are for agents working ON processkit.
- `src/skills/` — 102 multi-artifact skill packages this repo ships TO consumers.
  This is the SHIPPED CONTENT.

See CLAUDE.md for the full disambiguation.

## Status

### v0.1.0 — foundation (shipped 2026-04-06)
- [x] Repo scaffolding
- [x] Entity file format spec (`src/primitives/FORMAT.md`)
- [x] Schemas for WorkItem, LogEntry, DecisionRecord
- [x] State machines for WorkItem, DecisionRecord

### v0.2.0 — skill migration (shipped 2026-04-06)
- [x] `src/` restructure (content lives under `src/`)
- [x] `apiVersion: processkit.projectious.work/v1`
- [x] 85 skills migrated from aibox `templates/skills/`
- [x] 16 new process-primitive skills (event-log, workitem-management, ...)
- [x] 5 package tiers (minimal, managed, software, research, product)
- [x] Docusaurus docs-site bootstrapped
- [x] PRD.md drafted from DISC-002

### v0.3.0 — MCP servers (awaiting tag)
- [x] `src/lib/processkit/` shared Python library (entity, ids, paths, schema, state_machine, index, config)
- [x] `index.existing_ids(db, kind)` helper added on review feedback
- [x] index-management skill (Layer 0, read side) + MCP server
- [x] id-management skill (Layer 0, write side) + MCP server (added on review feedback — split out from index-management)
- [x] event-log MCP server (uses both Layer 0 foundations)
- [x] workitem-management MCP server (uses both Layer 0 foundations)
- [x] decision-record MCP server (uses both Layer 0 foundations)
- [x] binding-management MCP server (uses both Layer 0 foundations)
- [x] mcp-config.json + README.md per server (6 servers total)
- [x] Smoke test (`scripts/smoke-test-servers.py`) — covers all 6 servers
- [x] CONTRIBUTING.md
- [x] BACKLOG.md
- [x] Owner reviewed
- [ ] Push and tag v0.3.0

See aibox's `context/discussions/DISC-002-aibox-refocus.md` for the full plan.
