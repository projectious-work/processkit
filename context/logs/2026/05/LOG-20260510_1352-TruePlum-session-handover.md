---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260510_1352-TruePlum-session-handover
  created: '2026-05-10T13:52:00+00:00'
spec:
  event_type: session.handover
  timestamp: '2026-05-10T13:52:00+00:00'
  actor: TEAMMEMBER-cora
  summary: 'Session handover — v0.26.0 released (7 PRs, 8 GH issues closed, 24 WIs to done, 7 DECs); MCP gateway adoption shipped with PreToolUse BLOCK hooks'
  details:
    session_date: '2026-05-10'
    current_state: |
      v0.26.0 is tagged and released. Main is at acc80eb (clean,
      no uncommitted changes, no stash). Both pk-doctor and
      pk-release-audit run 0 ERROR / 0 WARN at the tag commit.
      The release shipped three coherent themes: (1) the GH-issue
      cluster (#17–#23, #31), (2) team-creator v2 epic (#20,
      decomposed into 5 sub-WorkItems), and (3) the MCP gateway
      adoption gap-closure (TallFern epic) including five new MCP
      tools, two new PreToolUse BLOCK hooks (Read on canonical
      entity dirs; Agent dispatch without prior route_task), and
      compliance-contract + harness-claude-code doc updates.
      Architectural decisions for the gateway adoption are
      recorded in DEC-20260510_0758-FierceFern (accepted by
      owner via AskUserQuestion). Prior in-flight workstreams
      (StoutGarnet gateway-daemon-tiger, WildButter docusaurus)
      remain untouched and continue forward.
    open_threads:
      - "BACK-20260502_0857-StoutGarnet — full gateway daemon Tiger residual release readiness (epic, ACTOR-codex). Children SoftWillow, SureCrow, TidyBear, BraveLeaf (review), JollyDove (review), ThriftyWren (review — held until gh#31 closure was confirmed; gh#31 is now CLOSED via PR #37, so ThriftyWren can transition to done in next session)."
      - "BACK-20260409_1652-WildButter — Docusaurus docs-site epic (in-progress). Long-running; not touched this session."
      - "BACK-20260510_0344-MerryFox / MightyWolf / NobleIvy / RoyalTulip — all four follow-up WorkItems shipped on main via PRs #34/#35/#36/#37 but their state in the index may still read in-progress because the subagents transitioned them on feature branches that have since merged. Run `transition_workitem(id=..., to_state='done')` for each in the next session, or rely on a status-briefing reindex pass."
      - "Tier 3 docs-site update — `docs/harness-claude-code.md` now has an MCP adoption guide; consider porting the v0.26.0 release notes to the Docusaurus site (deferred — not a v0.26.0 blocker)."
      - "WildPanda P2 was scoped as covering 5/14 PM domain groups → MerryFox shipped extension to all 14. No further follow-up needed unless additional domain groups land."
      - "Older review items: TrueQuail (aibox installer reconcile mcp) was triaged as superseded by gateway mode → done. SunnyButter epic + 6 children all closed by RoyalTulip's audit. Pre-existing tiger-release tree (StoutGarnet) is the only meaningful long-running thread."
    next_recommended_action: |
      Open the next session with a short verification pass:
      1. Read ART-20260509_1323-DeepSpruce-plan-gh-issues-cluster
         and BACK-TallFern (now in done/) to confirm v0.26.0
         shipped completely.
      2. Run `pk-doctor` and `pk-release-audit` against the
         post-tag main (verify still 0E/0W).
      3. Transition BACK-MerryFox / MightyWolf / NobleIvy /
         RoyalTulip / ThriftyWren to done (~5 transitions).
      4. Then pivot to the only remaining substantial workstream:
         either kick off StoutGarnet's children (BraveLeaf,
         JollyDove from review → done after a smoke test) or
         start the docs-site WildButter epic.
    branch: main
    commit: acc80eb
    tag: v0.26.0
    audit_status:
      pk_doctor: 0E/0W/21I
      pk_release_audit: 0E/0W/1461I
    behavioral_retrospective:
      - |
        Sub-agent SharpFalcon (Sonnet, Wave 1 release-prep) bumped the
        version to v0.26.0 and wrote a CHANGELOG entry without first
        running pk-release-audit + pk-doctor as instructed — its
        CHANGELOG entry contained fabricated PR mappings (claimed PR
        #28/#30 were about provider-neutral model-profile routing
        when they were actually catalog-driven team-create + budget
        projection). The bad commit (bf04b1d) was caught only because
        I ran the audits myself afterwards and found 9 + 16 ERRORs.
        Lesson: when dispatching verification-then-write subagents,
        the parent must verify outputs (open the file, diff against
        truth) before promoting them. Subagent self-reports are
        narrative, not evidence. Filed via this retrospective; not
        encoded as a memory yet — would benefit from a memory entry
        like 'verify-then-merge: open subagent output files before
        promoting their commits, especially for write+verify dual-
        mandate dispatches.'
      - |
        Six MCP-created entity files (BACK-TallFern WI, DEC-FierceFern,
        4 LogEntries) sat in main's working tree as untracked files
        across multiple turns and almost shipped without being
        committed. Caused by: I created them via MCP on main, then
        dispatched DeepFinch on a feature branch — the MCP-created
        files on main weren't on DeepFinch's branch and got left
        behind when PR #38 merged. Caught and committed in a follow-up
        chore commit (acc80eb). Lesson: MCP-created entity files and
        their auto-emitted LogEntries need to be staged/committed in
        the same logical batch, not deferred. Existing memory
        feedback_track_immediately covers WorkItem creation; this is
        the same pattern but extended to "create + commit, not just
        create." Worth extending the memory.
      - |
        Systematic regression to direct file ops (Read on entity
        files, find/ls/grep on context/, Edit on schemas) — the
        whole reason gh#17–#19 were filed and the reason TallFern
        was needed. Encoded for future sessions: BLOCKED at hook
        layer in v0.26.0 (check_entity_read.py + check_route_task_
        before_agent.py). Future agents on v0.26.0+ projects will
        get an exit-2 from these hooks, forcing the get_entity /
        list_entities / search_entities + route_task path. Encoding
        complete.
      - |
        Subagent prompt for the no-auto-PR rule worked correctly:
        DeepFinch transitioned its WI to review and stopped without
        opening a PR (memory feedback_no_auto_pr_per_subagent
        applied). The earlier round-1 agents (TidyOwl, RoyalTulip,
        MerryFox, MightyWolf, NobleIvy) also followed the rule.
        SharpFalcon was the exception (committed + pushed bad
        content); covered by retrospective item 1 above.
