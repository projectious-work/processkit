---
name: pk-resume
description: Use the status-briefing skill to generate a session-start orientation
---

Use the status-briefing skill to generate a session-start orientation
and catch-up summary.

Before writing the briefing, query `migration-management` for pending
and in-progress migrations. If any exist, surface them before normal
priorities and propose the next action: review, apply, continue, or
reject via the migration-management MCP tools. Do not apply or reject a
migration unless the user explicitly asks.


---

This command is a processkit skill shim. Load and follow the matching skill for `pk-resume` from `context/skills/` instead of executing underlying helper scripts directly. Do not run `context/skills/**/scripts/*.py`, `doctor.py`, or `uv run .../scripts/...` unless the skill instructions explicitly require that implementation detail for the current step.
