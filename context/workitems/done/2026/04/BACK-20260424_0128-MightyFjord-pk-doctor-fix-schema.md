---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260424_0128-MightyFjord-pk-doctor-fix-schema
  created: '2026-04-24T01:28:50+00:00'
  updated: '2026-04-24T20:51:32+00:00'
spec:
  title: pk-doctor --fix=schema_filename (narrow CalmAnt-class only) + AGENTS.md hand-edit
    note (supersedes SnappyBird, v0.21.0)
  state: done
  type: task
  priority: low
  assignee: TEAMMEMBER-cora
  description: |
    Per DEC-BrightHawk (SnappyBird narrow).

    **Scope (v0.21.0):**

    1. Add `run_fix(ctx, results)` to `context/skills/processkit/pk-doctor/scripts/checks/schema_filename.py`:
       - For each ERROR the check produced, inspect the failure pattern.
       - If and only if the failure is "missing required field `actor`" on a LogEntry, apply `actor: system`.
       - Validate post-patch against the schema; on success, write back; on failure, roll back and report.
       - Return `list[dict]` in the aggregator's expected shape.
       - Behind `--fix=schema_filename` opt-in (never default).

    2. Test: fixture LogEntry with `actor` missing; run `schema_filename --fix`; confirm patched + re-validates.

    3. AGENTS.md (and src/AGENTS.md) — add a ~3-line note under "Skill guards":
       > **LogEntry repair.** Direct hand-edit of a schema-invalid LogEntry
       > is permitted for known-safe narrow patches (e.g. adding a missing
       > `actor` field). Prefer `pk-doctor --fix=schema_filename` where it
       > applies. Commit with a clear reference. Generic LogEntries remain
       > append-only.

    **Explicit non-goals:**
    - No general "data-fix" migration kind.
    - No `log_event --repair` override.
    - No coverage for hypothetical future schema-invalid shapes; extend `run_fix` case-by-case when a real need arises.

    **Done when:**
    - `pk-doctor --category=schema_filename --fix` flips the CalmAnt-class fixture from ERROR → fixed with no collateral damage.
    - AGENTS.md note lands in both trees.
    - Drift guard + pk-doctor full run: 0 ERROR / 0 WARN.

    Estimate: ~2 hours. Target: v0.21.0. Supersedes BACK-20260424_0038-SnappyBird-data-repair-path-for.
  related_decisions:
  - DEC-20260424_0128-BrightHawk-narrow-snappybird-ship-pk
  started_at: '2026-04-24T20:35:10+00:00'
  completed_at: '2026-04-24T20:51:32+00:00'
---

## Transition note (2026-04-24T20:35:10+00:00)

Starting implementation per approval.


## Transition note (2026-04-24T20:51:18+00:00)

Implementation complete. (1) Added run_fix() to schema_filename.py — narrow to LogEntry missing-actor pattern ONLY, inserts `actor: system`, validates post-patch, rolls back if still invalid. (2) End-to-end test: fixture LogEntry → detect ERROR → --fix=schema_filename --yes → status: applied → re-detect 0 ERROR. (3) AGENTS.md + src/AGENTS.md updated with the escape-hatch note under Skill guards. Mirrored; drift green; pk-doctor 0 ERROR / 0 WARN on live repo.


## Transition note (2026-04-24T20:51:32+00:00)

Shipped in cc40660.
