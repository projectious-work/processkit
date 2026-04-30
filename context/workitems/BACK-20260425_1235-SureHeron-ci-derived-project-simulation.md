---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260425_1235-SureHeron-ci-derived-project-simulation
  created: '2026-04-25T12:35:35+00:00'
spec:
  title: 'CI: derived-project simulation harness for pk-doctor (catch dogfood-only
    path bugs)'
  state: backlog
  type: task
  priority: medium
  description: |
    **Problem.** v0.21.0 shipped two pk-doctor bugs (HappyReef in `schema_filename`, DeepMoss in `migrations`) that returned 0/0 in derived projects because the checks hardcoded the dogfood layout (`src/context/schemas/`, `context/migrations/pending/`). Both bugs passed our CI and dogfood `/pk-doctor` runs — they only surfaced when the user manually ran `/pk-doctor` inside the aibox container.

    **Root cause.** No automated coverage for the derived-project layout (`context/schemas/`, `context/migrations/*.md` flat). All current pk-doctor tests run against the dogfood tree.

    **Proposed fix.** Add a CI fixture that synthesizes a minimal derived-project tree (or symlinks the aibox layout via a checked-in fixture) and runs the doctor aggregator end-to-end against it. Assert non-zero counts for known seeded-bad entities. Wire into `make test` and the pre-release smoke checklist.

    **Sketch.**
    - `tests/fixtures/derived_project/` with the alternate layout + 2-3 deliberately-broken entities.
    - New test in `pk-doctor/scripts/test_doctor.py` — call `_run_doctor` with that fixture as `repo_root` and assert specific check IDs fire.
    - Optionally: parameterize existing dogfood tests to also run against the derived fixture.

    **Acceptance.** A regression of HappyReef or DeepMoss class (any check that hardcodes a single layout) fails the new test before release.

    **Origin.** Filed from session-handover behavioral retrospective in `LOG-20260425_1234-HappyRobin-session-handover`. Target: v0.22.0.
---
