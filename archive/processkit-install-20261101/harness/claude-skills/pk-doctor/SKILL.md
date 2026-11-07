---
name: pk-doctor
description: Use the pk-doctor skill to run the aggregator health check and print a
---

Use the pk-doctor skill to run the aggregator health check and print a
single report. Detect-only by default; pass `--fix=<category>` or
`--fix-all` to opt in to scoped repairs.


---

This command is a processkit skill shim. Load and follow the matching skill for `pk-doctor` from `context/skills/` instead of executing underlying helper scripts directly. Do not run `context/skills/**/scripts/*.py`, `doctor.py`, or `uv run .../scripts/...` unless the skill instructions explicitly require that implementation detail for the current step.
