# Command-line interface — requirements

This specification defines the processkit CLI: its command set, how it
selects the repository root, how its results, diagnostics, exit codes, and
logs are presented, how it plans and confirms writes, how its configuration
is layered and reported, and the platforms it supports. The CLI serves
humans, authoring agents that use shell tools, and automation, through the
same application core as the MCP server. The semantics of what individual
commands validate, resolve, assemble, or authorize belong to the slugs that
own that behavior (`ontology@v1`, `repository-storage@v1`,
`content-kinds@v1`, `inheritance@v1`, `mcp-context-serving@v1`,
`access-control@v1`, `security@v1`, `v0-migration@v1`).

Conventions: requirements use EARS; "shall" is mandatory, "should"
recommended, "may" optional; IDs are stable and never reused.

## Product scope

- **PK-PROD-005:** The processkit CLI shall cover initialization,
  validation, inspection, composition, and serving for humans and
  automation. The processkit CLI shall do so through the same application
  core as the MCP server.
- **PK-PROD-012:** processkit shall let authors create and change content
  with ordinary file edits and validate it before review. processkit shall
  also validate draft content passed as an argument without writing it.

## Commands

The processkit CLI provides these commands:

| Command | Purpose |
|---|---|
| `processkit init [--governing \| --project]` | Create configuration and the content directory in the current repository from a reviewed plan. |
| `processkit new KIND NAME` | Create an item from the published template. |
| `processkit validate [PATH...]` | Validate items, references, overrides, and the lock. Reads draft content from standard input with `-`. |
| `processkit format [PATH...]` | Rewrite items in deterministic serialization. |
| `processkit list KIND [--selector S] [--namespace N]` | List resolved items at level 0. |
| `processkit show KIND NAME [--level L] [--section S]` | Show one resolved item at a level, or one section. |
| `processkit context [--task T] [--profile P] [--path PATH]` | Assemble the context an agent would receive for the given arguments. |
| `processkit explain KIND NAME` | Show provenance, overrides, applicability basis, and validation status. |
| `processkit lock [--update [NAME]]` | Resolve upstreams from data already in the local cache and write the lock. |
| `processkit fetch` | Fetch the declared and locked upstreams into the local cache. |
| `processkit ontology list\|show` | Read the published ontology registry. |
| `processkit access whoami\|can-i` | Show the current principal or explain an access decision. |
| `processkit mcp serve --stdio` | Serve the repository over stdio MCP. |
| `processkit mcp serve --http --listen ADDRESS` | Run the read-only shared server. |
| `processkit migrate [--from v0]` | Rewrite content to a newer content API version, or convert v0 governance content, from a reviewed plan. |
| `processkit config show` | Show effective configuration with value sources and secrets redacted. |
| `processkit version` | Report the release, ontology, and schema versions. |

<!-- changed by owner decision: #213 finding 3 (2026-11-08) — rows `lock`
     and `fetch`: fetch, then lock -->

Every command also accepts the global options of `interfaces.yaml`
(`global_options`). Options that this specification adds to a command
beyond this table are listed with the command in `interfaces.yaml`
(`commands`) and marked `basis: agent-proposal`.

## Behavior

- **PK-CLI-001:** Every command available in both the processkit CLI and
  the MCP server shall call the same application operation and shall
  produce equivalent results and diagnostics.
- **PK-CLI-002:** Every data-bearing command of the processkit CLI shall
  support `--json` with a versioned result envelope. Text output is a
  projection and shall not be the only way to obtain names, digests,
  provenance, or diagnostics.
- **PK-CLI-003:** The processkit CLI shall use exit codes that distinguish
  success, validation failure, usage error, and environment failure, and
  those exit codes shall be documented.
- **PK-CLI-004:** When a command writes, the processkit CLI shall print its
  plan, and every writing command shall support `--dry-run`. Only `init`,
  `new`, `format`, `lock`, and `migrate` shall write repository files;
  `fetch` shall write only the local cache.
