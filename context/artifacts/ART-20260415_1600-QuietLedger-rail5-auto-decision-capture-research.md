---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260415_1600-QuietLedger-rail5-auto-decision-capture-research
  created: 2026-04-15T16:00:00Z
spec:
  name: "Rail 5 research — auto-capture of decisions from planning discussions"
  kind: document
  location: context/artifacts/ART-20260415_1600-QuietLedger-rail5-auto-decision-capture-research.md
  format: markdown
  version: "1.0.0"
  tags: [research, enforcement, rail5, decision-record, hooks, provider-neutral]
  produced_by: BACK-20260415_1520-GapScout-enforcement-rail5-auto-decision-capture
  owner: ACTOR-sr-researcher
  links:
    workitem: BACK-20260415_1520-GapScout-enforcement-rail5-auto-decision-capture
    inputs:
      - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
      - ART-20260414_1545-SharpGrid-follow-up-harness-capability-matrix
    related_decisions:
      - DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list
---

# Rail 5 research — auto-capture of decisions from planning discussions

**Author:** Senior Researcher (Opus) — ACTOR-sr-researcher
**Date:** 2026-04-15
**Parent WorkItem:** `BACK-20260415_1520-GapScout-enforcement-rail5-auto-decision-capture`

---

## 1. Methodology

Sources used:

- Primary: `code.claude.com/docs/en/hooks` (Claude Code hooks
  reference) — fetched directly; schema confirmed.
- Primary: `developers.openai.com/codex/hooks` — WebFetch blocked;
  relied on WebSearch snippets + github.com/openai/codex issue
  #16732 (PreToolUse Bash-only limitation) and discussion #2150.
- Primary: `cursor.com/docs/hooks` — WebSearch snippets; secondary
  GitButler deep-dive (blog.gitbutler.com/cursor-hooks-deep-dive).
- Primary: `opencode.ai/docs/commands/`, `opencode.ai/docs/plugins/`.
- Upstream artifacts: SharpGrid capability matrix (2026-04-14),
  SteadyBeacon implementation plan (2026-04-14).
- Codebase: `skill-gate/scripts/check_route_task_called.py` (existing
  PreToolUse gate shape we extend), `skill-gate/SKILL.md`,
  `decision-record/SKILL.md` + `commands/decision-record-write.md`.

Confidence convention (unchanged from prior rail research):
**Confirmed** (primary doc) / **Likely** (multiple secondary or
strong inference) / **Weak** (single secondary) / **Speculation**
(no source).

All web claims dated 2026-04-15; re-verify at implementation time.

---

## 2. Lever 1 — pre-action decision check

### 2.1 PreToolUse transcript access (the crux)

**Confirmed.** Claude Code's PreToolUse hook input includes
`transcript_path`, a JSONL file path to the live session transcript.
Exact fields per the hooks reference:

```
session_id, transcript_path, cwd, permission_mode,
hook_event_name, tool_name, tool_input, tool_use_id
```

The transcript JSONL contains user and assistant turns. The hook is
a stdlib-only Python process — it can open the file, tail the last
N entries, regex for markers, and decide. No additional SDK
dependency needed.

Source: https://code.claude.com/docs/en/hooks (Confirmed, 2026-04-15)

Implication: Lever 1 is **deliverable on Claude Code today**. The
starting hypothesis in the WorkItem (that PreToolUse might see only
the tool call) was the pessimistic case; the actual schema is the
optimistic case.

### 2.2 N-window choice

**Recommendation: N = 6 messages (3 user + 3 assistant turns).**
Confidence: **Weak** — no empirical measurement was available;
reasoning only.

- N = 5 (hypothesis) has an odd number so the split between user
  and assistant sides is asymmetric — if the decision language is
  in the assistant's turn just before the write tool, a user-only
  scan of the last 5 user messages may miss it.
- N = 10 inflates false-positive rate: planning drift across a
  longer horizon reuses decision-language markers ("let's") for
  sub-steps that were already resolved.
