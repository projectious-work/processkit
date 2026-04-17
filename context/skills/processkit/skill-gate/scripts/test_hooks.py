"""
test_hooks.py — smoke tests for skill-gate hook scripts.

WorkItems:
  FEAT-20260414_1433-SteadyHand-provider-neutral-hook-scripts
  FEAT-20260415_1700-QuietLedger-rail5-auto-decision-capture-implementation

Run from any directory:
    python3 context/skills/processkit/skill-gate/scripts/test_hooks.py

Or from inside the scripts/ directory:
    python3 test_hooks.py

Exit 0 = all tests passed.
Exit 1 = at least one test failed.
"""

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Locate files relative to this script, not cwd.
# ---------------------------------------------------------------------------
_SCRIPTS_DIR = Path(__file__).parent
_FIXTURES_DIR = _SCRIPTS_DIR / "fixtures"
_EMIT_SCRIPT = _SCRIPTS_DIR / "emit_compliance_contract.py"
_CHECK_SCRIPT = _SCRIPTS_DIR / "check_route_task_called.py"
_CONTRACT = _SCRIPTS_DIR.parent / "assets" / "compliance-contract.md"

_PRETOOLUSE_FIXTURE = _FIXTURES_DIR / "claude-code-pretooluse-sample.json"
_DECISION_MARKERS = _SCRIPTS_DIR / "decision_markers.py"
_CHECK_DECISION = _SCRIPTS_DIR / "check_decision_captured.py"
_RECORD_OBSERVER = _SCRIPTS_DIR / "record_decision_observer.py"
_DECISION_SWEEPER = _SCRIPTS_DIR / "decision_sweeper.py"
_TRANSCRIPT_WITH_DECISIONS = _FIXTURES_DIR / "sample-transcript-with-decisions.jsonl"
_TRANSCRIPT_NO_DECISIONS = _FIXTURES_DIR / "sample-transcript-no-decisions.jsonl"
_PRETOOLUSE_WITH_TRANSCRIPT = _FIXTURES_DIR / "claude-code-pretooluse-with-transcript.json"
_SESSIONEND_FIXTURE = _FIXTURES_DIR / "claude-code-sessionend.json"

PASS = "\033[32mPASS\033[0m"
FAIL = "\033[31mFAIL\033[0m"

failures: list[str] = []


def run(
    script: Path,
    stdin_text: str = "",
    env_override: dict | None = None,
    extra_args: list[str] | None = None,
) -> subprocess.CompletedProcess:
    env = os.environ.copy()
    # Strip Claude Code env vars first so default mode is plain-stdout;
    # env_override wins if a test wants to exercise Claude Code JSON mode.
    for var in ("CLAUDE_CODE_ENTRYPOINT", "CLAUDE_CODE_VERSION", "ANTHROPIC_CLAUDE_CODE"):
        env.pop(var, None)
    if env_override:
        env.update(env_override)
    cmd = [sys.executable, str(script)] + (extra_args or [])
    return subprocess.run(
        cmd,
        input=stdin_text,
        capture_output=True,
        text=True,
        env=env,
    )


def check(name: str, condition: bool, detail: str = "") -> None:
    if condition:
        print(f"  {PASS}  {name}")
    else:
        print(f"  {FAIL}  {name}" + (f": {detail}" if detail else ""))
        failures.append(name)


# ---------------------------------------------------------------------------
# Test 1: emit_compliance_contract.py — plain stdout mode
# ---------------------------------------------------------------------------
print("\n[1] emit_compliance_contract.py — plain stdout")

result = run(_EMIT_SCRIPT)
check("exit 0", result.returncode == 0, f"got {result.returncode}")
check("stdout contains contract marker", "pk-compliance v2" in result.stdout)
check("stderr empty", result.stderr.strip() == "", result.stderr.strip())

# ---------------------------------------------------------------------------
# Test 2: emit_compliance_contract.py — Claude Code JSON envelope mode
# ---------------------------------------------------------------------------
print("\n[2] emit_compliance_contract.py — Claude Code JSON envelope")

