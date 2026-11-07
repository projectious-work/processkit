# Repository storage — acceptance journeys

None of the release acceptance journeys is specific to this slug; the
journeys below exercise the repository layout, file formats, the write and
Git boundaries, and the "no instance storage" boundary. Every journey runs
in a temporary Git repository with synthetic data, no network, and no
ambient credentials or user configuration. Commands are those of `cli@v1`;
where an identifier is still open (see `interfaces.yaml`), the journey
states the observable effect, not the identifier.

## 1. Initialize a repository and inspect its layout

Preconditions: an empty Git repository with one commit; processkit installed;
no network access; no hosted processkit service reachable.

Steps:

1. Run `processkit init --governing`.
2. Run `processkit new Standard example-rule`, `processkit new Skill
   example-skill`, `processkit new MCPServer example-server`, and create a
   decision record and a document with `processkit new`.
3. Run `processkit validate`.
4. List the files in the repository and run `git status --porcelain`.

Expected results:

- `processkit.toml` exists at the repository root and the content directory
  `context/` exists inside the same working copy.
- Each item is one file at its declared location:
  `context/standards/example-rule.json`,
  `context/skills/example-skill/SKILL.md` (with its `skill.json` metadata),
  `context/mcp-servers/example-server.json`,
  `context/decisions/<name>.md`, and a file under `context/documents/`.
- JSON kinds are JSON files; decision records, documents, and skill bodies
  are Markdown with front matter holding every structured field.
- Every created item declares `apiVersion`
  (`processkit.projectious.work/v1`).
- No schema or template file was copied into the repository.
- All steps succeeded with no network and no hosted service.
- `.processkit/`, if created, is not proposed for commit and contains no
  credentials or machine-specific paths that must be committed.

Covers: PK-PROD-001, PK-STORE-002, PK-STORE-004, PK-STORE-011,
PK-STORE-030, PK-STORE-031

## 2. Undeclared paths are ignored

Preconditions: the repository from journey 1.

Steps:

1. Copy `context/standards/example-rule.json` to `context/stray/other.json`
   and to `notes/other.json`, changing `metadata.name` to `other`.
2. Run `processkit list Standard --json` and `processkit validate --json`.

Expected results:

- `other` appears in neither listing nor validation results; no diagnostic
  refers to the stray files as content.

Covers: PK-STORE-002

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
   four-space indentation, and no trailing newline.
2. Run `processkit format` twice, recording file digests after each run.
3. Run `processkit format` on a clean committed tree.

Expected results:

- After the first run the file is UTF-8 with LF line endings, keys sorted
  where the schema defines no order, two-space indentation, and a trailing
  newline.
- The second run changes no file; digests are identical.
- On the clean tree, `processkit format` reports no changed file.
- No temporary file remains in `context/standards/`.

Covers: PK-STORE-010, PK-STORE-020

## 5. Markdown front matter and safe YAML

Preconditions: the repository from journey 1.

Steps:

1. Create a decision record whose structured fields are in valid YAML front
   matter and validate it.
2. Move one required structured field from the front matter into a prose
   heading and validate.
3. Replace the front matter with YAML using a construct outside a safe
   subset (for example a custom tag or an alias bomb) and validate.
4. Malform the front-matter delimiter and validate.

Expected results:

- Step 1 succeeds.
- Step 2 fails: the field is reported missing; prose is not read as
  structure.
- Steps 3 and 4 fail with bounded diagnostics naming the file; nothing is
  executed or expanded.

Covers: PK-STORE-011, PK-STORE-012

## 6. Path containment

Preconditions: the repository from journey 1; a directory outside the
repository.

Steps:

1. Run `processkit new Standard ../../escape`.
2. Create `context/standards/link.json` as a symlink to a file outside the
   repository and run `processkit validate`.
3. Create a named pipe under `context/standards/` and run
   `processkit validate`.
4. Create `context/standards/Case.json` and `context/standards/case.json`
   on a case-sensitive filesystem and run `processkit validate`.

