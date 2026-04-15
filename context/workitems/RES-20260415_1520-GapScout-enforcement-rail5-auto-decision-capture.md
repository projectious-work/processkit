---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: RES-20260415_1520-GapScout-enforcement-rail5-auto-decision-capture
  created: '2026-04-15T15:20:00+00:00'
  labels:
    component: processkit-core
    area: enforcement
    priority_driver: owner-critical
spec:
  title: Rail 5 research — auto-capture of decisions from planning discussions
  state: done
  type: research
  priority: high
  size: M
  description: >
    Gap identified on 2026-04-15 while reviewing the v0.14.0
    enforcement rails: planning discussions that settle on an approach
    but don't invoke any `create_*` / `record_*` tool produce no
    structural trigger for `record_decision`, so DecisionRecords are
    created only when the agent self-polices. Rails 1–4 do not close
    this gap. This research item scopes three complementary levers so
    we can decide which to build.
  research_questions:
    lever_1_preaction_decision_check:
      description: >
        Before calling any write-tool, scan the last N user messages
        for decision-language markers (we'll / let's / I'll go with /
        approved / decided / ok / good / ship it / yes). If found,
        require either a `record_decision` call in the same turn or
        an explicit `skip_decision_record(reason=...)` acknowledgement.
        Implementation surface: a new clause in the compliance
        contract plus a PreToolUse hook that inspects transcript.
      questions:
        - What N (message window) minimises false positives without missing real decisions? Starting hypothesis: N=5.
        - Which decision-language markers give the best precision/recall on a sample of the last 20 sessions' transcripts?
        - Does the PreToolUse hook have access to the conversation transcript, or only to the current tool call? If the latter, this lever needs a different delivery surface.
        - How to avoid double-triggering when a DecisionRecord was already created earlier in the same session for the same topic?
    lever_2_sessionend_sweeper:
      description: >
        A SessionEnd hook runs a "decision audit": scans the session
        transcript for decision-language cues that don't correspond to
        any DecisionRecord created during the session. Surfaces a
        "candidate decisions you might want to record" list to the
        owner.
      questions:
        - Does Claude Code expose a SessionEnd hook event? (Research suggests yes; re-verify.)
        - What's the right output format — stdout list, a transient artifact, or a slack-to-self style note?
        - Can the sweeper reuse the lever-1 heuristic, or does it need a different (higher-recall, lower-precision) pass?
        - Owner UX: acceptable to be asked at session end, or should the sweeper only write to a log the owner reviews async?
    lever_3_decide_slash_command:
      description: >
        A documented `/decide <summary>` slash command that's a
        one-word shortcut for invoking `decision-record-write`. Not
        automatic, but lowers activation energy.
      questions:
        - Slash commands are a Claude Code surface — what's the provider-neutral equivalent so this works on Codex CLI / Cursor / OpenCode?
        - Should this be a skill command under `decision-record`, or a standalone skill-gate command?
  expected_outputs:
    - An artifact `ART-*-rail5-auto-decision-capture-research` with findings per lever.
    - A recommendation: which of {lever_1_only, lever_1+lever_2, all_three} to build, with cost/benefit per option.
    - If a FEAT follows, a separate WorkItem filed after this research lands.
  success_criteria:
    - All three levers have answered research questions with confidence labels (Confirmed / Likely / Weak / Speculation) per established convention.
    - The recommendation is defensible: explicit trade-offs, not just "build everything".
    - Any Claude-Code-specific findings have provider-neutral fallbacks documented for Codex / Cursor / OpenCode / Aider.
  out_of_scope:
    - Building any of the three levers. This item is research only.
    - Auto-capture for entity types other than DecisionRecord.
  related_workitems:
    sibling_of:
      - FEAT-20260414_1430-CleanCharter-compliance-contract-canonical-source
      - FEAT-20260414_1431-LoudBell-acknowledge-contract-mcp-tool
      - FEAT-20260414_1432-InkStamp-mcp-tool-description-1pct-rule
      - FEAT-20260414_1433-SteadyHand-provider-neutral-hook-scripts
    parent: ARCH-20260414_1245-FirmFoundation-enforcement-implementation-plan
  related_decisions:
    - DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list
  assigned_to: ACTOR-sr-researcher
  progress_notes:
    - 'Research completed by ACTOR-sr-researcher on 2026-04-15. Recommendation: lever_1+lever_2. See ART-20260415_1600-QuietLedger-rail5-auto-decision-capture-research.'
---

# Notes

Opened 2026-04-15 after owner reviewed the v0.14.0 rails and flagged
that planning-conversation decisions still fall through the cracks
unless the agent self-polices. This research scopes Rail 5 of the
enforcement initiative.
