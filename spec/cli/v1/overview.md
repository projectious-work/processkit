# Command-line interface — overview

Non-normative. The requirements are in `requirements.md`.

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
  lock and cache; fetching is the explicit `fetch` command.
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

## Open questions

Mirrors `open` in `interfaces.yaml`.

1. OPEN-cli-01 — numeric exit codes and whether stale-plan, missing
   confirmation, and interruption get their own codes.
2. OPEN-cli-02 — result envelope keys, version field, outcome values, and
   diagnostic shape.
3. OPEN-cli-03 — which commands are data-bearing; plan and changed-files
   fields in the envelope.
4. OPEN-cli-04 — how non-interactive mode is detected; interactive
   confirmation.
5. OPEN-cli-05 — whether `init` and `migrate` always need confirmation; plan
   expiry; saved plans.
6. OPEN-cli-06 — whether `init` writes an ignore entry, into which file, and
   the block markers.
7. OPEN-cli-07 — CLI-to-MCP argument mapping and the CLI principal for
   `context`.
8. OPEN-cli-08 — kind of a draft read from `-`; default PATH of `validate`.
9. OPEN-cli-09 — whether Windows is a supported release target.
10. OPEN-cli-10 — supported Python minor versions; where the tested matrix
    is stated.
11. OPEN-cli-11 — operator configuration location and schema version; other
    flags and `PROCESSKIT_` variables; secret patterns; log level control.
12. OPEN-cli-12 — definition of a filesystem boundary.
13. OPEN-cli-13 — `init` from a subdirectory of a working copy.
14. OPEN-cli-14 — field names and text format of `processkit version`.
