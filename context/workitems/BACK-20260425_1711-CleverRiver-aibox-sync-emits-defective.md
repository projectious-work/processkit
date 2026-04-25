---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260425_1711-CleverRiver-aibox-sync-emits-defective
  created: '2026-04-25T17:11:14+00:00'
spec:
  title: aibox sync emits defective same-version migrations (baseline appears empty
    → all on-disk files marked new-upstream)
  state: backlog
  type: bug
  priority: high
  description: '## Symptom


    `aibox sync` produced pending migration **MIG-20260425T164303** (rejected) with
    these red flags:


    - `from_version: v0.21.0` → `to_version: v0.21.0` (same version) yet **564 "new-upstream"
    entries**, **0 unchanged**, **0 changed**, **0 removed**, **0 conflict**.

    - `affected_files: []` despite 564 body entries.

    - Marked-new files already exist locally (e.g. `context/team/roster.md`, `context/models/MODEL-*.md`,
    every `context/bindings/BIND-*`).

    - Includes content from very recent commits: `4b56af5` (roster refresh) and `19b984c`
    (GPT-5.5 / Qwen 3.6 / Kimi K2.6 model rows). Applying would have reverted them.

    - Source-path conventions inconsistent within one migration: `schemas/INDEX` vs
    `context/team/roster.md` (some bare, some `context/`-prefixed). Two mapping rules
    in one diff.


    ## Suspected root cause


    The diff generator''s left-hand side (the "previously synced upstream" snapshot)
    is empty or missing, so every upstream file looks "new". The `affected_files:
    []` field corroborates — the post-processor that derives that list also saw nothing.


    ## Why this is high-priority


    1. Silent data-loss risk for any derived project that auto-applies pending migrations.

    2. Confuses pk-doctor (which now WARNs on pending migrations — derived projects
    will see noise).

    3. Same-version migrations should be a no-op or never generated; their existence
    breaks the user''s mental model of what `aibox sync` does.


    ## Suggested investigation


    - Trace `aibox sync`''s baseline-snapshot resolution path (where does it fetch
    the prior version''s tree to diff against?).

    - Add an invariant: if `from_version == to_version`, expected output is "no migration
    generated" or a migration with body.unchanged > 0 and 0 new-upstream.

    - Add an invariant: `affected_files` length must equal sum(body row counts) when
    there are body rows.

    - Consider a pk-doctor check that flags malformed migrations: `same-version +
    new-upstream > 0`, or `body rows > 0 + affected_files == []`.


    ## Reference


    - Rejected migration: `MIG-20260425T164303` (`context/migrations/applied/MIG-20260425T164303.md`)

    - Reject reason recorded on the migration via `reject_migration`.

    - Discovered: 2026-04-25 during /pk-resume triage. Created at 2026-04-25T16:43:03Z
    by aibox sync after the v0.21.0 release.


    ## Repository touchpoints (out-of-tree)


    This is an aibox CLI defect; the fix lives in the aibox repo, not processkit.
    Resolution path is to (a) fix aibox, (b) add a defensive pk-doctor check in processkit
    so derived projects detect this class of malformed migration before applying.'
---
