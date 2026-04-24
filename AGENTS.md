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
- Status briefing / standup / wrap-up → `status-briefing` /
  `standup-context` / `session-handover`.
- Retro / retrospective / post-release review / post-mortem →
  `retrospective` skill (`/pk-retro`).
- Any domain-specific task (PRD, audit, research ingest, discussion,
  backlog add) → `find_skill` first; see the six mandatory skill-check
  classes in `skill-gate/SKILL.md`.
- Otherwise → browse `context/skills/INDEX.md` before falling back to
  general knowledge.

## Sub-agent delegation

Harness `Agent`-tool sub-agents inherit the main session's permission
policy but run ephemerally — any unallowed tool call errors
immediately rather than prompting. Delegate **read-only** work to
sub-agents (Read, search Bash, MCP `query_*` / `get_*` / `search_*` /
`list_*`); keep **mutating** work on the main session (Write, Edit,
new `mkdir`, MCP `create_*` / `transition_*` / `record_*` / `link_*`
/ `open_*` / `log_event`, `git` mutations). A sub-agent permission
block is not a cue to broaden the allowlist — move the write back to
main.

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

51-role catalog under `context/roles/`, with **pure-ordinal seniority**
(`junior → specialist → expert → senior → principal`). Persistent
identities live as **TeamMembers** under `context/team-members/<slug>/`
(directory tree: persona + A2A card + tiered memory). Ad-hoc
invocations are ephemeral `(role, seniority)` dispatches resolved via
`model-recommender.resolve_model` against `model-assignment` bindings.

Charters: `DEC-20260422_0233-SpryTulip` (team-member model + memory),
`DEC-20260422_0234-BraveFalcon` (role catalog + seniority),
`DEC-20260422_0234-LoyalComet` (model artifacts + binding routing).
See [`context/team/roster.md`](context/team/roster.md) and
[`context/skills/processkit/team-manager/SKILL.md`](context/skills/processkit/team-manager/SKILL.md).

## Project-specific notes

- Required MCP servers: `index-management`, `id-management`,
  `workitem-management`, `discussion-management`, `decision-record`,
  `event-log`, `skill-finder`, `task-router`.
- Never edit `.devcontainer/Dockerfile`; use `Dockerfile.local`.
- `apiVersion` locked through v1.x; `v2` requires a full migration.
- `_find_lib()` uses cwd; smoke tests `os.chdir()` before invoking servers.

## MCP config manifest

`context/.processkit-mcp-manifest.json` records a sha256 per
`context/skills/*/*/mcp/mcp-config.json` plus an `aggregate_sha256` over
all of them. It is regenerated at release time by
`scripts/generate-mcp-manifest.py` and mirrored into
`src/context/` so consumers receive it in the release tarball.
Downstream installers (notably `aibox sync`) are expected to compare the
aggregate hash against their last-merged state and re-merge `.mcp.json`
when they differ — independently of whether the processkit version
changed. Without this signal, per-skill MCP-config edits made within a
release cycle never reach derived projects until the next version bump.
Tracking issue: [projectious-work/aibox#54](https://github.com/projectious-work/aibox/issues/54).
The `mcp_config_drift` pk-doctor check validates the manifest locally.

---

<sub>Scaffolded by processkit `v0.18.1` on `2026-04-17`. Re-rendered on each installer sync.</sub>