- N = 6 (three turn-pairs) covers one typical "propose → clarify →
  confirm" cycle without reaching back into earlier settled topics.

Concretely the scan window should be **the last 6 transcript
entries of kind user|assistant**, not the last 6 messages of any
kind (tool_use / tool_result entries inflate the count without
carrying decision language).

### 2.3 Marker list (precision/recall)

Empirical measurement against 20 real sessions was out of scope for
this research (no session-transcript access from this harness turn).
Recommendation is a **two-tier marker list** the implementer
calibrates against a sample once measurement is possible:

**Tier A — high-precision commit markers** (trigger the gate):

- `\bship it\b`
- `\blet'?s go with\b`
- `\bi'?ll go with\b`
- `\bwe'?ll go with\b`
- `\bgo with the\b.{0,30}\b(approach|option|plan)\b`
- `\bdecided\b` / `\bdecision\b` / `\bapproved\b`
- `\block(ed)? in\b`
- `\bfinal answer\b`

**Tier B — soft markers** (do NOT fire gate alone; require Tier A
co-occurrence in the window):

- `\bok(ay)?\b`, `\byes\b`, `\bsure\b`, `\bagreed\b`, `\bgood\b`
- `\bsounds (good|right)\b`

Reasoning: owner-flagged markers like "ok" and "yes" have such high
background frequency that they will dominate false positives. Using
them only as confirmers of a Tier A marker earlier in the window
keeps recall up without spamming the gate.

Confidence: **Speculation** on exact marker set; **Likely** on the
two-tier structure (standard NLP intent-detection pattern).

### 2.4 Dedup vs existing DecisionRecord

Options considered:

1. **Content hash of the decision topic.** Fragile — same decision
   gets worded differently in subsequent turns.
2. **Session-scoped "recent decision" cache.** A marker file at
   `context/.state/skill-gate/session-<SESSION_ID>.decisions`
   listing timestamps of `record_decision` calls observed via
   PostToolUse. If a `record_decision` fired in the last M minutes
   (M=10), suppress the gate. **Recommended.**
3. **Query the DecisionRecord index.** Higher latency, and the
   decision may be about something already-recorded months ago —
   spurious dedup.

The cache-file approach (option 2) reuses the existing state
directory pattern (`context/.state/skill-gate/`) that
`check_route_task_called.py` already uses. It requires a companion
PostToolUse hook that appends a timestamp line when `record_decision`
succeeds. Confidence: **Likely** workable; one-session-scope is
sufficient for the gap this rail closes.

### 2.5 Proposed PreToolUse hook pseudocode

Location: `context/skills/processkit/skill-gate/scripts/check_decision_captured.py`
(sibling of `check_route_task_called.py`). Same stdio contract, same
exit-code semantics.

```python
# check_decision_captured.py — PreToolUse gate for decision capture.
#
# Fires before write-side tools that are NOT record_decision itself.
# If recent user/assistant turns contain Tier-A decision-language
# markers AND no record_decision has been observed in the dedup
# window, exit 2 with a remediation message asking for either a
# record_decision call or an explicit skip_decision_record(reason=).

GATED_TOOLS = {
    "create_workitem", "transition_workitem", "create_artifact",
    "log_event", "create_note", "Write", "Edit", "MultiEdit",
}
# Note: record_decision is NOT gated (it IS the remediation path).

DEDUP_WINDOW_SECONDS = 600  # 10 minutes
SCAN_WINDOW_ENTRIES = 6     # last 6 user|assistant entries

def main():
    hook = json.loads(sys.stdin.read() or "{}")
    tool = hook.get("tool_name", "")
    if tool not in GATED_TOOLS:
        return 0

    transcript = Path(hook["transcript_path"])
    sid = hook.get("session_id") or env_sid() or str(os.getpid())

    # 1. Dedup — did record_decision fire recently in this session?
    if recent_decision_recorded(sid, DEDUP_WINDOW_SECONDS):
        return 0

    # 2. Scan last N user|assistant entries for Tier-A markers.
    entries = tail_user_assistant(transcript, SCAN_WINDOW_ENTRIES)
    if not has_tier_a_marker(entries):
        return 0

    # 3. Check for explicit skip acknowledgement.
    if skip_ack_present(sid):
        return 0

    print(REMEDIATION_MSG, file=sys.stderr)
    return 2  # block until agent calls record_decision or skip_*
```

