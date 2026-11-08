# Migration from v0 and contract compatibility — acceptance journeys

The baseline's release acceptance journeys include none for migration; the
journeys below cover converting v0 governance content, leaving v0 history
untouched, the safety rules of a conversion, and the contract-version report.
Every journey runs in a temporary Git repository with synthetic data, no
network, and no ambient credentials or user configuration, from the exact
release artifacts. The v0 repositories are the golden corpora of
`interfaces.yaml` (`verification.golden_corpora`): the `input/` tree is
committed, and `processkit.toml` selects the content directory `context`.
Commands, `--dry-run`, `--json`, `--yes`, plan confirmation, the result
envelope, and exit codes are those of `cli@v1`. Codes, field names, and the
field mapping are in `interfaces.yaml`.

## 1. Analyse and plan a v0 conversion without writing

Preconditions: the corpus `v0.28-v2`; a clean working copy.

Steps:

1. Record the content digest of every file in the working copy.
2. Run `processkit migrate --from v0 --dry-run`.
3. Run `processkit migrate --from v0 --dry-run --json`.
4. Record the content digests again and run `git status --porcelain`.

Expected results:

- Step 2 prints the plan to standard output. It names each decision
  record, skill, and process definition with its target, and the
  untouched counts.
- Step 3 prints exactly one result envelope with `command` `migrate`. Its
  `data` validates against `schemas/migrate-result.schema.json`, with
  `mode` `v0`, `source.v0Release` `v0.28.8`, one `items` entry per
  source with `status` `convertible`, and `untouched` entries for
  `LogEntry`, `Note`, and `WorkItem`. Its `plan.changes` creates each
  target file and deletes each source file; `changes` is empty.
- Step 3 exits with code 0.
- Every digest in step 4 equals the digest in step 1; `git status` reports
  no change.

Covers: PK-MIG-001, PK-MIG-003, PK-MIG-008, PK-MIG-009, PK-MIG-010,
PK-MIG-022, PK-COMPAT-003

## 2. Convert v0 decision records, skills, and process definitions

Preconditions: each of the corpora `v0.8-flat`, `v0.24-nested`, and
`v0.28-v2` in its own repository, unchanged; an interactive terminal.

Steps:

1. Run `processkit migrate --from v0`, review the printed plan, and
   confirm it.
2. Run `git status --porcelain` and `git diff`.
3. Run `processkit validate --json`.
4. Run `processkit list DecisionRecord`, `processkit list Skill`, and
   `processkit list ProcessSpecification`.
5. Compare the working tree with the corpus's `expected/` tree.
6. Run `processkit migrate --from v0 --json` again.

Expected results:

- Step 1 prints its plan before writing anything, writes only after
  confirmation, and reports every change it made.
- The changes reported in step 1 are exactly the changes shown in step 2;
  no file is staged and no commit exists (`cli@v1` PK-CLI-006).
- Each converted decision record is at `context/decisions/<name>.md` with
  JSON front matter, each process definition at
  `context/processes/<name>.json`, and each skill at
  `context/skills/<name>/` with `skill.json` and a byte-identical
  `SKILL.md`. No v0 source file of a converted item remains at its old
  path, and no empty directory remains below `context/`.
- Every converted item declares `apiVersion`
  `processkit.projectious.work/v1`; step 3 reports no error for any of
  them.
- Unmapped v0 fields, such as `metadata.id`, appear as annotations with
  the prefix `v0.processkit.projectious.work/`.
- Step 5 shows no difference.
- Step 6 reports `migration.nothing-to-migrate`, writes no file, and
  exits with code 0.

Covers: PK-MIG-001, PK-MIG-007, PK-MIG-012, PK-MIG-013, PK-MIG-014,
PK-MIG-015, PK-MIG-016, PK-MIG-023, PK-COMPAT-003

## 3. Leave v0 logs, events, work items, and memory untouched

Preconditions: the corpus `v0.28-v2`, before journey 2 ran. It contains
an untracked note below `context/notes/private/` and an unreadable log
file.

Steps:

1. Record the path and content digest of every v0 log, event, work-item,
   and memory record file, tracked or not.
2. Run `processkit migrate --from v0 --json` and confirm the plan with
   `--yes`.
3. Record the paths and digests again.
4. Run `processkit list` for every v1 kind and `processkit validate`.

Expected results:

- The plan in step 2 contains no change to any log, event, work-item, or
  memory record file. The untracked note is not counted in `untouched`.
- Step 2 reports `migration.unreadable-file` as a warning for the
  unreadable log file and still succeeds.
- Every path and digest in step 3 equals the one in step 1.
- No v1 item listed in step 4 originates from a log, event, work item, or
  memory record, and no such record is reported as an invalid item.

Covers: PK-MIG-002, PK-MIG-008, PK-MIG-011

## 4. Refuse to apply when a plan target is not committed

Preconditions: the corpus `v0.24-nested`; a non-interactive run.

Steps:

1. Modify one tracked v0 skill file without committing it.
2. Create an untracked file `notes.txt` in the repository root.
3. Run `processkit migrate --from v0 --dry-run --json`.
4. Run `processkit migrate --from v0 --yes --json`.
5. Commit the modification, keep `notes.txt` untracked, and run
   `processkit migrate --from v0 --yes`.

Expected results:

- Step 3 reports `storage.target-not-committed` for the modified file at
  severity `warning` and exits with code 0.
- Step 4 reports `storage.target-not-committed` for the modified file
  with category `refused`, exits with code 4, has outcome `refused` and
  empty `changes`, and writes no file: every file is byte-identical to
  before the step. No backup file or directory exists anywhere.
- No option of `processkit migrate` disables the check.
- Step 5 applies the plan and reports every change; the untracked
  `notes.txt` does not block it.

Covers: PK-MIG-004

## 5. Keep unknown fields or stop

Preconditions: the corpus `unknown-fields`. One decision record carries
the unknown field `spec.related` with a short list value. Another carries
an unknown field whose canonical JSON value is longer than 4096
characters.

Steps:

1. Run `processkit migrate --from v0 --dry-run --json`.
2. Remove the decision record with the long field from the corpus,
   commit, and run `processkit migrate --from v0 --yes`.
3. Inspect the converted decision record.

Expected results:

- Step 1 reports `migration.field-not-preservable` naming the file and
  the field of the long value, and exits with code 1. Its
  `data.items[].fields` lists `/spec/related` with treatment `annotated`
  and target `v0.processkit.projectious.work/spec/related`.
- After step 2, the converted decision record has the annotation
  `v0.processkit.projectious.work/spec/related` whose value is the RFC 8785
  serialization of the field's value, and it validates.
- In no outcome does a converted decision record exist without the field's
  value while the run reports success.

Covers: PK-MIG-005, PK-MIG-016, PK-MIG-017

## 6. Report a missing value as a blocking manual action

Preconditions: the corpus `manual-actions`. A v0 process definition of
kind `Process` has no supplement. A decision record has a supplement with
an unknown member. A file in `context/decisions/` has unreadable front
matter. Two decision records map to the same name. A skill declares
`metadata.processkit.apiVersion` `processkit.projectious.work/v3`.

Steps:

1. Run `processkit migrate --from v0 --dry-run --json`.
2. Run `processkit migrate --from v0 --yes --json`.
3. Inspect the repository.
4. Add a supplement with `status`, `owner`, `workItemType`, and
   `stateMachine` to the process definition, resolve the other cases as
   their fixes say, commit, and run `processkit migrate --from v0 --yes`.

Expected results:

- Step 1 reports `migration.converted-item-invalid` for each missing
  required field of the process definition, `migration.invalid-supplement`,
  `migration.unreadable-source`, `migration.target-conflict` for both
  decision records, and `migration.unsupported-source`. They equal the
  corpus's `expected-diagnostics.json`. Each has severity `error`, category
  `validation`, the v0 source path in `file`, and a fix. The affected
  items have `status` `blocked`.
- Step 2 asks for no confirmation, exits with code 1 with outcome
  `failed` and empty `changes`, and writes no file.
- No converted item exists after step 2.
- Step 4 succeeds. The converted process definition carries the supplement
  values, and no value other than those the field mapping states.

Covers: PK-MIG-006, PK-MIG-007, PK-MIG-011, PK-MIG-015, PK-MIG-018,
PK-MIG-019, PK-MIG-020, PK-MIG-021

## 7. Report the independently versioned contracts

Preconditions: an installed release candidate; any directory.

Steps:

1. Run `processkit version`.
2. Run `processkit version --json`.

Expected results:

