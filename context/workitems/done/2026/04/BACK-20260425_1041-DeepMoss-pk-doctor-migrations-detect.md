---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260425_1041-DeepMoss-pk-doctor-migrations-detect
  created: '2026-04-25T10:41:11+00:00'
  updated: '2026-04-25T10:56:27+00:00'
spec:
  title: 'pk-doctor migrations: detect both layouts (pending/ subdir AND top-level
    + applied/)'
  state: done
  type: bug
  priority: medium
  assignee: TEAMMEMBER-cora
  description: |
    **Observed (2026-04-25):** Companion to BACK-…-pk-doctor-schema_filename-fallback. The `migrations` check in `pk-doctor/scripts/checks/migrations.py` hard-codes `repo_root / "context" / "migrations" / "pending"` as the pending-migrations directory. processkit dogfood follows that convention, but aibox-derived projects keep pending migrations at the top level of `context/migrations/` and only move *applied* ones to `context/migrations/applied/`. Result: `0 pending migration(s)` even when 5 are sitting at the top of the directory.

    **Fix:**

    1. Detect the layout by probing `context/migrations/pending/` first; if absent, walk `context/migrations/*.md` minus `applied/` and `INDEX.md` and minus the aibox-CLI upgrade-doc filename pattern (`<YYYYMMDD>_<HHMM>_<from>-to-<to>.md` — already exempted in `schema_filename.CLI_MIGRATION_RE`; reuse that constant or move it to `common.py`).
    2. Document the supported layouts in the check's module docstring + pk-doctor README so consumers know which one to use.
    3. Add a regression test: a tmp `--repo-root` with a top-level pending migration .md and assert the check counts it.

    **Done when:**
    - pk-doctor against aibox correctly counts top-level pending migrations (excluding aibox-CLI upgrade docs) instead of returning 0.
    - pk-doctor against /workspace dogfood still reports the same count as today (no regression).
    - New regression test passes.

    **Target:** v0.21.0. **Owner:** cora. **Priority:** medium — less critical than schema_filename because the affected files in aibox are CLI upgrade docs (already exempted from schema validation), but the silent-zero is still misleading.
  started_at: '2026-04-25T10:42:49+00:00'
  completed_at: '2026-04-25T10:56:27+00:00'
---

## Transition note (2026-04-25T10:42:49+00:00)

Starting fix.


## Transition note (2026-04-25T10:56:25+00:00)

Fix: _candidate_pending_paths() probes pending/ subdir first (dogfood); falls back to top-level + applied/ exclusion + CLI-upgrade-doc filter (derived layout). _list_pending() now also filters by `kind: Migration` so non-Migration markdown next to migrations is ignored. Verified: derived-fixture run with 1 real Migration entity + 1 CLI upgrade doc reports "1 pending migration" (correctly filtered). aibox repo: 0 pending (all 5 top-level files are CLI upgrade docs). Dogfood unchanged. Test [9] covers the regression. Mirrored.


## Transition note (2026-04-25T10:56:27+00:00)

Will commit imminently as part of v0.21.0 release.