result_cc = run(_EMIT_SCRIPT, env_override={"CLAUDE_CODE_ENTRYPOINT": "cli"})
check("exit 0", result_cc.returncode == 0)
try:
    payload = json.loads(result_cc.stdout)
    check("JSON envelope present", "hookSpecificOutput" in payload)
    check(
        "additionalContext contains contract",
        "pk-compliance v2" in payload.get("hookSpecificOutput", {}).get("additionalContext", ""),
    )
except json.JSONDecodeError as exc:
    check("JSON envelope present", False, str(exc))
    check("additionalContext contains contract", False)

# ---------------------------------------------------------------------------
# Test 3: check_route_task_called.py — non-locked tool passes
# ---------------------------------------------------------------------------
print("\n[3] check_route_task_called.py — non-locked tool (Read) passes without marker")

non_locked_input = json.dumps(
    {
        "hook_event_name": "PreToolUse",
        "session_id": "test-session-fixture-999",
        "cwd": "/workspace",
        "tool_name": "Read",
        "tool_input": {"file_path": "context/workitems/foo.md"},
    }
)
result = run(_CHECK_SCRIPT, stdin_text=non_locked_input)
check("exit 0 (pass)", result.returncode == 0, f"got {result.returncode}")
check("stderr empty", result.stderr.strip() == "", result.stderr.strip())

# ---------------------------------------------------------------------------
# Test 4: check_route_task_called.py — fixture, no marker → exit 2
# ---------------------------------------------------------------------------
print("\n[4] check_route_task_called.py — fixture Write on context/ with no marker → exit 2")

fixture_text = _PRETOOLUSE_FIXTURE.read_text(encoding="utf-8")
result = run(_CHECK_SCRIPT, stdin_text=fixture_text)
check("exit 2 (block)", result.returncode == 2, f"got {result.returncode}")
check("remediation message on stderr", "acknowledge_contract" in result.stderr)

# ---------------------------------------------------------------------------
# Test 5: check_route_task_called.py — valid marker → exit 0
# ---------------------------------------------------------------------------
print("\n[5] check_route_task_called.py — Write on context/ with valid marker → exit 0")

# Build a valid marker.
contract_hash = hashlib.sha256(_CONTRACT.read_bytes()).hexdigest()
fixture_data = json.loads(fixture_text)
session_id = fixture_data["session_id"]

with tempfile.TemporaryDirectory() as tmp:
    # Create a fake project root with context/.state/skill-gate/
    project_root = Path(tmp)
    (project_root / "context").mkdir()
    state_dir = project_root / "context" / ".state" / "skill-gate"
    state_dir.mkdir(parents=True)
    marker_path = state_dir / f"session-{session_id}.ack"
    marker_path.write_text(
        json.dumps({"contract_hash": contract_hash, "acknowledged_at": "2026-04-14T14:31:00+00:00"}, indent=2)
        + "\n",
        encoding="utf-8",
    )

    # Point the fixture's cwd at the temp project root.
    fixture_with_tmp_cwd = dict(fixture_data)
    fixture_with_tmp_cwd["cwd"] = str(project_root)
    # Also fix the file_path to be relative so the context check matches.
    fixture_with_tmp_cwd["tool_input"] = {"file_path": "context/workitems/FEAT-fixture.md", "content": "x"}

    result = run(_CHECK_SCRIPT, stdin_text=json.dumps(fixture_with_tmp_cwd))
    check("exit 0 (pass)", result.returncode == 0, f"got {result.returncode}\n    stderr: {result.stderr.strip()}")

# ---------------------------------------------------------------------------
# Test 6: check_route_task_called.py — locked processkit tool, no marker → exit 2
# ---------------------------------------------------------------------------
print("\n[6] check_route_task_called.py — create_workitem (locked MCP tool), no marker → exit 2")

locked_mcp_input = json.dumps(
    {
        "hook_event_name": "PreToolUse",
        "session_id": "test-session-fixture-888",
        "cwd": "/workspace",
        "tool_name": "create_workitem",
        "tool_input": {"title": "New item", "type": "task"},
    }
)
result = run(_CHECK_SCRIPT, stdin_text=locked_mcp_input)
check("exit 2 (block)", result.returncode == 2, f"got {result.returncode}")
check("remediation on stderr", "acknowledge_contract" in result.stderr)

