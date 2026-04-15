"""
emit_compliance_contract.py — processkit SessionStart / UserPromptSubmit hook.

WorkItems:
  FEAT-20260414_1433-SteadyHand-provider-neutral-hook-scripts
  FEAT-20260415_1500-PathFinder-session-orientation-provider-neutral
Hooks guide: https://code.claude.com/docs/en/hooks-guide

Purpose
-------
Emit the canonical compliance contract (assets/compliance-contract.md)
to stdout so it lands in the current turn's context.  Wire this script
as a SessionStart AND UserPromptSubmit hook in your harness config.
aibox handles the wiring; see scripts/README.md for the target shape.

Claude Code detection
---------------------
Claude Code 2.1.0+ prefers a JSON envelope on stdout:
    {"hookSpecificOutput": {"additionalContext": "<text>"}}
We detect Claude Code by checking for any of these env vars (set by the
Claude Code runtime before invoking hook scripts):
    CLAUDE_CODE_ENTRYPOINT  — always present in Claude Code 2.x
    CLAUDE_CODE_VERSION     — present in Claude Code 2.1+
    ANTHROPIC_CLAUDE_CODE   — sometimes set by wrapper scripts

Limitation: this heuristic can produce a false positive if a non-Claude
harness sets one of those vars, and a false negative on a very old Claude
Code or a customised wrapper that strips env vars.  The plain-stdout
fallback is safe on both Claude Code (legacy) and Codex CLI.

Exit codes
----------
0  contract emitted successfully
1  contract file missing (error on stderr, nothing useful on stdout)
"""

import hashlib
import json
import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Session-start instruction appended when --include-session-start is given.
# ---------------------------------------------------------------------------
_SESSION_START_LINE = (
    "On session start, run `morning-briefing-generate` before acting."
    " It will read AGENTS.md, the most recent `session.handover` log,"
    " pending migrations under `context/migrations/pending/`,"
    " in-progress WorkItems, and open DecisionRecords."
)

# ---------------------------------------------------------------------------
# Locate the contract relative to this script, not cwd.
# ---------------------------------------------------------------------------
_ASSETS_DIR = Path(__file__).parent.parent / "assets"
_CONTRACT_PATH = _ASSETS_DIR / "compliance-contract.md"

_CLAUDE_CODE_ENV_INDICATORS = (
    "CLAUDE_CODE_ENTRYPOINT",
    "CLAUDE_CODE_VERSION",
    "ANTHROPIC_CLAUDE_CODE",
)


def _is_claude_code() -> bool:
    """Return True when we believe we're running inside Claude Code 2.1+."""
    return any(os.environ.get(var) for var in _CLAUDE_CODE_ENV_INDICATORS)


def main() -> int:
    include_session_start = "--include-session-start" in sys.argv[1:]

    if not _CONTRACT_PATH.exists():
        print(
            f"ERROR: compliance-contract.md not found at {_CONTRACT_PATH}; "
            "processkit installation may be incomplete.",
            file=sys.stderr,
        )
        return 1

    contract_text = _CONTRACT_PATH.read_text(encoding="utf-8")

    if _is_claude_code():
        # Claude Code 2.1.0+ preferred form: JSON envelope.
        additional_context = contract_text
        if include_session_start:
            additional_context = (
                contract_text.rstrip("\n")
                + "\n\n"
                + _SESSION_START_LINE
                + "\n"
            )
        output = json.dumps(
            {
                "hookSpecificOutput": {
                    "additionalContext": additional_context,
                }
            },
            ensure_ascii=False,
        )
        print(output)
    else:
        # Plain stdout — works for Claude Code (legacy) and Codex CLI.
        print(contract_text, end="")
        if include_session_start:
            print("\n" + _SESSION_START_LINE)

    return 0


if __name__ == "__main__":
    sys.exit(main())
