# Command-line interface — acceptance journeys

Journey 1 is release acceptance journey 1 of the baseline. The others
exercise the remaining CLI behavior. Every journey runs in a temporary Git
repository with synthetic data, no ambient credentials, no user
configuration, and no `PROCESSKIT_` variables, from the exact release
artifacts. Unless a step says otherwise, standard input is not a terminal.
Exit codes, diagnostic codes, and envelope fields are those of
`interfaces.yaml`; "the envelope" means the document of
`schemas/result-envelope.schema.json`.

## 1. Install a verified release and initialize an empty governing repository

Preconditions: a release candidate's artifacts; one of the release targets
(x86_64 or arm64 Linux, x86_64 or arm64 macOS); an empty Git repository with
one commit and no `.gitignore`; a process environment with `HOME` pointing
to a read-only directory, no Git credential helper, and `PATH` limited to
the installed `processkit` and `git` (no shell or GNU userland tools on
`PATH`); no network after installation.

Steps:

1. Install the release with the documented, verifying installation
   (`security@v1`).
2. Run `processkit version -o json`, `processkit version`, and
   `processkit --version`.
3. In the repository root, run `processkit init --governing --dry-run
   -o json`.
4. Run `processkit init --governing` without `--yes`.
5. Run `processkit init --governing --yes -o json`.
6. Run `processkit validate -o json`.
7. Run `git status --porcelain` and `git log --oneline`, and inspect the
   index.

Expected results:

- Step 2: `version -o json` prints exactly one envelope on standard output
  with `command` `version` whose `data` is valid against
  `schemas/version.schema.json` and reports `release`, `sourceCommit`,
  `ontologyVersion`, `contentApiVersions`, `mcpProtocolVersions`,
  `mcpToolContractVersion`, `resultContractVersion`
  (`cli.processkit.projectious.work/v1`), and `lockFormatVersion`; `root`
  and `revision` are null. The text output of `version` contains every one
  of these values. `--version` prints exactly
  `processkit <release>` and a line feed. All three exit with code 0.
- Step 3 exits with code 0, the envelope (`command` `init`) carries `plan`
  with `operation` `init`, the selected root, the release, and the inputs,
  `changes` is empty, and the repository is byte-identical.
- Step 4 is refused with `cli.confirmation-required` and exit code 4; the
  repository is byte-identical.
- Step 5 exits with code 0; `processkit.toml`, the content directory, and
  `.gitignore` with the processkit block exist afterwards in the current
  directory, and `changes` lists exactly the files created.
- Step 6 exits with code 0.
- No file is staged, no commit, branch, or remote change exists, and no
  pull request is opened.
- No step needed a shell, GNU tools, a writable home directory, Git
  credentials, or network access.
- The journey passes on each of the four release targets, and the release
  notes state the matrix it was tested on.

Covers: PK-PROD-005, PK-CLI-002, PK-CLI-004, PK-CLI-006, PK-CLI-008,
PK-CLI-014, PK-CLI-016, PK-CLI-017, PK-CLI-023, PK-CLI-031, PK-CLI-034,
PK-CLI-037, PK-CLI-046, PK-OUT-001, PK-OUT-005, PK-OUT-006, PK-OUT-010

## 2. Author content and validate a draft without writing it

Preconditions: the repository from journey 1, committed; a stdio MCP
client connected with `processkit mcp serve --stdio`.

Steps:

1. Run `processkit create standard example-rule -o json`.
2. Edit the created file with an ordinary text editor (no processkit
   command) to add a rule; run `processkit validate -o json`, then
   `processkit validate standard example-rule -o json`.
3. Prepare a draft Standard with a schema violation, not saved in the
   repository. Pipe it to `processkit validate -f - -o json`.
4. Call the MCP tool `validate(kind, content)` with the same draft and
   kind `Standard`.
5. Pipe the same draft to `processkit validate -f -` (text output).
6. Pipe the draft with its `kind` field removed to
   `processkit validate standard -f - -o json`, and then to
   `processkit validate -f - -o json`.
7. Run `processkit validate -f context/standards/example-rule.json -f -`,
   and `processkit validate standard example-rule
   -f context/standards/example-rule.json`.
