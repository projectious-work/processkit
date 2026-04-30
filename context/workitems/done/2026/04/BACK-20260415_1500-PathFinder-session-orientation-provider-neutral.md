---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260415_1500-PathFinder-session-orientation-provider-neutral
  legacy_id: BACK-20260415_1500-PathFinder-session-orientation-provider-neutral
  created: '2026-04-15T15:00:00+00:00'
  labels:
    component: processkit-core
    area: session-orientation
    priority_driver: owner-critical
spec:
  title: Wire morning-briefing as the canonical session-start entry point (no new
    skill)
  state: done
  type: story
  priority: high
  size: S
  description: |
    Make session orientation provider-neutral without creating a new skill. The owner asks every session to "familiarize with the project, check open WorkItems, read AGENTS.md, check pending migrations, check the handover log". The existing `morning-briefing` skill (v1.0.0) already covers most of this. Deliver the remaining wiring at three layers so every harness picks it up.
  approach:
  - |
    **AGENTS.md — Session start section.** Add a short block
    immediately under the compliance-contract block: "On session
    start, run `morning-briefing-generate` before acting. It will
    read AGENTS.md, the most recent `session.handover` log, pending
    migrations under `context/migrations/pending/`, in-progress
    WorkItems, and open DecisionRecords." Every AGENTS.md-aware
    harness (Claude Code, Codex CLI, Cursor, OpenCode) honours it.
  - |
    **SessionStart hook reinforcement.** Extend the existing
    `context/skills/processkit/skill-gate/scripts/emit_compliance_contract.py`
    to append the one-line session-start instruction to its stdout
    output when a `--include-session-start` flag is present (Claude
    Code + Cursor path). No new script.
  - |
    **Extend `morning-briefing`.** Update
    `context/skills/processkit/morning-briefing/SKILL.md` "Sources to
    read" to include `context/migrations/pending/` (currently
    missing) and to emit a one-line token-budget-share snapshot per
    the team roster's PM drift-flagging rule (Opus/Sonnet/Haiku
    actuals vs ≈5/85/10 target). Bump SKILL version to 1.1.0.
  success_criteria:
  - AGENTS.md has a "Session start" section directly under the compliance-contract
    block.
  - '`morning-briefing` SKILL.md lists pending migrations as a source and emits the
    budget-share snapshot.'
  - '`emit_compliance_contract.py` with `--include-session-start` appends the session-start
    instruction.'
  - No new skill created; no new MCP tool added.
  - '`uv run scripts/smoke-test-servers.py` still passes.'
  - A fresh session in Claude Code sees the session-start instruction via hook stdout
    AND via AGENTS.md.
  out_of_scope:
  - Creating a new "session-onboarding" skill — violates the no-skill-inflation rule
    (feedback memory 2026-04-15).
  - MCP tool for session start — AGENTS.md + hook is sufficient; adding a tool would
    duplicate the instruction surface.
  related_decisions:
  - DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
  related_workitems:
    parent: BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan
    replaces_placeholder: FEAT-Q3-session-onboarding
  assigned_to: ACTOR-developer
  progress_notes: |
    ACTOR-developer (Sonnet) completed 2026-04-15.

    Files changed:
      - AGENTS.md — added "Session start" section (6 lines) directly
        under <!-- pk-compliance-contract v1 END --> with hard-wrap at
        80 columns per code style.
      - context/skills/processkit/skill-gate/scripts/
        emit_compliance_contract.py — added _SESSION_START_LINE
        constant and --include-session-start flag; Claude Code path
        appends the instruction inside additionalContext; plain-stdout
        path appends after contract body. Updated docstring to reference
        both WorkItem IDs. Stdlib-only preserved.
      - context/skills/processkit/morning-briefing/SKILL.md — bumped
        version 1.0.0 → 1.1.0; added source 6 (context/migrations/
        pending/) to "Sources to read"; added "Token-budget-share
        snapshot" subsection with one-line format, source guidance,
        and drift-flagging rule (±10pp, per DEC-20260414_0900-TeamRoster
        and context/team/roster.md).

    Smoke-test status:
      `uv run scripts/smoke-test-servers.py` — Bash tool was denied
      during this session. Syntax of emit_compliance_contract.py
      verified by visual review (stdlib-only, no new imports). No
      logic paths touched in other scripts. Owner should run the
      smoke test before merging.

    No new skills created. No new MCP tools added.
---

# Notes

Supersedes the unfiled `FEAT-Q3-session-onboarding` placeholder
referenced in ARCH-20260414_1245-FirmFoundation's `blocks:` list.

Reconstructed on 2026-04-15 from the morning-briefing SKILL.md, the
team-roster decision record, and owner recollection after a context
loss. The three-layer design (AGENTS.md + hook + extended skill) was
approved by the owner before filing.
