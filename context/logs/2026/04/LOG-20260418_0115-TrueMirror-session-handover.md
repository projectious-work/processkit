---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260418_0115-TrueMirror-session-handover
  created: '2026-04-18T01:15:00Z'
spec:
  event_type: session.handover
  timestamp: '2026-04-18T01:15:00Z'
  actor: ACTOR-pm-claude
  summary: "Session handover — v0.18.1 hotfix shipped (src↔context drift sync + #7 hookEventName fix)"
  details:
    session_date: "2026-04-17 → 2026-04-18"
    session_duration: "Continued from compacted prior session; v0.18.0 ship + issue #7 triage + v0.18.1 hotfix"
    current_state: |
      processkit is at v0.18.1, tagged and published. Working tree is
      clean, remote is in sync.

      v0.18.1 is a pure-sync hotfix release. Prior releases (v0.15.0
      through v0.18.0) had been shipping tarballs packaged from
      src/context/ that were missing content which had landed only in
      the dogfooded context/ tree. The release notes claimed features
      (team-creator, /pk-* commands, Rail 5 scripts, schema updates)
      that weren't actually in the tarball. Consumer projects therefore
      received partial installs.

      Discovered via issue #7 (emit_compliance_contract.py omits
      hookEventName → Claude Code 2.1+ rejects envelope). The fix had
      been merged into the dogfood context/ tree but never ported back
      to src/context/. Release tarball verification turned up the
      broader drift.

      v0.18.1 synced src/context/ ← context/ for:
      - team-creator skill (whole tree — 8 files)
      - 26 /pk-* slash-command files across 13 skills (rename of legacy
        <skill>-<verb>.md names)
      - skill-gate Rail 5 scripts (check_decision_captured.py,
        decision_markers.py, decision_sweeper.py,
        record_decision_observer.py) + transcript / sessionend fixtures
      - discussion-management/commands/, id-management/config/,
        index-management/config/ (new directories)
      - owner-profiling OWNER-*.md assets (3 files)
      - actor.yaml / role.yaml schema updates for CapabilityProfileRouting
        (model_profiles, model_profile_override fields)
      - skills/INDEX.md, skill-gate/mcp/SERVER.md
      - src/AGENTS.md template: pk-compliance-contract v2 marker +
        decision-language clause + Session start block (pk-resume)
      - emit_compliance_contract.py: hookEventName echo (fixes #7)
      - check_route_task_called.py: marker lookup decoupled from
        session_id (scans .state/skill-gate/ for any valid marker with
        matching contract_hash + 12h TTL)
      - test_hooks.py: new coverage for hookEventName echo, stale marker,
        hash-mismatch

      Tests: 13/13 skill-gate green from src/; 16/16 MCP servers smoke-
      test green.

      Three-commit release pattern:
      - 39c894e fix: sync src/context/ ← dogfood context/ (65 files,
        +3134/−185)
      - 8668d66 chore: bump to v0.18.1 (CHANGELOG, AGENTS.md, docs-site)
      - bfa01e4 chore: regenerate src/PROVENANCE.toml for v0.18.1

      Tarball size: 722K (up from 689K for v0.18.0 — consistent with the
      added content). 6 hookEventName occurrences verified in the
      shipped script; 12 team-creator paths verified; 26 /pk-*
      command files verified.

      GitHub release published with tarball + sha256 sidecar. Issue #7
      commented and closed.

    open_threads:
      - id: AGENTS.md-v2-vs-contract-v1-inconsistency
        state: documented, deferred
        note: |
          AGENTS.md template carries pk-compliance-contract v2 marker
          (including the decision-language clause that references
          skip_decision_record). But skill-gate/assets/
          compliance-contract.md (printed by the hook into
          additionalContext) is still v1. Clauses remain a strict
          superset in v2 — not a contradiction — but internally
          inconsistent. Documented in v0.18.1 CHANGELOG + release notes
          as a known non-blocking follow-up. Reconciliation requires:
          (a) bumping the asset to v2 content, (b) implementing the
          skip_decision_record MCP tool on skill-gate/mcp/server.py,
          (c) re-running the smoke test since contract_hash changes
          will invalidate existing markers.

      - id: DEC-20260417_1800-unindexed
        state: deferred (same as before release)
        note: |
          DEC-20260417_1800-CapabilityProfileRouting was hand-written
          (not created via record_decision MCP) because aibox #53
          blocked MCP config merge at the time. The CLEANUP-REQUIRED
          marker is still on it. Re-record once aibox#53 lands and
          .mcp.json is properly wired in this dogfood project.

      - id: pk-standup-vs-pk-status-duplication
        state: "not started (v0.17.0 authoring glitch, still open)"
        note: |
          /pk-standup and /pk-status have identical bodies. Should be
          differentiated in a later release (v0.18.2?). Trivial fix.

      - id: workspace-cli-file-not-found
        state: "owner-project diagnosis, NOT processkit's bug"
        note: |
          Downstream project at /workspace/cli (separate dev container,
          not mounted here) reports:
            UserPromptSubmit operation blocked by hook:
            python3: can't open file
            '/workspace/cli/context/skills/processkit/skill-gate/scripts/
            emit_compliance_contract.py': No such file or directory
          This is a file-not-found, not the hookEventName envelope
          error. Root cause is one of: (a) aibox sync / init never ran
          in that project, (b) .claude/settings.json hook path doesn't
          match install layout, (c) install partial. Upgrading to
          v0.18.1 alone won't fix — the derived project must run
          aibox sync after bumping processkit_version. Confirmed NOT
          a processkit bug in this session.

      - id: LOG-entity-not-indexed-via-MCP
        state: "acknowledged deviation from compliance contract"
        note: |
          This handover log was hand-written rather than created via
          log_event MCP tool because the dogfood project's .mcp.json
          wiring is still blocked on aibox #53. Next session should
          run reindex to pick up this entry. Same for the previous
          v0.18.0 release handover. Pre-existing issue, not a new
          deviation.

    decisions_made_this_session:
      - |
        Chose v0.18.1 as a pure-sync hotfix rather than bundling
        additional changes. Scope was strictly "make src/context/
        match context/ as of now, ship, close issue #7". Three
        parallel workers dispatched (skill-gate, pk-* commands,
        team-creator + assets), all returned clean. AGENTS.md
        template merge done by PM directly to preserve placeholder
        tokens.
      - |
        AGENTS.md template: used `pk-resume` in the new Session start
        block rather than the stale `morning-briefing-generate`
        reference that existed in the runtime AGENTS.md. Runtime
        reference was a stale glitch — command was renamed in v0.17.0
        to pk-resume. Template now points at the command that
        actually exists at v0.18.1.
      - |
        Deferred AGENTS.md v2 ↔ contract asset v1 reconciliation
        out of v0.18.1 scope. Decision: the existing inconsistency
        was accepted by whoever bumped AGENTS.md to v2 originally;
        porting it forward unchanged is the minimum-surprise choice
        for a hotfix. Reconcile in a future release alongside the
        skip_decision_record tool implementation.

    artifacts_produced: []

    git_context:
      branch: main
      head: bfa01e4
      tag: v0.18.1
      remote: origin (in sync)
      clean: true

    token_budget_snapshot:
      opus_share: "~35% (PM coordinator role, worker dispatch,
        AGENTS.md template merge, release pipeline, release-notes
        drafting, issue-#7 diagnosis). High because session was
        short + tightly coordinated."
      sonnet_share: "~55% (3 parallel workers, each a general-purpose
        agent: skill-gate sync + test run, /pk-* command renames,
        team-creator + schema + INDEX.md sync)"
      haiku_share: "~10% (no explicit Haiku dispatch this session;
        minor reads/diffs)"
      note: |
        Opus still overweight vs 5/85/10 target, but justified for
        a release pipeline with parallelization and policy calls
        (which workers to dispatch, what to commit together, how to
        word the release notes). The workers did the heavy file-IO
        in Sonnet.

    next_recommended_action: |
      1. Run /pk-resume at next session start — morning-briefing will
         pick up this handover and surface the open threads.

      2. Reindex so index-management sees the new logs:
         call reindex from MCP once the harness has skill-gate + the
         other servers wired. Pre-existing blocker on aibox #53.

      3. File two WorkItems for v0.18.2 (or later):
         - Reconcile AGENTS.md v2 ↔ compliance-contract.md asset.
           Implement skip_decision_record MCP tool on skill-gate.
         - Differentiate /pk-standup and /pk-status (currently
           identical bodies; v0.17.0 authoring glitch).

      4. Add a CI guard — diff src/context/ ↔ dogfood context/ in
         the release workflow and fail if they drift. This bug cost
         4 versions of trust; a structural check would have caught
         it on any v0.15.0 PR. Trivial to implement with `diff -rq`
         and an allowlist for __pycache__ / .gitkeep / templates/.

      5. If the owner's /workspace/cli project still shows the file-
         not-found error after bumping processkit_version to v0.18.1
         and running aibox sync, diagnose over there (we confirmed
         it's not a processkit bug).

      6. Consider a /pk-retro skill now that we have a second recent
         release where the CHANGELOG claimed more than the tarball
         delivered. A retrospective would surface the systematic
         pattern earlier.
---

# Session narrative

Short, focused session with a long tail of forensic work at the end.

The session opened by continuing from a compact of the v0.18.0 release
conversation. First user request was "review this issue" (#7,
hookEventName omission in emit_compliance_contract.py). Investigation
revealed the fix was in the dogfood context/ tree but never in
src/context/ — meaning the v0.18.0 tarball we had just shipped did NOT
contain the fix. Extended diff turned up systemic drift across many
files going back to v0.15.0.

After reporting the finding the owner authorized a comprehensive
sync release (v0.18.1). Work was dispatched to three parallel workers:
- skill-gate sync (scripts, tests, fixtures, SERVER.md) — verified
  with test_hooks.py (13 green)
- /pk-* command renames across 13 skills — 16 target dirs verified
  diff-clean
- team-creator + owner-profiling assets + actor/role schemas +
  skills/INDEX.md — verified diff-clean; also audited SKILL.md drift
  (none found outside skill-gate)

The PM then merged the AGENTS.md template update directly, preserving
the {{PROJECT_NAME}} / {{BUILD_COMMAND}} / etc. placeholders while
porting the v2 compliance contract marker, the decision-language
clause, and the Session start block. Fixed one stale reference in the
merge: `morning-briefing-generate` (renamed in v0.17.0) → `pk-resume`.

Release pipeline executed cleanly on first try:
- skill-gate tests green (13/13)
- smoke-test-servers.py green (all 16)
- stamp-provenance.sh v0.18.1 (511 files)
- build-release-tarball.sh v0.18.1 (722K + sha256)
- 3 commits, 1 annotated tag, push main + tag
- gh release create with full release notes

Tarball verification confirmed the fix is actually in v0.18.1:
`grep hookEventName` returns 6 matches (vs 0 in v0.18.0). team-creator
appears 12 times; 26 /pk-* command files shipped. Issue #7 commented
and closed.

Tail end of session: owner asked whether a "file not found" error in
their derived /workspace/cli project would be fixed by v0.18.1.
Diagnosis: no — that error is a missing install, not a bug in any
processkit script. v0.18.1 still needs an `aibox sync` run in the
consumer project to land on disk. /workspace/cli is not mounted in
this dev container so deeper diagnosis requires switching to that
container. Confirmed to owner that processkit is not at fault.

Meta-observation for the next retrospective: v0.18.0 shipped with a
confident release summary ("v0.18.0 shipped. Tests green pre-release")
that was literally true (tests passed) but dangerously incomplete (the
tarball didn't contain the tested code). The gap between "local tests
pass" and "what consumers actually receive" was not instrumented. A
`diff -rq src/context/ context/` check in the release workflow, gated
to fail on non-allowlisted diffs, would have prevented four versions
of drift.