# ---------------------------------------------------------------------------
# Test 7: check_route_task_called.py — malformed JSON input → exit 0 (safe)
# ---------------------------------------------------------------------------
print("\n[7] check_route_task_called.py — malformed JSON → exit 0 (safe, non-blocking)")

result = run(_CHECK_SCRIPT, stdin_text="not valid json")
check("exit 0 (safe pass on bad input)", result.returncode == 0, f"got {result.returncode}")

# ---------------------------------------------------------------------------
# Rail-5 tests — decision_markers.py
# ---------------------------------------------------------------------------
print("\n[8] decision_markers.py — Tier A scan hits on known text")

import importlib.util as _ilu
import sys as _sys

if str(_SCRIPTS_DIR) not in _sys.path:
    _sys.path.insert(0, str(_SCRIPTS_DIR))
import decision_markers as _dm  # noqa: E402

tier_a_text = "Ok, let's go with blue-green. We'll use it. Ship it."
hits_a = _dm.scan(tier_a_text, tier="A")
check("Tier-A scan: at least 2 hits on decision text", len(hits_a) >= 2, f"got {len(hits_a)}")
check("Tier-A scan: all hits have tier=A", all(h.tier == "A" for h in hits_a), str(hits_a))

# ---------------------------------------------------------------------------
print("\n[9] decision_markers.py — Tier A scan zero hits on non-decision text")

no_decision_text = "What is the status of FEAT-001? When was it created?"
hits_none = _dm.scan(no_decision_text, tier="A")
# "ok" is a Tier-A marker; only truly neutral text should have 0 hits.
neutral_text = "What is the status of FEAT-001? When was it created? How many subtasks?"
# This text genuinely has no Tier-A markers.
hits_neutral = _dm.scan(neutral_text, tier="A")
check("Tier-A scan: 0 hits on neutral status-query text", len(hits_neutral) == 0, f"got {len(hits_neutral)}: {hits_neutral}")

# ---------------------------------------------------------------------------
print("\n[10] decision_markers.py — Tier B scan catches soft markers")

soft_text = "That makes sense. Agreed, it seems like the right call."
hits_b = _dm.scan(soft_text, tier="B")
check("Tier-B scan: hits on soft-marker text", len(hits_b) >= 2, f"got {len(hits_b)}")
check("Tier-B scan: all hits have tier=B", all(h.tier == "B" for h in hits_b), str(hits_b))

# ---------------------------------------------------------------------------
print("\n[11] decision_markers.py — A+B scan covers both tiers")

mixed_text = "Ship it. That makes sense."
hits_ab = _dm.scan(mixed_text, tier="A+B")
tiers_seen = {h.tier for h in hits_ab}
check("A+B scan: hits present", len(hits_ab) >= 2, f"got {len(hits_ab)}")
check("A+B scan: both A and B returned", "A" in tiers_seen and "B" in tiers_seen, str(tiers_seen))

# ---------------------------------------------------------------------------
print("\n[12] decision_markers.py — invalid tier raises ValueError")

try:
    _dm.scan("text", tier="C")
    check("invalid tier raises ValueError", False, "no exception raised")
except ValueError:
    check("invalid tier raises ValueError", True)

# ---------------------------------------------------------------------------
# Rail-5 tests — check_decision_captured.py
# ---------------------------------------------------------------------------
print("\n[13] check_decision_captured.py — non-gated tool (Read) exits 0, no stderr")

non_gated_input = json.dumps({
    "hook_event_name": "PreToolUse",
    "session_id": "test-rail5-001",
    "transcript_path": str(_TRANSCRIPT_WITH_DECISIONS),
    "cwd": "/workspace",
    "tool_name": "Read",
    "tool_input": {"file_path": "context/foo.md"},
})
result = run(_CHECK_DECISION, stdin_text=non_gated_input)
check("exit 0 (non-gated tool)", result.returncode == 0, f"got {result.returncode}")
check("stderr empty for non-gated tool", result.stderr.strip() == "", result.stderr.strip())

