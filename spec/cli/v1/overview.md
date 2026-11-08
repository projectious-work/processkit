# Command-line interface — overview

Non-normative. The requirements are in `requirements.md`.

## Owner goal

The owner wants one complete, scriptable command line for everything a
person or automation does with processkit content outside an agent:
initialize repositories, author and validate content as ordinary files,
inspect what agents will receive, pin and fetch upstreams, and start the
servers (PK-PROD-005, PK-PROD-012). Because content is reviewed Git files
(C1) and agents use MCP (C4), the CLI must never become a second, hidden
write path: it writes only from reviewed plans, never touches Git state,
and returns exactly what MCP returns (C5, C10). Its machine output and
exit codes are a stable contract so that CI and other specifications can
rely on them.

## Purpose

The processkit CLI is how humans, authoring agents with shell tools, and
automation initialize repositories, create content from templates, validate
files and drafts, inspect resolved content, lock and fetch upstreams, and
start the MCP servers, without a harness or a running server (roadmap phase
PK1-P2). It is a thin adapter over the same application core as the MCP
server, so `processkit context` shows exactly what an agent would receive.
This specification fixes the command set, root selection, output and exit
contract, the plan-and-confirm discipline for writes, configuration layering
and reporting, and the supported platforms.

## Boundaries

This slug does not cover:

- the item envelope, relations, selectors, and the ontology registry —
  `ontology@v1`;
- repository layout, file formats, atomic writes, the overwrite rule
  (PK-STORE-022), and the Git boundary — `repository-storage@v1`;
- what `new` creates and what `validate` checks per kind — `content-kinds@v1`;
- upstreams, the lock, `lock`, `fetch`, overrides, and `explain` provenance —
  `inheritance@v1`;
- the MCP tools, the briefing, and context assembly —
  `mcp-context-serving@v1`;
- authenticators, Roles, Bindings, `access whoami|can-i`, and the shared
  server — `access-control@v1`;
- the threat model, size limits, network and telemetry defaults, and release
  signing and verified installation — `security@v1`;
- converting v0 content with `migrate --from v0` — `v0-migration@v1`.

## Governing decisions

- **C1** Context, not memory: content changes are reviewed file edits; the
  CLI never stages, commits, or pushes.
- **C4** MCP is the agent interface: the CLI serves humans and automation
  and mirrors MCP results so authors can inspect what agents get.
- **C5** Deterministic, cacheable assembly: `processkit context` returns
  exactly the MCP result for equal inputs.