- **PK-CLI-005:** The processkit CLI shall run read commands offline from
  committed files, the lock, and the local cache. If a read command needs an
  upstream that has not been fetched, then the processkit CLI shall report
  it as an environment failure together with the fix.
- **PK-CLI-006:** The processkit CLI shall not stage, commit, push, or open
  pull requests.
- **PK-CLI-007:** When `processkit context` is run, the processkit CLI shall
  return exactly what the MCP server would return for the same principal and
  arguments, so authors can inspect what agents receive.
- **PK-CLI-044:** When `processkit lock` runs, the processkit CLI shall
  resolve upstreams only from data that `processkit fetch` has already
  stored in the local cache, and shall not access the network. If data that
  `lock` needs is not in the local cache, then the processkit CLI shall
  report `cli.upstream-not-fetched` as an environment failure with the fix
  (run `processkit fetch`), and shall not write the lock. The semantics of
  resolution belong to `inheritance@v1`.
  <!-- changed by owner decision: #213 finding 3 (2026-11-08) -->

## Command style

- **PK-CLI-021:** The processkit CLI shall follow style A (Unix utility,
  with Git-style subcommands) of the company command-line interface design
  standard, and the baseline of that standard, for every command. Commands
  and subcommands are words before the operands; options are long names;
  operands carry only the primary inputs (KIND, NAME, PATH, CONCEPT).
  <!-- agent proposal: OPEN-cli-15 -->
- **PK-CLI-022:** When `-h` or `--help` is given to any command, the
  processkit CLI shall print help that begins with examples to standard
  output, shall ignore the other arguments, and shall exit with code 0. If
  a command that requires operands gets none, then the processkit CLI shall
  print short help to standard error and shall fail with
  `cli.missing-argument` as a usage error.
- **PK-CLI-023:** When `processkit --version` is run, the processkit CLI
  shall print exactly one line, `processkit <release>`, to standard output
  and shall exit with code 0. `-v` shall not mean version.
- **PK-CLI-024:** The processkit CLI shall treat `--` as the end of option
  parsing. The processkit CLI shall accept options before and after
  operands. An option value shall never be optional.
  <!-- agent proposal: OPEN-cli-15 -->
- **PK-CLI-025:** The processkit CLI shall not accept a secret as the value
  of an option or of a `PROCESSKIT_` environment variable.
- **PK-CLI-026:** The processkit CLI shall write plain output without color
  or other terminal control sequences when standard output is not a
  terminal, when the environment variable `NO_COLOR` is set to a non-empty
  value, or when `--no-color` is given.

## Exit codes and outcomes

- **PK-CLI-027:** The processkit CLI shall exit with these codes: 0 for
  success, 1 for validation failure, 2 for usage error, 3 for environment
  failure, 4 for refusal, 5 for internal error, 130 for interruption by
  SIGINT, and 143 for termination by SIGTERM. The meaning of each category
  is listed in `interfaces.yaml` (`exit_codes`). A configuration file that
  violates its schema is a validation failure.
  <!-- agent proposal: OPEN-cli-01 -->
- **PK-CLI-028:** The processkit CLI shall derive the exit code from the
  `category` of the diagnostics with severity `error`. If there are several,
  then the first category in this order shall decide: `cancelled`,
  `internal`, `usage`, `environment`, `refused`, `validation`. If there is
  none, then the exit code shall be 0. Warnings shall not change the exit
  code.
  <!-- agent proposal: OPEN-cli-01 -->
- **PK-CLI-029:** If the processkit CLI receives SIGINT or SIGTERM, then it
  shall stop before it starts another file write, shall report
  `cli.interrupted` with outcome `cancelled`, and shall report every file it
  already changed in `changes`.
  <!-- agent proposal: OPEN-cli-01 -->

## Machine output

- **PK-CLI-030:** Every command except `mcp serve` shall be data-bearing
  and shall accept `--json`. If `--json` is given to `mcp serve`, then the
  processkit CLI shall fail with `cli.option-not-applicable` as a usage
  error.
  <!-- agent proposal: OPEN-cli-03 -->
