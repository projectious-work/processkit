---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260418_1930-GreenGate-session-handover
  created: '2026-04-18T19:30:00Z'
spec:
  event_type: session.handover
  timestamp: '2026-04-18T19:30:00Z'
  actor: ACTOR-pm-claude
  summary: "Session handover — v0.18.2 staged (issue #8 fix, contract v2, drift
    guard, SnappyTrout/LivelyTulip, threads 1–3 closed) — not yet released"
  details:
    session_date: "2026-04-18"
    session_duration: "Single session. PM + 5 parallel workers + owner."
    current_state: |
      processkit is still tagged at v0.18.1 on `main`. All v0.18.2
      content is staged on the working tree but NOT yet committed or
      released. Working tree has substantial uncommitted changes.

      Phases executed this session (see next_recommended_action for
      what remains):

      1.1  Issue #8 patch — 12 × 2 `mcp-config.json` files fixed.
           All now point at `context/skills/processkit/<skill>/mcp/
           server.py`. Grep-verified zero residue outside templates/.
      1.2  Smoke tests 16/16 green (post-fix).
      1.3  Reindex — DEFERRED: harness did not reload this session,
           index-management MCP never became reachable from the
           harness process.
      1.4  Verify deferred MCP tools — DEFERRED for same reason.
      2.1  All 3 pending migrations moved to applied/ and state flipped:
           - MIG-20260418T090604 (v0.17.0→v0.18.1) — verified no-op,
             v0.18.1 hotfix already synced.
           - MIG-20260418T172222 (AGENTS.md) — accepted live file;
             fixed stale `morning-briefing-generate` → `pk-resume` on
             line 45.
           - MIG-RUNTIME-20260418T090604 (aibox-home 0.18.3→0.18.5) —
             `.claude.json` already present, `keybindings.json`
             local-only as expected.
      2.2  /pk-standup vs /pk-status differentiated. /pk-standup now
           the brief daily form; /pk-status retains fuller snapshot.
           Both trees updated.
      2.3  DEC-20260417_1800 re-record — DEFERRED (needs record_decision
           MCP).
      3.1  skip_decision_record(reason, session_id?) tool added to
           skill-gate MCP server. 24h TTL marker under .state/skill-gate/
           matching existing .ack / .decision-observed layout. Empty
           reason rejected. check_decision_captured.py now honours skip
           markers in block mode. Mirror to src/context/.
      3.2  compliance-contract.md asset bumped to v2 (adds decision-
           language clause referencing skip_decision_record).
           _COMPLIANCE_VERSION constant bumped v1→v2 in server.py. Old
           session .ack markers now stale (correct — content hash
           changed). smoke-test-servers.py updated to read version
           from the asset instead of hardcoding v1.
      3.3  scripts/check-src-context-drift.sh added. Allowlist: dogfood-
           only dirs (actors/, artifacts/, bindings/, decisions/,
           discussions/, logs/, migrations/, notes/, roles/, team/,
           workitems/, root INDEX.md), runtime paths (.cache/, .state/,
           __pycache__/, .gitkeep), templates/. Wired into
           scripts/build-release-tarball.sh between staging mkdir and
           tree copy (lines 71–82). Currently PASS against live tree.
      3.4  /pk-retro backlog item — DEFERRED (needs create_workitem
           MCP).
      4.1  SnappyTrout + LivelyTulip plans drafted; scope confirmed.
      4.2  Owner signed off plans implicitly by approving "proceed
           with all phases".
      4.3  SnappyTrout implemented. Mandatory session-start skill-check
           checklist added to AGENTS.md "AI agents" section naming six
           task classes (research ingestion, artifact creation,
           discussion management, decision recording, backlog item
           creation, quality audits) with concrete tool calls
           (search_entities, find_skill, list_skills). Same cue added
           to session-handover SKILL.md "incoming session" block.
           morning-briefing deliberately skipped (justified: it's a
           generation skill, not a workstream-starter). Both trees.
      4.4  LivelyTulip verified — find_skill / list_skills already
           ship in skill-finder MCP and pass smoke tests
           (`find_skill workitem: ... match_confidence: 0.67`,
           `list_skills count: 2`). Acceptance criteria met without
           additional code.
      4.5  Transitions to done — DEFERRED (needs transition_workitem).
      5    Release v0.18.2 — NOT SHIPPED.

      Tests run this session:
      - scripts/smoke-test-servers.py — PASSED (16/16 servers).
      - src/context/.../skill-gate/scripts/test_hooks.py — PASSED
        (22/22 assertions incl. 6 new for skip_decision_record).
      - scripts/check-src-context-drift.sh — PASSED (zero diffs after
        allowlist).

      CHANGELOG drafted for v0.18.2 (already written into
      /workspace/CHANGELOG.md above the v0.18.1 section). Sections:
      Fixed (issue #8, AGENTS.md stale command), Added (skip_decision_
      record, contract v2, drift guard, SnappyTrout checklist, standup/
      status split), Closed work (SnappyTrout, LivelyTulip).

    open_threads:
      - id: harness-reload-blocker
        state: "still blocking — MCP client in the running Claude Code
          harness loaded the old merged config at startup and never
          picked up the fixed mcp-config.json paths"
        note: |
          Everything that requires `record_decision`, `create_workitem`,
          `transition_workitem`, `log_event`, `query_entities`, or
          `reindex` is blocked until the harness is restarted or
          `/mcp reconnect` is issued. The on-disk config is correct
          and servers launch cleanly when invoked by the smoke test.
          Next session MUST reload before attempting Phases 1.3, 1.4,
          2.3, 3.4, 4.5, 5 release tail.

      - id: v0.18.2-not-released
        state: staged on working tree, not committed
        note: |
          All v0.18.2 file changes are in the working tree. Nothing
          committed, nothing tagged, nothing pushed. PROVENANCE not
          stamped. Tarball not built. gh release not created. Issue
          #8 not closed. The v0.18.2 CHANGELOG entry is in place.
          Release pipeline is sequential (drift-guard, smoke,
          stamp, 3 commits, tag, push, tarball, release, close #8,
          handover-via-log_event).

      - id: handover-log-not-written-via-MCP
        state: "acknowledged deviation (same as LOG-20260418_0115 and
          LOG-20260417_0900)"
        note: |
          This file was hand-written because log_event MCP is not
          reachable this session. Run reindex after harness reload
          to pick it up. Same for the prior two handovers.

      - id: DEC-20260417_1800-unindexed
        state: "still deferred, same CLEANUP-REQUIRED marker as before"
        note: |
          Plan was Phase 2.3. Re-record via record_decision once MCP
          is reachable. No content change; just index the existing
          decision through the proper tool.

      - id: pk-retro-backlog-item
        state: "not created yet"
        note: |
          Phase 3.4. Plan: route_task then create_workitem with kind=FEAT,
          state=backlog, title "Add /pk-retro skill — post-release
          retrospective". Motivation: v0.15.0–v0.18.0 drift + v0.18.1
          hotfix + v0.18.2 (this session) shows enough of a pattern
          that a retrospective skill would pay for itself.

      - id: pending-migration-flag-upstream-pk-resume
        state: "resolved this session"
        note: |
          MIG-20260418T172222 surfaced that /workspace/AGENTS.md line
          45 still said `morning-briefing-generate` (renamed in
          v0.17.0). Fixed to `pk-resume` in this session. Mirror
          already OK.

    decisions_made_this_session:
      - |
        Treat MIG-20260418T090604 as a no-op record rather than
        re-applying the migration. The content shipped as part of the
        v0.18.1 hotfix (commit 39c894e). Worker B verified file-by-file
        that every listed new-upstream path exists and every
        removed-upstream is absent. Flipped state and moved to applied/.
      - |
        Close LivelyTulip as delivered without additional code.
        WorkItem scope is exactly find_skill + list_skills; both are
        already shipped in skill-finder MCP server and pass smoke
        tests. Supersedes BACK-AmberCliff per the WorkItem body.
      - |
        Bump compliance-contract.md asset to v2 in the same release as
        the skip_decision_record MCP tool. The two halves must ship
        together because the v2 clause references the tool. Old session
        .ack markers carrying the v1 hash are allowed to go stale —
        that is the correct re-acknowledge-on-change behavior.
      - |
        Drift guard allowlist explicitly includes the 11 dogfood-only
        data directories under context/. That is not a leak; those
        directories don't exist under src/context/ and are not meant
        to. The guard asserts the *shippable* template tree matches
        what the dogfood uses, not the dogfood's project data.
      - |
        Do NOT write a separate "session-start" skill for SnappyTrout.
        The checklist belongs inline in AGENTS.md and
        session-handover/SKILL.md. A standalone skill would be scope
        creep and would sit one indirection layer away from where the
        reader needs to see it.

    artifacts_produced:
      - "scripts/check-src-context-drift.sh (new)"
      - "v0.18.2 CHANGELOG entry (staged, not committed)"

    git_context:
      branch: main
      head: "bfa01e4 (unchanged from v0.18.1 tip)"
      tag: v0.18.1
      remote: "origin (in sync at v0.18.1)"
      clean: false
      working_tree_summary: |
        ~30+ modified/new files across AGENTS.md, CHANGELOG.md,
        scripts/, context/skills/processkit/{skill-gate,standup-context,
        session-handover}/, and src/ mirrors, plus the 24 mcp-config.json
        patches (12 × 2 trees), plus 3 migrations moved from pending/
        to applied/, plus this handover log.

    token_budget_snapshot:
      opus_share: "~15% (PM coordination, plan, 5 worker dispatches,
        1 inline fix for AGENTS.md pk-resume stale reference, 1 inline
        fix for smoke-test-servers.py version binding, CHANGELOG draft,
        this handover)"
      sonnet_share: "~80% (Workers A–F: issue #8 patch, migrations,
        skip_decision_record + contract v2 + test_hooks, drift guard +
        tarball wiring, SnappyTrout; 5 of 6 Sonnet)"
      haiku_share: "~5% (Worker C only — /pk-standup vs /pk-status
        split, 11 tool uses, 19s duration)"
      note: |
        Closer to target 5/85/10 mix than recent sessions. Opus stayed
        in coordinator / policy lane except for two small inline fixes
        the workers wouldn't have known to make. Drift-guard discovery
        by Worker E (initial run flagged 3 skill-gate files Worker D
        had just touched — tree settled to PASS after both workers
        finished) was a nice ordering check.

    next_recommended_action: |
      1. RELOAD the harness (`/mcp reconnect` or restart session) so
         the new MCP servers become reachable. Without this, steps 2–7
         are blocked.

      2. Verify deferred tools load via ToolSearch (query_workitems,
         record_decision, create_workitem, log_event, query_entities,
         reindex). Expect all to appear.

      3. Call `reindex()` to pick up this handover log and the prior
         two unindexed handovers.

      4. Re-record DEC-20260417_1800-CapabilityProfileRouting via
         `record_decision` MCP. Strip CLEANUP-REQUIRED marker.
         `log_event` the re-record.

      5. `route_task` + `create_workitem` for /pk-retro backlog
         (kind: FEAT, state: backlog).

      6. `transition_workitem` BACK-20260410_1049-SnappyTrout →
         done. `transition_workitem` BACK-20260411_0802-LivelyTulip →
         done. `log_event` both.

      7. Release pipeline v0.18.2:
         a. bash scripts/check-src-context-drift.sh (expect PASS).
         b. uv run scripts/smoke-test-servers.py (expect 16/16).
         c. uv run src/context/skills/processkit/skill-gate/scripts/
            test_hooks.py (expect 22/22).
         d. bash scripts/stamp-provenance.sh v0.18.2.
         e. Three commits (Conventional Commits):
            - fix: mcp-config.json path regression (#8) + sync (mcp-
              config patches + AGENTS.md pk-resume line + migrations
              moved to applied/)
            - chore: bump to v0.18.2 — CHANGELOG, AGENTS.md,
              docs-site, standup/status split, SnappyTrout checklist,
              skip_decision_record + contract v2, drift guard
            - chore: regenerate src/PROVENANCE.toml for v0.18.2
         f. git tag -a v0.18.2; git push main --follow-tags.
         g. bash scripts/build-release-tarball.sh v0.18.2.
         h. gh release create v0.18.2 --notes-file=<CHANGELOG excerpt>
            + attach tarball + sha256.
         i. gh issue close 8 with release link.
         j. `log_event` for the release (session.release).

      8. Optional cleanup — pk-pub (if applicable), update docs-site
         landing page version badge.

      Open owner question: does /workspace/cli still show the file-
      not-found error after bumping processkit_version? If so, switch
      to that container for diagnosis — confirmed not a processkit
      bug in the prior handover.