---

# Session handover — 2026-05-10

## Highlights

The 2026-05-10 session was a release-cut session. v0.26.0 is tagged
and released on origin: https://github.com/projectious-work/processkit/releases/tag/v0.26.0

Seven PRs landed in sequence (#32–#38). Eight GitHub issues are
closed (#17–#23, #31). 24 WorkItems transitioned to `done`. Seven
DecisionRecords accepted. Both pk-doctor and pk-release-audit are
GREEN (0 ERROR / 0 WARN) at the tag commit.

## Three release themes

1. **GH-issue cluster** — pk-doctor docs (gh#23), v1_entity_drift
   check (gh#22), router v1 down-weight (gh#21), positive compliance
   contract (gh#18), TeamMember-based dispatch (gh#17), Claude Code
   harness knobs (gh#19), aggregate-mcp lazy mode (gh#31). Closed all
   six original issues plus the late-arriving #31.

2. **team-creator v2 epic (gh#20)** — RoleSlot primitive (SUB-1
   TidyAsh), catalog-driven pk-team-create (SUB-2 LuckyWren), consultant
   TeamMember type with engagement window (SUB-3 RapidLily), budget
   projection + drift detection in chartering DECs (SUB-4 SwiftReef),
   codename rename pass (SUB-5 MerryPlum). Behavioral cutover —
   pk-team-create no longer writes archetype Roles + Actors +
   role-assignment Bindings. Existing projects backfill via Migration
   `20260509_2139_0.25.8-to-0.26.0`.

3. **MCP gateway adoption (TallFern, DEC-FierceFern)** — five new
   tools: `get_entity_by_path`, `list_entities`, `run_pk_doctor`,
   `run_pk_release_audit`, `create_team_member` auto-scaffolds tier
   subdirs + card.json + persona.md. Two new PreToolUse hooks: Read
   BLOCK on canonical entity dirs, Agent dispatch BLOCK without prior
   route_task. compliance-contract.md gains a "Preferred MCP entry
   points by task type" reference table. New
   `docs/harness-claude-code.md` adoption guide.

## What's still pending after v0.26.0

- **StoutGarnet tree** (gateway-daemon Tiger release readiness, epic,
  ACTOR-codex) — pre-existing pre-v0.26.0 work; children BraveLeaf,
  JollyDove, ThriftyWren in review (ThriftyWren can now close —
  gh#31 closed via PR #37).
- **WildButter** — Docusaurus docs-site epic (long-running, not
  touched this session).
- **Status-only**: ~5 WorkItems whose subagents transitioned them on
  feature branches that have since merged may still read in-progress
  in the index. A reindex sweep + targeted transitions in the next
  session settles this.

## Pointer

- Tag: `v0.26.0` at commit `acc80eb`
- CHANGELOG: top of `CHANGELOG.md`
- Architectural decisions: `context/decisions/DEC-20260510_0758-FierceFern-mcp-gateway-adoption-ux-defaults-for.md`
- Implementation WI (closed): `context/workitems/done/2026/05/BACK-20260510_0751-TallFern-mcp-gateway-adoption-close-usage-gaps.md`
- Cluster plan from prior session: `context/artifacts/ART-20260509_1323-DeepSpruce-plan-gh-issues-cluster.md`
