---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260422_1642-SmartBird-session-handover
  created: '2026-04-22T16:42:00+00:00'
spec:
  event_type: session.handover
  timestamp: '2026-04-22T16:42:00+00:00'
  actor: TEAMMEMBER-thrifty-otter
  summary: >-
    Session handover — v0.19.0 architecture refactor + v0.19.1 release
    bulletproofing both shipped, tagged, released; Cora created as first
    AI persona.
  details:
    session_date: "2026-04-22"
    current_state: |
      Two major releases shipped this session:

      - **v0.19.0** — TeamMember model + 51-role catalog + Model artifacts
        + binding routing. Three DecisionRecords (SpryTulip, BraveFalcon,
        LoyalComet). Six phase WorkItems all `done`. 388 files changed
        in the core commit. `ACTOR-ThriftyOtter-owner` migrated to
        `TEAMMEMBER-thrifty-otter`; `ACTOR-AmberDawn` + 8 role-class
        actors + 7 legacy roles + 8 legacy bindings deleted. `team-manager`
        skill replaces `actor-profile` (49 tests pass). 34 Model artifacts
        extracted from `model_scores.json` (20 tests pass). 51 Role files
        with pure-ordinal seniority + function groups. 789-LOC binding
        resolver with 8-layer precedence (25 tests pass). 30 default
        bindings materialised. pk-doctor gained `team_consistency` (5th
        category). Released via manual `gh release create` (prepare-only
        slip, addressed in v0.19.1).
      - **v0.19.1** — local-only release bulletproofing. DEC-MerryArch
        (CI-workflow approach) withdrawn in favour of DEC-SnowyWolf
        (skill flow + doctor detection). `release-semver/SKILL.md`
        collapsed into a single 9-step bulletproof flow ending in
        `gh release view` as the completion gate. pk-doctor gained
        `release_integrity` (6th category); backfilled 5 historical
        Releases (v0.1.0–v0.6.0) so the check is clean. No CI
        workflows shipped.
      - **Cora** — first named AI persona created: `TEAMMEMBER-cora`,
        product-manager @ senior. Persona, A2A card, seeded relationship
        with `thrifty-otter`. Replaces the retired `ACTOR-pm-claude`.

      **Health:** `pk-doctor` across all 6 check categories — 0 ERROR / 0
      WARN / 6 INFO. `context/` ↔ `src/context/` in sync. 23 GitHub
      Releases on origin, every local `v*` tag has a matching Release.

    open_threads:
      - "WildButter (BACK-20260409_1652) — Docusaurus docs-site epic; pre-existing in-progress from a prior session. Not touched in this session."
      - "BraveDove (BACK-20260422_1643) — schema drift: workitem.yaml assignee + decisionrecord.yaml deciders[] patterns still require ACTOR-* and reject TEAMMEMBER-*. Two workarounds used in this session (omitting fields); filed as standalone follow-up. Candidate for v0.19.2."
      - "Cora's MCP tools (team-manager.create_team_member, etc.) and resolve_model / explain_routing on model-recommender — not yet callable this session; require a harness MCP-config reload. New session should pick them up automatically."
      - "src/AGENTS.md is a template with placeholders; only the AI-agents-on-this-project section was updated for v0.19.0. Other placeholder sections (project description, build/test commands, code style, prefs, gotchas) are still template scaffolding for downstream projects and will be filled per-project at install time — not processkit's job to populate."
      - "Historical Releases v0.1.0–v0.6.0 now exist with placeholder notes (`Historical release … no CHANGELOG section`). If anyone wants to enrich them with actual historical notes, that's pure content work; current state is honest and release_integrity is clean."
      - "Running MCP servers still pre-date the WarmGrove auto-log actor fix. LogEntries emitted by those servers during this session lacked the actor field; ~30+ were backfilled by a one-liner script. Restarting MCP servers (harness reload) ends the recurrence."

    next_recommended_action: |
      Reload the harness MCP config so the new tools are callable:
      - `team-manager.*` (17 tools: lifecycle, name pool, memory tree,
        export/import, consistency)
      - `model-recommender.resolve_model` + `explain_routing`
      - new pk-doctor `release_integrity` category is already wired
        into the doctor.py script (no reload needed for it)

      Then dispatch a task end-to-end via Cora:
      `resolve_model(role="ROLE-product-manager", seniority="senior",
      team_member="TEAMMEMBER-cora")` and confirm it returns a ranked
      candidate list via Layer 2 (team-member preference) or Layer 5
      (role+seniority). This validates the new routing path on a real
      MCP transport (not just the pytest fixtures).

    branch: main
    commit: "eb91f86"
    behavioral_retrospective:
      - "Stopped halfway through the v0.19.0 release (tag pushed, no GH Release). Root cause: /pk-release prepared but /pk-publish was never invoked. Fixed permanently in v0.19.1 via single-turn flow + release_integrity check + DEC-SnowyWolf. Skill flow now has an explicit completion gate that cannot be skipped."
      - "Missed schema drift on workitem.assignee + decisionrecord.deciders[] during v0.19.0 Phase 1 (they still require ACTOR-*). Noticed mid-session when create_workitem and record_decision both rejected TEAMMEMBER-* IDs; worked around by omitting fields and filed BACK-BraveDove for the real fix. Lesson: when doing a cross-cutting ID scheme change, grep every schema for the old ID prefix before claiming Phase 1 done."
      - "Binding filename hash (first 8 hex chars of SHA1) happened to be all digits for one entry, which pk-doctor's schema_filename check parsed as YYYYMMDD and flagged. Fixed by shortening to 6 chars and prefixing with 'h'. Lesson: when generating identifier suffixes for entity files, ensure the tail cannot form an 8-digit run."
      - "Initial v0.19.1 fix attempt reached for a GitHub Actions workflow; owner rejected on vendor-lock + cost grounds. The revised no-CI approach (skill flow + pk-doctor check) turned out cleaner and was also cheaper to implement. Lesson: match the fix to the project's cost/vendor stance before reaching for CI. processkit's value is provider-neutral; CI-specific workflows are an anti-pattern for this codebase."
      - "Git push was rejected on first v0.19.1 attempt because the PAT lacked `workflow` scope. Confirmed the remote state stayed clean (nothing leaked); did a clean rollback via soft reset + tag delete + file removal. Lesson: for files under .github/workflows/, GitHub enforces a token-scope check above and beyond normal push permissions — useful as an unintentional guard but needs to be remembered."
      - "Three background agents were used this session (Phase 2 team-manager skill, Phase 3 model extraction, Phase 5 binding resolver). All three returned clean, comprehensive results with tests passing. Pattern worked well for large self-contained implementation blocks with clear boundaries. Smaller phases (1 schemas, 4 roles, 6 migration) were kept in the main context and finished faster. Lesson: delegate when the task is self-contained, test-able, and non-overlapping with other parallel work; keep in main context when it needs judgment, iteration, or tight coordination."
---