8. Run `processkit validate -f context/standards/example-rule.json
   -f context/standards -o json`.
9. Pipe a valid draft Standard to `processkit validate -f - -f -`, and to
   `processkit format -f -`.

Expected results:

- Step 1 exits with code 0; the envelope has `command` `create`, and
  `changes` lists exactly `context/standards/example-rule.json`.
- Step 2 succeeds with exit code 0 both times; the edited item is valid;
  the first run validated the whole repository (the envelope reports the
  edited item), the second only `example-rule`.
- Step 3 exits with code 1, prints exactly one envelope on standard output
  with `outcome` `failed` whose diagnostics are valid against
  `schemas/diagnostic.schema.json`, have `category` `validation`, and name
  the violated constraint; the same diagnostics appear as text on standard
  error, each with severity, code, and message; no file is created or
  changed.
- The step 3 `data` and `diagnostics` equal the step 4 result and
  diagnostics.
- Every name and diagnostic in the step 5 text output is also present in
  the step 3 envelope.
- Step 6: with TYPE `standard`, the result equals step 3; without it, the
  draft fails validation with exit code 1.
- Step 7: both fail with `cli.conflicting-options` and exit code 2.
- Step 8 exits with code 0 and reports `example-rule` as valid.
- Step 9: both fail as usage errors with exit code 2 (`-f -` at most once,
  and only for `validate` and `apply`); no file is created or changed.

Covers: PK-PROD-005, PK-PROD-012, PK-CLI-001, PK-CLI-002, PK-CLI-003,
PK-CLI-004, PK-CLI-040, PK-CLI-042, PK-CLI-043, PK-CLI-054, PK-OUT-001,
PK-OUT-002, PK-OUT-007

## 3. Exit codes

Preconditions: the repository from journey 2, committed.

Steps:

1. Run `processkit get standards -o json`.
2. Run `processkit get standards --no-such-option`, and `processkit get`
   with no operands.
3. Break `context/standards/example-rule.json` so it violates its schema and
   run `processkit validate -o json`.
4. Run any repository command with `-o json` from a directory outside every
   processkit repository, with no `--root` and no `PROCESSKIT_ROOT`.
5. Restore the file, mis-format it, commit it, and run `processkit format`
   without `--yes`.
6. Run `processkit validate` with the broken file of step 3 and, at the
   same time, an unknown option.

Expected results:

- Step 1 exits with 0 and `outcome` `succeeded`.
- Step 2 exits with 2 and reports `cli.unknown-option`, then
  `cli.missing-argument` with short help on standard error.
- Step 3 exits with 1 and `outcome` `failed`.
- Step 4 exits with 3, `outcome` `failed`, and reports
  `cli.root-not-found`.
- Step 5 exits with 4, `outcome` `refused`, and reports
  `cli.confirmation-required`.
- Step 6 exits with 2 (usage wins over validation).
- Each code is listed in the release's documentation.

Covers: PK-CLI-003, PK-CLI-008, PK-CLI-022, PK-CLI-027, PK-CLI-028,
PK-OUT-006

## 4. Offline reads, fetch, then lock

Preconditions: a project repository whose `processkit.toml` declares one
governing upstream and whose `processkit.lock` pins it; the upstream has
not been fetched; network access disabled.

Steps:

1. Run `processkit get standards -o json` and `processkit get standard
   NAME -o json` for an inherited item NAME.
2. Run `processkit lock --update -o json`.
3. Run `processkit fetch --dry-run=server`. Then enable network access and
   run `processkit fetch --dry-run`, then `processkit fetch`. Record
   repository file digests and the local cache before and after.
4. Disable network access and repeat step 1, and run
   `processkit describe standard NAME` on the inherited item.
5. With network access still disabled, run
   `processkit lock --update --yes -o json`.

Expected results:

- Step 1 fails with exit code 3; the diagnostic is
  `cli.upstream-not-fetched`, names the missing upstream, has
  `nextAction` `run-fetch`, and its fix (running `processkit fetch`) is the
  last line of its text form.
- Step 2 fails with exit code 3 and `cli.upstream-not-fetched`; the lock is
  byte-identical; no network access was attempted.
