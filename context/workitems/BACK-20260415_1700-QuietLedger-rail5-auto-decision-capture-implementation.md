---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260415_1700-QuietLedger-rail5-auto-decision-capture-implementation
  legacy_id: BACK-20260415_1700-QuietLedger-rail5-auto-decision-capture-implementation
  created: '2026-04-15T17:00:00+00:00'
  labels:
    component: skill-gate
    area: enforcement
    priority_driver: owner-critical
spec:
  title: Rail 5 implementation — auto-capture of decisions (Lever 1 PreToolUse gate + Lever 2 SessionEnd sweeper)
  state: done
  type: story
  priority: high
  size: M
  description: >
    Implement the Rail 5 recommendation from RES-GapScout
    (ART-20260415_1600-QuietLedger): Lever 1 (PreToolUse decision-
    language gate, precision-biased) + Lever 2 (SessionEnd sweeper
    that writes a Note artifact for owner async review). Skip Lever 3
    (slash command) — file as a trivial follow-up if owner asks.
  approach:
    lever_1_preaction_gate:
      description: >
        New PreToolUse hook script that reads `transcript_path` from
        the Claude Code hook input, scans the last N=5 user messages
        for Tier-A decision markers, and blocks any
        `create_*`/`record_*`/`transition_*`/`link_*` MCP write that
        is not preceded by a `record_decision` call OR an explicit
        `skip_decision_record(reason=...)` acknowledgement in the
        same session.
      deliverables:
        - context/skills/processkit/skill-gate/scripts/check_decision_captured.py
        - context/skills/processkit/skill-gate/scripts/decision_markers.py  # shared regex lib
        - context/skills/processkit/skill-gate/scripts/record_decision_observer.py  # PostToolUse — records the ack
        - context/skills/processkit/skill-gate/scripts/fixtures/claude-code-pretooluse-with-transcript.json
        - "new MCP tool on skill-gate: skip_decision_record(reason: str)"
        - compliance-contract.md updated with Rail-5 clause
      success_criteria:
        - Hook reads transcript_path correctly on Claude Code 2.1+ fixture.
        - With 0 markers in last 5 messages → exit 0 (allow).
        - With ≥1 Tier-A marker AND no record_decision/skip in this session → exit 2 with remediation message.
        - skip_decision_record acknowledgement persists per-session for 24h then expires.
        - Tier-A markers calibrated against 20-session shadow-mode run before flipping to blocking (see open question 1).
    lever_2_sessionend_sweeper:
      description: >
        New SessionEnd hook script that re-scans the full session
        transcript for decision-language cues (Tier-A + Tier-B,
        higher-recall pass) and writes a Note artifact tagged
        `decision-candidates` listing each cue with timestamp and a
        link to the matching DecisionRecord (or "no record" flag).
        Owner reviews async — sweeper does NOT block session end.
      deliverables:
        - context/skills/processkit/skill-gate/scripts/decision_sweeper.py
        - context/skills/processkit/skill-gate/scripts/fixtures/claude-code-sessionend.json
        - skill-gate hook config additions for SessionEnd wiring (Claude Code, Cursor)
      success_criteria:
        - Sweeper produces a Note artifact even on empty sessions (zero candidates).
        - Note artifact uses tag `decision-candidates` for owner-side index queries.
        - Sweeper exits 0 in all cases (never blocks SessionEnd).
        - Per-harness fallback: where SessionEnd doesn't exist (Codex, Aider), sweeper is no-op with a clear log line.
  shadow_mode_calibration:
    description: >
      Per RES-GapScout open question 1: before flipping Lever 1 to
      blocking, run the marker library in shadow mode for 20 sessions
      and compute precision/recall on owner-confirmed decisions vs
      flagged cues. Tune Tier-A markers to ≥0.80 precision before
      enabling block mode. Tier-B markers stay sweeper-only (Lever 2)
      regardless.
    deliverables:
      - context/artifacts/ART-*-rail5-shadow-mode-calibration.md
  per_harness_matrix:
    claude_code: full L1+L2 supported (primary target).
    codex_cli: L1 degraded (PreToolUse Bash-only per openai/codex#16732); L2 likely; document gracefully.
    cursor: L1 via preToolUse + beforeMCPExecution; L2 via sessionEnd; transcript-path access unverified (RES-GapScout open question 2).
    opencode: L1 partial (MCP-tool bypass bug #2319); L2 weak (no clear session-end event).
    aider: neither lever deliverable (no hook system) — degrade gracefully via AGENTS.md prose only.
  out_of_scope:
    - Lever 3 (/decide slash command) — file as separate FEAT-S if owner asks.
    - Auto-capture of entity types other than DecisionRecord.
    - Building a UI for reviewing decision-candidate Notes.
  related_artifacts:
    - ART-20260415_1600-QuietLedger-rail5-auto-decision-capture-research
  related_workitems:
    parent: BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan
    sibling_of:
      - BACK-20260414_1430-CleanCharter-compliance-contract-canonical-source
      - BACK-20260414_1431-LoudBell-acknowledge-contract-mcp-tool
      - BACK-20260414_1432-InkStamp-mcp-tool-description-1pct-rule
      - BACK-20260414_1433-SteadyHand-provider-neutral-hook-scripts
  related_decisions:
    - DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list
  assigned_to: ACTOR-pm-claude  # PM dispatches; per-lever implementer TBD
---

# Notes

Filed 2026-04-15 directly after RES-GapScout's recommendation
(L1+L2). Estimated effort: 1.5–2 dev-days. Two open questions
inherited from the research:

1. Empirical shadow-mode calibration of marker tiers (deliverable
   ART listed above).
2. Cursor `preToolUse` transcript-path availability (determines
   whether L1 is Claude-Code-only or cross-harness).

Schedule: post-v0.15.0 release.

## Progress notes

Implementation completed by ACTOR-developer on 2026-04-15. Ships in
shadow-mode-ON by default; 20-session calibration required before
flipping to block. Follow-up calibration item: file separately if
needed.
