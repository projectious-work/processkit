---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260510_0751-TallFern-mcp-gateway-adoption-close-usage-gaps
  created: '2026-05-10T07:51:51+00:00'
  labels:
    release: v0.26.0
    cluster: agent-dispatch
    harness: claude-code
  updated: '2026-05-10T08:43:38+00:00'
spec:
  title: 'MCP gateway adoption: close usage gaps so Claude Code agents default to
    gateway over direct file ops'
  state: done
  type: epic
  priority: high
  description: |
    ## Problem

    Even with the v2 compliance contract (PR #24, NobleLeaf) explicitly directing agents to use index-management for entity reads and route_task before write-side ops, this session's tool log shows systematic regression to direct file ops:

    - `Read /workspace/context/team-members/finn/team-member.md` instead of `get_team_member(slug='finn')`
    - `Read /workspace/context/migrations/applied/MIG-LOCK-*.md` instead of `get_migration(id=...)`
    - `find context/team-members -maxdepth 1 -type d` instead of `list_team_members`
    - `ls context/team-members/finn/` (direct contract violation)
    - Edit on `context/schemas/migration.yaml` (no MCP equivalent exists)
    - `uv run context/skills/processkit/pk-doctor/scripts/doctor.py` instead of an MCP wrapper

    Root causes:
    1. Tool-default bias: Bash/Read/Edit are top-level; MCP needs ToolSearch first
    2. Real gaps in gateway coverage (schema editing, script wrappers, scaffolding)
    3. Compliance hook becomes background noise after acknowledge_contract
    4. Knowing the file path defeats the gateway (Read is one call vs route_task → get_entity)
    5. Subagents inherit the parent agent's pattern

    ## Cost
    - Bypasses index re-validate that get_entity runs
    - Skips routing telemetry (route_task dataset thins)
    - Drift between contract and behavior (the very failure mode of gh#17/#18/#19)

    ## Scope (Tier 1 — close real gaps with new tools)

    1. **`get_entity_by_path(path)`** in index-management — single tool that takes a relative path and dispatches to the right `get_*`. Removes the ID-vs-path mental overhead.
    2. **`list_entities(kind, state=None, limit=50)`** in index-management — unified listing across kinds; replaces per-kind `list_*` shortcuts.
    3. **`run_pk_doctor(check=None, fix=None)`** in pk-doctor — MCP wrapper around doctor.py returning structured JSON findings; agent-friendly iteration.
    4. **`run_pk_release_audit(tree=None)`** in release-audit — same wrapper pattern.
    5. **`create_team_member` auto-scaffolds**: 6 tier subdirs (knowledge/journal/skills/relations/lessons/private with .gitkeep) + card.json template + persona.md template. Closes the team_consistency.tier_missing class of bug at source (the bug we just patched).

    ## Scope (Tier 2 — Claude Code harness improvements)

    6. **PreToolUse hook on Read for `context/<entity-dir>/*.md`** — intercept and emit nudge ("use get_entity instead, route_task → get_entity is one extra call"). Decision needed: BLOCK or WARN.
    7. **PreToolUse hook on Bash for `find|grep|ls|cat` patterns over `context/`** — same nudge pattern.
    8. **SessionStart preload of common gateway tools** — eliminate ToolSearch friction for the top-N tools (acknowledge_contract, route_task, find_skill, get_*, list_*, create_*).
    9. **Subagent template** that auto-includes contract reminders + route_task handshake.

    ## Scope (Tier 3 — workflow / docs)

    10. compliance-contract.md: add "Preferred MCP entry points by task type" reference table.
    11. compliance-contract.md: explicit "Read is OK for non-entity files" clarification (skill code, configs, docs).
    12. docs/harness-claude-code.md: section on common MCP calls + Claude Code shortcuts; document the pre-loading recipe.

    ## Deliverable surface (src/)

    All Tier 1 tools ship in their respective skill MCP servers (mirrored to src/context/...).
    Tier 2 hooks ship as additions to .claude/settings.json template + hook scripts under skill-gate.
    Tier 3 docs ship in compliance-contract.md and docs/harness-claude-code.md.

    ## Target release
    v0.26.0 (not yet tagged). This work integrates into the release before tagging.

    ## Sub-WorkItems (to be split during implementation)
    - SUB-1: index-management — get_entity_by_path + list_entities
    - SUB-2: pk-doctor + release-audit MCP wrappers
    - SUB-3: team-manager — create_team_member auto-scaffold
    - SUB-4: skill-gate — PreToolUse Read/Bash hooks (gated on architectural answers)
    - SUB-5: docs + contract updates

    ## Architectural questions outstanding
    See AskUserQuestion.
  started_at: '2026-05-10T07:58:28+00:00'
  completed_at: '2026-05-10T08:43:38+00:00'
---

## Transition note (2026-05-10T07:58:28+00:00)

Architectural decisions accepted by owner via AskUserQuestion. DEC-20260510_0758-FierceFern recorded. Dispatching Sonnet senior software-engineer to implement Tier 1 + Tier 2 + Tier 3 in a single coordinated branch for v0.26.0 integration.


## Transition note (2026-05-10T08:18:35+00:00)

Branch feat/v0.26.0-mcp-gateway-adoption pushed. 5 commits: T1.1 get_entity_by_path, T1.2 list_entities, T1.3 run_pk_doctor MCP wrapper + --json flag, T1.4 run_pk_release_audit MCP wrapper + --json flag, T1.5 create_team_member auto-scaffold, T2.1 check_entity_read.py PreToolUse BLOCK hook, T2.2 check_route_task_before_agent.py PreToolUse BLOCK hook + route_task marker writing, T3.1 compliance-contract MCP entry points table + Read clarification, T3.2 harness-claude-code.md adoption guide. Tests: 9 index-management + 20+22 doctor/audit + 44 hook assertions + 97 team-manager all green. Doctor: 0E/0W/21I. Release-audit: 0E/0W. Do not open PR — Cora reviews.


## Transition note (2026-05-10T08:43:38+00:00)

DeepFinch (Sonnet) shipped Tier 1 + Tier 2 + Tier 3 in 5 commits. PR #38 merged to main (commit 817a9d1). Audits remain GREEN: pk-doctor 0E/0W/21I, release-audit 0E/0W/1461I.