Expected results:

- Step 1 is rejected and no file is written outside the content directory.
- Steps 2 to 4 each report a rejection for the offending path; no content
  outside the repository is read.

Covers: PK-STORE-013

## 7. Multi-file write plan and no unconfirmed overwrite

Preconditions: the repository from journey 1, committed; one item edited by
hand so it is not in deterministic serialization.

Steps:

1. Run `processkit format --dry-run --json`.
2. Run `processkit format` without confirming the plan.
3. Run `processkit format` with the plan confirmed.
4. Run `processkit init --governing` again in the initialized repository
   without confirmation.

Expected results:

- Step 1 states the plan (the files to be changed) and writes nothing.
- Step 2 leaves every pre-existing file byte-identical.
- Step 3 states the plan before writing, then reports exactly the files it
  changed; the report matches `git status --porcelain`; nothing claims
  atomicity across files.
- Step 4 leaves `processkit.toml` and existing content byte-identical.

Covers: PK-STORE-021, PK-STORE-022

## 8. Vendored release files and apiVersion

Preconditions: a repository that pins a release in configuration and
vendors its schemas and templates explicitly.

Steps:

1. Run `processkit validate`.
2. Modify one vendored schema and run `processkit validate`.
3. Restore it; create an item declaring an `apiVersion` the installed
   release supports but is not the newest (if available), and one declaring
   an unsupported `apiVersion`; validate.

Expected results:

- Step 1 succeeds; each vendored copy carries the release version and
  digest.
- Step 2 fails verification for the modified copy.
- Step 3 validates each item against the schema of its declared
  `apiVersion`; the unsupported one fails.

Covers: PK-STORE-030, PK-STORE-031

## 9. Git boundary and revision attribution

Preconditions: the repository from journey 1, committed on branch `main`;
snapshot of `HEAD`, all refs, the index, and `.git/config`.

Steps:

1. Run every writing command (`init` with confirmation declined, `new`,
   `format`, `lock`) and every read command, including
   `processkit mcp serve --stdio` answering one `get_context` call.
2. Edit one standard without committing; call `get_context` and
   `processkit show Standard example-rule --json`.

Expected results:

- `HEAD`, the current branch, refs, and `.git/config` are unchanged; no
  commit, branch, merge, rebase, or push occurred; only working-tree files
  changed, as reported.
- Every served result names the working-copy revision.
- The edited standard is marked uncommitted; unchanged items are not.

Covers: PK-STORE-040, PK-STORE-041, PK-PROD-001

## 10. Nested repositories stay independent

Preconditions: a processkit repository containing a nested Git repository
and a submodule, each with files under paths matching `context/standards/`.

Steps:

1. Run `processkit list Standard --json` from the outer repository root.
2. Run the same command from inside the nested repository.

Expected results:

- Step 1 lists only items of the outer working copy.
- Step 2 resolves the nested repository as its own root and does not read
  the outer repository's content.

Covers: PK-STORE-001

## 11. No instance storage

Preconditions: the repository from journey 1 with a ProcessSpecification
that uses WorkItem, Event, and LogEntry as vocabulary.

Steps:

1. Run every CLI command and serve several MCP requests over stdio.
2. Create `context/processes/ticket-42.json` whose `kind` is `WorkItem`,
   and a file whose `kind` is `LogEntry`; run `processkit validate`.
3. List all files created in the repository and in `.processkit/`.

Expected results:

- The ProcessSpecification validates and is served.
- The instance files are not accepted as content (validation fails).
- No event log, LogEntry record, work-item instance, session transcript, or
  agent memory exists in the repository or in `.processkit/` after the
  journey.

Covers: PK-PROD-020

## Verified by component tests only

- PK-STORE-020 (atomic replace under interruption): proving that a crash
  mid-write never leaves a partial destination file needs fault injection
  through the filesystem port; journey 4 covers only the observable absence
  of leftover temporary files.
