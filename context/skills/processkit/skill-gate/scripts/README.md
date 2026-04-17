# processkit skill-gate hook scripts

WorkItems:
- `FEAT-20260414_1433-SteadyHand-provider-neutral-hook-scripts`
- `FEAT-20260415_1700-QuietLedger-rail5-auto-decision-capture-implementation`

These scripts are shipped by processkit and wired into harness configs by
`aibox sync` (aibox issue 6.2).  They are **stdlib-only Python 3.10+**
with no third-party dependencies.

---

## Scripts

### `emit_compliance_contract.py`

**Event:** `SessionStart` and `UserPromptSubmit`

Reads `assets/compliance-contract.md` relative to its own location and
emits it to stdout, injecting it into the turn's context.

**Claude Code 2.1.0+ (preferred):** if any of `CLAUDE_CODE_ENTRYPOINT`,
`CLAUDE_CODE_VERSION`, or `ANTHROPIC_CLAUDE_CODE` is set in the
environment, emits JSON:

```json
{"hookSpecificOutput": {"additionalContext": "<contract text>"}}
```

**Fallback:** plain text on stdout (works for Claude Code legacy and Codex CLI).

**Exit codes:** `0` success, `1` contract file missing (stderr explains).

---

### `check_route_task_called.py`

**Event:** `PreToolUse`

Gates write-side processkit tools and generic file writes under
`context/` until `acknowledge_contract(version='v2')` has been called.

**Locked tool names** (always gated regardless of path):

```
create_workitem  transition_workitem  record_decision  link_entities
open_discussion  create_artifact      log_event        create_note
```

**Generic file tools** (`Write`, `Edit`, `MultiEdit`, `Bash`) are gated
only when the target path resolves under `context/`.

**Session-ID precedence:**
1. `session_id` field in hook input JSON
2. `PROCESSKIT_SESSION_ID` env var
3. `str(os.getpid())`

**Exit codes:** `0` pass, `2` block (stderr message shown to user).

---

### `decision_markers.py` *(Rail-5 shared library)*

Shared regex library for detecting decision language in text.

**Two marker tiers:**

- **Tier A** (high-precision, Lever 1 gate trigger): `we'll`, `i'll`,
  `let's go with`, `approved`, `decided`, `ship it`, `ok(ay)?`,
  `good`, `yes`, `proceed`, `confirmed`, `locked in`, `final answer`.
- **Tier B** (softer, Lever 2 sweeper only): `makes sense`, `right call`,
  `i think`, `probably`, `seems`, `agreed`, `sure`, `sounds good/right`,
  `we picked/chose/settled on`, `let's`.

**API:**

```python
from decision_markers import scan, MatchResult

hits = scan(text, tier="A")       # Tier A only
hits = scan(text, tier="B")       # Tier B only
hits = scan(text, tier="A+B")     # Both tiers (sweeper use)
```

Returns `list[MatchResult]` — each with `.pattern`, `.match`, `.start`, `.end`, `.tier`.

---

### `check_decision_captured.py` *(Rail-5 Lever 1)*

**Event:** `PreToolUse`

**Default mode: shadow (warn, do not block).** Pass `--mode=block` to enable blocking.

Reads `transcript_path` from the hook input, scans the last 5 user messages
for Tier-A decision language. If markers are found and no `record_decision`
or `skip_decision_record` ack is present for this session:

- **Shadow mode (default):** exit 0 + one-line warning to stderr:
  `[rail-5 shadow] Tier-A decision marker detected …`
- **Block mode (`--mode=block`):** exit 2 + remediation message:
  `[rail-5] Call record_decision() or skip_decision_record(reason='…') before continuing.`

On non-Claude-Code harnesses (no `transcript_path`): logs to stderr and exits 0.

**Session acknowledgement files read (either is sufficient):**
- `context/.state/skill-gate/session-<SID>.decision-skip` — written by
  `skip_decision_record` MCP tool; expires after 24 h.
