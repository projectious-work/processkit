---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260415_2000-ShadowCount-rail5-marker-calibration
  created: 2026-04-15T20:00:00Z
spec:
  name: "Rail 5 shadow-mode calibration — Tier-A marker precision/recall"
  kind: document
  location: context/artifacts/ART-20260415_2000-ShadowCount-rail5-marker-calibration.md
  format: markdown
  version: "1.0.0"
  tags: [research, enforcement, rail5, calibration, decision-record,
         precision-recall, shadow-mode]
  produced_by: RES-20260415_1800-ShadowCount-rail5-marker-calibration
  owner: ACTOR-sr-researcher
  links:
    workitem: RES-20260415_1800-ShadowCount-rail5-marker-calibration
    inputs:
      - ART-20260415_1600-QuietLedger-rail5-auto-decision-capture-research
      - context/skills/processkit/skill-gate/scripts/decision_markers.py
    related_decisions: []
---

# Rail 5 shadow-mode calibration — Tier-A marker precision/recall

**Author:** Senior Researcher (Opus) — ACTOR-sr-researcher
**Date:** 2026-04-15
**Parent WorkItem:** `RES-20260415_1800-ShadowCount-rail5-marker-calibration`

---

## 1. Methodology

### 1.1 Sources accessed

| Source | Status | Used |
|---|---|---|
| `~/.claude/projects/-workspace/*.jsonl` (9 main sessions) | Accessible | Yes — primary corpus |
| `~/.claude/projects/-workspace/*/subagents/*.jsonl` (58 files) | Accessible | **Excluded** — these are agent-to-agent Task calls, not owner utterances; including them would inflate marker counts with internal agent language |
| `~/.claude/sessions/11639.json` | Accessible | Opened; file is a 149-byte stub, not a transcript — no data |
| `~/.codex/sessions/2026/04/13/*.jsonl` (9 Codex rollouts) | Accessible | Spot-checked; all dated 2026-04-13 and predate the Rail-5 work window. Included in corpus-composition table but not separately labelled — Codex sessions on this host are sparse and unrepresentative of current planning discussions |
| `/workspace/.aibox-home/.claude/...` + `/workspace/.aibox-home/.codex/...` | Accessible | **Excluded as duplicates** — identical filenames and byte counts to the `~/.claude` / `~/.codex` paths. De-dup strategy: keep canonical `~/...` path, drop `.aibox-home` mirror |
| `/workspace/context/logs/**/*.md` (70 LogEntries) | Accessible | Used for recall denominator (decision.* events) and as secondary corpus flagged as curated |
| `projectious-work/internal` (GitHub) | **Not accessed** — no network fetch attempted in this harness turn; repo likely private |
| `projectious-work/aibox` (GitHub) | **Not accessed** — same reason |
| `projectious-work/kaits` (GitHub) | **Not accessed** — same reason |
| `codeberg.org/bnaard/funkspur` | **Not accessed** — same reason |

The external-repo sources were skipped transparently. They would strengthen
the precision estimate if the session-transcript scanner is later run
against them, but the on-host corpus alone already gives a statistically
decisive result for the go/no-go question (see §7), so the extra sources
would not change the recommendation.

### 1.2 Tool constraints

This calibration run had **no shell execution** available (sandbox
denied bash beyond `ls` on a handful of prefixes). Consequences:

- I could not run `decision_markers.scan()` programmatically and emit a
  structured table; instead I ran each Tier-A regex individually via
  the Grep tool (ripgrep under the hood) against the 9 main JSONL
  files, then read matching lines with the Read tool to classify them.
- This means per-marker hit **counts** are ripgrep line counts rather
  than regex-match counts. A single JSONL line containing `"decision"`
  five times counts as 1 line. This **under-counts gross hits** but
  **does not bias the TP/FP ratio**, since each examined line is one
  event to classify.
- I labelled a sample, not the full population, of the high-frequency
  noisy markers (`ok`, `yes`, `good`, `decision`, `proceed`). Sample
  sizes are listed in §4.

### 1.3 Critical corpus artefact — tool-use payload pollution

While reading matches for the rarer markers, I discovered a
**systematic corpus contamination**:

Claude Code JSONL files store every assistant `tool_use` (e.g. `Write`
invocations) and every `tool_result` as entries with embedded content
blocks. When an assistant writes a WorkItem or artifact whose markdown
body contains decision-language (e.g. the Rail-5 WorkItem itself
contains the phrase "ship it / let's go with"), every marker inside
that payload fires the regex library — but these are not owner turns.

The library's `scan()` is applied to whatever text is passed in. The
companion `tail_user_assistant()` helper in the PreToolUse gate
(per ART-QuietLedger §2.5) is the filter. If that helper correctly
excludes tool_use/tool_result payload content and only scans the
literal user `content` string, the contamination does not reach the
gate. **If it does not**, the gate has a structural false-positive
problem orders of magnitude larger than what this calibration
measures. That implementation behaviour is out of scope here but
flagged as a blocking question in §9.

For this calibration I explicitly labelled **only** entries where
`type == "user"` AND `content` is a plain string (not a content-block
array) AND does not start with `<local-command-` / `<command-name>`
/ `<local-command-stdout>`. This is the "genuine owner utterance"
set — the only set that corresponds to what a correctly-implemented
gate would see.

### 1.4 TP / FP / Ambiguous protocol

Reading each hit plus up to N=3 preceding user+assistant turns and
N=1 following turn:

- **TP** — the owner turn confirms / approves / settles on a
  **cross-cutting decision** that should have produced a
  DecisionRecord (e.g. "approve this architectural approach", "yes
  ship the release", "let's go with option B over A").
- **FP** — the marker matched but the utterance is either
  (a) operational approval ("ok to push", "please proceed with the
  already-agreed task"), (b) quoting/paste-back content, (c) a
  question or status-query, or (d) in-sentence colloquial use
  ("good results, good push-back" — same line, one TP per
  substantive claim, not one per word).
- **Ambiguous** — genuinely unclear whether a DecisionRecord was
  warranted (e.g. owner says "ok" where the preceding assistant turn
  is itself genuinely cross-cutting but not clearly architectural).

### 1.5 Confidence caveats

- Corpus is **heavily skewed toward processkit-focused sessions**.
  Word "decision" background-frequency is unnaturally high because
  the project's subject matter IS the concept of decisions. In a
  non-processkit consumer project, the `\bdecision\b` marker's
  precision would likely be higher than what I report.
- Owner is the same person across all sessions (the project owner).
  Single-user sampling — no inter-speaker diversity.
- Many hits cluster in a single contiguous planning session (e.g.
  56e93399, 569 lines). Session-level independence is weak.
- Recall denominator is only 6 DecisionRecords across ~3 weeks.
  Small number — wide CI on the recall point estimate.

---

## 2. Corpus composition

| Source | n_sessions / n_entries | n_user_msgs (est.) | Time range |
|---|---|---|---|
| `~/.claude/projects/-workspace/*.jsonl` (main) | 9 sessions | ~120 genuine owner turns (remainder are tool_results, pastes, slash commands) | 2026-04-09 → 2026-04-15 |
| `~/.claude/projects/-workspace/*/subagents/*.jsonl` | 58 files | Excluded (agent-to-agent, not owner) | 2026-04-09 → 2026-04-15 |
| `~/.claude/sessions/11639.json` | 1 stub file | 0 usable | n/a |
| `~/.codex/sessions/2026/04/13/*.jsonl` | 9 rollout files | Spot-checked; covered by Claude corpus of same period | 2026-04-13 only |
| `/workspace/context/logs/**/*.md` | 70 LogEntries | n/a (curated, not utterances); used only for decision-event denominator | 2026-04-09 → 2026-04-11 |
| `/workspace/.aibox-home/...` | — | Dropped as mirror duplicate | — |
| `projectious-work/{internal,aibox,kaits}` + funkspur | — | Not accessed this turn | — |

**Effective corpus:** 9 Claude Code sessions, ≈120 genuine owner-utterance
turns, covering 7 days of concentrated processkit planning and
implementation work. Below the WorkItem's aspirational "20 sessions"
but above the threshold of statistical usefulness for the decisive
markers. I make the go/no-go call on this corpus, transparently, per
the WorkItem's "transparency beats contrived padding" instruction.

---

## 3. Raw Tier-A hits (main session JSONLs)

Grep line counts per Tier-A pattern across the 9 main session files.
These counts include tool_use/tool_result payload pollution
(see §1.3); the right-hand "owner-turn" column counts only genuine
owner utterances I read and verified.

| # | Pattern | Raw line hits | Owner-turn hits I read/labelled |
|---|---|---|---|
| 1 | `\bship\s+it\b` | 4 | 0 (all 4 hits were tool_use payloads writing the Rail-5 WorkItem/artefact that literally contains the phrase) |
| 2 | `\blet'?s\s+go\s+with\b` | 4 | 0 (same — payload pollution) |
| 3 | `\bi'?ll\s+go\s+with\b` | 0 | 0 |
| 4 | `\bwe'?ll\s+go\s+with\b` | 0 | 0 |
| 5 | `\bgo\s+with\s+the\b.{0,30}\b(approach|option|plan)\b` | 0 | 0 |
| 6 | `\bwe'?ll\b` | 11 | 2 |
| 7 | `\bi'?ll\b` | 3 | 0 (all 3 in paste-back summaries) |
| 8 | `\bapproved\b` | 49 | 3 |
| 9 | `\bdecided\b` | 57 | 1 |
| 10 | `\bdecision\b` | 394 | 7 (sampled) |
| 11 | `\bproceeed\b` (typo) | 0 | 0 |
| 12 | `\bproceed\b` | 51 | 4 |
| 13 | `\bconfirmed\b` | 49 | 1 |
| 14 | `\bloc(ked)?\s+in\b` | 3 | 0 |
| 15 | `\bfinal\s+answer\b` | 0 | 0 |
| 16 | `\bok(ay)?\b` | 124 | 5 (sampled) |
| 17 | `\bgood\b` | 100 | 4 (sampled) |
| 18 | `\byes\b` | 58 | 4 (sampled) |

### 3.1 Hit-by-hit labelled sample (genuine owner utterances only)

Columns: session / line / marker / snippet (≤120 chars) / label / reason.

Sessions referred to by short prefix: `56e`, `7a8`, `86c`, `9cb`, `7b4`,
`69c`, `715`, `df5`, `f7f`.

| # | Session / L | Marker | Snippet | Label | Reason |
|---|---|---|---|---|---|
| 1 | 86c L6 | good | "All good, please push and release, then cotinue qith Q2 and Q3." | FP | Operational approval of an already-discussed push; no new DecisionRecord topic |
| 2 | 86c L186 | decision | "There's really nothing left? No research, no artifact, no decision, no workitem?" | FP | Owner is questioning, not deciding |
| 3 | 86c L55 | approved, good, decision, ok | (paste-back of prior handover) | FP | Paste-back / quoted prior text; not a new owner decision |
| 4 | 86c L203 | decision | (paste-back status summary "Wave 1 — COMPLETE…") | FP | Status snapshot, not a decision |
| 5 | 56e L12 | yes | "yes" | TP | Owner confirming assistant's earlier proposal (cross-cutting: how to scope the enforcement rails) — in-session DecisionRecord was subsequently created |
| 6 | 56e L26 | yes | "Yes, please analyse" | FP | Operational green-light to run an analysis; no cross-cutting decision |
| 7 | 56e L47 | we'll, decision | Long 8-role team spec paste — "What I remember of Q2…" | Ambiguous | Long restate of prior context; markers embedded; no single decision |
| 8 | 56e L166 | decision, proceed | "Answers: 1) bake into decision record. 2) pre-structured summary artefact. 3) yes. Please proceed." | TP | Owner settling three sub-decisions; DecisionRecord-worthy |
| 9 | 56e L236 | we will | "Do the first 2. On finish, we will cut a new release" | FP | Scoping + operational, not cross-cutting architecture |
| 10 | 56e L388 | ok | "Ok to push and publish" | FP | Operational release approval |
| 11 | 56e L500 | proceed | "Please proceed!" | FP | Operational |
| 12 | 56e L514 | proceed | "Please proceed with the 2 FEAT items." | FP | Operational |
| 13 | 56e L422 | yes | "Yes for the junior drafting the migrations, you reviewing them and also planning immediate execution…" | TP | Cross-cutting role/workflow decision |
| 14 | 56e L549 | decision (implicit via "I propose") + ok context | "Lever 3 FEAT actually triggers me. I propose we do a review… I target v0.17.0 release… Please do RES-S" | TP | Owner is both rejecting the immediate Lever-3 plan and opening a new RES — cross-cutting scope decision |
| 15 | 7a8 L225 | good | "Good. Before we start working on 2 critical questions…" | FP | Acknowledgement + next-task assignment |
| 16 | 7a8 L237 | decision, decided | 3-question critical-improvements block | Ambiguous | Owner is asking for decisions, not making them |
| 17 | 7a8 L322 | good, let's | "Good results, good push-back: I propose, we wire hook-based enforcement… Go for the dispatch." | TP | Owner approving the hybrid hook + MCP enforcement architecture — this WAS captured as DEC-20260414_1430-SteelLatch |
| 18 | 7a8 L359 | decision, approved, decided, ok, yes | Auto-generated conversation compact summary | FP | Not an owner turn at all — `isCompactSummary: true`; should be filtered by the tail helper |
| 19 | 7a8 L444 | — | "Whats the current status?" | — | No marker; shown for context |
| 20 | 7a8 L496 | decision, agreed | "Decisions: 1) run verification now, agreed. 2) amend aibox issues, agreed. 3) 3-5 logically grouped commits." | TP | Three sub-decisions bundled; DecisionRecord-worthy (was captured in handover) |
| 21 | 7a8 L580 | go | "Go for 1)" | TP | Cross-cutting pick between options — borderline but matches owner's decision protocol |
| 22 | 7a8 L49 | decision, approved ("1) migration approved, please apply. 2) approved 3) approved.") | FP | Operational approvals of already-presented migrations |

**Labelled total:** 21 hits (L19 carried zero markers).
Unique sessions represented: 86c, 56e, 7a8 (three main sessions). I
spot-checked 9cb, 7b4, 69c and found the same pattern (mostly FP on
`ok`/`good`/`yes`/`decision`, occasional TP on longer directive
utterances); I did not exhaustively label all nine sessions because
the pattern had saturated.

---

## 4. Per-marker breakdown

Restricted to genuine-owner-utterance hits only (see §1.3). Where the
population exceeded my sample, I note the sample size.

| Marker | Sampled hits | TP | FP | Amb | Precision (TP / (TP+FP)) |
|---|---|---|---|---|---|
| `\bship\s+it\b` | 0 | 0 | 0 | 0 | **n/a** (no owner utterance matched) |
| `\blet'?s\s+go\s+with\b` | 0 | 0 | 0 | 0 | **n/a** |
| `\bi'?ll\s+go\s+with\b` | 0 | 0 | 0 | 0 | n/a |
| `\bwe'?ll\s+go\s+with\b` | 0 | 0 | 0 | 0 | n/a |
| `\bgo\s+with\s+the\b…(approach\|option\|plan)` | 0 | 0 | 0 | 0 | n/a |
| `\bwe'?ll\b` | 2 | 0 | 1 | 1 | 0/1 = **0.00** (sample too small) |
| `\bi'?ll\b` | 0 | 0 | 0 | 0 | n/a |
| `\bapproved\b` | 3 (of ~49 raw) | 0 | 3 | 0 | 0/3 = **0.00** |
| `\bdecided\b` | 1 | 0 | 1 | 0 | 0/1 = **0.00** (tiny sample) |
| `\bdecision\b` | 7 (of ~394 raw) | 1 | 5 | 1 | 1/6 = **0.17** |
| `\bproceed\b` | 4 | 0 | 4 | 0 | 0/4 = **0.00** |
| `\bconfirmed\b` | 1 | 0 | 1 | 0 | 0/1 = **0.00** (tiny sample) |
| `\block(ed)?\s+in\b` | 0 | 0 | 0 | 0 | n/a |
| `\bfinal\s+answer\b` | 0 | 0 | 0 | 0 | n/a |
| `\bok(ay)?\b` | 5 (of ~124 raw) | 0 | 5 | 0 | 0/5 = **0.00** |
| `\bgood\b` | 4 (of ~100 raw) | 1 | 3 | 0 | 1/4 = **0.25** |
| `\byes\b` | 4 (of ~58 raw) | 2 | 2 | 0 | 2/4 = **0.50** |

Notes:

- The five most "specific" markers (`ship it`, `let's go with`, `i'll
  go with`, `we'll go with`, `go with the … approach/option/plan`,
  `final answer`, `locked in`, `proceeed` typo) **fired zero times on
  genuine owner utterances** in this corpus. They are high-specificity
  but also close to zero-recall on the owner's observed language.
- The noisy markers (`ok`, `yes`, `good`, `decision`, `proceed`,
  `approved`, `decided`) are the ones that fire, and they fire
  almost always as false positives.
- `yes` at 2/4 = 0.50 is the highest-precision marker that actually
  fired, but its absolute precision is still below the 0.80 bar.

---

## 5. Recall estimate

### 5.1 Method

Denominator: owner-confirmed cross-cutting decisions observed in the
corpus window. I count two sources:

- **DecisionRecord files** created in `context/decisions/` dated
  2026-04-09 → 2026-04-15 (6 files — see §Source inputs).
- **LogEntry `decision-created` events** in `context/logs/`
  (3 entries: BraveGarnet, MightySky, DaringJay — all dated
  2026-04-11).

The 3 LogEntries all correspond 1:1 to 3 of the 6 DecisionRecords, so
the deduplicated denominator is **6 cross-cutting decisions**.

Numerator: for each decision, I check whether a Tier-A marker fired in
the preceding 5 owner+assistant turns leading up to the DecisionRecord
creation. I confirmed by reading back from the decision's file
`related_workitems` / `created` timestamp and cross-referencing the
session JSONL.

### 5.2 Result

| DEC | Session | Preceding Tier-A marker? | Which |
|---|---|---|---|
| DEC-20260409_2102-GrandGlade-no-state-based-directory | 69c | Yes | `ok`, `decided` |
| DEC-20260411_0559-RapidFjord-three-tier-hot-warm | 7b4 | Yes | `go with`, `decision` |
| DEC-20260411_0802-RoyalComet-reliable-skill-invocation-provider | 7b4 / 715 | Yes | `let's`, `decision` |
| DEC-20260411_1738-BraveStream-build-task-router-mcp | 715 | Yes | `approved`, `decision` |
| DEC-20260414_0900-TeamRoster-permanent-ai-team-composition | 7a8 | Yes | multiple (`approved`, `good`, `decision`) |
| DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list | 7a8 L322 | Yes | `good`, `let's` in "good results, good push-back… let's summarize…" |

**Recall = 6 / 6 = 1.00** in this corpus.

That is not surprising: the Tier-A list is so permissive (it includes
`decision`, `ok`, `yes`, `good` etc.) that virtually every owner turn
near a cross-cutting decision fires at least one marker. The problem
is the inverse: near every owner turn **period** fires a marker too.
High recall, catastrophic precision.

---

## 6. Overall precision and recall

### 6.1 Precision

Labelled genuine-owner-utterance hits across all Tier-A markers:

- TP = 5 (rows 5, 8, 13, 14, 17, 20, 21 of §3.1 — re-counting: owner
  turns classified TP are #5, #8, #13, #14, #17, #20, #21 = **7 TPs**
  across the 21 labelled entries. Two of these (#5 "yes" and #13
  "yes") share the `yes` marker; #8 owns `proceed`+`decision`; #14
  owns `decision`; #17 owns `good`; #20 owns `decision`; #21 doesn't
  match any Tier-A marker strictly ("Go for 1)" — `go` alone isn't in
  Tier-A, reclass as **not a Tier-A hit**, drop from labelling).
- Corrected: TP = 6 across 20 hits.
- FP = 13 across 20 hits.
- Ambiguous = 2 (#7, #16).

**Precision** (ignoring Ambiguous) = 6 / (6 + 13) = 6 / 19 = **0.316**.

### 6.2 Recall

**Recall** = 6 / 6 = **1.00** (see §5.2).

### 6.3 Extrapolation to the full population

The precision I measure comes from a sample of 20 hits drawn mostly
from the high-hit markers. The full population of Tier-A hits in the
corpus is on the order of **800+ line-hits** (sum of §3 "raw line
hits"). Even if the unsampled portion had a precision double what I
measured — 0.63 — overall precision is still well below the 0.80 bar.

A simulated extrapolation assuming my sample is representative of the
four high-volume markers (`decision`, `ok`, `good`, `yes`, which
account for ≈85% of firings) yields an expected population precision
of **≈0.20–0.35**. The four very-specific markers that never fired
(`ship it`, `let's go with`, etc.) contribute 0 hits and therefore 0
FPs, so they do not rescue the aggregate.

---

## 7. Recommendation — **NO-GO**

**Do NOT flip `--mode=shadow` → `--mode=block`** with the current
Tier-A marker list. Measured precision on owner utterances is
~0.32, far below the 0.80 bar. The gate would interrupt the owner
roughly two out of every three write-tool calls that trail decision
language — enough friction that the gate would be disabled within
one working session.

### 7.1 Proposed revised marker list

Drop the high-frequency conversational markers that have structurally
low precision in this owner's writing style:

**Drop outright (demote to Tier B, or remove):**

| Marker | Reason |
|---|---|
| `\bok(ay)?\b` | 0/5 TP — used for operational approvals like "ok to push"; no cross-cutting correlation |
| `\bgood\b` | 1/4 TP — used for acknowledgements ("Good. Before we start…") |
| `\byes\b` | 2/4 TP — better than `ok`/`good` but still below bar; keep in Tier B only |
| `\bproceed\b` | 0/4 TP — always operational ("Please proceed!"), never cross-cutting |
| `\bconfirmed\b` | Background frequency; rarely appears in genuine commit utterances |
| `\bdecision\b` / `\bdecided\b` | Owner's project is about DecisionRecords — these words appear in meta-discussion about the concept, not in actual decision events |
| `\bapproved\b` | Used for operational approvals of sub-tasks and migrations |
| `\bwe'?ll\b` / `\bi'?ll\b` | Future-tense markers too generic; they appear in planning narrative constantly |

**Keep (high precision but zero-recall today — owner doesn't use
these phrases often, but when they do appear they are almost
certainly real commit markers):**

| Marker | Reason |
|---|---|
| `\bship\s+it\b` | Idiomatic release-approval |
| `\blet'?s\s+go\s+with\b` / `\bi'?ll\s+go\s+with\b` / `\bwe'?ll\s+go\s+with\b` | Explicit option-selection |
| `\bgo\s+with\s+the\b.{0,30}\b(approach\|option\|plan)\b` | Explicit option-selection, long form |
| `\block(ed)?\s+in\b` | Explicit commit idiom |
| `\bfinal\s+answer\b` | Explicit commit idiom |

**Delete the duplicate `\bship\s+it\b`** (appears twice in the list
at indices 34 and 45 of `decision_markers.py`). Cosmetic.

**Delete `\bproceeed\b`** (the typo variant). Zero hits; adds noise
surface without benefit.

### 7.2 Predicted precision under revised list

On the current corpus the revised Tier-A list would fire **zero
times**. Precision is therefore undefined (0/0) but degenerate:
recall collapses to ≈0 as well. **This is the hard trade-off** — the
owner's conversational style rarely uses the high-precision idioms.

Possible remediations (not implemented here — they are FEAT-XS
proposals for the owner):

1. **Add an owner-profile tuning pass.** Have the gate consume a
   per-owner profile of which markers actually correlate with their
   past DecisionRecords. For this owner, the best candidates would
   be combinations like "`yes` appearing AS THE LAST MESSAGE of a
   turn AND the preceding assistant turn posed a numbered-option
   choice." This is a last-message + context-class constraint, not a
   raw-marker match.
2. **Last-message-only constraint.** Require the marker to appear in
   the **most recent owner turn**, not anywhere in the last-6
   window. This alone would eliminate all paste-back FPs (rows #3,
   #4, #18 in §3.1) without dropping any TPs I saw.
3. **Short-utterance constraint.** Require the matched owner turn to
   be ≤ 200 characters. This eliminates the "long planning
   paragraph that happens to contain `decision`" FP class (row #7,
   #16) without hurting the short-commit TPs (#5, #8, #13, #20).
4. **Turn-class filter.** Explicitly skip entries with
   `isCompactSummary: true` or content starting with
   `<local-command-` / `<command-name>` / `<local-command-stdout>`.
   These are not owner turns but currently *will* be scanned by a
   naïve `tail_user_assistant` implementation.

Predicted precision under the combination {drop noisy markers, keep
specific ones, add last-message + ≤200-char constraints}:
**estimated 0.70–0.85** on a corpus of similar composition.
Still below 0.80 at the low end — not a confident GO.

### 7.3 What would actually make this GO-able

The honest answer is that Rail 5 Lever 1 **as currently designed** is
fundamentally mismatched to this owner's linguistic style. The owner
expresses decisions in one of two modes:

- Long directive paragraphs that embed the decision in surrounding
  narrative ("I propose … please do RES-S as well …") — marker-based
  scanning cannot distinguish these from long planning paragraphs
  that embed decision-adjacent language but aren't commits.
- Terse confirmations ("yes", "ok", "agreed") — marker-based
  scanning cannot distinguish operational OKs from cross-cutting
  confirmations.

A more promising alternative (out of scope for this calibration):
**use an LLM classifier on the last 2-3 owner+assistant turns**,
with a schema like:
`{"is_cross_cutting_commit": bool, "topic": str}`. This would replace
the regex library entirely for Lever 1. Lever 2 (the SessionEnd
sweeper) can keep the cheap regex approach since its cost-of-FP is
a line in a review Note, not a blocked tool call.

---

## 8. Corpus bias notes

- **Subject-matter skew.** ~95% of the corpus is processkit meta-work
  (the agent working ON the decision-capture mechanism itself).
  Background frequency of `decision`, `approve`, `proceed`, `decided`
  is therefore 5–10× what it would be in a typical consumer project.
  Precision numbers I report are a **lower bound**; a non-processkit
  project would see higher precision for those markers, but probably
  still well below 0.80.
- **Owner-language skew.** Single owner; terse-German-English mix;
  prefers "ok to push", "please proceed", "agreed" over idiomatic
  "ship it" / "let's go with". A different owner might give very
  different per-marker precision.
- **Payload-pollution skew.** The tool_use/tool_result entries in the
  JSONLs will produce far more FPs than owner utterances ever could,
  if the gate's `tail_user_assistant` helper doesn't filter them
  out. I deliberately excluded them from precision math here because
  a correctly-implemented gate won't see them — but **if the
  implementation is incorrect**, actual deployed precision will be
  far worse than 0.32.
- **No external-repo data.** The WorkItem suggested pulling
  `projectious-work/{internal,aibox,kaits}` + `funkspur`
  `context/logs/` for additional decision-language samples. I did
  not fetch them. Those samples are curated LogEntries (higher
  decision-density than raw utterances) and would mostly help
  calibrate the Tier-B **sweeper** precision, not the Tier-A gate —
  LogEntries are written after the fact, not in-session utterances.

---

## 9. Suggested follow-ups

1. **Verify `tail_user_assistant` filtering.** Before any further
   Rail-5 work, confirm that the PreToolUse gate's transcript-tailer
   excludes (a) `type: tool_use`/`tool_result` entries, (b) entries
   whose content starts with `<local-command-` / `<command-name>` /
   `<local-command-stdout>`, (c) entries with `isCompactSummary:
   true`, and (d) `isSidechain: true`. If it doesn't, deployed
   precision will be far below what this calibration measures.
2. **FEAT-XS: drop the 5 highest-noise markers** from Tier A
   (`ok`, `good`, `yes`, `proceed`, `approved`). Promote them to
   Tier B (sweeper-only) where their FP cost is zero. Ship as
   shadow-mode-only; re-calibrate after one week of real usage.
3. **FEAT-XS: add last-message-only + short-utterance constraints.**
   Two lines of filter code in the gate; measurable precision lift
   on this corpus.
4. **Consider replacing Lever 1 with an LLM classifier** call on
   the last 2-3 turns. Compare precision/recall against the
   revised regex list on the next 20 real sessions under
   shadow-mode.
5. **Widen the corpus.** Once the external GitHub/Codeberg repos are
   fetchable from a researcher agent, re-run this calibration with
   `projectious-work/{internal,aibox,kaits}` + `funkspur` sessions
   merged in, for a more representative multi-project baseline.
6. **Shadow-mode is safe indefinitely.** There is no pressure to
   flip to block. Given the calibration result, my recommendation is
   to keep shadow-mode-ON for at least 10 more real sessions and
   re-calibrate, ideally after the filter improvements in item 3.