- **PK-CLI-031:** In text mode, a writing command shall print its plan to
  standard output when `--dry-run` is given, and to standard error
  otherwise. When a writing command runs with `--json`, its envelope
  shall carry the plan in `plan` (`schemas/plan.schema.json`) and the files
  it actually changed in `changes`. With `--dry-run`, and when the plan is
  refused, `changes` shall be empty.
  <!-- agent proposal: OPEN-cli-03 -->

## Equivalence with MCP

- **PK-CLI-040:** When a command has an MCP equivalent, the processkit CLI
  shall map its operands and options to the tool arguments as listed in
  `interfaces.yaml` (`mcp_mapping`), shall omit every argument whose option
  is not given, and shall put the tool's structured result in `data` and
  its diagnostics in `diagnostics`.
  <!-- agent proposal: OPEN-cli-07 -->
- **PK-CLI-041:** The processkit CLI shall act as the `local` principal of
  `access-control@v1` (the operating-system user that runs the command).
  `processkit context` shall therefore return what a stdio MCP server
  started by the same user returns.
  <!-- agent proposal: OPEN-cli-07 -->

## Validation input

- **PK-CLI-042:** When `processkit validate -` reads a draft from standard
  input, the processkit CLI shall use the value of `--kind` as the kind if
  it is given, and otherwise the draft's own `kind` field. If neither gives
  a kind, then the draft shall fail validation. The processkit CLI shall not
  accept `-` together with a PATH.
  <!-- agent proposal: OPEN-cli-08 -->
- **PK-CLI-043:** When `processkit validate` is run without PATH, the
  processkit CLI shall validate the whole selected repository: project
  configuration, every item in the content directory, references,
  overrides, and the lock. When a PATH names a directory, the processkit CLI
  shall validate every item file below it. Named files shall be validated in
  the context of the selected repository. When `processkit format` is run
  without PATH, it shall format every item in the content directory.
  <!-- agent proposal: OPEN-cli-08 -->

## Repository root selection

- **PK-CLI-008:** The processkit CLI shall select the repository root from,
  in order: an explicit `--root`, then the `PROCESSKIT_ROOT` environment
  variable, then the nearest ancestor of the current directory (including
  the current directory) that contains `processkit.toml`. If none of these
  yields a root, then the processkit CLI shall use the current directory
  only for `init` and shall fail for every other command that requires a
  repository.
  <!-- from governance draft: 05-application-and-lifecycle.md PK-CLI-024 -->
- **PK-CLI-009:** When discovering the repository root, the processkit CLI
  shall not search configured lists of roots, shall not cross a filesystem
  boundary implicitly, shall not select a descendant of the current
  directory, and shall not choose between several repositories by basename.
  <!-- from governance draft: 05-application-and-lifecycle.md PK-CLI-025 -->
- **PK-CLI-010:** If `--root` names the content directory instead of the
  repository root, then the processkit CLI shall report an error, unless it
  can unambiguously normalize the path to the owning repository root; when
  it normalizes, it shall report the normalized root before any write.
  <!-- from governance draft: 05-application-and-lifecycle.md PK-CLI-026 -->
- **PK-CLI-011:** The processkit CLI shall resolve root selection before it
  loads any other project configuration. After root selection has loaded
  project configuration, environment and invocation layers shall not change
  the selected root.
  <!-- from governance draft: 07-configuration-output-and-evidence.md
       PK-CONFIG-009 -->
- **PK-CLI-038:** When `processkit init` uses the current directory
  (PK-CLI-008), the processkit CLI shall use the current directory as it
  is, and shall not move to the top level of the Git working copy. If the
  selected root already contains `processkit.toml`, then `init` shall fail
  with `cli.already-initialized` as a refusal and shall write no file. If
  neither `--governing` nor `--project` is given, then `init` shall
  initialize a project repository. If the current directory is not the top
  level of a Git working copy, then `init` fails as `repository-storage@v1`
  PK-STORE-043 states.
  <!-- agent proposal: OPEN-cli-13 -->
