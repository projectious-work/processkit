# Repository storage — acceptance journeys

None of the release acceptance journeys is specific to this slug; the
journeys below exercise the repository layout, file formats, the write and
Git boundaries, and the "no instance storage" boundary. Every journey runs
in a temporary Git repository with synthetic data, no network, and no
ambient credentials or user configuration. Commands are those of `cli@v1`.
Diagnostic codes and their categories are those in `interfaces.yaml`
(`errors`); exit codes follow from the categories as `cli@v1` defines. A
writing command that replaces a file is run with `--yes` unless the journey
says otherwise (`cli@v1` PK-CLI-014).

## 1. Initialize a repository and inspect its layout

Preconditions: an empty Git repository with one commit; processkit installed;
no network access; no hosted processkit service reachable.

Steps:

1. Run `processkit init --governing`.
2. Declare a document source in `processkit.toml` that matches
   `context/documents/*.md` (keys per `content-kinds@v1`) and commit.
3. Run `processkit new Standard example-rule`, `processkit new Skill
   example-skill`, `processkit new MCPServer example-server`, create the
   decision record `context/decisions/example-decision.md`, and create the
   document `context/documents/guide.md`.
4. Run `processkit validate`.
5. List the files in the repository and run `git status --porcelain`.

Expected results:

- `processkit.toml` exists at the repository root and contains the table
  `[content]` with `directory = "context"`; the directory `context/` exists.
- The plan of step 1 lists `processkit.toml` with action `create` and no
  item, schema, or template file.
- Each item is one file at its declared location:
  `context/standards/example-rule.json`,
  `context/skills/example-skill/skill.json` with
  `context/skills/example-skill/SKILL.md`,
  `context/mcp-servers/example-server.json`,
  `context/decisions/example-decision.md`, and `context/documents/guide.md`.
- Each file name stem (for the Skill, the directory name) equals the item's
  `metadata.name`.
- JSON kinds are JSON files; decision records, documents, and skill bodies
  are Markdown; the decision record's structured fields are in its front
  matter; the Skill's structured fields are in `skill.json`.
- Every created item declares `apiVersion`
  (`processkit.projectious.work/v1`).
- No schema or template file was copied into the repository.
- All steps succeeded with no network and no hosted service.
- `.processkit/`, if created, is at the repository root, is not proposed
  for commit, and contains no credentials or machine-specific paths that
  must be committed.

Covers: PK-PROD-001, PK-STORE-002, PK-STORE-004, PK-STORE-011,
PK-STORE-030, PK-STORE-031, PK-STORE-042, PK-STORE-045, PK-STORE-046,
PK-STORE-053, PK-STORE-054, PK-STORE-060

## 2. Undeclared paths are ignored

Preconditions: the repository from journey 1.

Steps:

1. Copy `context/standards/example-rule.json` to `context/stray/other.json`
   and to `notes/other.json`, changing `metadata.name` to `other`.
2. Run `processkit list Standard --json` and `processkit validate --json`.
3. Run `processkit validate notes/other.json --json`.

Expected results:

- Step 2: `other` appears in neither result; no diagnostic names the stray
  files.
- Step 3 fails with `storage.undeclared-path` (category usage) naming
  `notes/other.json`.

Covers: PK-STORE-002, PK-STORE-047

## 3. The cache is disposable

Preconditions: a project repository with one locked upstream that has been
fetched, and a warm cache from `processkit context --json`.

Steps:

1. Record the output of `processkit context --json`.
2. Delete `.processkit/`.
3. Run `processkit fetch`, then `processkit context --json` again.
4. Inspect `.processkit/` and `git status --porcelain`.

Expected results:

- The second context output is byte-identical to the first.
- `.processkit/` contains only caches and fetched upstream copies.
- No file under `.processkit/` is tracked or needs to be committed;
  `git status` shows no change to committed files.

Covers: PK-STORE-003, PK-STORE-004

## 4. Deterministic serialization

Preconditions: the repository from journey 1, committed.

Steps:

1. Rewrite `context/standards/example-rule.json` with unsorted keys,
   four-space indentation, CRLF line endings, a summary containing `é` and
   `/`, an added field `x` with the number `1e2` (format parses JSON but
   does not validate it against a schema), and no trailing newline. Commit
   it.
