---
updated: 2026-04-09
processkit: v0.7.0
---

# processkit dev session handover

Quick-start for any new agent (or human) picking up processkit development.

## Current state

**v0.7.0 shipped 2026-04-09.** All changes are committed, tagged, pushed, and
released as a tarball at github.com/projectious-work/processkit/releases/tag/v0.7.0.

What landed in v0.7.0:
- **Skill commands convention** — skills declare user-invocable slash commands via
  `metadata.processkit.commands`; adapter files live at `commands/<skill>-<workflow>.md`.
  Provider-neutral intent in frontmatter, Claude-specific adapter in `commands/`.
  See `src/skills/FORMAT.md` → `### commands/` for the full spec.
- **23 commands across 13 skills** wired up (session-handover, standup-context,
  morning-briefing, context-grooming, skill-builder, skill-reviewer,
  research-with-confidence, decision-record, workitem-management, release-semver,
  note-management, model-recommender, owner-profiling).
- **MCP tool annotations** — all 62 tools across all 12 MCP servers now carry
  `readOnlyHint`, `destructiveHint`, `idempotentHint`, `openWorldHint`.
- **model-recommender skill** — spider-chart AI model profiles and task-plan
  routing; 34-model roster; MCP server with 8 tools; 4 commands.
- **skill-reviewer** now has 11 review categories (was 8): Category 10 (command
  adapter hygiene) and Category 11 (security & permission audit).
- **skill-builder** has a new Step 8 (command adapter creation) and MCP
  annotation rules.

## The non-negotiable principles

When a design call is ambiguous, pick the option that respects more of these:

1. **Provider neutrality.** No path/config/binary is bound to a specific AI
   provider. `AGENTS.md` is canonical; `CLAUDE.md` is a thin pointer.
5. **Forkability.** All upstream references go through `[processkit].source`.
   One config line to switch to a fork.
7. **Provider-neutral install destinations.** `context/skills/`,
   `context/schemas/`, `context/state-machines/`. Agent-discoverable via
   plain filesystem walk.

## Collaboration notes

These are non-obvious preferences that took time to learn — save a new agent
the discovery cost:

- **Provider-independence is a hard constraint**, not a preference. When
  something is Claude-specific (command adapter format, `argument-hint`
  frontmatter), name it as such and scope it to the appropriate layer —
  don't try to make it neutral by renaming it.
- **Propose before executing on large sweeps.** For catalog-wide changes
  (e.g. the annotation audit, command wiring), present the plan and get
  confirmation before launching parallel agents. The user decides scope.
- **Parallel agents are welcome** for independent file edits — confirmed
  to work well in practice. Use them for batching similar mechanical work.
- **The user thinks in systems.** Rationale matters as much as the change.
  Explain the design principle, not just what you did.
