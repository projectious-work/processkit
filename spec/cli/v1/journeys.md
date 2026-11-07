# Command-line interface — acceptance journeys

Journey 1 is release acceptance journey 1 of the baseline. The others
exercise the remaining CLI behavior. Every journey runs in a temporary Git
repository with synthetic data, no ambient credentials, and no user
configuration, from the exact release artifacts. Where an identifier is
still open (see `interfaces.yaml`), the journey states the observable effect,
not the identifier; "the documented exit code for X" means the code the
release documents for category X (OPEN-cli-01).

## 1. Install a verified release and initialize an empty governing repository

Preconditions: a release candidate's artifacts; one of the release targets
(x86_64 or arm64 Linux, x86_64 or arm64 macOS); an empty Git repository with
one commit; a process environment with `HOME` pointing to a read-only
directory, no Git credential helper, and `PATH` limited to the installed
`processkit` and `git` (no shell or GNU userland tools on `PATH`); no network
after installation.

Steps:

1. Install the release with the documented, verifying installation
   (`security@v1`).
2. Run `processkit version --json`.
3. In the repository root, run `processkit init --governing --dry-run`.
4. Run `processkit init --governing` and confirm the plan.
5. Run `processkit validate --json`.
6. Run `git status --porcelain` and `git log --oneline`, and inspect the
   index.

Expected results:

- Step 2 prints exactly one JSON envelope on standard output whose data
  reports the release, source commit, ontology version, supported content
  API versions, and supported MCP protocol versions.
- Step 3 prints a plan and leaves the repository byte-identical.
- Step 4 prints its plan before writing; `processkit.toml` and the content
  directory exist afterwards in the current directory, and the command
  reports exactly the files it created.
- Step 5 succeeds with the documented success exit code.
- No file is staged, no commit, branch, or remote change exists, and no
  pull request is opened.
- No step needed a shell, GNU tools, a writable home directory, Git
  credentials, or network access.
- The journey passes on each of the four release targets, and the release
  states the matrix it was tested on.

Covers: PK-PROD-005, PK-CLI-002, PK-CLI-004, PK-CLI-006, PK-CLI-008,
PK-CLI-016, PK-CLI-017, PK-OUT-001, PK-OUT-005

## 2. Author content and validate a draft without writing it

Preconditions: the repository from journey 1; a stdio MCP client connected
with `processkit mcp serve --stdio`.

Steps:

1. Run `processkit new Standard example-rule`.
2. Edit the created file with an ordinary text editor (no processkit
   command) to add a rule; run `processkit validate --json`.
3. Prepare a draft Standard with a schema violation, not saved in the
   repository. Pipe it to `processkit validate - --json`.
4. Call the MCP tool `validate(kind, content)` with the same draft.
5. Pipe the same draft to `processkit validate -` (text output).

Expected results:

- Step 2 succeeds; the edited item is valid.
- Step 3 exits with the documented validation-failure exit code, prints
  exactly one envelope on standard output whose diagnostics name the
  violated constraint, writes diagnostics in text form only to standard
  error, and creates or changes no file.
- The step 3 and step 4 results and diagnostics are equivalent.
- Every name and diagnostic in the step 5 text output is also present in
  the step 3 envelope.

Covers: PK-PROD-005, PK-PROD-012, PK-CLI-001, PK-CLI-002, PK-CLI-003,
PK-CLI-004, PK-OUT-001, PK-OUT-002

## 3. Exit-code categories

Preconditions: the repository from journey 2.

Steps:

1. Run `processkit list Standard --json`.
2. Run `processkit list` with an option that does not exist.
3. Break `context/standards/example-rule.json` so it violates its schema and
   run `processkit validate`.
4. Run any repository command from a directory outside every processkit
   repository, with no `--root` and no `PROCESSKIT_ROOT`.

Expected results:

- Steps 1 to 3 exit with the documented codes for success, usage error,
  and validation failure, which are pairwise distinct.
- Step 4 fails with a code other than success; it is distinct from the
  validation-failure code.
- Each code is listed in the release's documentation.

Covers: PK-CLI-003, PK-CLI-008

## 4. Offline reads and a missing upstream fetch

Preconditions: a project repository whose `processkit.lock` pins one
governing upstream that has not been fetched; network access disabled.

Steps:

1. Run `processkit list Standard --json` and `processkit show` for an
   inherited item.
2. Enable network access and run `processkit fetch --dry-run`, then
   `processkit fetch`. Record repository file digests before and after.
3. Disable network access and repeat step 1, and run `processkit explain`
   on the inherited item.

Expected results:

- Step 1 fails with the documented environment-failure exit code; the
  diagnostic names the missing upstream and states the fix (running
  `processkit fetch`).
- `fetch --dry-run` writes nothing; `fetch` changes only the local cache,
  and every repository file is byte-identical.
- Step 3 succeeds with no network access, using committed files, the lock,
  and the local cache.

Covers: PK-CLI-003, PK-CLI-004, PK-CLI-005

## 5. What agents receive equals `processkit context`

Preconditions: the repository from journey 2 with a second standard and a
skill; a stdio MCP client connected as the same local principal.

Steps:

1. Run `processkit context --task "review a change" --json`.
2. Call `get_context` over MCP with the same task.
3. Run `processkit show Standard example-rule --level 1 --json` and call
   `get` over MCP with the same arguments; do the same for `list`,
   `explain`, and `ontology`.

Expected results:

- The context data of step 1 is byte-identical to the step 2 result.
- Each CLI result in step 3 is equivalent to its MCP counterpart,
  including diagnostics.

Covers: PK-CLI-001, PK-CLI-007, PK-PROD-005

## 6. Repository root selection

Preconditions: two governing repositories `a/` and `b/` initialized as in
journey 1; `a/sub/deep/` an existing directory inside `a/`; a directory
`parent/` that contains repository `c/` as a child but no `processkit.toml`
itself; a temporary directory `empty/` that is a Git repository with no
`processkit.toml`.

Steps:

1. From `a/sub/deep/`, run `processkit validate --json`.
2. From `a/sub/deep/`, run it with `--root b`.
3. From `a/sub/deep/`, run it with `PROCESSKIT_ROOT=b`, then with both
   `PROCESSKIT_ROOT=b` and `--root a`.
4. From `parent/`, run `processkit validate`.
5. From `a/`, run `processkit validate --root a/context`.
6. From `empty/`, run `processkit list Standard`, then
   `processkit init --governing`.
7. From `a/sub/deep/` with `PROCESSKIT_ROOT=b`, run
   `processkit config show --json`.

Expected results:

- Step 1 validates `a`; step 2 validates `b`; step 3 validates `b`, then
  `a`.
- Step 4 fails; it does not select `c/`.
- Step 5 either fails with an error naming the content directory, or
  reports the normalized root `a` before doing anything else.
- Step 6: `list` fails; `init` initializes `empty/` in the current
  directory.
- Step 7 reports the selected root `b` and project configuration of `b`
  only; no configuration value of `a` appears.

Covers: PK-CLI-008, PK-CLI-009, PK-CLI-010, PK-CLI-011

## 7. Reviewed plans, confirmation, and stale plans

Preconditions: the repository from journey 2 with
`context/standards/example-rule.json` deliberately mis-formatted;
an existing `.gitignore` with project-owned lines before and after any
processkit entries.

Steps:

1. Run `processkit format --dry-run`.
2. Run `processkit format` non-interactively without `--yes`.
3. Run `processkit format` non-interactively with `--yes`.
4. Mis-format the file again. Run `processkit format` interactively; while
   it waits for confirmation, edit the file; then confirm.
5. Run `processkit init --governing` in a fresh repository whose
   `.gitignore` has project-owned content; run it again with the
   confirmation the second run requires.

Expected results:

- Step 1 prints a plan that names the root, the operation, the release, and
  the digests of its inputs, and writes nothing.
- Step 2 refuses, and the file is byte-identical.
- Step 3 rewrites the file and reports exactly the changed file.
- Step 4 refuses the stale plan and writes no file.
- Step 5: if `init` changes the ignore file, the change appears in the
  plan, lies inside a marked processkit block, the second run leaves the
  ignore file byte-identical, and every line outside the block is
  unchanged.

Covers: PK-CLI-004, PK-CLI-012, PK-CLI-013, PK-CLI-014, PK-CLI-015

## 8. Configuration schema, layers, and redaction

Preconditions: the repository from journey 1; an operator configuration
file that contains an authenticator secret and a configured secret pattern.

Steps:

1. Add an unknown key to `processkit.toml`; run `processkit validate`.
2. Replace it with a listen address, then with an authenticator; run
   `processkit validate` each time.
3. Restore `processkit.toml`; set one value through a `PROCESSKIT_`
   environment variable; run `processkit config show --json` with the
   operator configuration.
4. Add an unknown key to the operator configuration and run
   `processkit config show`.

Expected results:

- Steps 1, 2, and 4 fail, naming the offending key.
- Step 3 reports every effective value with its source (project,
  operator, environment, or flag); the secret and any value matching the
  configured pattern are redacted on standard output and standard error.

Covers: PK-CONFIG-001, PK-CONFIG-002, PK-CONFIG-003, PK-OUT-004

## 9. Output streams and logs

Preconditions: the repository from journey 2; a configured secret pattern;
an item whose content contains a bearer token and a PEM certificate.

Steps:

1. Run `processkit list Standard --json` with standard output and standard
   error captured separately.
2. Run `processkit validate --json` in a state that produces at least one
   warning-level and one debug-level log record.
3. Cause an error whose message would include the bearer token or the
   certificate.
4. Configure another log sink in the operator configuration and repeat
   step 2.

Expected results:

- Standard output holds exactly one envelope with outcome, data,
  diagnostics, and revision; standard error holds only diagnostics and
  logs.
- By default, the warning appears on standard error as a structured
  record; the debug record does not appear.
- No bearer token, certificate, or pattern-matching value appears in any
  output or log.
- With another sink configured, logs go to that sink.

Covers: PK-OUT-001, PK-OUT-002, PK-OUT-003, PK-OUT-004

## Verified by component tests only

- PK-CLI-009 (filesystem boundary): a filesystem boundary between the
  current directory and an ancestor needs a mount; component tests drive
  root discovery through the filesystem port. Journey 6 covers the
  descendant and basename rules.
- PK-CLI-013 (non-interactive stale plan): a change between planning and
  writing in a non-interactive run is a race; component tests inject it
  through the filesystem port. Journey 7 covers the interactive case.
- PK-CLI-018, PK-CLI-019, PK-CLI-020 (release evidence): these state what
  pre-release evidence must contain (Python minors, release targets,
  case-sensitive and case-insensitive filesystems, black-box tests of
  platform differences). They are checked by the release gate inspecting
  the evidence, not by a user journey.