2. Rewrite the front matter of `context/decisions/example-decision.md` as
   JSON front matter (`---json`) with unsorted keys and commit it.
3. Run `processkit format --yes --json` twice, recording file digests after
   each run.
4. Commit, then run `processkit format --json` on the clean tree.

Expected results:

- After the first run, `example-rule.json` equals Python
  `json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True)` plus
  one LF: keys sorted, two-space indentation, LF only, `é` and `/`
  unescaped, `1e2` written as `100.0`, exactly one trailing LF.
- The decision record starts with `---json`, LF, its front matter in the
  same serialization, then `---`, LF; its body is unchanged.
- The first run's `plan.changes` and `changes` list exactly these two
  files with action `replace`, sorted by path, with `sha256:` digests that
  match the files before and after.
- The second run and step 4 report an empty plan and change no file.
- No file matching `.*.processkit-tmp-*` remains anywhere.

Covers: PK-STORE-010, PK-STORE-020, PK-STORE-049, PK-STORE-050,
PK-STORE-057, PK-STORE-058

## 5. Markdown front matter and safe YAML

Preconditions: the repository from journey 1.

Steps:

1. Give the decision record YAML front matter (`---` ... `---`) that holds
   every structured field, including the values `no` and `2026-11-08`, and
   validate it.
2. Move one required structured field from the front matter into a prose
   heading and validate.
3. In turn, put each of these into the front matter and validate: an
   anchor with an alias, a tag `!!python/object`, a merge key `<<`, an
   explicit key `?`, a `%YAML` directive, a second document, and a repeated
   key.
4. Remove the closing `---` and validate.
5. Replace the front matter with a YAML sequence and validate.
6. In `SKILL.md` of the Skill, add front matter `name: other-name` and
   validate; then add front matter with `name: example-skill`, an
   Agent Skills `description`, and an unknown field, and validate.

Expected results:

- Step 1 succeeds; `no` and `2026-11-08` are read as strings.
- Step 2 fails: the field is reported missing; prose is not read as
  structure.
- Step 3 fails each time with a bounded diagnostic naming the file:
  `storage.duplicate-key` for the repeated key, `storage.unsafe-yaml` for
  every other construct; nothing is executed or expanded.
- Steps 4 and 5 fail with `storage.front-matter-delimiter`.
- Step 6 fails first with `storage.location-mismatch`, then succeeds; the
  unknown front-matter field is not reported.

Covers: PK-STORE-011, PK-STORE-012, PK-STORE-049, PK-STORE-051,
PK-STORE-052, PK-STORE-053, PK-STORE-054

## 6. Path containment

Preconditions: the repository from journey 1; a directory outside the
repository.

Steps:

1. Run `processkit new Standard ../../escape`.
2. Create `context/standards/link.json` as a symlink to a file outside the
   repository and run `processkit validate --json`.
3. Replace it with a symlink to `context/standards/example-rule.json`
   and run `processkit validate --json`.
4. Create a named pipe under `context/standards/` and run
   `processkit validate --json`.
5. Create `context/standards/Case.json` and `context/standards/case.json`
   on a case-sensitive filesystem and run `processkit validate --json`.
6. Copy `context/standards/example-rule.json` to `fixtures/rule.json`,
   make `context/standards/example-rule.json` a symlink to it, commit, and
   run `processkit format --yes`.

Expected results:

- Step 1 fails with `storage.path-traversal` (category usage); no file is
  written.
- Step 2 reports `storage.symlink-escape` for `link.json`; no content
  outside the repository is read.
- Step 3 reports no path diagnostic for `link.json` (its name check is
  `storage.location-mismatch`, because its stem is not `example-rule`).
- Step 4 reports `storage.special-file`.
- Step 5 reports `storage.case-collision` for both paths.
- Step 6 refuses to write through the link with `storage.symlink-escape`;
  the link and its target are unchanged.

Covers: PK-STORE-013, PK-STORE-055

## 7. Write plan and no unconfirmed overwrite

Preconditions: the repository from journey 1, committed; one item edited by
hand so it is not in deterministic serialization, and that edit committed.

Steps:

1. Run `processkit format --dry-run --json`.
2. Run `processkit format` non-interactively without `--yes`.
3. Run `processkit format --yes --json`.
4. Run `processkit init --governing` again, non-interactively, without
   `--yes`.

Expected results:

- Step 1 lists the item with action `replace` in `plan.changes`; `changes`
  is empty; nothing is written.
- Step 2 is refused with `cli.confirmation-required` (`cli@v1`
  PK-CLI-014); every file is byte-identical.
- Step 3 lists the plan before writing, then `changes` equals
  `plan.changes`; the changed paths equal those in
  `git status --porcelain`; nothing claims atomicity across files.
- Step 4 plans `processkit.toml` with action `replace` (it differs from
  what `init` writes, because journey 1 added a document source) and is
  refused; `processkit.toml` and all content are byte-identical.

Covers: PK-STORE-021, PK-STORE-022, PK-STORE-057

## 8. apiVersion

Preconditions: the repository from journey 1.

Steps:

1. Run `processkit version --json` and record the supported content API
   versions.
2. Create one Standard declaring `processkit.projectious.work/v1`, one
   declaring `processkit.projectious.work/v99`, and one without
   `apiVersion`; run `processkit validate --json` and
   `processkit list Standard --json`.

Expected results:

- Step 1 reports exactly `processkit.projectious.work/v1`.
- The first item validates against the v1 schema and is listed.
- The second fails with `storage.unsupported-api-version` and is not
  listed.
- The third fails with the missing-envelope-field diagnostic of
  `ontology@v1` and is not listed.

Covers: PK-STORE-031, PK-STORE-061

## 9. Git boundary and revision attribution

Preconditions: the repository from journey 1, committed on branch `main`;
snapshot of `HEAD`, all refs, the index, and `.git/config`.

Steps:

1. Run every writing command (`init` with confirmation declined, `new`,
   `format`, `lock`) and every read command, including
   `processkit mcp serve --stdio` answering one `get_context` call. Commit
   the result with Git and take a new snapshot.
2. Edit one standard without committing; call `get_context` and run
   `processkit show Standard example-rule --json` and
   `processkit list Standard --json`.
3. In a new repository with no commit, run `processkit init --governing
   --yes`, `processkit new Standard first`, and `processkit list Standard
   --json`.

Expected results:

- Apart from the commit made in step 1 by the test itself, `HEAD`, the
  current branch, refs, the index, and `.git/config` are unchanged; only
  working-tree files changed, as reported.
- Every served result carries a revision object that validates against
  `schemas/revision.schema.json`; `commit` is the full object name of
  `HEAD`.
- In step 2, the edited standard has `status.uncommitted` true, unchanged
  items have it false, and `revision.uncommitted` is true. Before the
  edit, `revision.uncommitted` is false.
- In step 3, `revision.commit` is null, `revision.uncommitted` is true, and
  `first` has `status.uncommitted` true.

Covers: PK-STORE-040, PK-STORE-041, PK-STORE-062, PK-PROD-001

## 10. Nested repositories stay independent

Preconditions: a processkit repository containing a nested Git repository
at `context/standards/vendor-x/` and a submodule at `sub/`, each with
files under paths matching `context/standards/`.

Steps:

1. Run `processkit list Standard --json` and `processkit validate --json`
   from the outer repository root.
2. Run `processkit list Standard --json --root sub` after giving `sub/` its
   own `processkit.toml`.
3. Set `[content] directory = "sub/context"` in the outer
   `processkit.toml` and run `processkit validate --json`.
4. Run `processkit validate --json --root` with a subdirectory of the outer
   working copy that contains its own `processkit.toml`.
5. Run `processkit validate --json` in a directory with `processkit.toml`
   that is not inside any Git working copy.

Expected results:

- Step 1 lists and validates only items of the outer working copy; no
  diagnostic names a file below `vendor-x/` or `sub/`.
- Step 2 resolves `sub/` as its own root and reads only its own content.
- Step 3 fails with `storage.invalid-content-directory` (category usage).
- Steps 4 and 5 fail with `storage.not-a-working-copy` (category
  environment).

Covers: PK-STORE-001, PK-STORE-042, PK-STORE-043, PK-STORE-044

## 11. No instance storage