- **PK-CLI-039:** When discovering the repository root, the processkit CLI
  shall stop at a filesystem boundary: a directory whose device ID differs
  from the device ID of the directory below it on the search path. Only
  `--root` and `PROCESSKIT_ROOT` shall select a root across such a
  boundary.
  <!-- agent proposal: OPEN-cli-12 -->
- **PK-CLI-048:** If `--root` or `PROCESSKIT_ROOT` names a directory
  without `processkit.toml`, and the nearest ancestor of that directory
  that contains `processkit.toml` configures exactly that directory as its
  content directory, then the processkit CLI shall select that ancestor as
  the root and shall report `cli.root-normalized` (severity `info`) before
  it does anything else. In every other case where the named directory has
  no `processkit.toml`, every command except `init` shall fail with
  `cli.root-not-found` as an environment failure.
  <!-- agent proposal: OPEN-cli-16 -->

## Reviewed plans

A reviewed plan is the plan a writing command prints before it writes, as
required by PK-CLI-004. `init` and `migrate` write only from a reviewed
plan. Confirmation of a plan that overwrites files processkit did not
create in the same command is required by PK-STORE-022 of
`repository-storage@v1`; this section adds how a plan is bound and
confirmed.

- **PK-CLI-012:** When the processkit CLI creates a plan for a writing
  command, the plan shall bind the selected repository root, the operation,
  the processkit release, and the digest of every input the plan was
  computed from.
  <!-- from governance draft: 05-application-and-lifecycle.md PK-CLI-001 -->
- **PK-CLI-013:** If any bound input or any target path of a plan changed
  after the plan was created, then the processkit CLI shall refuse to apply
  the plan and shall write no file.
  <!-- from governance draft: 05-application-and-lifecycle.md PK-CLI-002 -->
- **PK-CLI-014:** When a plan overwrites, replaces, or deletes an existing
  file, the processkit CLI shall apply the plan only after explicit
  confirmation. If the processkit CLI runs
  non-interactively, then it shall treat only `--yes` as confirmation and,
  without `--yes`, shall refuse to apply the plan and write no file.
  <!-- from governance draft: 05-application-and-lifecycle.md PK-CLI-003 -->
- **PK-CLI-015:** When a command updates a Git ignore file, the processkit
  CLI shall include the change in the command's plan, confine it to a
  marked processkit block, make it idempotent, and preserve all content
  outside that block byte for byte.
  <!-- from governance draft: 03-project-storage-and-ownership.md
       PK-STORE-037 -->
- **PK-CLI-032:** The processkit CLI shall run interactively only when
  standard input is a terminal and `--no-input` is not given. Otherwise it
  shall run non-interactively and shall not prompt.
- **PK-CLI-033:** When the processkit CLI asks for confirmation
  interactively, it shall print the plan and the question to standard
  error, and shall accept only `y` or `yes` (in any letter case) as
  confirmation. Any other answer, or end of input, shall refuse the plan
  with `cli.confirmation-declined`, and no file shall be written. When
  `--yes` is given, the processkit CLI shall not ask.
  <!-- agent proposal: OPEN-cli-04 -->
- **PK-CLI-034:** `processkit init` and `processkit migrate` shall always
  require confirmation, also when their plan only creates files. Other
  writing commands shall require confirmation as PK-CLI-014 states. If a
  plan that requires confirmation runs non-interactively without `--yes`,
  then the processkit CLI shall refuse it with `cli.confirmation-required`.
  <!-- agent proposal: OPEN-cli-05 -->
- **PK-CLI-035:** A plan shall be valid only inside the invocation that
  computed it. The processkit CLI shall not save a plan for later use and
  shall not accept a plan as input. A plan shall have no time limit; the
  staleness check of PK-CLI-013 shall run after confirmation and
  immediately before the first write, and shall report `cli.plan-stale`.
  <!-- agent proposal: OPEN-cli-05 -->