- Step 1 shows a version for each of: content `apiVersion`, the ontology,
  the MCP tool contract, the CLI result contract, and the lock format.
- Step 2 prints exactly one result envelope whose `data` validates against
  `cli@v1` `schemas/version.schema.json` and carries the non-empty fields
  `contentApiVersions`, `ontologyVersion`, `mcpToolContractVersion`,
  `resultContractVersion`, and `lockFormatVersion`.
- `contentApiVersions` is `["processkit.projectious.work/v1"]`,
  `resultContractVersion` is `cli.processkit.projectious.work/v1`, and
  `lockFormatVersion` is `lock.processkit.projectious.work/v1`.

Covers: PK-COMPAT-001

## 8. Check the conversion against every golden corpus

Preconditions: the golden corpora at `tests/golden/v0-migration/`.

Steps:

1. For each corpus, copy `input/` into a fresh temporary repository,
   commit it, run `processkit migrate --from v0 --yes --json`, and compare
   the result with the corpus's `expected/` tree and
   `expected-diagnostics.json`.
2. Collect every member of the front matter root, of `metadata`, of
   `spec`, and of `metadata.processkit` of every v0 source in all corpora.
   Look each up in the run's `data.items[].fields` and in
   `interfaces.yaml` `field_mapping`.

Expected results:

- The corpora listed in `interfaces.yaml` exist, each with `input/` and
  `expected-diagnostics.json`.
- Every corpus yields exactly its golden tree and its golden diagnostics.
- Every member collected in step 2 has an entry in the per-run `fields`
  of its item, with one of the treatments `mapped`, `annotated`, `kept`,
  or `supplement`.

Covers: PK-MIG-007, PK-MIG-025, PK-MIG-026

## 9. Refuse unsupported sources and options

Preconditions: the corpus `unsupported-release`, whose provenance marker
names `v0.7.0`; a separate repository initialized with `processkit init`
that holds only v1 content.

Steps:

1. In the corpus, run `processkit migrate --from v0 --json`.
2. In the v1 repository, run `processkit migrate --json`.
3. In the v1 repository, run `processkit migrate --from v1`.
4. In the corpus, delete `processkit.toml`, commit, and run
   `processkit migrate --from v0`.

Expected results:

- Step 1 reports `migration.unsupported-v0-release`, exits with code 1,
  and writes no file.
- Step 2 reports `migration.nothing-to-migrate` with severity `info`,
  `data.mode` `content-api`, exits with code 0, asks for no
  confirmation, and writes no file.
- Step 3 fails with `cli.invalid-option-value` and exit code 2.
- Step 4 fails as `cli@v1` PK-CLI-008 states for a missing
  `processkit.toml` and writes no file.

Covers: PK-MIG-009, PK-MIG-012, PK-MIG-023, PK-MIG-024

## 10. Report leftovers in v1 locations

Preconditions: the corpus `v0.24-nested`, which contains
`context/skills/_lib/processkit/__init__.py` and `context/skills/INDEX.md`.

Steps:

1. Run `processkit migrate --from v0 --dry-run --json`.

Expected results:

- Step 1 reports `migration.leftover-in-content-location` as a warning
  for each file left at a v1 kind location, for example below
  `context/skills/_lib/`, and the plan does not change those files.

Covers: PK-MIG-027

## Verified by component tests only

- PK-COMPAT-002, PK-COMPAT-004, and PK-COMPAT-005 (contract break policy,
  release notes, and change classification): they govern how contract
  versions change between releases. The release gate checks them by
  comparing the published contracts with those of the previous release
  and by checking the `Breaking changes` section of the release notes. No
  user journey covers them.
- PK-COMPAT-003 (no silent reinterpretation under a newer schema): v1
  defines a single content `apiVersion`, so no newer schema exists to
  reinterpret against. Component tests register a synthetic newer schema
  and prove that stored content is still validated under its declared
  `apiVersion` until `processkit migrate` rewrites it. Journeys 1, 2, and
  9 cover the "rewrite explicitly and report every change" part.
- PK-MIG-007 (not a source of v1 semantics): this constrains where v1
  behavior is defined. It is checked by review: every v1 rule the
  conversion relies on is a requirement in a v1 slug, not code of the v0
  adapter.
- PK-MIG-013 (write order): the order of created files before deleted
  files is observable only when a write is interrupted. Component tests
  inject a write failure after the first created file and check that no
  source file was deleted.