Companion scripts needed:

- `record_decision_observer.py` — PostToolUse hook, matcher
  `record_decision`, appends timestamp to
  `context/.state/skill-gate/session-<SID>.decisions`.
- A tiny MCP tool `skip_decision_record(reason: str)` on
  `skill-gate` that writes `session-<SID>.skip-decision` — the
  owner-approved escape hatch from the WorkItem spec.

### 2.6 Lever 1 summary table

| Question | Answer | Confidence |
|---|---|---|
| PreToolUse transcript access? | Yes — `transcript_path` in input | Confirmed |
| N window | 6 user/assistant entries | Weak |
| Markers | Two-tier (A=trigger, B=confirmer) | Likely |
| Dedup strategy | Session-scoped `.decisions` cache file | Likely |
| Delivery surface | New script in `skill-gate/scripts/` | Confirmed |

---

## 3. Lever 2 — SessionEnd sweeper

### 3.1 Does SessionEnd exist?

| Harness | SessionEnd / equivalent | Confidence | Notes |
|---|---|---|---|
| Claude Code | **Yes.** `SessionEnd` event with matchers `clear`, `resume`, `logout`, `prompt_input_exit`, `bypass_permissions_disabled`, `other`. Input includes `session_id`, `transcript_path`, `cwd`, `reason`. Cannot block (stderr only). | Confirmed | code.claude.com/docs/en/hooks |
| Codex CLI | **Yes.** SessionEnd listed as once-per-session cadence alongside SessionStart. JSON-on-stdin shape follows same pattern. | Likely | developers.openai.com/codex/hooks (WebSearch snippet, WebFetch denied) |
| Cursor | **Yes.** `sessionEnd` in v1.7 hooks.json event list. Plus `stop` event ("task completed"). | Likely | cursor.com/docs/hooks |
| OpenCode | **Partial.** `session.compacted` exists; explicit `session.end` not confirmed in docs. Plugin `session.created` is the documented one. | Weak | opencode.ai/docs/plugins |
| Aider | No hook system at all. | Confirmed | (SharpGrid matrix, 2026-04-14) |

Known gotcha (Claude Code): issue anthropics/claude-code#6428 —
SessionEnd does not always fire on `/clear` despite being documented
to. Implementation should treat SessionEnd as **best-effort**, not
guaranteed.

### 3.2 Output format

Owner UX preference answer: **write-only, async log.** Reasoning:

- Asking at session end forces a synchronous turn right when the
  owner has mental closure. High friction.
- A transient stdout list is lost if the terminal scrolls or the
  session is closed by `/clear`.
- A durable artifact review-able at leisure matches existing
  `note-management` patterns already in the skill catalog.

Concrete proposal: write a Note (primitive) per sweep run at
`context/notes/NOTE-<timestamp>-session-sweep.md` with a list of
candidate decisions + the transcript excerpts that triggered them.
Owner reviews during the next session; `note-management-review`
promotes the real ones into DecisionRecords and discards the rest.

Confidence: **Likely** — matches existing review pattern.

### 3.3 Heuristic: reuse Lever 1 or separate?

**Recommendation: separate, higher-recall pass.** The gate in
Lever 1 is intentionally precision-biased (only Tier A triggers)
because a false positive blocks a tool call — expensive friction.
The sweeper is advisory, so the cost of a false positive is a Note
line the owner skims and discards — cheap. Therefore the sweeper
should use Tier A **plus** Tier B, plus sentence-level patterns
like `/\bwe (picked|chose|settled on)\b/i`.

Implementation: share the marker-regex library between the two
scripts but parameterise the tier filter. One file, two entry
points.

### 3.4 Lever 2 summary

