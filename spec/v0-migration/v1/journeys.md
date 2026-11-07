# Migration from v0 and contract compatibility — acceptance journeys

The baseline's release acceptance journeys include none for migration; the
journeys below cover converting v0 governance content, leaving v0 history
untouched, the safety rules of a conversion, and the contract-version report.
Every journey runs in a temporary Git repository with synthetic data, no
network, and no ambient credentials or user configuration, from the exact
release artifacts. The synthetic v0 repositories are taken from the v0
golden corpora (PK-MIG-007). Commands, `--dry-run`, `--json`, `--yes`, plan
confirmation, and exit codes are those of `cli@v1`. Where an identifier is
still open (see `interfaces.yaml`), the journey states the observable
effect, not the identifier.

## 1. Analyse and plan a v0 conversion without writing

Preconditions: a committed v0 repository from the golden corpora containing
at least one decision record, one skill, one process definition, and v0
logs, events, work items, and memory records; a clean working copy.

Steps:

1. Record the content digest of every file in the working copy.
2. Run `processkit migrate --from v0 --dry-run`.
3. Run `processkit migrate --from v0 --dry-run --json`.
4. Record the content digests again and run `git status --porcelain`.

Expected results:

- Step 2 prints the analysis and the plan, naming each decision record,
  skill, and process definition to be converted and every change the plan
  would make.
- Step 3 prints exactly one versioned result envelope on standard output
  that carries the same analysis and plan.
- Every digest in step 4 equals the digest in step 1; `git status` reports
  no change.

Covers: PK-MIG-001, PK-MIG-003, PK-COMPAT-003

## 2. Convert v0 decision records, skills, and process definitions

Preconditions: the repository from journey 1, unchanged; an interactive
terminal.

Steps:

1. Run `processkit migrate --from v0`, review the printed plan, and
   confirm it.
2. Run `git status --porcelain` and `git diff`.
3. Run `processkit validate --json`.
4. Run `processkit list DecisionRecord`, `processkit list Skill`, and
   `processkit list ProcessSpecification`.

Expected results:

- Step 1 prints its plan before writing anything, writes only after
  confirmation, and reports every change it made.
- The changes reported in step 1 are exactly the changes shown in step 2;
  no file is staged and no commit exists (`cli@v1` PK-CLI-006).
- Every converted item declares `apiVersion`
  `processkit.projectious.work/v1` and validates in step 3.
- Step 4 lists one v1 item for each v0 decision record, skill, and process
  definition of the corpus; their content matches the golden v1 output of
  the corpus.

Covers: PK-MIG-001, PK-MIG-007, PK-COMPAT-003

## 3. Leave v0 logs, events, work items, and memory untouched

Preconditions: the repository from journey 1, before journey 2 ran.

Steps:

1. Record the path and content digest of every v0 log, event, work-item,
   and memory record file.
2. Run `processkit migrate --from v0` and confirm the plan.
3. Record the paths and digests again.
4. Run `processkit list` for every v1 kind and `processkit validate`.

Expected results:

- The plan printed in step 2 contains no conversion of any log, event,
  work-item, or memory record.
- Every path and digest in step 3 equals the one in step 1.
- No v1 item listed in step 4 originates from a log, event, work item, or
  memory record, and no such record is reported as an invalid item.

Covers: PK-MIG-002

## 4. Refuse to apply on a dirty working copy without a recovery path

Preconditions: a committed v0 repository from the golden corpora; a
non-interactive run.

Steps:

1. Modify one tracked v0 skill file without committing it.
2. Run `processkit migrate --from v0 --yes`, without creating a backup and
   without accepting a narrower recovery boundary.
3. Revert the modification so the working copy is clean, and run
   `processkit migrate --from v0 --yes`.
4. In a fresh copy of the corpus, repeat step 1, then run the migration in
   the documented way that first creates a complete, contained backup.
5. In another fresh copy, repeat step 1, then run the migration with the
   documented explicit acceptance of the narrower recovery boundary.

Expected results:

- Step 2 refuses to apply the plan with a documented non-success exit code
  and writes no file: every file is byte-identical to before the step.
- Step 3 applies the plan and reports every change.
- Step 4 creates the backup before writing any converted file; the backup
  holds the pre-migration content, and the plan is applied.
- Step 5 applies the plan only after the explicit acceptance.

Covers: PK-MIG-004

## 5. Keep unknown fields or stop

Preconditions: a v0 corpus repository in which one decision record carries
a field that the conversion does not know; a clean working copy.

Steps:

1. Run `processkit migrate --from v0 --dry-run --json`.
2. Run `processkit migrate --from v0` and confirm the plan if it is
   offered.
3. Inspect the converted decision record, if one was written.

Expected results:

- Either the plan states that the unknown field is preserved and the
  converted decision record carries the field's value after step 2 and
  validates; or the run stops, names the file and the field, and writes no
  converted decision record for it.
- In no outcome does a converted decision record exist without the field's
  value while the run reports success.

Covers: PK-MIG-005

## 6. Report an ambiguous case as a blocking manual action

Preconditions: a v0 corpus repository in which one process definition
cannot be converted unambiguously (the corpus marks the case and its golden
manual action); a clean working copy.

Steps:

1. Run `processkit migrate --from v0 --dry-run --json`.
2. Run `processkit migrate --from v0` and confirm the plan if it is
   offered.
3. Inspect the repository.

Expected results:

- Step 1 reports a manual action naming the process definition and the
  ambiguity; it equals the golden manual action of the corpus.
- Step 2 does not report the migration as complete and exits with a
  documented non-success exit code.
- No converted item contains a value that the v0 source did not state.

Covers: PK-MIG-006, PK-MIG-007

## 7. Report the independently versioned contracts

Preconditions: an installed release candidate; any directory.

Steps:

1. Run `processkit version`.
2. Run `processkit version --json`.

Expected results:

- Step 1 shows a version for each of: content `apiVersion`, the ontology,
  the MCP tool contract, the CLI result contract, and the lock format.
- Step 2 prints exactly one result envelope whose data carries a separate
  version value for each of these five contracts.
- The reported content `apiVersion` includes
  `processkit.projectious.work/v1`.

Covers: PK-COMPAT-001

## 8. Check the conversion against every golden corpus

Preconditions: the v0 golden corpora with their golden v1 outputs and
golden manual actions; the field-level preservation report of the release.

Steps:

1. For each corpus, copy it into a fresh temporary repository, run
   `processkit migrate --from v0` with confirmation, and compare the result
   with the golden output.
2. Collect every field occurring in the v0 items of all corpora and look
   each up in the preservation report.

Expected results:

- Every corpus yields exactly its golden v1 output and its golden manual
  actions.
- Every field collected in step 2 has an entry in the preservation report
  stating how the conversion treats it.

Covers: PK-MIG-007

## Verified by component tests only

- PK-COMPAT-002 (contract break policy): it governs how contract versions
  change between releases. It is checked by the release gate comparing the
  published contracts with those of the previous release, not by a user
  journey.
- PK-COMPAT-003 (no silent reinterpretation under a newer schema): v1
  defines a single content `apiVersion`, so no newer schema exists to
  reinterpret against. Component tests register a synthetic newer schema
  and prove that stored content is still validated under its declared
  `apiVersion` until `processkit migrate` rewrites it. Journeys 1 and 2
  cover the "rewrite explicitly and report every change" part.
- PK-MIG-007 (not a source of v1 semantics): this constrains where v1
  behavior is defined. It is checked by review: every v1 rule the
  conversion relies on is a requirement in a v1 slug, not code of the v0
  adapter.