- Step 3: `fetch --dry-run=server` fails with exit code 3, because it
  resolves refs over the network; `fetch --dry-run` writes nothing; `fetch`
  changes only the local cache, and every repository file is
  byte-identical.
- Step 4 succeeds with no network access, using committed files, the lock,
  and the local cache.
- Step 5 succeeds with no network access, resolving from the local cache.

Covers: PK-CLI-003, PK-CLI-004, PK-CLI-005, PK-CLI-044, PK-CLI-052,
PK-OUT-007

## 5. What agents receive equals `processkit get context`

Preconditions: the repository from journey 2 with a second standard and a
skill; a stdio MCP client connected to a server started by the same
operating-system user.

Steps:

1. Run `processkit get context --task "review a change" --profile p1
   --path src -o json`.
2. Call `get_context` over MCP with `task`, `profiles` `["p1"]`, and
   `paths` `["src"]`.
3. Run `processkit get standard example-rule --level 1 -o json` and call
   `get` over MCP with the same arguments and `namespace` `root`. Do the
   same for `get standards --limit 1 -o json` and then with `--cursor` from
   its result (MCP `list`), for `describe standard example-rule -o json`
   (MCP `explain`), for `api-resources -o json` (MCP `ontology()`), and for
   `explain policy -o json` (MCP `ontology` with `concept` `Policy`).

Expected results:

- The `data` of step 1 is byte-identical to the step 2 result; the
  envelope has `command` `get context`.
- In step 3, the envelope `command` is `get item` for
  `get standard example-rule` and `get` for `get standards`.
- Each CLI `data` and `diagnostics` in step 3 equal its MCP counterpart's
  result and diagnostics.

Covers: PK-CLI-001, PK-CLI-007, PK-CLI-040, PK-CLI-041, PK-PROD-005

## 6. Repository root selection

Preconditions: two governing repositories `a/` and `b/` initialized as in
journey 1 (each the top level of its own Git working copy, content
directory `context`); `a/sub/deep/` an existing directory inside `a/`; a
directory `parent/` that contains repository `c/` as a child but no
`processkit.toml` itself; a Git repository `empty/` with no
`processkit.toml`; a Git repository `fresh/`.

Steps:

1. From `a/sub/deep/`, run `processkit validate -o json`.
2. From `a/sub/deep/`, run it with `--root b`.
3. From `a/sub/deep/`, run it with `PROCESSKIT_ROOT=b`, then with both
   `PROCESSKIT_ROOT=b` and `--root a`.
4. From `parent/`, run `processkit validate`.
5. From `a/`, run `processkit validate --root a/context -o json`.
6. From `empty/`, run `processkit get standards`, then
   `processkit init --yes`.
7. From `a/sub/deep/` with `PROCESSKIT_ROOT=b`, run
   `processkit config view -o json`.
8. From `a/`, run `processkit init --governing --yes`.

Expected results:

- Step 1 validates `a`; step 2 validates `b`; step 3 validates `b`, then
  `a`; the envelope `root` names the validated repository.
- Step 4 fails with `cli.root-not-found` and exit code 3; it does not
  select `c/`.
- Step 5 reports `cli.root-normalized` (severity `info`) as its first
  diagnostic and validates `a`; `root` names `a`.
- Step 6: `get` fails with exit code 3; `init` initializes `empty/` in the
  current directory as a project repository.
- Step 7 reports `root` `b` and project configuration of `b` only; no
  configuration value of `a` appears.
- Step 8 is refused with `cli.already-initialized` and exit code 4; every
  file in `a/` is byte-identical.

Covers: PK-CLI-008, PK-CLI-009, PK-CLI-010, PK-CLI-011, PK-CLI-038,
PK-CLI-048

## 7. Reviewed plans, confirmation, and stale plans

Preconditions: the repository from journey 2 with
`context/standards/example-rule.json` deliberately mis-formatted and
committed; a pseudo-terminal available to the test driver.

Steps:

1. Run `processkit format --dry-run` and `processkit format --dry-run
   -o json`.
2. Run `processkit format` non-interactively without `--yes`.
3. Run `processkit format --yes -o json`.
4. Mis-format the file again and commit it. Run `processkit format` with
   standard input on a pseudo-terminal and answer `n`.
