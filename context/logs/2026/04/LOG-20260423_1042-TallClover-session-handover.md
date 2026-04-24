---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260423_1042-TallClover-session-handover
  created: '2026-04-23T10:42:16+00:00'
spec:
  event_type: session.handover
  timestamp: '2026-04-23T10:42:16+00:00'
  summary: 'v0.19.2 scope accepted (DEC-SnowyFox: SteadyCedar → BraveDove → TrueQuail);
    SteadyCedar done (pyyaml PEP 723 fix verified live); BraveDove in review (5-schema
    alternation fix, offline-verified, awaits harness restart for live smoke test);
    TrueQuail untouched; 14 mod + 17 untracked files uncommitted.'
  actor: TEAMMEMBER-cora
  details:
    session_date: '2026-04-23'
    current_state: 'Productive v0.19.2 scoping + first-item-shipped + second-item-on-review
      session. DEC-20260423_0838-SnowyFox locked v0.19.2 scope and fix order: SteadyCedar
      → BraveDove → TrueQuail. SteadyCedar (BACK-20260423_0829-SteadyCedar) is DONE:
      added `pyyaml>=6.0` to the model-recommender MCP server''s PEP 723 header in
      both `context/` and `src/context/` trees, verified end-to-end via a live resolve_model
      call (post-harness-restart) returning a valid Layer-5 candidate (MODEL-anthropic-claude-sonnet
      v4.6 for ROLE-product-manager@senior) with full 8-layer trace. BraveDove (BACK-20260422_1643)
      is IN REVIEW: audit expanded scope from 2 to 5 schemas (workitem.assignee, decisionrecord.deciders[],
      discussion.participants[], artifact.owner, metric.owner); chose alternation
      pattern `^(ACTOR|TEAMMEMBER)-[a-zA-Z0-9_-]+$` over clean flip because 90 residual
      ACTOR-* references in 44 entity files would otherwise retroactively invalidate;
      offline regex verification passed; live smoke test FAILED because workitem-management
      MCP server caches schemas at startup — harness restart required. TrueQuail (BACK-20260423_0829-TrueQuail,
      filed this session) untouched, nothing blocks it. Both aibox no-op migrations
      applied to clear pending queue. Branch main at 7cba2c5; 14 modified + 17 untracked
      files uncommitted.'
    open_threads:
    - '**Harness restart required for BraveDove verification**. After restart, run
      `create_workitem(title="[smoke-test]", type="task", priority="low", assignee="TEAMMEMBER-cora")`
      and `record_decision(..., deciders=["TEAMMEMBER-thrifty-otter"])`. If both succeed,
      transition BACK-20260422_1643-BraveDove review → done. If either still fails,
      there is a deeper bug beneath the schema — investigate the schema loader in
      workitem-management/decision-record servers.'
    - '**TrueQuail untouched** (BACK-20260423_0829-TrueQuail, backlog, high). aibox
      installer must reconcile .mcp.json on per-skill-config drift, not just version
      delta. Third in v0.19.2 scope. No blocker.'
    - '**Uncommitted work** — 14 modified + 17 untracked files. All this-session writes.
      Suggested two-commit split: (a) `fix(v0.19.2): pyyaml dep + schema drift alternation`
      covers SteadyCedar + BraveDove code/schema changes (the 8 modified source files
      under src/ and context/schemas); (b) `chore: session entity writes` covers migrations
      applied + WIs/decisions/logs. Commit BEFORE any aibox sync to avoid work loss.'
    - '**Observation: MCP servers cache schemas and uv envs at startup**. Each schema
      edit under `context/schemas/` requires a full harness restart to take live effect;
      same for PEP 723 header changes (uv env is keyed on the deps hash). This cost
      two turns this session (SteadyCedar + BraveDove). Worth considering as a DX
      improvement in v0.19.2 or v0.20.0 (watchdog + schema hot-reload, or a reload_schemas
      MCP tool). Not yet filed as a WI — evaluate whether it''s worth filing or just
      a note.'
    - '**All six carryover threads from LOG-20260422_1642-SmartBird** triaged earlier
      this session: WildButter (leave in-progress), BraveDove (now in review), Cora
      MCP tools (verified live), src/AGENTS.md (per SmartBird not processkit''s job),
      v0.1.0–v0.6.0 release notes (SmartBird: current state is honest), WarmGrove
      auto-log (marked done via harness reload).'
    next_recommended_action: 'Restart the harness. Then immediately run the BraveDove
      smoke test: `create_workitem(title="[smoke-test] BraveDove verification", type="task",
      priority="low", assignee="TEAMMEMBER-cora")`. On success, transition BACK-20260422_1643-BraveDove
      to done, then transition the smoke-test WI to cancelled or done. Then start
      TrueQuail: read the WI body, design the drift-detection approach (sha256 of
      sorted per-skill mcp-config.json hashes stored in an installer manifest), implement
      in the aibox installer, add a pk-doctor check to catch regressions, verify.
      BEFORE the restart, commit the current on-disk work as two commits (fix + chore)
      so nothing is lost.'
    branch: main
    commit: 7cba2c5
    uncommitted: '14 modified + 17 untracked files. Modified: context/migrations/INDEX.md,
      context/schemas/{artifact,decisionrecord,discussion,metric,workitem}.yaml, context/skills/processkit/model-recommender/mcp/server.py,
      context/workitems/BACK-20260422_1643-BraveDove-schema-drift-workitem-assignee.md,
      and the five src/context/ mirror files. Untracked: DEC-20260423_0838-SnowyFox,
      11 session LogEntries, 2 applied migrations, 2 new WIs (SteadyCedar + TrueQuail),
      ProudStone handover from the earlier session, this new handover file.'
    behavioral_retrospective:
    - 'Initial SteadyCedar verification used `uv run --script server.py` while the
      harness uses `uv run server.py` without `--script`. The two invocations can
      differ. The `--script` form was smoke-test-positive yet I missed confirming
      the harness-native form. Lesson: when verifying MCP server fixes, mirror the
      harness''s exact command line before claiming fix-verified.'
    - 'BraveDove''s WI scoped 2 schemas but its own ‘Also consider: any other schemas
      that reference entity IDs of the identity class. Full audit’ note was load-bearing
      — the audit found 3 more (artifact.owner, metric.owner, discussion.participants[]).
      Lesson: when a WI body says ‘also consider’, treat the audit as required not
      optional — otherwise the fix ships incomplete and a follow-up WI is inevitable.'
    - 'The running MCP servers cache schemas and uv envs at startup. Every schema
      or PEP 723 edit requires a full harness restart — SteadyCedar and BraveDove
      both hit this, costing a turn each. Lesson: when proposing a schema- or dep-level
      fix, name the restart requirement in the plan from the start; consider filing
      a DX improvement (schema hot-reload or reload_schemas tool) if this keeps happening.'
    - 'Two restart-dependent fixes stacked in a single session reduce isolation on
      the next restart — if a regression appears, it is harder to bisect across two
      fixes than one. Acceptable for small well-understood changes like these; riskier
      for larger ones. Lesson: for bigger changes, pace restarts so each fix gets
      its own green.'
    - 'Offline regex/jsonschema verification of the BraveDove patch was fast and conclusive
      and let me separate ‘schema change correct’ from ‘server picks it up’ cleanly.
      Lesson: keep the offline test in the flow for all schema edits — it catches
      the pure-correctness failures without requiring a restart.'
    - 'Compliance: skill-gate blocked the very first Edit under context/ until acknowledge_contract(v2)
      was called, despite MCP writes already succeeding in the session. The contract-version
      bump from v1 → v2 returned a clean ‘version mismatch’ error. Lesson: call acknowledge_contract
      at session start, not on first block.'
---