| Question | Answer | Confidence |
|---|---|---|
| SessionEnd exists? | Claude Code Confirmed; Codex/Cursor Likely; OpenCode Weak | — |
| Output format | Note artifact (async review) | Likely |
| Reuse Lever 1 heuristic? | Share regex library; higher-recall tier filter | Likely |
| Owner UX | Write-only log, no end-of-session prompt | Confirmed (owner-stated preference) |

---

## 4. Lever 3 — `/decide` slash command

### 4.1 Per-harness slash-command surface

| Harness | Custom slash commands? | Confidence | Mechanism |
|---|---|---|---|
| Claude Code | Yes. Markdown files in `.claude/commands/` or skill `commands/` dir. | Confirmed | code.claude.com/docs/en/slash-commands |
| Codex CLI | **Built-in only** (`/exit`, `/help` etc). Custom commands not a documented feature as of 2026-04. | Weak | developers.openai.com/codex/cli |
| Cursor | Limited. Cursor has its own `/` prompt conventions but no user-configurable slash registry documented. | Weak | — |
| OpenCode | Yes. Markdown files in `commands/` with YAML frontmatter. Can override built-ins. Plugin-command PR #7563 extends. | Confirmed | opencode.ai/docs/commands |
| Aider | No. | Confirmed | — |

### 4.2 Provider-neutral fallback

Slash commands are **not** a universally portable surface. The
provider-neutral fallback for harnesses without them is simply
**typing the natural-language phrase "record decision: <summary>"**,
which AGENTS.md + the `decision-record` skill's trigger phrases
already cover.

Put differently: `/decide` is pure ergonomics on harnesses that
support it, and a no-op on the others (the natural-language path
already works everywhere). There is no structural gap to close for
the non-slash harnesses — they already have the decision-record
skill's trigger phrases.

### 4.3 Home: `decision-record` or `skill-gate`?

**Recommendation: `decision-record/commands/decide.md` as a thin
alias of `decision-record-write`.**

Reasoning (no-skill-inflation rule from the WorkItem):

- `decision-record` already owns the `decision-record-write` and
  `decision-record-query` commands. A second slash command in the
  same skill is zero new skills.
- Putting it in `skill-gate` would be semantically wrong —
  `skill-gate` is about *enforcement*, and `/decide` is about
  *ergonomic invocation of an existing primitive*.
- The alias is trivially two lines:
  ```markdown
  ---
  argument-hint: decision-title
  allowed-tools: []
  ---
  Use the decision-record skill to record a new decision titled $ARGUMENTS.
  ```
  (Same body as `decision-record-write.md`, just shorter filename.)

OpenCode format differs slightly but the content stays the same;
aibox's installer handles path translation (analogous to how it
handles `mcp-config.json` translation).

### 4.4 Lever 3 summary

| Question | Answer | Confidence |
|---|---|---|
| Slash surface | Claude Code + OpenCode yes; Cursor/Codex/Aider no | Confirmed |
| Provider-neutral fallback | Natural-language trigger via existing skill | Confirmed |
| Home skill | `decision-record/commands/decide.md` (alias) | Likely |
| New skill required? | No | Confirmed |

---

## 5. Per-harness capability matrix

Rows are the three levers. Cells mark deliverability + what remains
after the known bugs/limitations.