5. Run it again on the pseudo-terminal; while it waits for confirmation,
   edit the file; then answer `yes`.
6. Restore and commit the mis-formatted file. Run `processkit format
   --no-input` with standard input on the pseudo-terminal.
7. In a fresh Git repository whose committed `.gitignore` has
   project-owned lines, run `processkit init --yes`. Then, in a second
   fresh Git repository whose committed `.gitignore` already contains the
   resulting processkit block, run `processkit init --yes`.

Expected results:

- Step 1: the text plan is on standard output; the envelope `plan` names
  the root, the operation `format`, the release, and the `sha256:` digests
  of its inputs, and has `confirmationRequired` true; `changes` is empty;
  nothing is written; both exit with 0.
- Step 2 is refused with `cli.confirmation-required` and exit code 4, and
  the file is byte-identical.
- Step 3 rewrites the file; `changes` lists exactly the changed file.
- Step 4 shows the plan and the question on standard error and is refused
  with `cli.confirmation-declined` and exit code 4; no file is written.
- Step 5 is refused with `cli.plan-stale` and exit code 4; no file is
  written by processkit.
- Step 6 does not prompt and is refused with `cli.confirmation-required`.
- Step 7: the plan lists `.gitignore`; after the run, `.gitignore` ends
  with the block `# BEGIN processkit (managed block; do not edit)`,
  `/.processkit/`, `# END processkit`; every line outside the block is
  unchanged; in the second repository, `.gitignore` is byte-identical
  after the run.

Covers: PK-CLI-004, PK-CLI-012, PK-CLI-013, PK-CLI-014, PK-CLI-015,
PK-CLI-031, PK-CLI-032, PK-CLI-033, PK-CLI-034, PK-CLI-035, PK-CLI-037

## 8. Configuration schema, layers, and redaction

Preconditions: the repository from journey 1; an operator configuration
file `op.toml` with `schema-version = 1`, an authenticator setting with
a secret-shaped value, `redaction.patterns` with one pattern, and
`logging.level = "info"`.

Steps:

1. Add an unknown key to `processkit.toml`; run `processkit validate`.
2. Replace it with a listen address, then with an authenticator; run
   `processkit validate` each time.
3. Restore `processkit.toml`; remove its `schema-version`; run
   `processkit validate`; restore it again.
4. Run `processkit config view -o json --config op.toml` with
   `PROCESSKIT_LOG_LEVEL=debug`, then add `--log-level error`.
5. Run `processkit config view -o json` with no `--config` and no
   `PROCESSKIT_CONFIG`, then with `--config missing.toml`.
6. Add an unknown key to `op.toml` and run
   `processkit config view --config op.toml`.
7. Set `PROCESSKIT_NO_SUCH_VARIABLE=1` and run `processkit validate`.

Expected results:

- Step 1 fails with `cli.config-unknown-key` and exit code 1, naming the
  key; step 2 fails with `cli.config-forbidden-key` and exit code 1 each
  time; step 3 fails with `cli.config-version-unsupported` and exit code 1.
- Step 4: `data` is valid against `schemas/config-report.schema.json`;
  every supported key appears exactly once, sorted by key, with its source
  (`default`, `project`, `operator`, `environment`, or `flag`) and origin;
  `logging.level` is `debug` from `environment`, then `error` from `flag`
  with the environment value listed as overridden; the secret and any value
  matching the pattern appear only as `[REDACTED]` on standard output and
  standard error.
- Step 5: the operator file layer is reported as not loaded, and no file
  outside the repository was read; with `missing.toml` the command fails
  with `cli.config-unreadable` and exit code 3.
- Step 6 fails with `cli.config-unknown-key` and exit code 1, naming the
  key.
- Step 7 succeeds and reports `cli.unknown-environment-variable` as a
  warning.

Covers: PK-CONFIG-001, PK-CONFIG-002, PK-CONFIG-003, PK-CONFIG-004,
PK-CONFIG-005, PK-CONFIG-006, PK-CONFIG-007, PK-CONFIG-008, PK-OUT-004,
PK-OUT-009

## 9. Output streams and logs

Preconditions: the repository from journey 2; an operator configuration
with a configured secret pattern; an item whose content contains a bearer
token and a PEM certificate.

Steps:

1. Run `processkit get standards -o json` with standard output and
   standard error captured separately.
2. Run `processkit validate -o json` in a state that produces at least one
   warning-level and one debug-level log record.
3. Cause an error whose message would include the bearer token or the
   certificate.
4. Set `logging.sink = "file"` and `logging.file` to an absolute path in
   the operator configuration and repeat step 2; then point `logging.file`
   at a directory that cannot be written and repeat it.

Expected results:

- Standard output holds exactly one envelope with `apiVersion`, `kind`,
  `command`, `outcome`, `root`, `revision`, `data`, and `diagnostics`;
  standard error holds only text diagnostics and log records.
- By default, the warning appears on standard error as one JSON line valid
  against `schemas/log-record.schema.json`; the debug record does not
  appear.
- No bearer token, certificate, or pattern-matching value appears in any
  output or log; redacted values read `[REDACTED]`.
- With the file sink, log records go to the file and not to standard
  error; with the unwritable path, the command fails with
  `cli.log-sink-unavailable` and exit code 3.

Covers: PK-OUT-001, PK-OUT-002, PK-OUT-003, PK-OUT-004, PK-OUT-006,
PK-OUT-008, PK-OUT-009

## 10. Command-line conventions

Preconditions: the repository from journey 2.

Steps:

1. Run `processkit --help`, `processkit get --help`, and
   `processkit get standard example-rule --no-such-option --help`.
2. Run `processkit -v`.
3. Run `processkit get standard -o json example-rule`,
   `processkit get -o json -- standard example-rule`, and
   `processkit get standard/example-rule -o json`.
4. Run `processkit lock example`.
5. Run `processkit get standards` with standard output to a pipe, and with
   standard output on a pseudo-terminal and `NO_COLOR=1`, and with
   `--no-color`.
6. Run `processkit mcp serve --stdio -o json`.
7. Put an executable `processkit-foo` that creates a marker file on `PATH`,
   next to `processkit`, and run `processkit foo -o json`.

Expected results:

- Step 1: each prints help that begins with examples on standard output
  and exits with 0.
- Step 2 does not print the version; it fails with exit code 2.
- Step 3: all three succeed with equal envelopes.
- Step 4 fails with `cli.unexpected-argument` and exit code 2.
- Step 5: no output contains a terminal control sequence.
- Step 6 fails with `cli.option-not-applicable` and exit code 2, and writes
  nothing to standard output.
- Step 7 fails with `cli.unknown-command` and exit code 2; the marker file
  does not exist afterwards.

Covers: PK-CLI-021, PK-CLI-022, PK-CLI-023, PK-CLI-024, PK-CLI-026,
PK-CLI-030, PK-CLI-055

## 11. Writes need committed targets; dry-run modes

Preconditions: the repository from journey 2, committed, with
`context/standards/example-rule.json` mis-formatted and committed.

Steps:

1. Change the file without committing it. Run `processkit format --yes
   -o json`.
2. Run `processkit format --dry-run=client -o json` and
   `processkit format --dry-run -o json`.
3. Run `processkit format --dry-run=server --yes -o json`.
4. Run `processkit format --dry-run=maybe`.
5. Stage the change without committing it and repeat step 1.
6. Commit the change. Run `processkit format --dry-run=server -o json`,
   with standard input on a pseudo-terminal.
7. Run `processkit format --dry-run=none --yes -o json`.

Expected results:

- Step 1 is refused before any prompt: exit code 4, `outcome` `refused`,
  one `storage.target-not-committed` diagnostic for the file with
  `nextAction` `commit-or-stash` and a fix line; the file is
  byte-identical.
- Step 2: both runs exit with 0, carry the same `plan`, report the same
  diagnostic with severity `warning`, and have empty `changes`; the file is
  byte-identical.
- Step 3 is refused as in step 1 (exit code 4, `outcome` `refused`, the
  diagnostic with severity `error`), although `--yes` is given; `plan` is
  present, `changes` is empty, and the file is byte-identical.
- Step 4 fails with `cli.invalid-option-value` and exit code 2; the file is
  byte-identical.
- Step 5 is refused as in step 1.
- Step 6 exits with 0, carries `plan`, reports no
  `storage.target-not-committed` diagnostic, does not prompt, and writes
  nothing; `changes` is empty.
