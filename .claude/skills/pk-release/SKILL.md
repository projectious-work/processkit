---
name: pk-release
description: "Use the release-semver skill to prepare a $ARGUMENTS release: bump"
---

Use the release-semver skill to prepare a $ARGUMENTS release: bump
version, draft changelog, create tag.


---

This command is a processkit skill shim. Load and follow the matching skill for `pk-release` from `context/skills/` instead of executing underlying helper scripts directly. Do not run `context/skills/**/scripts/*.py`, `doctor.py`, or `uv run .../scripts/...` unless the skill instructions explicitly require that implementation detail for the current step.
