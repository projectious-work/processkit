---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260423_0818-ProudStone-session-handover
  created: '2026-04-23T08:18:38+00:00'
spec:
  event_type: session.handover
  timestamp: '2026-04-23T08:18:00+00:00'
  summary: Short session — diagnosed and fixed stale `.mcp.json` (missing team-manager
    + migration-management); hand-merged from reference because aibox installer is
    version-delta gated and saw no upgrade; harness reload still pending.
  actor: TEAMMEMBER-cora
  details:
    session_date: '2026-04-23'
    current_state: 'Short diagnostic-plus-fix session. Root cause of the v0.19.0 MCP-tool
      gap found: `/workspace/.mcp.json` (which is gitignored, managed by the aibox
      installer) still carried the pre-v0.19.0 server set — `processkit-actor-profile`
      registered, `processkit-team-manager` and `processkit-migration-management`
      missing. Container rebuild this morning triggered an aibox sync at 07:06 UTC
      (see untracked `context/migrations/pending/MIG-20260423T070619.md`) but it ran
      as a no-op: `from_version: v0.19.1 → to_version: v0.19.1`. No processkit version
      delta → installer did not rewrite `.mcp.json` → new v0.19.0 MCP servers invisible
      after rebuild. Hand-merged all 18 per-skill `mcp-config.json` files into `/workspace/.mcp.json`
      from a reference the user supplied from another v0.19.1 project (kept retired
      `processkit-actor-profile` in place for now; added `processkit-migration-management`
      + `processkit-team-manager`). JSON validated; 18 servers listed; every per-skill
      config has a root entry. Harness reload has NOT yet been performed — the fix
      is on disk but not in the running harness. Branch `main` is clean at `7cba2c5`;
      only untracked files are the two pending migrations aibox dropped.'
    open_threads:
    - '**Harness reload required** — `/workspace/.mcp.json` now contains `processkit-team-manager`
      (17 tools) and `processkit-migration-management`, but the running Claude Code
      harness still reflects the pre-merge state. After next restart, confirm the
      deferred tool list shows `mcp__processkit-team-manager__*` and `mcp__processkit-migration-management__*`,
      then run the Cora routing dogfood from yesterday''s handover.'
    - '**Installer reconciliation gap (v0.19.2 candidate)** — aibox sync regenerates
      `.mcp.json` only on processkit version-delta, not on per-skill-config drift.
      Manual `src/` ↔ `context/` alignment (as done in the v0.19.0/v0.19.1 ship) hides
      new MCP servers from downstream harnesses until the NEXT version bump. Should
      be filed as a WorkItem alongside BraveDove for v0.19.2. Not filed this session
      — defer to next session so it can go in via the (by then) working `create_workitem`
      path with proper TEAMMEMBER-* assignee once BraveDove''s schema drift is also
      fixed.'
    - '**Pending migrations untracked** — `context/migrations/pending/MIG-20260423T070619.md`
      (processkit v0.19.1→v0.19.1, 540 ''new'' files flagged, 0 conflicts) and `MIG-RUNTIME-20260423T070617.md`
      (aibox runtime 0.18.7→0.18.7, 0 changes). Both look like no-op diffs. Accept
      or discard via `migration-management` MCP tools once the harness reload makes
      them callable.'
    - '**All six threads from yesterday''s handover (LOG-20260422_1642-SmartBird)
      remain open** — WildButter docs-site epic, BraveDove schema drift (workitem.assignee
      + deciders[] reject TEAMMEMBER-*), src/AGENTS.md template placeholders, historical
      Release notes v0.1.0–v0.6.0 placeholder content, WarmGrove auto-log actor fix
      requires harness restart. Harness reload in #1 resolves the WarmGrove item.'
    next_recommended_action: 'Reload the Claude Code harness so the hand-merged `/workspace/.mcp.json`
      is applied. On next session start, verify the deferred tool list now contains
      `mcp__processkit-team-manager__*` (expected 17 tools) and `mcp__processkit-migration-management__*`.
      Then execute yesterday''s deferred Cora routing dogfood: `resolve_model(role="ROLE-product-manager",
      seniority="senior", team_member="TEAMMEMBER-cora")` and confirm Layer-2 or Layer-5
      resolution on the live MCP transport.'
    branch: main
    commit: 7cba2c5
    uncommitted: '`/workspace/.mcp.json` hand-merged (gitignored — persists via workspace
      volume, will NOT appear in `git status`). Untracked: `context/migrations/pending/MIG-20260423T070619.md`,
      `context/migrations/pending/MIG-RUNTIME-20260423T070617.md` (both aibox-generated
      no-ops).'
    behavioral_retrospective:
    - 'Compliance contract explicitly forbids hand-editing the merged harness MCP
      config, with the escape hatch of ''let the installer re-merge''. With no installer
      available in-repo and the user explicitly requesting a manual write from a reference
      example, I proceeded — but flagged the contract tension and recommended filing
      the installer-reconciliation gap as v0.19.2 work. Lesson: when a contract rule
      has a fallback that doesn''t exist yet, the rule is effectively broken; surface
      the gap rather than treating the rule as a silent block.'
    - 'Status briefing correctly flagged the harness-reload blocker as priority #1
      but mis-diagnosed the cause as ''container rebuild not yet done''. User''s counter
      (''I DID rebuild'') forced a deeper look and found the real cause (aibox sync
      is version-delta-gated). Lesson: when a briefing attributes a blocker to a user-side
      action, verify the user-side state rather than assuming it when the user says
      the action was taken.'
---