# ---------------------------------------------------------------------------
print("\n[14] check_decision_captured.py — absent transcript_path exits 0 with note")

no_transcript_input = json.dumps({
    "hook_event_name": "PreToolUse",
    "session_id": "test-rail5-002",
    "transcript_path": "",
    "cwd": "/workspace",
    "tool_name": "create_workitem",
    "tool_input": {"title": "test"},
})
result = run(_CHECK_DECISION, stdin_text=no_transcript_input)
check("exit 0 (no transcript)", result.returncode == 0, f"got {result.returncode}")
check("stderr note about absent transcript", "transcript_path" in result.stderr or "non-Claude" in result.stderr, result.stderr.strip())

# ---------------------------------------------------------------------------
print("\n[15] check_decision_captured.py — shadow mode: Tier-A markers → exit 0 + stderr warning")

shadow_input = json.dumps({
    "hook_event_name": "PreToolUse",
    "session_id": "test-rail5-shadow-001",
    "transcript_path": str(_TRANSCRIPT_WITH_DECISIONS),
    "cwd": "/tmp",
    "tool_name": "create_workitem",
    "tool_input": {"title": "test"},
})
result = run(_CHECK_DECISION, stdin_text=shadow_input)
check("shadow mode: exit 0 (not blocked)", result.returncode == 0, f"got {result.returncode}")
check("shadow mode: [rail-5 shadow] warning on stderr", "[rail-5 shadow]" in result.stderr, repr(result.stderr))

# ---------------------------------------------------------------------------
print("\n[16] check_decision_captured.py — no Tier-A markers → exit 0, no warning")

no_marker_input = json.dumps({
    "hook_event_name": "PreToolUse",
    "session_id": "test-rail5-no-marker-001",
    "transcript_path": str(_TRANSCRIPT_NO_DECISIONS),
    "cwd": "/tmp",
    "tool_name": "create_workitem",
    "tool_input": {"title": "test"},
})
result = run(_CHECK_DECISION, stdin_text=no_marker_input)
check("no markers: exit 0", result.returncode == 0, f"got {result.returncode}")
check("no markers: no [rail-5] on stderr", "[rail-5]" not in result.stderr, repr(result.stderr))

# ---------------------------------------------------------------------------
print("\n[17] check_decision_captured.py — --mode=block + Tier-A markers → exit 2")

block_input = json.dumps({
    "hook_event_name": "PreToolUse",
    "session_id": "test-rail5-block-001",
    "transcript_path": str(_TRANSCRIPT_WITH_DECISIONS),
    "cwd": "/tmp",
    "tool_name": "create_workitem",
    "tool_input": {"title": "test"},
})
result = run(_CHECK_DECISION, stdin_text=block_input, extra_args=["--mode=block"])
check("block mode: exit 2 (blocked)", result.returncode == 2, f"got {result.returncode}")
check("block mode: [rail-5] remediation on stderr", "[rail-5]" in result.stderr, repr(result.stderr))
check("block mode: mentions record_decision", "record_decision" in result.stderr)

# ---------------------------------------------------------------------------
print("\n[18] check_decision_captured.py — --mode=block + skip marker → exit 0 (ack)")

with tempfile.TemporaryDirectory() as tmp:
    project_root = Path(tmp)
    (project_root / "context").mkdir()
    state_dir = project_root / "context" / ".state" / "skill-gate"
    state_dir.mkdir(parents=True)
    from datetime import datetime, timezone, timedelta
    now_dt = datetime.now(timezone.utc)
    expires = (now_dt + timedelta(hours=24)).isoformat()
    sid = "test-rail5-skip-001"
    skip_marker = state_dir / f"session-{sid}.decision-skip"
    skip_marker.write_text(
        json.dumps({"reason": "test", "acknowledged_at": now_dt.isoformat(), "expires_at": expires}) + "\n",
        encoding="utf-8",
    )

    skip_block_input = json.dumps({
        "hook_event_name": "PreToolUse",
        "session_id": sid,
        "transcript_path": str(_TRANSCRIPT_WITH_DECISIONS),
        "cwd": str(project_root),
        "tool_name": "create_workitem",
        "tool_input": {"title": "test"},
    })
    result = run(_CHECK_DECISION, stdin_text=skip_block_input, extra_args=["--mode=block"])
    check("skip marker: exit 0 (allowed despite block mode)", result.returncode == 0, f"got {result.returncode}\n    stderr: {result.stderr.strip()}")

