# aibox Configuration Notes — processkit

**Project:** processkit — content layer for aibox (primitives, skills, processes, MCP servers).

## Bootstrap version pinning

This repo pins **aibox 0.14.1** in `aibox.toml`. That version still ships embedded
skills and does not yet consume processkit, which is what makes the dogfooding loop
safe during bootstrap:

- aibox 0.14.1 scaffolds `.devcontainer/` and `context/` for this repo.
- processkit has shipped v0.1.0 → v0.4.0 in parallel.
- aibox Phase 4.1+ will add processkit consumption logic (work in flight on the aibox side).
- Only after that lands is it safe to bump aibox here — and the upgrade should be
  coordinated with a processkit tag that the new aibox knows about.

**Rule:** do not upgrade `[aibox] version` in `aibox.toml` here until
(a) aibox ≥ X consumes processkit, and (b) processkit has a tag ≥ Y that X knows about.

Pure bug-fix bumps (0.14.1 → 0.14.4) are technically safe — they don't change
the consumption story — but currently a deferred decision. Today's pin remains
0.14.1 until coordinated with the in-flight aibox work.

## The skills in `.claude/skills/` vs `src/skills/`

- `.claude/skills/` — 6 skills aibox 0.14.1 deployed for the agent working on this repo
  (agent-management, estimation-planning, fastapi-patterns, pandas-polars,
  python-best-practices, retrospective). These are for agents working ON processkit.
- `src/skills/` — 106 multi-artifact skill packages this repo ships TO consumers.
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

### v0.3.0 — MCP servers (shipped 2026-04-06)
- [x] `src/lib/processkit/` shared Python library (entity, ids, paths, schema, state_machine, index, config)
- [x] `index.existing_ids(db, kind)` helper added on review feedback
- [x] index-management skill (Layer 0, read side) + MCP server
- [x] id-management skill (Layer 0, write side) + MCP server (split out from index-management on review)
- [x] event-log MCP server (uses both Layer 0 foundations)
- [x] workitem-management MCP server
- [x] decision-record MCP server
- [x] binding-management MCP server
- [x] mcp-config.json + README.md per server (6 servers total)
- [x] Smoke test (`scripts/smoke-test-servers.py`) covers all 6 servers
- [x] CONTRIBUTING.md
- [x] BACKLOG.md

### v0.4.0 — Migration primitive, owner-profiling, context-grooming, PROVENANCE (shipped 2026-04-07)
- [x] **Migration primitive (19th)** — schema, state machine, MIG prefix in lib KIND_PREFIXES
- [x] **migration-management skill** (Layer 3) — workflow for the pending → in-progress → applied lifecycle
- [x] **owner-profiling skill** (Layer 4) — interview-driven owner profile bootstrap with 4 templates and 2 reference docs
- [x] **context-grooming skill** (Layer 4) — periodic context cleanup with default ruleset and report template
- [x] **`src/PROVENANCE.toml`** — single-file provenance map, fully stamped against current git history (240 files)
- [x] **`scripts/stamp-provenance.sh`** — release-time PROVENANCE.toml generator
- [x] **`scripts/processkit-diff.sh`** — generic, fork-neutral diff between two tags (text/toml/json)
- [x] **Privacy tier convention** documented in FORMAT.md and `docs-site/docs/reference/privacy.md`; the `context/**/private/` gitignore rule
- [x] **Context efficiency**: new "Context budget and lazy loading" section in `agent-management/SKILL.md` paired with the `context-grooming` skill
- [x] **docs-site updates**: 19 primitives in primitives/overview, reference/migration rewritten for v0.4.0 model, NEW reference/privacy page, intro updated
- [x] **README.md updated** for v0.4.0
- [x] **HANDOVER.md updated** with "What changed in v0.4.0" preamble + status table
- [x] **CLAUDE.md updated** for v0.4.0 (covers all the new content)
- [x] **Tagged v0.4.0** and pushed to origin

## What's next (per BACKLOG.md)

The processkit-side roadmap continues with: BACK-002 remaining 15 primitive
schemas; BACK-003 MCP servers for the other process-primitive skills; BACK-001
three-level rewrite of 85 migrated skills; BACK-007 SQLite WAL mode; BACK-009
docs-site catalog refresh; BACK-005 FTS5 search.

The **aibox-side** work front (separate repo) is the in-flight consumption logic:
`[processkit]` section in `aibox.toml`, fetch + cache, manifest model, `aibox lint`,
migration document lifecycle. See aibox's `context/discussions/DISC-002-aibox-refocus.md`
§16 Phase 4.

See aibox's `context/discussions/DISC-002-aibox-refocus.md` for the full plan.
