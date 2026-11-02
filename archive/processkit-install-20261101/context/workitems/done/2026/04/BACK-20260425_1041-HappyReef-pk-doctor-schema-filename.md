---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260425_1041-HappyReef-pk-doctor-schema-filename
  created: '2026-04-25T10:41:01+00:00'
  updated: '2026-04-25T10:56:26+00:00'
spec:
  title: 'pk-doctor schema_filename: derived-project schemas-dir fallback (fix silent-zero
    walk)'
  state: done
  type: bug
  priority: high
  assignee: TEAMMEMBER-cora
  description: |
    **Observed (2026-04-25):** `/pk-doctor` run inside the aibox derived-project container returned 0 ERROR / 0 WARN despite obvious entity-hygiene problems (filenames with `_0000` placeholder times, etc.). Diagnosis: `pk-doctor/scripts/checks/schema_filename.py` resolves the schemas dir as `repo_root / "src" / "context" / "schemas"`, which only exists in processkit's own dogfood repo. Derived projects (aibox, etc.) have schemas at `context/schemas/`. When the dogfood path is missing, every kind's schema is `None`, every `kind` is skipped, and the check reports `walked 0 entity file(s) across 13 kinds` — a silent zero.

    **Fix:**

    1. Replace the hard-coded path with a fallback chain:
       - prefer `repo_root / "src" / "context" / "schemas"` (dogfood / processkit repo),
       - fall back to `repo_root / "context" / "schemas"` (derived projects post-`aibox sync`).
    2. If neither exists, emit a single `WARN schema_filename.no-schemas-dir` rather than failing silently.
    3. Add a regression test: pass a tmp `--repo-root` with `context/schemas/<kind>.yaml` (no src/) and assert the check actually walks entity files.

    **Done when:**
    - pk-doctor run with `--repo-root /tmp/aibox-investigation --category=schema_filename` walks > 0 entity files and reports the real findings.
    - Drift guard green; existing dogfood `/pk-doctor` run still reports identical results to today (no regression).
    - New regression test passes.

    **Target:** v0.21.0. **Owner:** cora. **Priority:** high — this hides correctness signals across every derived install.
  started_at: '2026-04-25T10:41:15+00:00'
  completed_at: '2026-04-25T10:56:26+00:00'
---

## Transition note (2026-04-25T10:41:15+00:00)

Starting fix.


## Transition note (2026-04-25T10:56:20+00:00)

Fix: added _resolve_schemas_dir() with fallback chain (src/context/schemas/ → context/schemas/). schemas_dir=None now emits a single WARN instead of silently walking 0 files. schema validation gracefully skipped when no schema dir, but filename/id, filename-date, and actor-id checks still fire. Verified: pk-doctor against /tmp/aibox-investigation now reports 96 ERROR / 129 WARN (walked 186 entity files) — the real problems are now visible. Dogfood unchanged: 0/0 with 582 entity files walked. Test [8] in test_doctor.py covers the regression. Mirrored.


## Transition note (2026-04-25T10:56:26+00:00)

Will commit imminently as part of v0.21.0 release.