# ---------------------------------------------------------------------------
print("\n[19] record_decision_observer.py — non-record_decision tool → exit 0, no file written")

with tempfile.TemporaryDirectory() as tmp:
    project_root = Path(tmp)
    (project_root / "context").mkdir()
    state_dir = project_root / "context" / ".state" / "skill-gate"
    state_dir.mkdir(parents=True)
    sid = "test-observer-001"

    obs_input = json.dumps({
        "hook_event_name": "PostToolUse",
        "session_id": sid,
        "tool_name": "create_workitem",
        "tool_input": {},
        "cwd": str(project_root),
    })
    result = run(_RECORD_OBSERVER, stdin_text=obs_input)
    check("observer: exit 0 for non-record_decision", result.returncode == 0, f"got {result.returncode}")
    marker_path = state_dir / f"session-{sid}.decision-observed"
    check("observer: no marker written for non-record_decision", not marker_path.exists())

# ---------------------------------------------------------------------------
print("\n[20] record_decision_observer.py — record_decision tool → exit 0, marker written")

with tempfile.TemporaryDirectory() as tmp:
    project_root = Path(tmp)
    (project_root / "context").mkdir()
    state_dir = project_root / "context" / ".state" / "skill-gate"
    state_dir.mkdir(parents=True)
    sid = "test-observer-002"

    obs_input = json.dumps({
        "hook_event_name": "PostToolUse",
        "session_id": sid,
        "tool_name": "record_decision",
        "tool_input": {"title": "Use blue-green deployment"},
        "cwd": str(project_root),
    })
    result = run(_RECORD_OBSERVER, stdin_text=obs_input)
    check("observer: exit 0 for record_decision", result.returncode == 0, f"got {result.returncode}")
    marker_path = state_dir / f"session-{sid}.decision-observed"
    check("observer: marker file written", marker_path.exists())
    if marker_path.exists():
        data = json.loads(marker_path.read_text())
        check("observer: marker has observed_at field", "observed_at" in data, str(data))

# ---------------------------------------------------------------------------
print("\n[21] decision_sweeper.py — transcript with decisions → exit 0, note written")

with tempfile.TemporaryDirectory() as tmp:
    project_root = Path(tmp)
    (project_root / "context").mkdir()
    (project_root / "context" / "notes").mkdir(parents=True)
    state_dir = project_root / "context" / ".state" / "skill-gate"
    state_dir.mkdir(parents=True)
    sid = "test-sweeper-001"

    sweep_input = json.dumps({
        "hook_event_name": "SessionEnd",
        "session_id": sid,
        "transcript_path": str(_TRANSCRIPT_WITH_DECISIONS),
        "cwd": str(project_root),
        "reason": "prompt_input_exit",
    })
    result = run(_DECISION_SWEEPER, stdin_text=sweep_input)
    check("sweeper: exit 0", result.returncode == 0, f"got {result.returncode}")
    notes_dir = project_root / "context" / "notes"
    note_files = list(notes_dir.glob("NOTE-*.md"))
    check("sweeper: note file created", len(note_files) == 1, f"found {len(note_files)}")
    if note_files:
        note_content = note_files[0].read_text()
        check("sweeper: note has decision-candidates tag", "decision-candidates" in note_content)
        check("sweeper: note has table header", "| Tier |" in note_content)

# ---------------------------------------------------------------------------
print("\n[22] decision_sweeper.py — absent transcript_path → exit 0 (graceful degrade)")

