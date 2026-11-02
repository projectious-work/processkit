---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260425_1316-WildGrove-processkit-ships-no-preauth
  created: '2026-04-25T13:16:20+00:00'
  updated: '2026-04-26T12:05:24+00:00'
spec:
  title: processkit ships no preauth for MCP tools — derived projects re-prompt on
    every container rebuild
  state: done
  type: bug
  priority: high
  description: |
    ## Symptom

    After a derived-project (e.g. aibox) devcontainer rebuild, the user is re-prompted to authorize processkit MCP servers (e.g. workitem-management, decision-record, task-router, etc.) on first use, even though the same authorizations were granted in the prior container.

    ## Root cause

    processkit ships **only** the skill-gate hooks block in `.claude/settings.json`. It does NOT ship:

    - `permissions.allow[]` — the per-tool allow list, and
    - `enabledMcpjsonServers[]` — the list of pre-authorized `.mcp.json` servers.

    As a result, the user's allowlist is built up incrementally per-machine and lands in `.claude/settings.local.json`, which:

    1. is `.gitignored` (`.gitignore` line: `.claude/settings.local.json`),
    2. is NOT under the persistent `.aibox-home/` volume mount, and
    3. has no shipping/merger mechanism via `aibox sync`.

    When the container is rebuilt, the only persistent surfaces are the git-tracked tree (which has no preauth) and `.aibox-home/` (which carries Claude Code's user-level state, but not the project-scoped permissions). The local allowlist file is wiped, and the user re-authorizes from zero.

    ## Evidence

    - `/workspace/.claude/settings.json` (committed): hooks block only, no `permissions` key.
    - `/workspace/.claude/settings.local.json` (gitignored): 100+ entries in `permissions.allow[]` plus 18 entries in `enabledMcpjsonServers[]` for processkit servers.
    - `/workspace/src/context/skills/processkit/skill-gate/scripts/README.md` "Wiring targets for `aibox sync`" section: documents only the hooks block; never mentions a permissions/preauth block.
    - `command grep -rln '"permissions"' /workspace/src` returns zero hits — nothing in deliverables ships a permissions JSON.

    ## Proposed fix

    Extend the `_processkit_managed: true` block that ships in `.claude/settings.json` (merged in by `aibox sync`) to include a known-good preauth surface for processkit:

    ```json
    {
      "permissions": {
        "allow": [
          "mcp__processkit-task-router__route_task",
          "mcp__processkit-skill-finder__find_skill",
          "mcp__processkit-skill-gate__acknowledge_contract",
          "mcp__processkit-skill-gate__skip_decision_record",
          "mcp__processkit-index-management__query_entities",
          "mcp__processkit-index-management__get_entity",
          "mcp__processkit-index-management__search_entities",
          "mcp__processkit-event-log__recent_events",
          "mcp__processkit-event-log__query_events",
          "mcp__processkit-workitem-management__query_workitems",
          "mcp__processkit-workitem-management__get_workitem",
          "mcp__processkit-decision-record__query_decisions",
          "mcp__processkit-decision-record__get_decision",
          "mcp__processkit-migration-management__list_migrations",
          "mcp__processkit-migration-management__get_migration"
        ]
      },
      "enabledMcpjsonServers": [
        "processkit-actor-profile", "processkit-artifact-management",
        "processkit-binding-management", "processkit-decision-record",
        "processkit-discussion-management", "processkit-event-log",
        "processkit-gate-management", "processkit-id-management",
        "processkit-index-management", "processkit-migration-management",
        "processkit-model-recommender", "processkit-role-management",
        "processkit-scope-management", "processkit-skill-finder",
        "processkit-skill-gate", "processkit-task-router",
        "processkit-team-manager", "processkit-workitem-management"
      ]
    }
    ```

    ## Open scope questions

    1. **Read-only vs. write-side preauth.** Read-side processkit tools (`query_*`, `get_*`, `list_*`) and the gate/router tools are clearly safe to preauth. Write-side tools (`create_*`, `transition_*`, `record_*`, `apply_*`) are already gated by the skill-gate `PreToolUse` hook, so preauth would not bypass safety. Decision: ship preauth for ALL processkit MCP tools.
    2. **`enabledMcpjsonServers` list** — should be auto-derived from the shipped `.processkit-mcp-manifest.json` (already exists) at install time, not hand-maintained.
    3. **Codex CLI parity** — does Codex have an equivalent permissions surface? `.codex/hooks.json` only carries hooks. Investigate.
    4. **Per-skill-config drift interaction (TrueQuail).** The `aibox installer reconcile .mcp.json on per-skill-config drift` WorkItem (review) overlaps. The preauth fix lands in `.claude/settings.json` (a different file), but both should be merged by the same installer pass. Worth coordinating.

    ## Acceptance

    - After fresh container rebuild, user can call any processkit MCP tool (read or write) with zero permission prompts.
    - `pk-doctor mcp_config_drift` continues to pass.
    - The `enabledMcpjsonServers` list is sourced from a single source of truth (the manifest), not duplicated.
  started_at: '2026-04-25T17:17:16+00:00'
  completed_at: '2026-04-26T12:05:24+00:00'
---

## Transition note (2026-04-26T12:05:20+00:00)

Phase B landed in aibox v0.20.0: .claude/settings.json now contains the preauth merge from context/skills/processkit/skill-gate/assets/preauth.json (18 mcp__processkit-* allow patterns + 18 enabledMcpjsonServers + _processkit_managed_keys block). pk-doctor preauth_applied check: 0 ERROR / 0 WARN / 1 INFO — "preauth.json fully merged into .claude/settings.json (18 permission patterns, 18 servers)". The 2 preauth_applied WARNs that gated this WI have flipped to 1 INFO.


## Transition note (2026-04-26T12:05:24+00:00)

Closed. Phase A shipped in processkit v0.22.0; Phase B shipped in aibox v0.20.0; verified via pk-doctor preauth_applied INFO. Acceptance criterion (the 2 preauth_applied WARNs flip to 1 INFO) met.
