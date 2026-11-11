# 1. CLI command style: verb–resource (kubectl)

Date: 2026-11-11

## Status

Accepted. Owner decision on #212 (agent working conversation, 2026-11-11):
style B, with `apply -f`, root-Container default scope with `-A`, kubectl
names for `explain` and `describe`, and all four output formats. Replaces
the 2026-11-08 proposal of style A.

## Context

The company command-line interface design standard
(`.standards/command-line-interface-design.md`, standards v2.2.0) requires
every CLI to record exactly one command style:

- A: Unix utility;
- B: verb–resource, as in kubectl;
- C: object–action, as in OpenStackClient.

processkit manages many resource types of one API (the kinds of
`ontology@v1` and `content-kinds@v1`) with a shared set of read operations
and declarative, Git-tracked state. That is the case style B is meant for.
The #197 command table was Git-shaped (`list KIND`, `show KIND NAME`,
`--json`), so style B changes owner-approved commands; the owner accepted
that.

## Decision

The processkit CLI uses style B, the verb–resource style of kubectl, plus
the standard's baseline for every command (`cli@v1` PK-CLI-021 to
PK-CLI-026, PK-CLI-049 to PK-CLI-055).

Grammar: `processkit <verb> <type> [<name>...] [options]`. `<type>/<name>`
is accepted wherever `<type> <name>` is, and `-f`/`--filename` names input
files. Commands that do not act on a resource type are non-resource
commands, as `version`, `config view`, and `api-resources` are in kubectl.

| #197 / style A | Style B | MCP equivalent |
|---|---|---|
| `init [--governing \| --project]` | `init [--governing \| --project]` (non-resource) | — |
| `new KIND NAME` | `create TYPE NAME` | — |
| — | `apply -f FILE\|DIR\|-` (new) | — |
| `validate [PATH... \| -] [--kind K]` | `validate [TYPE [NAME...]] [-f PATH\|-]...` | `validate` |
| `format [PATH...]` | `format [TYPE [NAME...]] [-f PATH]...` | — |
| `list KIND [--selector S] [--namespace N]` | `get TYPE [-l S] [-n N \| -A]` | `list` |
| `show KIND NAME [--level L] [--section S]` | `get TYPE NAME [-n N] [--level L] [--section S]` | `get` |
| `context [--task T] [--profile P]...` | `get context [--task T] [--profile P]...` | `get_context` |
| `explain KIND NAME` | `describe TYPE NAME [-n N]` | `explain` |
| `ontology list` | `api-resources` (non-resource) | `ontology()` |
| `ontology show CONCEPT` | `explain TYPE` | `ontology(concept)` |
| `lock [--update [NAME]]` | `lock [--update] [UPSTREAM...]` (non-resource) | — |
| `fetch` | `fetch` (non-resource) | — |
| `access whoami` | `auth whoami` | — |
| `access can-i VERB KIND [NAME] --as USER` | `auth can-i VERB TYPE [NAME] --as USER [-n N]` | — |
| `mcp serve --stdio \| --http --listen ADDRESS` | unchanged (non-resource) | — |
| `migrate [--from v0]` | unchanged (non-resource) | — |
| `config show` | `config view` (non-resource) | — |
| `version` | unchanged (non-resource) | — |

Options:

| #197 / style A | Style B |
|---|---|
| `--json` | `-o json` (`-o`/`--output` `json`, `yaml`, `name`, `wide`) |
| `--namespace N` | `-n N` / `--namespace N`; default the root Container |
| — | `-A` / `--all-namespaces` (`get TYPE` only) |
| `--selector S` | `-l S` / `--selector S` |
| `PATH` operands, `-` | `-f PATH` / `--filename PATH`, repeatable; `-f -` reads standard input |
| `--dry-run` | `--dry-run=none\|client\|server`; bare `--dry-run` means `client` |
| `--yes`, `--root`, `--config`, `--no-input`, `--no-color`, `--log-level` | unchanged |

Rules that style B adds:

- **Type names** (PK-CLI-049): case-insensitive; each kind accepts its
  singular, its plural, and one short name (table `type_names` in
  `cli@v1`; extension kinds declare `plural` and `shortName` in their
  OntologyExtension, `ontology@v1`). Resource names are case-sensitive.
  Omitting the name addresses every resource of the type.
- **Output** (PK-CLI-050): `-o json` is the result envelope; `-o yaml` is the
  same envelope as YAML; `-o name` prints one `<Kind>/<namespace>/<name>` per
  line (`get`, `create`, `apply`, `format`); `-o wide` is text with extra columns. Default text output and `wide`
  are not a contract.
- **Scope** (PK-CLI-051): without `-n`, a command uses the root Container;
  `-A` lists every namespace (the CLI then omits `namespace` from the MCP
  call).
- **Dry run** (PK-CLI-052): `client` computes and prints the plan and
  reports failed committed-target checks only as warnings; `server` runs
  every check a real run runs, with real-run severity
  (committed targets, validation of the planned content, for `fetch`
  resolution over the network) and then stops before confirmation and
  writing.
- **Declarative path** (PK-CLI-053): `apply -f` writes item documents to
  their canonical locations, creating or replacing, through the usual
  plan and confirmation. It never deletes.
- **Plugins** (PK-CLI-055): v1 has no plugin mechanism; processkit never
  executes `processkit-<name>` programs.

## Consequences

- Every #197 command and the earlier `--json` option change name; each
  changed baseline requirement carries `<!-- changed by owner decision:
  2026-11-11 (#212), CLI style B -->`. Every specification that shows a
  command was updated in the same change.
- The style-A deviation for `lock --update [NAME]` is gone: under style B,
  `UPSTREAM...` are operands allowed only with `--update`.
- CLI `explain` documents a type (MCP `ontology`), and CLI `describe`
  explains an item (MCP `explain`). The `mcp_mapping` table of `cli@v1` is
  the authority for which tool each command calls.
- `apply -f` is a new writing command; `get context` uses `context` as a
  read-only virtual type that names no stored resource.
- New commands follow style B, even where another style would read better
  in that one place.