sweep_no_transcript = json.dumps({
    "hook_event_name": "SessionEnd",
    "session_id": "test-sweeper-002",
    "transcript_path": "",
    "cwd": "/tmp",
    "reason": "other",
})
result = run(_DECISION_SWEEPER, stdin_text=sweep_no_transcript)
check("sweeper no-transcript: exit 0", result.returncode == 0, f"got {result.returncode}")
check("sweeper no-transcript: stderr note", "no-op" in result.stderr or "transcript_path" in result.stderr, result.stderr.strip())

# ---------------------------------------------------------------------------
# Tests 23-24: False-positive filtering (ART-20260415_2000-ShadowCount §9)
# ---------------------------------------------------------------------------
_TRANSCRIPT_POISON = _FIXTURES_DIR / "sample-transcript-with-poison-entries.jsonl"

print("\n[23] check_decision_captured.py — tool_use block with 'ship it' in payload → no gate fire")
# The poison transcript has a tool_use assistant block containing "ship it" in
# the YAML being written, plus isCompactSummary and isSidechain entries with
# decision markers.  The only genuine user message is a neutral follow-up.
# The gate must NOT fire (no Tier-A hit from non-user content).
poison_shadow_input = json.dumps({
    "hook_event_name": "PreToolUse",
    "session_id": "test-rail5-poison-001",
    "transcript_path": str(_TRANSCRIPT_POISON),
    "cwd": "/tmp",
    "tool_name": "create_workitem",
    "tool_input": {"title": "test"},
})
result = run(_CHECK_DECISION, stdin_text=poison_shadow_input)
check(
    "tool_use poison: exit 0 (no false-positive gate fire)",
    result.returncode == 0,
    f"got {result.returncode}\n    stderr: {result.stderr.strip()}",
)
check(
    "tool_use poison: no [rail-5 shadow] warning emitted",
    "[rail-5" not in result.stderr,
    repr(result.stderr),
)

# ---------------------------------------------------------------------------
print("\n[24] check_decision_captured.py — isCompactSummary entry with markers → not counted")
# Build a minimal in-memory transcript: one isCompactSummary entry that
# contains "ship it approved decided" (would be Tier-A if scanned), plus
# one genuinely neutral real user message.  Gate must not fire.
import tempfile as _tmpfile

with _tmpfile.NamedTemporaryFile(
    mode="w", suffix=".jsonl", delete=False, encoding="utf-8"
) as _tf:
    _tf.write(
        json.dumps({
            "isCompactSummary": True,
            "type": "user",
            "message": {"role": "user", "content": [{"type": "text", "text": "ship it approved decided proceed"}]},
            "timestamp": "2026-04-15T13:00:00Z",
        }) + "\n"
    )
    _tf.write(
        json.dumps({
            "type": "user",
            "message": {"role": "user", "content": [{"type": "text", "text": "What is the weather today?"}]},
            "timestamp": "2026-04-15T13:00:30Z",
        }) + "\n"
    )
    _compact_summary_transcript = _tf.name

compact_input = json.dumps({
    "hook_event_name": "PreToolUse",
    "session_id": "test-rail5-compact-001",
    "transcript_path": _compact_summary_transcript,
    "cwd": "/tmp",
    "tool_name": "create_workitem",
    "tool_input": {"title": "test"},
})
result = run(_CHECK_DECISION, stdin_text=compact_input)
check(
    "isCompactSummary: exit 0 (filtered, not counted as Tier-A)",
    result.returncode == 0,
    f"got {result.returncode}\n    stderr: {result.stderr.strip()}",
)
check(
    "isCompactSummary: no [rail-5 shadow] warning emitted",
    "[rail-5" not in result.stderr,
    repr(result.stderr),
)
# Clean up temp file.
Path(_compact_summary_transcript).unlink(missing_ok=True)

# ---------------------------------------------------------------------------
# Summary
# ---------------------------------------------------------------------------
print()
if failures:
    print(f"FAILED ({len(failures)} test(s)):", ", ".join(failures))
    sys.exit(1)
else:
    print(f"All tests passed.")
    sys.exit(0)