| Lever | Claude Code | Codex CLI | Cursor | OpenCode | Aider |
|---|---|---|---|---|---|
| **L1 — PreToolUse decision gate** | Yes. Full transcript access via `transcript_path`. **Primary deliverable.** [Confirmed] | **Degraded.** PreToolUse only emits for Bash (issue openai/codex#16732). The gate fires but mostly no-ops on Codex's non-Bash writes. [Confirmed] | **Yes** via `preToolUse` + `beforeMCPExecution` (v1.7). But hook input lacks transcript path — would need to read Cursor's own session store if reachable. [Likely — transcript access unverified] | **Partial.** `tool.execute.before` blocks native tools only; MCP writes bypass (bug sst/opencode#2319). [Confirmed] | **No.** No hook system. [Confirmed] |
| **L2 — SessionEnd sweeper** | Yes. `SessionEnd` + `transcript_path`. Known flake on `/clear` (issue #6428). [Confirmed] | Yes in principle (SessionEnd listed); scan target is the Codex session log, shape not verified. [Likely] | Yes (`sessionEnd` + `stop`). [Likely] | Weak — `session.created` documented, `session.end` not clearly. `session.compacted` closest. [Weak] | **No.** [Confirmed] |
| **L3 — `/decide` slash command** | Yes — alias file. [Confirmed] | **No native slash surface**; natural-language fallback only. [Weak] | No custom slash surface confirmed. [Weak] | Yes — `commands/decide.md`. [Confirmed] | **No.** [Confirmed] |

Shape identical to ART-SharpGrid §1.

---

## 6. Recommendation

**Build `lever_1 + lever_2` (the first two). Defer Lever 3 to a
trivial follow-on.**

### 6.1 Why this option

**Cost to build:**

- L1: ~1 day. One new PreToolUse script, one PostToolUse observer,
  one small MCP tool (`skip_decision_record`), one session cache
  file format. All patterns already exist in `skill-gate/scripts/`.
- L2: ~0.5 day incremental. Reuses the same regex library; adds a
  SessionEnd script that writes a Note artifact via existing
  `note-management` MCP tool.
- L3: ~30 minutes. Two-line alias markdown file per harness that
  supports it.

Total: ~1.5 dev-days for L1+L2.

**False-positive rate:**

- L1 alone: medium. Gate will fire on some non-decisions. Mitigated
  by the `skip_decision_record` escape hatch, but it still adds
  friction per false positive.
- L1+L2: L2 **corrects** for L1's precision bias. Cases where L1
  fails open (Tier A marker didn't match, decision language was
  colloquial) get surfaced by L2's higher-recall sweep. The owner
  reviews the sweeper's Note async and promotes what L1 missed.
  Net FP experience is **lower friction**, not higher, than L1
  alone.
- Adding L3 changes nothing about FP rate — it is pure ergonomics.

**Owner friction:**

- L1 alone: in-session blocks with remediation. Acceptable but
  interruptive.
- L1+L2: in-session blocks are the gate's job; async Note is
  backstop. Matches the owner's stated preference (WorkItem §3.4)
  for "write to a log the owner reviews async."
- L3: saves 4-5 keystrokes once the owner already decided to
  record. Low marginal value.

**Robustness across harnesses:**

- L1 is best on Claude Code (full power), degraded on Codex (Bash
  only), yes on Cursor (different config key), bypassed on MCP
  writes in OpenCode, impossible on Aider.
- L2 is best on Claude Code, likely on Codex/Cursor, weak on
  OpenCode, impossible on Aider.
- L3 is ergonomics-only. Its absence on Codex/Cursor/Aider is a
  non-issue since the natural-language path covers those.

### 6.2 Why not `lever_1_only`

L1's precision bias is a feature, not a bug — but it means the gap
that motivated this research ("planning discussions that settle on
an approach but don't invoke `record_*`") is only *half* closed.
L2 closes the other half at 50% the incremental cost of L1 and
exactly zero additional MCP surface. Shipping L1 alone locks in the
gap L2 closes without a structural reason.

### 6.3 Why not `all_three`

L3 is cheap but its value is minimal compared to L1+L2 — the
decision-record skill already has trigger phrases, and the 4-5
keystroke savings don't justify a new surface in the plan's scope.
**File L3 as a FEAT-S follow-up**: it can ship opportunistically
when someone is touching `decision-record/commands/` for another
reason. Not urgent, not blocking, not justifying a top-level lever.

### 6.4 Rough effort estimate

| Deliverable | Size | Notes |
|---|---|---|
| `check_decision_captured.py` (L1 gate) | S | Mirror of `check_route_task_called.py`; reuses session-state path |
| `record_decision_observer.py` (L1 dedup feed) | XS | PostToolUse, one-line append |
| `skip_decision_record` MCP tool on skill-gate | S | Two functions + test; same file pattern as `acknowledge_contract` |
| `decision_sweeper.py` (L2 sweeper) | S | SessionEnd; writes Note via `note-management` |
| Shared `decision_markers.py` regex library | XS | Tier A + Tier B tables |
| Compliance contract addendum | XS | One new rule sentence about capture |
| Golden-file fixtures for tests | S | Real transcript JSONL samples |
| aibox wiring issues (Bucket B) | — | 1 issue: wire PostToolUse + SessionEnd on sync |

Total: ~M-size FEAT, one developer, ~1.5-2 days end-to-end including
tests. Comparable to SteadyHand.

---

## 7. Open questions for any follow-on FEAT

1. **Empirical calibration of Tier A vs Tier B markers.** This
   research could not run a 20-session A/B. FEAT should include a
   success criterion: run the hook in shadow-mode (log but never
   block) for 10 real sessions, compute precision/recall against
   owner-labeled decisions, then flip to blocking.
2. **Claude Code `SessionEnd` flakiness on `/clear`** (issue #6428).
   FEAT should either wait for upstream fix or add a UserPromptSubmit
   fallback that detects `/clear` and triggers the sweep manually.
3. **Transcript access on Cursor's `preToolUse` hook.** Unverified
   whether Cursor's hook input includes a transcript-path equivalent.
   If not, Lever 1 on Cursor falls back to stdin-only and the
   transcript-scan feature is Claude-Code-only.
4. **Codex CLI SessionEnd input shape.** Web research could not
   fetch the primary doc directly. Implementation-time probe needed
   before writing the sweeper's Codex fallback.
5. **Dedup window tuning (M=10 min).** Arbitrary. Measure whether
   15 or 30 min better matches real planning-cycle durations.
6. **Interaction with `acknowledge_contract` session markers.**
   Confirm the two session-state files (`session-<SID>.ack` and
   `session-<SID>.decisions`) do not race; they live in the same
   directory but are independent.
7. **Escape hatch discoverability.** If the gate remediation message
   does not clearly surface the `skip_decision_record` path, owners
   will grind against the block. UX copy for the remediation string
   is worth a FEAT-S on its own.

---

## 8. Provenance / sources

| Ref | URL | Used for | Confidence |
|---|---|---|---|
| 1 | https://code.claude.com/docs/en/hooks | PreToolUse schema incl. `transcript_path`; SessionEnd event + matchers | Confirmed |
| 2 | https://github.com/anthropics/claude-code/issues/6428 | SessionEnd `/clear` flake | Confirmed |
| 3 | https://developers.openai.com/codex/hooks | Codex hook cadences (session/turn/tool); hooks.json discovery | Likely (WebFetch denied; WebSearch snippets only) |
| 4 | https://github.com/openai/codex/issues/16732 | PreToolUse Bash-only on Codex | Confirmed |
| 5 | https://cursor.com/docs/hooks | Cursor hooks.json event list incl. sessionEnd, stop, beforeSubmitPrompt | Likely |
| 6 | https://blog.gitbutler.com/cursor-hooks-deep-dive | Cursor hooks practical usage | Likely |
| 7 | https://opencode.ai/docs/commands | OpenCode custom slash commands | Confirmed |
| 8 | https://opencode.ai/docs/plugins | OpenCode plugin lifecycle events | Confirmed |
| 9 | https://github.com/sst/opencode/issues/2319 | MCP tools bypass `tool.execute.before` on OpenCode | Confirmed (via SharpGrid) |
| 10 | https://code.claude.com/docs/en/slash-commands | Claude Code custom slash commands in `.claude/commands/` | Confirmed |
| 11 | ART-20260414_1545-SharpGrid-follow-up-harness-capability-matrix | Cross-harness hook + MCP capability ground truth | — |
| 12 | ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan | Existing Rail 1–4 plan this extends | — |

All web sources verified 2026-04-15; re-verify at implementation.