- Step 7 rewrites the file and reports it in `changes`.

Covers: PK-CLI-031, PK-CLI-036, PK-CLI-052

## 12. Type names and output formats

Preconditions: the repository from journey 2, committed, with
`context/standards/example-rule.json` valid; no other Standard.

Steps:

1. Run `processkit get Standard -o json`, `processkit get standards -o
   json`, `processkit get STD -o json`, and `processkit get StAnDaRdS -o
   json`.
2. Run `processkit get standard example-rule -o json`,
   `processkit get std example-rule -o json`, and
   `processkit get Standards/example-rule -o json`.
3. Run `processkit get standard Example-Rule -o json`.
4. Run `processkit get widgets -o json` and
   `processkit create widget w1 -o json`.
5. Run `processkit explain std -o json` and
   `processkit explain Standard -o json`.
6. Run `processkit get standards -o yaml` and compare it with step 1.
7. Run `processkit get standards -o name`.
8. Run `processkit get standards -o wide`.
9. Run `processkit get context -o name`, `processkit validate -o name`,
   and `processkit version -o name`.
10. Run `processkit get standards -o xml`.

Expected results:

- Step 1: all four exit with 0, have `command` `get`, and have equal
  `data`, which lists `example-rule`, every Standard of the root
  namespace.
- Step 2: all three exit with 0, have `command` `get item`, and have equal
  `data`.
- Step 3 fails with `mcp-context-serving.item-not-found` and exit code 2:
  names are case-sensitive.
- Step 4: both fail with `content-kinds.unknown-kind` and exit code 2; no
  file is created.
- Step 5: both exit with 0, have `command` `explain`, and have equal
  `data`, which equals the result of the MCP tool `ontology` with `concept`
  `Standard`.
- Step 6 exits with 0 and writes one YAML 1.2 document whose parsed value
  equals the parsed `-o json` envelope of step 1.
- Step 7 exits with 0 and writes exactly one line,
  `Standard/root/example-rule`.
- Step 8 exits with 0 and its text output names `example-rule`.
- Step 9: each fails with `cli.option-not-applicable` and exit code 2, and
  writes nothing to standard output.
- Step 10 fails with `cli.invalid-option-value` and exit code 2.

Covers: PK-CLI-002, PK-CLI-040, PK-CLI-049, PK-CLI-050, PK-OUT-001

## 13. Namespaces

Preconditions: the repository from journey 2, committed; a stdio MCP
client connected with `processkit mcp serve --stdio`.

Steps:

1. Run `processkit create container team-a --yes`, then
   `processkit create standard team-rule -n team-a --yes`; commit both
   files.
2. Run `processkit get standards -o name`.
3. Run `processkit get standards -n team-a -o name` and
   `processkit get standards --namespace team-a -o name`.
4. Run `processkit get standards -A -o json` and
   `processkit get standards --all-namespaces -o name`; call the MCP tool
   `list` with `kind` `Standard` and no `namespace`.
5. Run `processkit get standard team-rule -o json`, then
   `processkit get standard team-rule -n team-a -o json`.
6. Run `processkit get standards -A -n team-a`.

Expected results:

- Step 1 exits with 0 both times; the second item declares
  `metadata.namespace` `team-a`.
- Step 2 writes exactly `Standard/root/example-rule`.
- Step 3: both write exactly `Standard/team-a/team-rule`.
- Step 4: the `-o json` `data` equals the MCP `list` result; the `-o name`
  output has one line for each of `Standard/root/example-rule` and
  `Standard/team-a/team-rule`.
- Step 5: the first fails with `mcp-context-serving.item-not-found` and
  exit code 2; the second exits with 0.
- Step 6 fails with `cli.conflicting-options` and exit code 2, and writes
  nothing to standard output.

Covers: PK-CLI-040, PK-CLI-049, PK-CLI-050, PK-CLI-051

## 14. Declarative changes with `apply`

