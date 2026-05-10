---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260510_0758-FierceFern-mcp-gateway-adoption-ux-defaults-for
  created: '2026-05-10T07:58:21+00:00'
spec:
  title: MCP gateway adoption — UX defaults for v0.26.0 integration
  state: accepted
  decision: |
    Ship four UX defaults in v0.26.0 to close the gap between the v2 compliance contract and observed agent behavior:

    1. **PreToolUse Read hook**: BLOCK Read for paths matching `context/{workitems,decisions,artifacts,team-members,scopes,gates,actors,roles,bindings}/*.md` (canonical entity dirs). WARN-only for grayer paths (`logs/`, `schemas/`, `migrations/applied/`, `team-members/<slug>/{persona.md,card.json,knowledge/,journal/,...}` non-entity sub-files).

    2. **`create_team_member` always auto-scaffolds**: 6 tier subdirs (`knowledge/`, `journal/`, `skills/`, `relations/`, `lessons/`, `private/`) each with `.gitkeep`, plus `card.json` and `persona.md` templates rendered from the TeamMember spec. No opt-out parameter.

    3. **`run_pk_doctor` and `run_pk_release_audit` MCP wrappers return structured JSON**: `{findings: [...], totals: {error, warn, info}, exit_code}`. doctor.py and release_audit.py grow a `--json` flag if not already present; the MCP wrapper invokes the script and parses.

    4. **Subagent dispatch enforcement is strengthened by hook, not by a new slash command**: PreToolUse hook on the `Agent` tool validates that a `route_task` call happened earlier in the same turn (per-turn-state in `context/.state/skill-gate/`). Bare-model dispatch fails the hook. No `/pk-dispatch` command in v0.26.0.
  context: 'Session 2026-05-10 surfaced systematic regression: even with the v2 contract
    directing agents to use index-management for entity reads and route_task before
    write-side ops, agents (including this session''s main agent) defaulted to Read/find/grep/Edit
    on context/ paths. Root causes: tool-default bias, real gateway coverage gaps,
    hook becomes background noise, knowing the file path defeats the gateway. WorkItem
    BACK-TallFern enumerates the gaps; these four decisions set the UX defaults for
    the implementation.'
  rationale: |
    - Choice 1 (BLOCK strict, WARN lenient): WARN alone reproduces the failure mode we observed (background noise). Full BLOCK risks edge cases. Strict-on-canonical + WARN-on-gray is the compromise that preserves high-value enforcement without breaking grayer reads (logs and applied migrations are append-only and frequently scanned for context).
    - Choice 2 (always auto-scaffold): Closes the team_consistency.tier_missing class of bug at source. Cost is a few empty dirs; benefit is no derived project ever lands a half-formed TeamMember entity again.
    - Choice 3 (structured JSON): Enables agents to iterate, filter, and route audit findings to other MCP calls. Raw text would force re-parsing.
    - Choice 4 (hook over slash command): Same enforcement bar via lower surface area; no new entry point for users to learn. /pk-dispatch can ship in v0.27 if the hook proves insufficient.
  alternatives:
  - option: WARN-only Read hook
    reason_rejected: reproduces background-noise failure mode
  - option: Full BLOCK on all context/ Read
    reason_rejected: edge cases (logs, migrations/applied) need ad-hoc scan access
  - option: create_team_member opt-in scaffold
    reason_rejected: callers forget; bug recurs
  - option: /pk-dispatch slash command
    reason_rejected: extra surface for same enforcement; defer until proven necessary
  consequences: |
    - v0.26.0 release blocks until SUB-1..SUB-5 land
    - Derived projects on v0.26.0 will see Read fail on canonical entity paths — needs a clear migration note in the v0.26.0 release notes ("if your scripts cat or grep entity files, replace with get_entity / list_entities / search_entities")
    - pk-doctor and release-audit gain --json flags; existing text output preserved as default for human invocation
  deciders:
  - TEAMMEMBER-thrifty-otter
  related_workitems:
  - BACK-20260510_0751-TallFern-mcp-gateway-adoption-close-usage-gaps
  decided_at: '2026-05-10T07:58:21+00:00'
---
