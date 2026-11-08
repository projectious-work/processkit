# 1. CLI command style: Unix utility with Git-style subcommands

Date: 2026-11-08

## Status

Proposed (agent proposal, to be approved with the `cli@v1` freeze, #212).

## Context

The company command-line interface design standard
(`.standards/command-line-interface-design.md`, standards v2.2.0) requires
every CLI to record exactly one command style:

- A: Unix utility;
- B: verb–resource, as in kubectl;
- C: object–action, as in OpenStackClient.

The owner-approved v1 command table (#197) already reads like Git:

- top-level verbs such as `init`, `validate PATH...`, `lock`, and `fetch`;
- grouped subcommands such as `ontology list`, `mcp serve`, and
  `config show`;
- operands that carry only the primary inputs (KIND, NAME, PATH);
- machine output through `--json`.

## Decision

The processkit CLI uses style A, the Unix utility style with Git-style
subcommands, plus the standard's baseline for every command (`cli@v1`
PK-CLI-021 to PK-CLI-026).

## Consequences

- Every baseline command and option stays as approved.
- Style B would have forced `-o json`, `--dry-run=none|client|server`, and
  kind aliases. Style C would have forced object-first commands. Both would
  change owner-approved behavior.
- One deviation is recorded in `spec/cli/v1/overview.md`:
  `lock --update [NAME]` is read as a flag plus an optional operand, because
  style A never allows an optional option argument.
- New commands follow style A, even where another style would read better
  in that one place.
