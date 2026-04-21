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

<!-- PLACEHOLDER:PROJECT_DESCRIPTION class=B
     One paragraph: what {{PROJECT_NAME}} does, who it is for, and what
     success looks like. Anything longer belongs in README.md. -->
{{PROJECT_DESCRIPTION}}

Run `pk-resume` before acting. Provider-specific files (`CLAUDE.md`,
`CODEX.md`, `.cursor/rules`, …) are thin pointers — edit **this** file.

## First-time setup (delete once done)

This file ships from
[processkit](https://github.com/projectious-work/processkit) as a
template. Scan for `{{TOKEN}}` strings and `<!-- PLACEHOLDER:TOKEN
class=X -->` comments, then follow the matching protocol below. Delete
this entire section once every placeholder is filled in.

| Class | Source | What you do |
|---|---|---|
| **A — installer** | Installer substitutes at render time (`{{PROJECT_NAME}}`, `{{PROCESSKIT_VERSION}}`). | If still literal, read `aibox.toml` or ask the owner. |
| **B — owner** | Owner-only info: description, conventions, gotchas. | Interview the owner one question at a time. |
| **C — discoverable** | Build/test/lint commands from `package.json` / `Makefile` / `pyproject.toml` / etc. | Propose a value, owner confirms, write it in. |

Unannotated placeholders default to **Class B**.

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
- Status briefing / standup / wrap-up → `status-briefing` /
  `standup-context` / `session-handover`.
- Retro / retrospective / post-release review / post-mortem →
  `retrospective` skill (`/pk-retro`).
- Any domain-specific task (PRD, audit, research ingest, discussion,
  backlog add) → `find_skill` first; see the six mandatory skill-check
  classes in `skill-gate/SKILL.md`.
- Otherwise → browse `context/skills/INDEX.md` before falling back to
  general knowledge.

## Setup

<!-- PLACEHOLDER:BUILD_COMMAND class=C -->
<!-- PLACEHOLDER:TEST_COMMAND class=C -->
<!-- PLACEHOLDER:LINT_COMMAND class=C -->

```sh
{{BUILD_COMMAND}}
{{TEST_COMMAND}}
{{LINT_COMMAND}}
```

<!-- pk-commands BEGIN -->
<!--
build: "{{BUILD_COMMAND}}"
test: "{{TEST_COMMAND}}"
lint: "{{LINT_COMMAND}}"
fmt: ""
typecheck: ""
-->
<!-- pk-commands END -->

## Code style & PRs

<!-- PLACEHOLDER:CODE_STYLE_NOTES class=B -->
<!-- PLACEHOLDER:PR_CONVENTIONS class=B -->
{{CODE_STYLE_NOTES}}
{{PR_CONVENTIONS}}

## processkit preferences

Runtime config lives in per-skill `context/skills/<name>/config/settings.toml`.
MCP servers read them on every call — no restart needed.
<!-- PLACEHOLDER:PROCESSKIT_PREFS class=B -->
{{PROCESSKIT_PREFS}}

## AI agents on this project

Configured providers: **{{AI_PROVIDERS}}**. Coordinate via the entity
layer (`workitem-management`, `event-log`, `discussion-management`)
rather than assuming you are alone.

## Project-specific notes

<!-- PLACEHOLDER:NONOBVIOUS_GOTCHAS class=B -->
{{NONOBVIOUS_GOTCHAS}}

---

<sub>Scaffolded by processkit `{{PROCESSKIT_VERSION}}` on `{{INSTALL_DATE}}`. Re-rendered on each installer sync.</sub>
