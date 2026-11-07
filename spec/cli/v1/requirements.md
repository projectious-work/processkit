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
| `processkit lock [--update [NAME]]` | Resolve upstreams and write the lock. |
| `processkit fetch` | Fetch locked upstream commits into the local cache. |
| `processkit ontology list\|show` | Read the published ontology registry. |
| `processkit access whoami\|can-i` | Show the current principal or explain an access decision. |
| `processkit mcp serve --stdio` | Serve the repository over stdio MCP. |
| `processkit mcp serve --http --listen ADDRESS` | Run the read-only shared server. |
| `processkit migrate [--from v0]` | Rewrite content to a newer content API version, or convert v0 governance content, from a reviewed plan. |
| `processkit config show` | Show effective configuration with value sources and secrets redacted. |
| `processkit version` | Report the release, ontology, and schema versions. |

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
