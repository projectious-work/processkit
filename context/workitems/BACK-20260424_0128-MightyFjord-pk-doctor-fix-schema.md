---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260424_0128-MightyFjord-pk-doctor-fix-schema
  created: '2026-04-24T01:28:50+00:00'
  updated: '2026-04-24T20:51:18+00:00'
spec:
  title: pk-doctor --fix=schema_filename (narrow CalmAnt-class only) + AGENTS.md hand-edit
    note (supersedes SnappyBird, v0.21.0)
  state: review
  type: task
  priority: low
  assignee: TEAMMEMBER-cora
  description: "Per DEC-BrightHawk (SnappyBird narrow).\n\n**Scope (v0.21.0):**\n\n\
    1. Add `run_fix(ctx, results)` to `context/skills/processkit/pk-doctor/scripts/checks/schema_filename.py`:\n\
    \   - For each ERROR the check produced, inspect the failure pattern.\n   - If\
    \ and only if the failure is \"missing required field `actor`\" on a LogEntry,\
    \ apply `actor: system`.\n   - Validate post-patch against the schema; on success,\
    \ write back; on failure, roll back and report.\n   - Return `list[dict]` in the\
    \ aggregator's expected shape.\n   - Behind `--fix=schema_filename` opt-in (never\
    \ default).\n\n2. Test: fixture LogEntry with `actor` missing; run `schema_filename\
    \ --fix`; confirm patched + re-validates.\n\n3. AGENTS.md (and src/AGENTS.md)\
    \ — add a ~3-line note under \"Skill guards\":\n   > **LogEntry repair.** Direct\
    \ hand-edit of a schema-invalid LogEntry\n   > is permitted for known-safe narrow\
    \ patches (e.g. adding a missing\n   > `actor` field). Prefer `pk-doctor --fix=schema_filename`\
    \ where it\n   > applies. Commit with a clear reference. Generic LogEntries remain\n\
    \   > append-only.\n\n**Explicit non-goals:**\n- No general \"data-fix\" migration\
    \ kind.\n- No `log_event --repair` override.\n- No coverage for hypothetical future\
    \ schema-invalid shapes; extend `run_fix` case-by-case when a real need arises.\n\
    \n**Done when:**\n- `pk-doctor --category=schema_filename --fix` flips the CalmAnt-class\
    \ fixture from ERROR → fixed with no collateral damage.\n- AGENTS.md note lands\
    \ in both trees.\n- Drift guard + pk-doctor full run: 0 ERROR / 0 WARN.\n\nEstimate:\
    \ ~2 hours. Target: v0.21.0. Supersedes BACK-20260424_0038-SnappyBird-data-repair-path-for."
  related_decisions:
  - DEC-20260424_0128-BrightHawk-narrow-snappybird-ship-pk
  started_at: '2026-04-24T20:35:10+00:00'
---

## Transition note (2026-04-24T20:35:10+00:00)

Starting implementation per approval.


## Transition note (2026-04-24T20:51:18+00:00)

Implementation complete. (1) Added run_fix() to schema_filename.py — narrow to LogEntry missing-actor pattern ONLY, inserts `actor: system`, validates post-patch, rolls back if still invalid. (2) End-to-end test: fixture LogEntry → detect ERROR → --fix=schema_filename --yes → status: applied → re-detect 0 ERROR. (3) AGENTS.md + src/AGENTS.md updated with the escape-hatch note under Skill guards. Mirrored; drift green; pk-doctor 0 ERROR / 0 WARN on live repo.
