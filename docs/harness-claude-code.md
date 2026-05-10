# processkit on Claude Code — harness reference

This document captures how processkit surfaces itself inside the Claude
Code harness: which payloads land at session start vs. each turn, which
hooks fire, and which Claude Code settings we recommend for any
processkit project.

WorkItem: BACK-20260509_1317-DaringRaven (issue #19). Companion file:
[`harness-claude-code.settings.example.json`](harness-claude-code.settings.example.json).

## What the per-turn hook injects

`scripts/emit_compliance_contract.py` runs as **both** a `SessionStart`
and a `UserPromptSubmit` hook (wired in
`/workspace/.claude/settings.json` under `hooks.SessionStart` and
`hooks.UserPromptSubmit`). It now emits two different payloads:

- **SessionStart** — the *full* compliance contract from
  `context/skills/processkit/skill-gate/assets/compliance-contract.md`
  (~78 lines: 6 sections covering session start, sub-agent dispatch,
  tool routing, entity writes, decisions, prohibitions). One-shot per
  session.
- **UserPromptSubmit** — the *slim* per-turn checklist (~14 lines):
  3 positive actions (acknowledge, route, find skill), 3 prohibitions
  (no hand-edit / no `ls`/`grep` / no `templates/`), and a one-line
  pointer to the full contract. Runs on every prompt.

The single source of truth is still
`compliance-contract.md`. The slim payload is the block delimited by
`<!-- BEGIN HOOK -->` ... `<!-- END HOOK -->` markers in that file —
edit one file, both payloads update together. `_extract_hook_block()`
in `emit_compliance_contract.py` does the slicing.

If either marker is missing (e.g. partially-edited file), the slim
payload falls back to the full contract — safe by default.

## How to use the full contract

Three reliable ways to load the full contract on demand:

1. **Start a fresh session** — `SessionStart` hook injects the full
   text automatically.
2. **Read the file** —
   `context/skills/processkit/skill-gate/assets/compliance-contract.md`
   is plain Markdown, no preprocessing.
3. **Call the MCP tool** — `acknowledge_contract(version="v2")` returns
   the full contract text in its response (`contract` field).

Sub-agents dispatched mid-session inherit the parent's context — they
get the slim payload from the most recent `UserPromptSubmit` plus the
full text the parent loaded at SessionStart, so the catalogue is
already in scope.

## Recommended settings

See [`harness-claude-code.settings.example.json`](harness-claude-code.settings.example.json)
for a copy-paste block. Two recommendations:

### `skillOverrides` — name-only loading for verbose, rarely-used skills

The processkit ships ~30 skills under `context/skills/processkit/`.
Four of them are >400 lines and are creation/audit/setup skills, not
per-session workflow skills:

| Skill | Lines | When invoked |
|-------|-------|--------------|
| `skill-builder` | 514 | Authoring a new skill |
| `skill-reviewer` | 496 | Auditing an existing skill |
| `team-creator` | 445 | Bootstrapping or rebalancing a team |
| `agent-management` | 437 | Multi-agent orchestration setup |

Setting `skillOverrides.<name>.mode = "name-only"` for these tells
Claude Code to load a one-line description instead of the full
SKILL.md. The skill remains discoverable via `/pk-*` commands and
`find_skill`, and Claude Code loads the full body when the skill is
explicitly invoked.

Workflow-critical and routing skills (`model-recommender`,
`team-manager`, `skill-finder`, `skill-gate`) should stay fully loaded
— they are consulted by hooks and routing on most turns.

### `env.ENABLE_TOOL_SEARCH=auto` — defer tool schemas

processkit installs the `processkit-gateway` MCP server, which exposes
130+ tools. By default Claude Code embeds every tool's full JSONSchema
in the session prompt. `ENABLE_TOOL_SEARCH=auto` tells Claude Code to
hide tool schemas behind a `ToolSearch` tool until they are actually
needed, saving substantial per-turn tokens.

The trade-off is one extra round-trip the first time each tool is
called. With sticky caching (Claude Code 2.1+), the cost amortises
across the session.

## Sub-agent dispatch

When dispatching a sub-agent, follow `AGENTS.md` ➜ "Before sub-agent
dispatch":

1. Call `route_task(task_description)` to get
   `recommended_team_member_slug` and `recommended_model_class`.
2. Pass the slug as Claude Code's `subagent_type` so the harness loads
   the matching `.claude/agents/<slug>.md` adapter.
3. Pick the cheapest concrete model in the recommended class (Haiku <
   Sonnet < Opus). Do not let the sub-agent inherit the parent's
   model — that defeats the team-dispatch token-efficiency strategy.

The adapter file written by `team-manager.export_claude_subagent` is
self-describing as of DaringRaven (rec 6): it carries a header comment
with the TeamMember ID, slug, role, seniority, model policy, and
resolved binding so a reader can audit `.claude/agents/<slug>.md`
against the live roster without re-resolving.

## Verification

`pk-doctor` covers this surface with two checks:

- **`preauth_applied`** — confirms the processkit MCP-tool allowlist
  is preauthorised in `.claude/settings.json` so MCP calls don't
  prompt mid-turn.
- **`team_member_exports`** — reconciles active TeamMembers against
  `.claude/agents/<slug>.md` adapter files. Detects stale or missing
  exports.

Run `/pk-doctor` for a full report. To smoke-test the hook payload
without restarting:

```sh
echo '{"hook_event_name":"UserPromptSubmit"}' | \
  python3 context/skills/processkit/skill-gate/scripts/emit_compliance_contract.py
```

Should emit the slim ~14-line payload. Same with
`hook_event_name=SessionStart` should emit the full contract.

The hook-script tests live in
`context/skills/processkit/skill-gate/scripts/test_hooks.py` (run with
`python3 ...` — no extra deps). Tests `[2c]` and `[2d]` cover the
slim/full split.

## Common MCP calls + Claude Code shortcuts (v0.26.0)

### Top-N gateway tools

The `processkit-gateway` aggregator exposes all processkit MCP tools
through a single server. The most frequently needed calls:

| Goal | Tool | Notes |
|------|------|-------|
| Read entity by ID | `get_entity(id=...)` | Accepts prefix, word-pair, or full ID |
| Read entity by path | `get_entity_by_path(path=...)` | Path relative to project root |
| List entities | `list_entities(kind?, state?, limit?)` | All kinds; v1-penalty annotated |
| Search entities | `search_entities(text)` / `hybrid_search_entities(text)` | FTS + semantic |
| Create work item | `create_workitem(...)` | Route first via `route_task` |
| Transition state | `transition_workitem(id, to_state)` | Enforces state machine |
| Run health check | `run_pk_doctor(check?, fix?)` | Returns structured JSON |
| Run release audit | `run_pk_release_audit(tree?)` | Returns structured JSON |
| Route a task | `route_task(task_description=...)` | Required before write calls + Agent dispatch |

### ToolSearch friction

With `ENABLE_TOOL_SEARCH=auto`, tool schemas are deferred. You must call
`ToolSearch(query="select:<tool_name>")` before invoking a deferred tool.
Common selects:

```
ToolSearch(query="select:mcp__processkit-gateway__get_entity,mcp__processkit-gateway__route_task")
ToolSearch(query="select:mcp__processkit-gateway__create_workitem,mcp__processkit-gateway__transition_workitem")
```

### Recommended `enabledMcpjsonServers`

Only `processkit-gateway` needs to be in `enabledMcpjsonServers`. The
gateway proxies all other processkit MCP servers without requiring each
one to be individually listed.

```json
{ "enabledMcpjsonServers": ["processkit-gateway"] }
```

### Entity-read BLOCK behavior (v0.26.0)

A new `check_entity_read.py` PreToolUse hook **blocks** `Read` on
canonical entity paths:

```
context/{workitems,decisions,artifacts,team-members,scopes,
          gates,actors,roles,bindings}/**/*.md
```

**Blocked** → use `get_entity(id='...')` or `get_entity_by_path(path='...')`.

**Not blocked** (gray area): skill source code under
`context/skills/<skill>/`, log entries, schemas, applied migrations,
TeamMember sub-files (`persona.md`, `card.json`, `knowledge/`, etc.),
and anything outside `context/`.

If you see `BLOCKED: <path> is a canonical entity file`, the remediation
is always one of:

```python
get_entity(id="<derived-id>")            # by ID
get_entity_by_path(path="<rel-path>")    # by path
list_entities(kind="WorkItem", state="open")  # browse
search_entities(text="<keyword>")        # search
```

### Agent dispatch validation (v0.26.0)

A new `check_route_task_before_agent.py` PreToolUse hook **blocks**
`Agent` and `Task` dispatch without a prior `route_task` call in the
same turn.

Correct pattern:
```python
route = route_task(task_description="summarise the release notes")
# read route["recommended_team_member_slug"] and route["recommended_model_class"]
Agent(prompt="...", model="<recommended model>")
```

If the `context/.state/skill-gate/` directory does not exist (first run
before any processkit MCP call), the hook **warns but does not block**
(graceful degradation).

## Open items

- `.claude/settings.example.json` was the natural home for the
  recommended-settings JSON, but the harness sandbox currently blocks
  unattended writes under `.claude/`. The file lives at
  `docs/harness-claude-code.settings.example.json` instead and must be
  copied into `.claude/settings.json` (or the user-level config) by
  hand. If/when sandbox policy permits, the canonical location is
  `.claude/settings.example.json`.
- `skillOverrides` schema validation: Claude Code accepts the
  `name-only` mode but the project hasn't yet wired schema acceptance
  into `pk-doctor`. Track in a follow-up if drift is observed.