---

# Session narrative

Short, focused session planned as six phases and executed in roughly
the planned order with one structural deviation: the running Claude
Code harness cached the old (broken) merged MCP config at startup and
never picked up the Phase 1.1 fix in-process. That pushed Phases 1.3,
1.4, 2.3, 3.4, 4.5, and the Phase 5 release tail onto the "next
session after reload" path. The file-level work (Phases 1.1, 1.2, 2.1,
2.2, 3.1–3.3, 4.1–4.4) all completed green.

Planning was front-loaded. After the owner asked for a full review,
PM produced a 5-phase plan mapping each task to a team member and a
model tier, with explicit parallelization marks and a flagged risk
around the harness reload. Owner confirmed three decisions (LivelyTulip
scope investigation, migration no-op treatment, harness-reload
agreement) and gave green light.

Phase 1 executed sequentially as planned. Worker A (Sonnet) patched
all 24 mcp-config.json files across both trees and grep-verified zero
residue. PM ran the smoke suite — 16/16 green. Reindex became the
first casualty of the harness-cache problem: the running process
didn't know about the fixed servers, so even though the smoke test
launched them successfully, `ToolSearch +reindex` returned nothing.
PM surfaced this to the owner and continued on file-only tasks.

Phase 2/3 dispatched five parallel workers (B, C, D, E, F) covering
three migrations, the /pk-standup vs /pk-status split, the combined
skip_decision_record + contract v2 bump, the drift guard + tarball
wiring, and SnappyTrout. Worker C ran on Haiku (cheapest tier for a
trivial rewrite). The others ran on Sonnet. All five returned clean
with tight reports.

