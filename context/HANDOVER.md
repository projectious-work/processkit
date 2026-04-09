---
updated: 2026-04-09
processkit: v0.7.0
---

# processkit dev session handover

Quick-start for any new agent (or human) picking up processkit development.
Read this, then `AGENTS.md`, then dig into specific files as the work demands.

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

## First things after aibox reset + init

1. **Bump the processkit pin** in `aibox.toml` from `v0.5.1` to `v0.7.0` and
   run `aibox sync` so the installed `context/` reflects the current release.
2. **Smoke-test** the MCP servers: `uv run scripts/smoke-test-servers.py`.
3. The model-recommender MCP server has a separate dependency (`httpx`) —
   it is self-contained via PEP 723 inline deps and needs no extra setup.

## Open issues and next priorities

| Item | Tracker | Notes |
|---|---|---|
| Command registration automation | projectious-work/aibox#37 | aibox sync should walk `context/skills/*/commands/*.md` and copy to `.claude/commands/`; Claude-specific for now, provider-neutral-ready |
| Privacy tier model | projectious-work/processkit#1 | `metadata.privacy` frontmatter, docs-site filtering, per-user private dirs; `.gitignore` rule landed in aibox v0.16.3 (DEC-030) |
| Drop single-file Markdown skill track | no ticket | backlog-context, decisions-adr, context-archiving are legacy; entity-sharded track with MCP servers is the intended future |
| model-recommender roster validation | no ticket | 9 estimated models (post Aug-2025) need Workflow C (Roster Refresh) to validate scores against live benchmarks |
| Narrative profiles for new models | no ticket | `references/model-profiles.md` covers 12 of 34 models; 22 added later have no narrative profile yet |

## Key architectural decisions made this session

**Commands live under skills, not as a separate top-level entity.** Same
reasoning as MCP servers: the skill is the domain authority. The command is a
projection of the skill, not an independent entity. `commands/` adapter files
are install-time artifacts (same as `mcp/mcp-config.json`), not runtime reads.

**`metadata.processkit.commands` is provider-neutral; adapter files are not.**
The intent (`commands:` list with `name`, `args`, `description`) is in
processkit schema. The Claude-specific frontmatter (`argument-hint`,
`allowed-tools`) lives only in `commands/*.md`. Other harnesses will have their
own adapter format.

**Command naming is namespaced** (`<skill-name>-<workflow>`, never just
`<workflow>`). Collision avoidance when all commands land in `.claude/commands/`.

**MCP tool annotations are mandatory, not optional.** Missing annotations are a
must-fix in skill-reviewer Category 11. The harness cannot surface confirmation
prompts for destructive tools without them.

**skill is the leading entity overall** — MCP servers under skills, commands
under skills. Nothing stands alone outside a skill.

## The 7 non-negotiable principles

When a design call is ambiguous, pick the option that respects more of these:

1. **Provider neutrality.** No path/config/binary is bound to a specific AI
   provider. `AGENTS.md` is canonical; `CLAUDE.md` is a thin pointer.
2. **Reproducibility.** Every consumed processkit release is pinned by
   `(source, version, sha256)` in `aibox.lock`.
3. **Locality.** Everything a project needs lives inside the project dir.
   No external state, no central registry.
4. **Edit-in-place.** Installed content is editable directly. No override
   locations, no rebase ritual.
5. **Forkability.** All upstream references go through `[processkit].source`.
   One config line to switch to a fork.
6. **Single source of truth.** Skills/primitives/processes → processkit.
   Container/addons/install pipeline → aibox. No duplicates.
7. **Provider-neutral install destinations.** `context/skills/`,
   `context/schemas/`, `context/state-machines/`. Agent-discoverable via
   plain filesystem walk.

## Collaboration notes

These are non-obvious preferences that took time to learn — save a new agent
the discovery cost:

- **Terse responses.** No trailing "here's what I did" summaries after edits.
  The diff speaks for itself.
- **No trailing emoji** unless explicitly requested.
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