- `context/.state/skill-gate/session-<SID>.decision-observed` — written by
  `record_decision_observer.py`.

**Exit codes:** `0` pass (always in shadow mode; or when no markers / ack present in block mode), `2` block (block mode only).

---

### `record_decision_observer.py` *(Rail-5 Lever 1 dedup feed)*

**Event:** `PostToolUse`

Observes `record_decision` calls and writes a session marker at
`context/.state/skill-gate/session-<SID>.decision-observed`.

Never blocks. Exit 0 in all cases.

---

### `decision_sweeper.py` *(Rail-5 Lever 2)*

**Event:** `SessionEnd`

Scans the full session transcript for Tier-A + Tier-B markers (higher
recall). Writes a Note artifact at:

```
context/notes/NOTE-<SESSION_ID>-decision-candidates.md
```

The note has frontmatter tag `decision-candidates` and a table of marker
hits with snippet, timestamp, and whether `record_decision` was observed.

Owner reviews async; promotes real decisions via `record_decision` or
discards false positives.

Never blocks. Exit 0 in all cases. On non-Claude-Code harnesses (no
`SessionEnd` event), this script is simply not wired — document this in
the per-harness hook config.

---

## Wiring targets for `aibox sync`

### Claude Code — `.claude/settings.json`

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 context/skills/processkit/skill-gate/scripts/emit_compliance_contract.py"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 context/skills/processkit/skill-gate/scripts/emit_compliance_contract.py"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit|create_workitem|transition_workitem|record_decision|link_entities|open_discussion|create_artifact|log_event|create_note",
        "hooks": [
          {
            "type": "command",
            "command": "python3 context/skills/processkit/skill-gate/scripts/check_route_task_called.py"
          }
        ]
      },
      {
        "matcher": "create_workitem|transition_workitem|record_decision|link_entities|open_discussion|create_artifact|log_event|create_note|Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "python3 context/skills/processkit/skill-gate/scripts/check_decision_captured.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "record_decision",
        "hooks": [
          {
            "type": "command",
            "command": "python3 context/skills/processkit/skill-gate/scripts/record_decision_observer.py"
          }
        ]
      }
    ],
    "SessionEnd": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "python3 context/skills/processkit/skill-gate/scripts/decision_sweeper.py"
          }
        ]
      }
    ]
  }
}
```

**Rail-5 `--mode` flag:** To enable blocking mode for `check_decision_captured.py`,
change the command to:

```
python3 context/skills/processkit/skill-gate/scripts/check_decision_captured.py --mode=block
```

Default is shadow mode (warn to stderr, do NOT block). Run 20 sessions in
shadow mode before flipping to block — see calibration WorkItem.

### Codex CLI — `.codex/hooks.json`

```json
{
  "hooks": {
    "session_start": {
      "command": "python3 context/skills/processkit/skill-gate/scripts/emit_compliance_contract.py"
    },
    "user_prompt_submit": {
      "command": "python3 context/skills/processkit/skill-gate/scripts/emit_compliance_contract.py"
    }
  }
}
```

> **Known limitation (Codex):** as of 2026-04-14, Codex CLI `PreToolUse`
> only intercepts `Bash` calls (upstream openai/codex#16732).
> `check_route_task_called.py` and `check_decision_captured.py` are NOT
> wired for `PreToolUse` on Codex.  `aibox sync` should log this limitation
> for Codex-only projects.  The scripts remain deployable without change
> once Codex lifts the restriction.

> **Rail-5 Lever 2 (Codex):** `decision_sweeper.py` can be wired to Codex
> `SessionEnd` when that event's input shape is confirmed (see open question
> in ART-20260415_1600-QuietLedger).

---

## Running tests

```sh
python3 context/skills/processkit/skill-gate/scripts/test_hooks.py
```

All tests are stdlib-only and self-contained.