Worker B surfaced one small delta during migration verification:
AGENTS.md line 45 still referenced the old `morning-briefing-generate`
command (renamed to `pk-resume` in v0.17.0). PM fixed inline. Worker D
reported a test-design choice: `importlib` can't import the FastMCP
server outside `uv run`, so the three new skip_decision_record tests
assert on the marker-file contract directly, matching the pattern
used by the existing `.ack` marker tests. Worker E found that the
drift guard initially flagged three skill-gate files that Worker D
had just modified; both workers finished and the guard settled to
PASS without intervention — nice natural ordering check.

Contract-version bump surfaced a latent coupling: `smoke-test-servers.py`
hardcoded `version="v1"` in its skill-gate smoke section. First post-
bump smoke run failed with a "version mismatch: caller supplied 'v1'
but on-disk contract is 'v2'" error. PM replaced the hardcode with
a regex read of the current `pk-compliance v<N>` marker from the asset
text, so future bumps don't break the test the same way. Second smoke
run green.

Phase 4.1 reading confirmed LivelyTulip is effectively delivered —
the two tools it scopes (find_skill, list_skills) are already in the
skill-finder MCP server and pass smoke tests. No code needed; just a
state transition in the next session.

The CHANGELOG draft was written at the end so the release pipeline
can run without further prose work. Both `[v0.18.2]` and the "Closed
work" subsection are already in place above the `[v0.18.1]` heading.

The main meta-observation: the harness-reload problem is the same
shape as the v0.15.0–v0.18.0 drift problem — a silent divergence
between what's on disk and what's actually running. Drift guard
catches on-disk vs on-disk. A runtime guard (e.g. "session startup
hook verifies every MCP server in merged config actually handshook")
would catch this class. Out of scope for v0.18.2 but worth a future
backlog item.