- **PK-CLI-036:** Before the processkit CLI asks for confirmation or
  writes a repository file, it shall run the committed-target check of
  `repository-storage@v1` (PK-STORE-056). If a target fails the check, then
  the processkit CLI shall report each `storage.target-not-committed`
  diagnostic as a refusal with the fix (commit or stash the change, then
  run the command again), shall exit with code 4, and shall write no file.
  With `--dry-run`, the processkit CLI shall report the same diagnostics
  with severity `warning`. No option shall bypass the check.
  <!-- changed by owner decision: #213 finding 4 (2026-11-08) -->
- **PK-CLI-037:** When `processkit init` runs, the processkit CLI shall
  ensure that the Git ignore file `.gitignore` in the repository root
  ignores `/.processkit/`. It shall create the file if it is absent. It
  shall write the entry in a block that starts with the line
  `# BEGIN processkit (managed block; do not edit)` and ends with the line
  `# END processkit`, and shall append the block at the end of the file if
  no block exists.
  <!-- agent proposal: OPEN-cli-06 -->

## Supported platforms

- **PK-CLI-016:** The processkit CLI shall support x86_64 and arm64 Linux
  and x86_64 and arm64 macOS as release targets. Each release shall state
  the platform matrix it was actually tested on.
  <!-- from governance draft: 05-application-and-lifecycle.md PK-CLI-021 -->
- **PK-CLI-017:** The processkit CLI shall not assume a shell, a GNU
  userland, a writable home directory, or ambient Git credentials for any
  command.
  <!-- from governance draft: 05-application-and-lifecycle.md PK-CLI-023 -->
- **PK-CLI-018:** Pre-release evidence for every release shall include test
  results for every supported Python minor version and every supported
  release target.
  <!-- from governance draft: 10-verification-strategy.md Platform matrix -->
- **PK-CLI-019:** Where a supported target offers case-sensitive and
  case-insensitive filesystems, filesystem-sensitive behavior shall be
  tested on both.
  <!-- from governance draft: 10-verification-strategy.md Platform matrix -->
- **PK-CLI-020:** Where a supported target differs from Linux in path
  handling, file locking, file replacement, signals, or terminal behavior,
  that behavior shall be verified by explicit black-box tests on that target
  and shall not be inferred from Linux results. Where Windows becomes a
  supported target, this applies to Windows.
  <!-- from governance draft: 10-verification-strategy.md Platform matrix -->
- **PK-CLI-045:** The processkit CLI shall support CPython 3.12, 3.13, and
  3.14 on every release target.
  <!-- agent proposal: OPEN-cli-10 -->
- **PK-CLI-046:** The release notes of every release shall contain a
  section `Tested platforms` that lists every tested combination of
  operating system and version, architecture, and Python version.
  <!-- agent proposal: OPEN-cli-10 -->
- **PK-CLI-047:** processkit v1 shall not publish release artifacts for
  Windows. Windows is not a release target of v1.

## Configuration

Configuration has three layers, lowest precedence first:

1. project configuration `processkit.toml`, committed: content directory,
   profiles, document sources, upstreams, override winners, briefing budget;
2. operator configuration, outside the repository: listen address, TLS
   material, authenticators, imported access rules, limits, log sinks;
3. invocation flags and `PROCESSKIT_` environment variables.

- **PK-CONFIG-001:** processkit shall use a closed, versioned schema for
  every configuration file. If a configuration file contains an unknown key,
  then processkit shall fail.
- **PK-CONFIG-002:** processkit shall not accept project configuration that
  configures authenticators, credentials, listen addresses, or executables.
- **PK-CONFIG-003:** When `processkit config show --json` is run, the
  processkit CLI shall report the effective configuration with the source of
  every value and with secrets redacted.

- **PK-CONFIG-004:** processkit shall load operator configuration only
  from the file that `--config PATH` names, or else the file that
  `PROCESSKIT_CONFIG` names. processkit shall not read operator
  configuration from any implicit location. If the named file does not
  exist or cannot be read, then processkit shall fail with
  `cli.config-unreadable` as an environment failure.
  <!-- agent proposal: OPEN-cli-11 -->
