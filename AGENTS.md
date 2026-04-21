# AGENTS.md

<!-- pk-compliance-contract v2 BEGIN -->
<!-- pk-compliance v2 -->

## processkit Compliance Contract (ToC)

Ten non-negotiables — full text in
[`context/skills/processkit/skill-gate/SKILL.md`](context/skills/processkit/skill-gate/SKILL.md):
(1) `route_task` before writes; (2) 1% skill-finder rule; (3) commit
to entity creation same turn; (4) write via MCP, never hand-edit
`context/` YAML; (5) read via `index-management`; (6) log events for
non-MCP state changes; (7) record accepted cross-cutting decisions;
(8) acknowledge user decision language (`record_decision` or
`skip_decision_record`); (9) `context/templates/` is read-only;
(10) never hand-edit merged harness MCP config.
<!-- pk-compliance-contract v2 END -->

## About & session start

processkit is a versioned, provider-neutral library of process
primitives, skills, and MCP servers consumed by aibox and dogfooded
here. Run `pk-resume` before acting. Provider-specific files
(`CLAUDE.md`, `CODEX.md`, `.cursor/rules`) are thin pointers — edit
**this** file.

## Skill guards (if/then)

- Editing/creating a file under `context/` → call `find_skill`; never
  hand-edit entity YAML.
- Creating or transitioning any entity (WorkItem, Decision, Note,
  Artifact, Discussion, Scope, Gate, Binding) → use the relevant
  `*-management` MCP tool.
- Pending migration under `context/migrations/pending/` → use
  `migration-management` MCP; don't move files by hand.
- Cross-cutting recommendation accepted → `record_decision` or
  `skip_decision_record(reason=...)` same turn.
- Authoring/reviewing a skill → `skill-builder` / `skill-reviewer`.
- Morning brief / standup / wrap-up → `morning-briefing` /
  `standup-context` / `session-handover`.
- Any domain-specific task (PRD, audit, research ingest, discussion,
  backlog add) → `find_skill` first; see the six mandatory skill-check
  classes in `skill-gate/SKILL.md`.
- Otherwise → browse `context/skills/INDEX.md` before falling back to
  general knowledge.

## Setup

```sh
npm --prefix docs-site install && npm --prefix docs-site run build
uv run scripts/smoke-test-servers.py
```

<!-- pk-commands BEGIN -->
<!--
build: "npm --prefix docs-site run build"
test: "uv run scripts/smoke-test-servers.py"
lint: ""
fmt: ""
typecheck: ""
-->
<!-- pk-commands END -->

## Code style & PRs

Hard-wrap Markdown/Python/YAML at 80 cols (exempt: tables, URLs,
frontmatter, code fences). Conventional Commits; never `--no-verify`.
`src/` ships to consumers, `context/` is local — never mix. Preferences
live in per-skill `context/skills/<name>/config/settings.toml`. PRs:
link WorkItem ID, squash-merge, green tests before merge.

## Team

Eight-role AI team defined under `context/roles/`, `context/actors/`,
`context/bindings/`. PM (`ACTOR-pm-claude`, Opus) is the default session
agent. Charter: `DEC-20260414_0900-TeamRoster-permanent-ai-team-composition`.
See [`context/team/roster.md`](context/team/roster.md).

## Project-specific notes

- Required MCP servers: `index-management`, `id-management`,
  `workitem-management`, `discussion-management`, `decision-record`,
  `event-log`, `skill-finder`, `task-router`.
- Never edit `.devcontainer/Dockerfile`; use `Dockerfile.local`.
- `apiVersion` locked through v1.x; `v2` requires a full migration.
- `_find_lib()` uses cwd; smoke tests `os.chdir()` before invoking servers.

---

<sub>Scaffolded by processkit `v0.18.1` on `2026-04-17`. Re-rendered on each installer sync.</sub>
