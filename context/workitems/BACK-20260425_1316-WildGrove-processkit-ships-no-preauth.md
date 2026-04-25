---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260425_1316-WildGrove-processkit-ships-no-preauth
  created: '2026-04-25T13:16:20+00:00'
spec:
  title: processkit ships no preauth for MCP tools — derived projects re-prompt on
    every container rebuild
  state: backlog
  type: bug
  priority: high
  description: "## Symptom\n\nAfter a derived-project (e.g. aibox) devcontainer rebuild,\
    \ the user is re-prompted to authorize processkit MCP servers (e.g. workitem-management,\
    \ decision-record, task-router, etc.) on first use, even though the same authorizations\
    \ were granted in the prior container.\n\n## Root cause\n\nprocesskit ships **only**\
    \ the skill-gate hooks block in `.claude/settings.json`. It does NOT ship:\n\n\
    - `permissions.allow[]` — the per-tool allow list, and\n- `enabledMcpjsonServers[]`\
    \ — the list of pre-authorized `.mcp.json` servers.\n\nAs a result, the user's\
    \ allowlist is built up incrementally per-machine and lands in `.claude/settings.local.json`,\
    \ which:\n\n1. is `.gitignored` (`.gitignore` line: `.claude/settings.local.json`),\n\
    2. is NOT under the persistent `.aibox-home/` volume mount, and\n3. has no shipping/merger\
    \ mechanism via `aibox sync`.\n\nWhen the container is rebuilt, the only persistent\
    \ surfaces are the git-tracked tree (which has no preauth) and `.aibox-home/`\
    \ (which carries Claude Code's user-level state, but not the project-scoped permissions).\
    \ The local allowlist file is wiped, and the user re-authorizes from zero.\n\n\
    ## Evidence\n\n- `/workspace/.claude/settings.json` (committed): hooks block only,\
    \ no `permissions` key.\n- `/workspace/.claude/settings.local.json` (gitignored):\
    \ 100+ entries in `permissions.allow[]` plus 18 entries in `enabledMcpjsonServers[]`\
    \ for processkit servers.\n- `/workspace/src/context/skills/processkit/skill-gate/scripts/README.md`\
    \ \"Wiring targets for `aibox sync`\" section: documents only the hooks block;\
    \ never mentions a permissions/preauth block.\n- `command grep -rln '\"permissions\"\
    ' /workspace/src` returns zero hits — nothing in deliverables ships a permissions\
    \ JSON.\n\n## Proposed fix\n\nExtend the `_processkit_managed: true` block that\
    \ ships in `.claude/settings.json` (merged in by `aibox sync`) to include a known-good\
    \ preauth surface for processkit:\n\n```json\n{\n  \"permissions\": {\n    \"\
    allow\": [\n      \"mcp__processkit-task-router__route_task\",\n      \"mcp__processkit-skill-finder__find_skill\"\
    ,\n      \"mcp__processkit-skill-gate__acknowledge_contract\",\n      \"mcp__processkit-skill-gate__skip_decision_record\"\
    ,\n      \"mcp__processkit-index-management__query_entities\",\n      \"mcp__processkit-index-management__get_entity\"\
    ,\n      \"mcp__processkit-index-management__search_entities\",\n      \"mcp__processkit-event-log__recent_events\"\
    ,\n      \"mcp__processkit-event-log__query_events\",\n      \"mcp__processkit-workitem-management__query_workitems\"\
    ,\n      \"mcp__processkit-workitem-management__get_workitem\",\n      \"mcp__processkit-decision-record__query_decisions\"\
    ,\n      \"mcp__processkit-decision-record__get_decision\",\n      \"mcp__processkit-migration-management__list_migrations\"\
    ,\n      \"mcp__processkit-migration-management__get_migration\"\n    ]\n  },\n\
    \  \"enabledMcpjsonServers\": [\n    \"processkit-actor-profile\", \"processkit-artifact-management\"\
    ,\n    \"processkit-binding-management\", \"processkit-decision-record\",\n  \
    \  \"processkit-discussion-management\", \"processkit-event-log\",\n    \"processkit-gate-management\"\
    , \"processkit-id-management\",\n    \"processkit-index-management\", \"processkit-migration-management\"\
    ,\n    \"processkit-model-recommender\", \"processkit-role-management\",\n   \
    \ \"processkit-scope-management\", \"processkit-skill-finder\",\n    \"processkit-skill-gate\"\
    , \"processkit-task-router\",\n    \"processkit-team-manager\", \"processkit-workitem-management\"\
    \n  ]\n}\n```\n\n## Open scope questions\n\n1. **Read-only vs. write-side preauth.**\
    \ Read-side processkit tools (`query_*`, `get_*`, `list_*`) and the gate/router\
    \ tools are clearly safe to preauth. Write-side tools (`create_*`, `transition_*`,\
    \ `record_*`, `apply_*`) are already gated by the skill-gate `PreToolUse` hook,\
    \ so preauth would not bypass safety. Decision: ship preauth for ALL processkit\
    \ MCP tools.\n2. **`enabledMcpjsonServers` list** — should be auto-derived from\
    \ the shipped `.processkit-mcp-manifest.json` (already exists) at install time,\
    \ not hand-maintained.\n3. **Codex CLI parity** — does Codex have an equivalent\
    \ permissions surface? `.codex/hooks.json` only carries hooks. Investigate.\n\
    4. **Per-skill-config drift interaction (TrueQuail).** The `aibox installer reconcile\
    \ .mcp.json on per-skill-config drift` WorkItem (review) overlaps. The preauth\
    \ fix lands in `.claude/settings.json` (a different file), but both should be\
    \ merged by the same installer pass. Worth coordinating.\n\n## Acceptance\n\n\
    - After fresh container rebuild, user can call any processkit MCP tool (read or\
    \ write) with zero permission prompts.\n- `pk-doctor mcp_config_drift` continues\
    \ to pass.\n- The `enabledMcpjsonServers` list is sourced from a single source\
    \ of truth (the manifest), not duplicated."
---