- **PK-CONFIG-005:** Every configuration file shall declare the top-level
  key `schema-version` with the integer value `1`. If the key is missing or
  has another value, then processkit shall fail with
  `cli.config-version-unsupported`.
  <!-- agent proposal: OPEN-cli-11 -->
- **PK-CONFIG-006:** In the invocation layer, an option shall take
  precedence over the `PROCESSKIT_` environment variable for the same key.
  An option shall affect only the invocation in which it is given.
- **PK-CONFIG-007:** The report of `processkit config show` shall list, in
  key order, every supported key exactly once with its redacted effective
  value, its source, and its origin; it shall also list the loaded and
  absent configuration files and every rejected setting with its reason
  (`schemas/config-report.schema.json`).
- **PK-CONFIG-008:** If the environment contains a `PROCESSKIT_` variable
  that processkit does not define, then processkit shall report
  `cli.unknown-environment-variable` as a warning and shall otherwise
  ignore the variable.
  <!-- agent proposal: OPEN-cli-11 -->

## Output and logging

- **PK-OUT-001:** When JSON output is requested, processkit shall emit
  exactly one versioned result envelope containing outcome, data,
  diagnostics, and revision.
- **PK-OUT-002:** processkit shall write results to standard output and
  diagnostics to standard error.
- **PK-OUT-003:** processkit shall write operational logs as structured
  records, with a default level of `warning`, to standard error unless an
  operator configures another sink.
- **PK-OUT-004:** processkit shall redact bearer material, certificates, and
  values matching configured secret patterns from logs, diagnostics, and
  errors.
- **PK-OUT-005:** When `processkit version --json` is run, the processkit
  CLI shall report the release, source commit, ontology version, supported
  content API versions, and supported MCP protocol versions.
- **PK-OUT-006:** The result envelope shall have exactly the members of
  `schemas/result-envelope.schema.json`. Its `apiVersion` shall be
  `cli.processkit.projectious.work/v1`. Its `outcome` shall be
  `succeeded` for exit code 0, `refused` for exit code 4, `cancelled` for
  exit codes 130 and 143, `partial` for exit codes 3 and 5 when the
  command changed at least one file, and `failed` otherwise.
  <!-- agent proposal: OPEN-cli-02 -->
- **PK-OUT-007:** Every diagnostic shall have the shape of
  `schemas/diagnostic.schema.json`, with a stable code of the form
  `<area>.<condition>`. processkit shall write every diagnostic as text to
  standard error, also when `--json` is given. A text diagnostic shall
  contain its severity, code, and message, and its fix, if any, shall be its
  last line.
  <!-- agent proposal: OPEN-cli-02 -->
- **PK-OUT-008:** processkit shall write each operational log record as one
  JSON line in the shape of `schemas/log-record.schema.json`. The log level
  shall be set by `--log-level`, else `PROCESSKIT_LOG_LEVEL`, else the
  operator key `logging.level`, else `warning`. The sink shall be standard
  error, or a file when the operator configuration sets `logging.sink` to
  `file` and `logging.file` to an absolute path. If the file sink cannot be
  opened, then processkit shall fail with `cli.log-sink-unavailable` as an
  environment failure.
  <!-- agent proposal: OPEN-cli-11 -->
- **PK-OUT-009:** processkit shall read secret patterns from the operator
  key `redaction.patterns`, a list of regular expressions. processkit shall
  replace every redacted value with the text `[REDACTED]`.
  <!-- agent proposal: OPEN-cli-11 -->
- **PK-OUT-010:** When `processkit version --json` is run, the processkit
  CLI shall report the fields of `schemas/version.schema.json`: `release`,
  `sourceCommit`, `ontologyVersion`, `contentApiVersions`,
  `mcpProtocolVersions`, `mcpToolContractVersion`, `resultContractVersion`,
  and `lockFormatVersion`. These fields are the canonical report of
  PK-OUT-005 and of PK-COMPAT-001 (`v0-migration@v1`). The text output of
  `processkit version` shall contain every one of these values.
  <!-- agent proposal: OPEN-cli-14 -->
