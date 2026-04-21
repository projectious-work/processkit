---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260415_1800-ShadowCount-rail5-marker-calibration
  legacy_id: BACK-20260415_1800-ShadowCount-rail5-marker-calibration
  created: '2026-04-15T18:00:00+00:00'
  labels:
    component: skill-gate
    area: enforcement
    priority_driver: owner-critical
spec:
  title: Rail 5 shadow-mode calibration — 20-session precision/recall run before flipping to block
  state: done
  type: spike
  priority: high
  size: S
  description: >
    QuietLedger ships the PreToolUse decision-capture gate in
    shadow-mode-ON by default. Before flipping to `--mode=block`
    (the gate actually blocking writes on Tier-A marker hits), we
    need empirical precision/recall on the owner's real session
    transcripts. Flipping blindly risks interrupting legitimate work
    on conversational words like "ok" and "yes".
  method:
    corpus:
      - Collect ~20 recent session transcripts from
        `~/.claude/projects/<this-repo>/sessions/*.jsonl` (or wherever
        Claude Code persists them on this host).
      - Prefer sessions with user-labeled outcomes so TP/FP labelling
        is tractable.
    procedure:
      - |
        1. Run `decision_markers.scan(tier="A")` on the user-message
        stream of each transcript. Emit a table:
        session_id × timestamp × matched_marker × matched_text ×
        next_tool_call.
      - |
        2. Manually label each hit: TP = this user-turn was genuinely
        owner approval of a cross-cutting decision; FP = the marker
        was conversational or referred to trivial in-turn work.
      - |
        3. Compute precision (TP / (TP + FP)) and recall
        (TP / total-owner-confirmed-decisions-in-corpus).
      - |
        4. If precision < 0.80, propose marker-list revisions (drop
        bare `ok`/`yes`; require longer phrases like
        `ok let's`/`yes let's`; or add a last-message-only
        constraint so 5-message-back matches never fire).
      - |
        5. If recall < ~0.60, propose Tier-B promotions to Tier-A
        (but only if they clear the precision gate).
  success_criteria:
    - Artifact lists all Tier-A hits in the 20-session corpus with
      TP/FP labels.
    - Precision and recall computed with clear numerator/denominator.
    - "Explicit go/no-go recommendation on flipping to `--mode=block`."
    - "If no-go: a concrete marker-list revision with expected precision under the new list."
  deliverables:
    - context/artifacts/ART-*-ShadowCount-rail5-marker-calibration.md
  out_of_scope:
    - Writing any code. If a marker-list patch is indicated, file a
      ~5-line FEAT-XS follow-up after this research lands.
    - Calibrating Tier-B markers (sweeper-only; higher recall is
      fine there).
  related_workitems:
    depends_on: BACK-20260415_1700-QuietLedger-rail5-auto-decision-capture-implementation
    sibling_of:
      - BACK-20260415_1700-QuietLedger-rail5-auto-decision-capture-implementation
  related_artifacts:
    - ART-20260415_1600-QuietLedger-rail5-auto-decision-capture-research
  assigned_to: ACTOR-sr-researcher
---

# Notes

Prereq before `--mode=block` is safe. Filed 2026-04-15 right after
QuietLedger shipped in shadow-mode-ON.

Recommended execution timing: after enough real sessions have
accumulated that the corpus is representative (owner judgement).
Don't rush into 20 sessions of contrived test traffic — shadow mode
is safe indefinitely, so this can wait for natural usage.

# progress_notes

- 2026-04-15T20:00Z — Sr Researcher (Opus) completed the calibration
  run.
  - **Corpus:** 9 Claude Code main-session JSONLs under
    `~/.claude/projects/-workspace/` (2026-04-09 → 2026-04-15),
    ≈120 genuine owner-utterance turns after filtering out
    tool_use/tool_result/slash-command payload pollution. Below the
    aspirational 20-session target but statistically decisive for
    the go/no-go question per the WorkItem instructions. External
    repos (`projectious-work/*`, `funkspur`) not fetched this turn;
    noted transparently in the artifact.
  - **Overall Tier-A precision (labelled sample of 20 owner-turn
    hits):** 6 / 19 = **0.316** (Ambiguous excluded).
  - **Overall Tier-A recall (6 DecisionRecords in window):**
    6 / 6 = **1.00** — at least one Tier-A marker fired before
    every cross-cutting decision, but the marker list is so
    permissive that precision collapses.
  - **Verdict: NO-GO.** Do not flip `--mode=shadow` →
    `--mode=block` with the current Tier-A list.
  - **Top three highest-noise markers:** `\bok(ay)?\b` (0/5),
    `\bproceed\b` (0/4), `\bapproved\b` (0/3). `\bdecision\b`
    sits at 1/6 = 0.17 and `\bgood\b` at 1/4 = 0.25.
  - **Proposed revised Tier-A list** (see artifact §7): drop
    `ok`, `good`, `yes`, `proceed`, `approved`, `decision`,
    `decided`, `confirmed`, `we'll`, `i'll` from Tier A
    (demote to Tier B for sweeper-only); keep `ship it`,
    `let's/i'll/we'll go with`, `go with the approach/option/plan`,
    `locked in`, `final answer`. Also add last-message-only and
    ≤200-char turn-length constraints, plus filter
    tool_use/tool_result/isCompactSummary/isSidechain entries in
    `tail_user_assistant`. Predicted precision under revision:
    ~0.70–0.85 on similar corpora; still not a confident GO.
  - **Meta-finding:** owner's linguistic style rarely uses the
    high-precision idioms. Lever 1 may be structurally mismatched;
    an LLM-classifier variant is worth evaluating as a follow-up
    FEAT.
  - **Deliverable:**
    `context/artifacts/ART-20260415_2000-ShadowCount-rail5-marker-calibration.md`
  - **State:** proposed → done.