- **C6** Inheritance through locked upstreams: reads are offline from the
  lock and cache; fetching is the explicit `fetch` command, and `lock`
  resolves only from fetched data (owner decision #213 finding 3).
- **C8** Two serving modes, read-only: `mcp serve --stdio` and
  `mcp serve --http` start the servers; neither writes content.
- **C10** Python, one application core: CLI and MCP are thin adapters over
  one core, so equivalent operations give equivalent results.

## Provenance

| Baseline (#197) | This slug |
|---|---|
| `spec/doc/v1/06-cli.md` — Commands | command table |
| 06 — Behavior | PK-CLI-001 to 007 |
| `09-security-configuration-and-output.md` — Configuration | layer list, PK-CONFIG-001 to 003 |
| 09 — Output and logging | PK-OUT-001 to 005 |
| `01-product-definition.md` — Goals | PK-PROD-005, PK-PROD-012 |
| `11-verification-and-release.md` — Acceptance journeys | journey 1 |

Supporting context (not carried as requirements): PK-ARCH-001 (Python 3.12
or later), the MCP tool signatures in `07-mcp-and-context-assembly.md` used
as CLI equivalents, and PK-STORE-021/022 of `repository-storage@v1`.

Gap items carried from the governance draft (tag
`archive/processkit-v1-governance-standards`):

| New ID | Source | Adaptation |
|---|---|---|
| PK-CLI-008 | `05-application-and-lifecycle.md` PK-CLI-024 | root marker is `processkit.toml` only; "installed-state metadata" dropped (no installed state in #197) |
| PK-CLI-009 | 05 PK-CLI-025 | unchanged |
| PK-CLI-010 | 05 PK-CLI-026 | "context directory" renamed content directory |
| PK-CLI-011 | `07-configuration-output-and-evidence.md` PK-CONFIG-009 | "project policy" read as project configuration |
| PK-CLI-012 | 05 PK-CLI-001 | binds root, operation, release, input digests; profile, adapters, ownership state, and expiration dropped (retired concepts; expiration is OPEN-cli-05) |
| PK-CLI-013 | 05 PK-CLI-002 | "apply" read as applying a plan within the writing command |
| PK-CLI-014 | 05 PK-CLI-003 | `--yes` kept; `--non-interactive` flag not carried (OPEN-cli-04) |
| PK-CLI-015 | `03-project-storage-and-ownership.md` PK-STORE-037 | unchanged |
| PK-CLI-016 | 05 PK-CLI-021 | targets per issue #165; Windows moved to OPEN-cli-09 |
| PK-CLI-017 | 05 PK-CLI-023 | unchanged |
| PK-CLI-018 to 020 | `10-verification-strategy.md` Platform matrix | Windows-specific tests made conditional on Windows support |

## Command style

The CLI follows style A of the company command-line interface design
standard (`.standards/command-line-interface-design.md`, standards
v2.2.0): Unix utility grammar with Git-style subcommands (PK-CLI-021). The
decision is to be recorded in an ADR; this is the agent's proposal.

Reasons:

- The baseline table is already Git-shaped (`processkit init`,
  `processkit validate PATH...`, `processkit ontology list`); operands are
  the primary inputs, as style A requires.
- Style B (kubectl) would force `-o json` instead of `--json`,
  `--dry-run=none|client|server`, case-insensitive kind aliases, and an
  `apply -f` path; style C would force `processkit standard list`-style
  object-first commands. Both change owner-approved commands.
- Style A keeps every baseline option (`--json`, `--dry-run`, `--yes`,
  `--root`, `--selector`, `--namespace`) unchanged.
- processkit works on files and streams (`validate -`), the case style A
  is made for.

Deviations and choices within style A:

- `lock --update [NAME]`: style A forbids an option with an optional value.
  `--update` is read as a flag and `NAME` as an optional operand that is
  allowed only with `--update`. Every baseline invocation keeps working;
  only `--update=NAME` is not accepted.
- Options may follow operands (GNU interleaving, allowed by style A), so
  `processkit validate - --json` works as the baseline journeys write it.
- Only `-h` has a one-letter form; `-n` is not defined.
- Baseline items added: `--help`, `--version`, `--no-input`, `--no-color`,
  `--` and `-`, prompts only on a terminal, `--yes` as the explicit
  confirmation option for scripts.

## Configuration layer order

The baseline puts operator configuration above project configuration; the
configuration standard lists system and user layers below the project
layer. Project and operator configuration accept disjoint keys
(PK-CONFIG-002), so no value is ever decided by their order. This is
recorded here as a non-conflict, not a reordering.

## Owner decisions applied

- #213 finding 3 (2026-11-08), "fetch, then lock": command table rows of
  `lock` and `fetch`, PK-CLI-044, `commands.lock` in `interfaces.yaml`,
  journey 4. `inheritance@v1` owns the lock semantics; PK-SEC-005 of
  `security@v1` is unchanged.
- #213 finding 4 (2026-11-08), writes need committed targets: the check is
  `repository-storage@v1` PK-STORE-056; the CLI side (refusal, exit code 4,
  `--dry-run` warning, no bypass option) is PK-CLI-036 and journey 11.

## Resolved open items

| Item | Resolution | Basis |
|---|---|---|
| OPEN-cli-01 | Exit codes 0 success, 1 validation, 2 usage, 3 environment, 4 refused (stale plan, missing or declined confirmation, uncommitted target), 5 internal, 130 SIGINT, 143 SIGTERM; priority order for several errors (PK-CLI-027 to 029). | agent proposal |
| OPEN-cli-02 | Envelope `apiVersion` `cli.processkit.projectious.work/v1`, `kind`, `command`, `outcome` (succeeded, failed, refused, cancelled, partial), `root`, `revision`, `data`, `diagnostics`; diagnostic shape with code, severity, category, scope, message, and optional location, evidence, fix, next action (PK-OUT-006, PK-OUT-007, schemas). | agent proposal |
| OPEN-cli-03 | Every command except `mcp serve` is data-bearing; writing commands carry `plan` and `changes` (PK-CLI-030, PK-CLI-031). | agent proposal |
| OPEN-cli-04 | Interactive only when stdin is a terminal and `--no-input` is absent; prompt on stderr; `y` or `yes` confirms (PK-CLI-032, PK-CLI-033). | standard: command-line-interface-design.md#baseline-for-every-style (detection); agent proposal (answers) |
| OPEN-cli-05 | `init` and `migrate` always confirm; plans live only in one invocation, have no time limit, and are never saved (PK-CLI-034, PK-CLI-035). | agent proposal |
| OPEN-cli-06 | `init` writes `/.processkit/` into the root `.gitignore` inside `# BEGIN processkit (managed block; do not edit)` / `# END processkit` (PK-CLI-037). | agent proposal |
| OPEN-cli-07 | Mapping table `mcp_mapping`; added `--limit`, `--cursor`, `--namespace`, `--kind`, `--level` options; repeatable `--profile` and `--path`; the CLI is the `local` principal (PK-CLI-040, PK-CLI-041). | agent proposal |
| OPEN-cli-08 | Draft kind from `--kind`, else the draft's `kind`; no PATH validates the whole repository; a directory PATH validates the items below it (PK-CLI-042, PK-CLI-043). | agent proposal |
| OPEN-cli-09 | Windows is not a v1 release target (PK-CLI-047). | baseline (PK-CLI-016, issue #165) |
| OPEN-cli-10 | CPython 3.12, 3.13, 3.14; tested matrix in the release notes section `Tested platforms` (PK-CLI-045, PK-CLI-046). | agent proposal |
| OPEN-cli-11 | Operator file only from `--config` or `PROCESSKIT_CONFIG`; `schema-version = 1` in every configuration file; `PROCESSKIT_ROOT`, `PROCESSKIT_CONFIG`, `PROCESSKIT_LOG_LEVEL`; unknown `PROCESSKIT_` variables warn; `redaction.patterns`; `logging.level`, `logging.sink`, `logging.file`; JSON Lines logs (PK-CONFIG-004 to 008, PK-OUT-008, PK-OUT-009). | agent proposal; standard: application-configuration.md#precedence (flag over environment), application-configuration.md#effective-configuration-and-provenance (report) |
| OPEN-cli-12 | A filesystem boundary is a device ID change; only `--root` and `PROCESSKIT_ROOT` cross it (PK-CLI-039). | agent proposal |
| OPEN-cli-13 | `init` uses the current directory as is; `repository-storage@v1` PK-STORE-043 makes it fail unless that is the working-copy top level; `init` refuses an initialized root and defaults to `--project` (PK-CLI-038). | baseline (PK-CLI-008); agent proposal (refusal, default) |
| OPEN-cli-14 | Canonical `processkit version --json` fields, covering PK-OUT-005 and PK-COMPAT-001; text output contains every value; `--version` prints `processkit <release>` (PK-OUT-010, PK-CLI-023). | agent proposal; standard: command-line-interface-design.md#baseline-for-every-style (`--version`) |
| OPEN-cli-15 | New in this pass: command style A with Git-style subcommands, option interleaving (PK-CLI-021, PK-CLI-024). | agent proposal (ADR to be written) |
| OPEN-cli-16 | New in this pass: PK-CLI-010 made decidable; `--root` naming the configured content directory is normalized with `cli.root-normalized`, every other root without `processkit.toml` fails with `cli.root-not-found` (PK-CLI-048). | agent proposal |