Preconditions: the repository from journey 2, committed; a directory
`drafts/` outside the repository. In `drafts/`: `new-rule.json`, a valid
Standard `new-rule` without `metadata.namespace`; `example-rule.json`, a
valid Standard `example-rule` whose content differs from
`context/standards/example-rule.json`; `other-rule.json`, a valid Standard
`other-rule`; `bad-rule.json`, a Standard `bad-rule` with a schema
violation. A directory `same/` outside the repository that holds only a
copy of `drafts/new-rule.json`.

Steps:

1. Run `processkit apply -f drafts/new-rule.json -o json`. Then run
   `processkit get standard new-rule -o json` and commit.
2. Run `processkit apply -f drafts/example-rule.json -o json` without
   `--yes`.
3. Run `processkit apply -f drafts/example-rule.json --yes -o json`, then
   commit.
4. Run `processkit apply -f drafts/new-rule.json
   -f drafts/example-rule.json -o json`.
5. Run `processkit apply -f drafts/other-rule.json -f drafts/bad-rule.json
   --yes -o json`.
6. Run `processkit apply -f same --yes -o json`.
7. Pipe `drafts/other-rule.json` to
   `processkit apply -f - --yes -o name`.
8. Pipe `drafts/other-rule.json` to `processkit apply -f - -f - --yes`.

Expected results:

- Step 1 exits with 0 without confirmation; the envelope has `command`
  `apply`, its `plan` creates exactly one file,
  `context/standards/new-rule.json`, the location `repository-storage@v1`
  assigns, and `changes` lists that file; `get` returns the applied
  content.
- Step 2 is refused with `cli.confirmation-required` and exit code 4;
  `context/standards/example-rule.json` is byte-identical.
- Step 3 exits with 0, replaces `context/standards/example-rule.json`, and
  `changes` lists exactly that file.
- Step 4 exits with 0 without confirmation; `plan` has no changes,
  `changes` is empty, and every file is byte-identical.
- Step 5 fails with exit code 1 and `outcome` `failed`; a diagnostic names
  `bad-rule`; no file is created or changed, also not for `other-rule`.
- Step 6 exits with 0, `plan` has no changes, and nothing is written; the
  file of `example-rule`, which `same/` does not hold, is not deleted.
- Step 7 exits with 0, creates the file of `other-rule`, and writes exactly
  `Standard/root/other-rule`.
- Step 8 fails as a usage error with exit code 2 and writes nothing.

Covers: PK-PROD-012, PK-CLI-004, PK-CLI-014, PK-CLI-050, PK-CLI-053,
PK-CLI-054

## Verified by component tests only

- PK-CLI-009, PK-CLI-039 (filesystem boundary): a filesystem boundary
  between the current directory and an ancestor needs a mount; component
  tests drive root discovery through the filesystem port with a changed
  device ID. Journey 6 covers the descendant and basename rules.
- PK-CLI-013 (non-interactive stale plan): a change between planning and
  writing in a non-interactive run is a race; component tests inject it
  through the filesystem port. Journey 7 covers the interactive case.
- PK-CLI-025 (no secret options): checked by a component test over the
  option and environment-variable registry of every command.
- PK-CLI-027 code 5, PK-CLI-028 (internal error and full priority order):
  a defect cannot be caused from outside; component tests inject one and
  combine categories. Journey 3 covers the other codes and one priority
  pair.
- PK-CLI-029 (interruption): delivering SIGINT or SIGTERM between two file
  writes is a race; component tests inject the signal through the write
  port and check `cli.interrupted`, exit codes 130 and 143, and `changes`.
- PK-CLI-049 (extension kinds): the plural and short name that an
  OntologyExtension declares are resolved by the same type lookup as the
  names of `type_names`; component tests register an extension kind and
  check every form. Journey 12 covers the kinds of this release.
- PK-CLI-052 (`--dry-run` on every writing command): component tests run
  `client` and `server` against each writing command through the storage
  and Git ports. Journeys 4 and 11 cover `fetch` and `format`.
- PK-CLI-018, PK-CLI-019, PK-CLI-020, PK-CLI-045, PK-CLI-046, PK-CLI-047
  (release evidence): these state what the release and its pre-release
  evidence must contain (Python minors, release targets, case-sensitive
  and case-insensitive filesystems, black-box tests of platform
  differences, the `Tested platforms` section, no Windows artifact). They
  are checked by the release gate inspecting the evidence, not by a user
  journey.
