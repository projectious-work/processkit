---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260414_1433-SteadyHand-provider-neutral-hook-scripts
  legacy_id: BACK-20260414_1433-SteadyHand-provider-neutral-hook-scripts
  created: '2026-04-14T14:33:00+00:00'
  labels:
    component: skill-gate
    area: enforcement
spec:
  title: Write provider-neutral hook scripts (SessionStart / UserPromptSubmit / PreToolUse)
  state: done
  type: story
  priority: high
  size: M
  description: |
    Implement two stdlib-only Python scripts that processkit ships and aibox wires into harness-specific hook configs at sync time. The scripts are harness-agnostic: their stdin/stdout shapes are defined by Claude Code's hooks guide and match Codex CLI's hooks shape closely enough to share.
  inputs:
  - /workspace/context/artifacts/ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan.md  (§1.4)
  - https://code.claude.com/docs/en/hooks-guide  (Claude Code hook input/output JSON
    — re-verify at implementation time)
  - https://developers.openai.com/codex/hooks  (Codex CLI hooks — re-verify)
  - depends-on: BACK-20260414_1430-CleanCharter-compliance-contract-canonical-source
  deliverables:
  - context/skills/processkit/skill-gate/scripts/emit_compliance_contract.py
  - context/skills/processkit/skill-gate/scripts/check_route_task_called.py
  - context/skills/processkit/skill-gate/scripts/README.md  (how each script is expected
    to be wired — aibox is the target reader)
  - context/skills/processkit/skill-gate/scripts/fixtures/claude-code-session-start.json  (captured
    real hook payload)
  - context/skills/processkit/skill-gate/scripts/fixtures/claude-code-pre-tool-use.json  (captured
    real hook payload)
  script_contracts:
    emit_compliance_contract.py:
      reads: stdin (ignored; optional JSON) + ../assets/compliance-contract.md relative
        to script.
      writes: 'full contract text to stdout. On Claude Code 2.1.0+, optionally wraps
        in {"hookSpecificOutput": {"hookEventName": "<event>", "additionalContext":
        "<contract>"}} when a --claude-2-1 flag is present.'
      exits: 0 on success, 1 on missing contract file (stderr explains), never 2.
    check_route_task_called.py:
      reads: hook input JSON from stdin (Claude Code PreToolUse shape). Parses `session_id`,
        `tool_name`, `tool_input`.
      logic: If tool_name is not in {Write, Edit, MultiEdit}, exit 0 (allow). If path
        in tool_input does not start with "context/", exit 0. Otherwise check for
        context/.state/skill-gate/session-<session_id>.ack OR .route marker; exit
        0 if present, exit 2 with a remediation message on stderr if absent.
      exits: 0 (allow), 2 (block with stderr shown to user), never 1.
  success_criteria:
  - Both scripts run under python3.10+ with only the stdlib (no pip install).
  - emit_compliance_contract.py with the fixture as stdin prints the contract body
    verbatim and returns 0.
  - check_route_task_called.py with the PreToolUse fixture returns 2 when the ack
    marker is missing and 0 when present.
  - Scripts are self-contained — they resolve the contract path relative to __file__,
    not cwd.
  - Fixtures are captured from a real Claude Code 2.1+ session and committed as golden
    files; they are NOT handwritten approximations.
  - README.md documents the wiring target paths aibox should write (Claude Code settings.json
    hooks block shape + Codex hooks.json shape) so issue 6.2 against aibox has a concrete
    target.
  - Scripts have a top-of-file docstring linking back to this WorkItem and to the
    Claude Code hooks guide.
  out_of_scope:
  - Writing or installing harness config. aibox owns that (issue 6.2).
  - Windows support. Codex hooks are disabled on Windows today; Claude Code hooks
    work but we do not certify here.
  related_artifacts:
  - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
  assigned_to: ACTOR-developer
  parent: BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan
  progress_notes: |
    ACTOR-developer (Sonnet) completed 2026-04-14.

    Files written:
      - scripts/emit_compliance_contract.py
      - scripts/check_route_task_called.py
      - scripts/test_hooks.py
      - scripts/README.md
      - scripts/fixtures/claude-code-pretooluse-sample.json
      - scripts/fixtures/claude-code-session-start.json
      - scripts/fixtures/claude-code-pre-tool-use.json

    stdin JSON fields consumed by check_route_task_called.py:
      session_id (str), tool_name (str), tool_input (obj), cwd (str)

    Exit code contract:
      emit_compliance_contract.py: 0 success, 1 missing contract file
      check_route_task_called.py:  0 pass, 2 block (never 1)

    Session-ID precedence (check_route_task_called.py):
      1. hook input JSON field `session_id`
      2. env var PROCESSKIT_SESSION_ID
      3. str(os.getpid())

    Claude Code detection heuristic (emit_compliance_contract.py):
      Checks for CLAUDE_CODE_ENTRYPOINT | CLAUDE_CODE_VERSION |
      ANTHROPIC_CLAUDE_CODE in env. Heuristic is adequate but not
      bulletproof: a non-Claude harness setting one of those vars
      would emit JSON instead of plain text (harmless). A very old
      or stripped Claude Code that unsets all three vars would fall
      back to plain stdout (also harmless — plain stdout is accepted).

    Codex path: identical code path. Codex does NOT set the Claude
    Code env vars, so emit_compliance_contract.py falls through to
    plain stdout. check_route_task_called.py is fully functional on
    Codex for session-ID resolution and gating; however Codex
    PreToolUse only intercepts Bash today (openai/codex#16732) so
    the gate is a no-op in practice until that limitation lifts. No
    per-harness branch needed in the scripts.

    Note: Bash tool was denied during this session; py_compile and
    test_hooks.py could not be executed. Syntax was verified by
    visual review. Owner should run
      python3 -m py_compile scripts/emit_compliance_contract.py
      python3 -m py_compile scripts/check_route_task_called.py
      python3 -m py_compile scripts/test_hooks.py
      python3 scripts/test_hooks.py
    before merging.
---