Preconditions: the repository from journey 1 with a ProcessSpecification
that uses WorkItem, Event, and LogEntry as vocabulary.

Steps:

1. Run every CLI command and serve several MCP requests over stdio.
2. Create `context/processes/ticket-42.json` whose `kind` is `WorkItem`,
   and `context/standards/log-1.json` whose `kind` is `LogEntry`; run
   `processkit validate --json`.
3. List all files created in the repository and in `.processkit/`.

Expected results:

- The ProcessSpecification validates and is served.
- Each instance file fails with the instance-concept diagnostic of
  `ontology@v1` and with no `storage.location-mismatch`; neither is served.
- No event log, LogEntry record, work-item instance, session transcript, or
  agent memory exists in the repository or in `.processkit/` after the
  journey.

Covers: PK-PROD-020, PK-STORE-046

## 12. Writes only over committed files

Preconditions: the repository from journey 1, committed; one Standard
`a` not in deterministic serialization, committed; an unrelated file
`notes.txt` with uncommitted changes and an untracked file `scratch.txt`.

Steps:

1. Run `processkit format --yes --json`.
2. Edit `a` again without committing and run `processkit format --yes
   --json` and `processkit format --dry-run --json`.
3. Stage the edit (`git add`) without committing and run
   `processkit format --yes --json`.
4. Commit. Create `context/standards/b.json` that is untracked and not in
   deterministic serialization; add `context/standards/c.json` to
   `.gitignore` and create it the same way. Run
   `processkit format --yes --json`.
5. Hand-edit `processkit.lock` without committing and run
   `processkit lock --yes --json` with a change of a declared upstream.

Expected results:

- Step 1 succeeds although `notes.txt` and `scratch.txt` are uncommitted;
  those files are unchanged.
- Steps 2 and 3 are refused (category `refused`) with
  `storage.target-not-committed` naming `context/standards/a.json`; the
  dry run reports the same code as a warning; no file changes.
- Step 4 fails with `storage.target-not-committed` naming both `b.json`
  and `c.json`; no file changes.
- Step 5 fails with `storage.target-not-committed` naming
  `processkit.lock`; the lock is unchanged.
- No run creates a backup file or directory anywhere.

Covers: PK-STORE-021, PK-STORE-056

## 13. Encoding and line endings

Preconditions: the repository from journey 1, committed.

Steps:

1. Write a Standard file with invalid UTF-8 and validate.
2. Write a Standard file that starts with a UTF-8 byte order mark and
   validate.
3. Write a Standard file with CRLF line endings and validate.
4. Write a Standard file with a repeated key and validate.

Expected results:

- Steps 1 and 2 fail with `storage.invalid-encoding`.
- Step 3 fails with `storage.invalid-line-ending`.
- Step 4 fails with `storage.duplicate-key`.
- Each has category validation; the other items stay valid and served.

Covers: PK-STORE-010, PK-STORE-048, PK-STORE-049

## 14. Item location rules

Preconditions: the repository from journey 1, committed.

Steps:

1. Copy `context/standards/example-rule.json` to
   `context/standards/renamed.json` without changing `metadata.name`.
2. Copy `context/mcp-servers/example-server.json` to
   `context/standards/example-server.json`.
3. Run `processkit validate --json` and `processkit list Standard --json`.

Expected results:

- Both copies fail with `storage.location-mismatch` and are not listed.
- `example-rule` is listed once, from its original file.

Covers: PK-STORE-046

## Verified by component tests only

- PK-STORE-020 (atomic replace under interruption): proving that a crash
  mid-write never leaves a partial destination file needs fault injection
  through the filesystem port; journey 4 covers only the observable absence
  of leftover temporary files.
- PK-STORE-057 (partial failure): a write that fails after other files
  were written needs fault injection through the filesystem port; the
  component test checks `storage.write-failed` and that the envelope's
  `changes` lists exactly the files already written.
- PK-STORE-058 (exclusive creation, flush, kept permission bits): needs a
  filesystem port that records calls; journey 4 covers naming and cleanup.
- PK-STORE-059 (no non-atomic fallback): the supported targets
  (`cli@v1` PK-CLI-016) always offer atomic rename within one directory,
  so a failing replace needs fault injection through the filesystem port.
