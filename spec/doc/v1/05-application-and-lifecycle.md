# Application and lifecycle

## Distribution

The reference implementation is installed as a Python application with
`uv tool install processkit==<exact-version>` or an equivalent isolated Python
application installer. Releases publish a wheel, source distribution, source
archive, checksums, SBOM, and signature or attestation material.

- **PK-CLI-000:** the installed CLI is `processkit`; `pk` MAY be supplied as a
  documented alias. All commands accept `--root` and operate on exactly one
  project root.

## Command surface

| Command | Purpose |
|---|---|
| `processkit version` | Report product, source, runtime, and contract versions. |
| `processkit help` | Show stable command help. |
| `processkit list KIND` | List installed `skills`, `ontology`, `packages`, `profiles`, `mcp-servers`, or other declared catalog kinds. |
| `processkit init` | Create a new installation plan for an uninitialized root. |
| `processkit plan` | Preview install, update, profile, adapter, or removal changes. |
| `processkit apply --plan PLAN` | Apply an exact reviewed plan. |
| `processkit verify` | Verify ownership, contracts, projections, and derived state. |
| `processkit doctor [--reconcile]` | Diagnose and optionally apply bounded safe repairs. |
| `processkit migrate` | Plan or apply an explicit contract/data migration. |
| `processkit reindex` | Rebuild disposable indexes from canonical files. |
| `processkit generate` | Regenerate declared schemas, indexes, docs, or projections. |
| `processkit mcp serve` | Serve the configured MCP capability set. |
| `processkit mcp proxy` | Adapt stdio to an explicitly configured local MCP endpoint. |
| `processkit package validate` | Validate a package or extension in isolation. |

- **PK-CLI-009:** EntityType- and skill-specific convenience commands MAY be
  added after their MCP operations are stable. They use the same application
  services rather than reimplementing semantics.
- **PK-CLI-013:** `list` MUST be read-only and return canonical identity,
  version, source package, installation status, enabled state where
  applicable, and compatibility metadata in text and versioned machine form.
- **PK-CLI-014:** listable kinds MUST derive from the installed ontology and
  capability catalogs. The CLI MUST NOT maintain a second hard-coded catalog
  that can drift from MCP discovery or package manifests.

## Lifecycle requirements

- **PK-CLI-001:** lifecycle plans MUST bind root identity, operation, release,
  profile, adapters, current ownership state, input digests, and expiration.
- **PK-CLI-002:** apply MUST refuse a plan when any bound input or relevant
  target path changed after planning.
- **PK-CLI-003:** destructive changes require an explicit plan and confirmation;
  non-interactive confirmation requires both `--non-interactive` and `--yes`.
- **PK-CLI-004:** `init`, `plan`, `verify`, and doctor without `--reconcile`
  MUST be read-only with respect to canonical project state.
- **PK-CLI-005:** `doctor --reconcile` MAY repair only registered,
  deterministic, idempotent, locally contained derived or processkit-owned
  state.
- **PK-CLI-006:** doctor MUST NOT rewrite project entities, accept policy,
  install runtimes, fetch releases, or resolve semantic conflicts.
- **PK-CLI-007:** migration MUST separate analysis, plan, application, and
  verification and MUST preserve a recovery record.
- **PK-CLI-008:** all mutating commands MUST support interruption and report
  whether rollback completed, recovery is required, or no mutation occurred.

## Exit categories

| Code | Category |
|---:|---|
| 0 | Success or completed diagnostic with no blocking finding. |
| 2 | Invalid invocation or malformed input. |
| 3 | Contract, policy, or compatibility refusal. |
| 4 | Conflict or stale plan. |
| 5 | Dependency or environment unavailable. |
| 6 | Operation failed with canonical state preserved. |
| 7 | Recovery or manual inspection required. |
| 130 | Interrupted by SIGINT where supported. |

- **PK-CLI-010:** exit meanings MUST remain stable within v1.x.
- **PK-CLI-011:** commands MUST NOT use success for skipped required work,
  unresolved conflicts, or unavailable checks that determine correctness.
- **PK-CLI-012:** cancellation and termination handling MUST be tested on every
  supported operating system, with platform differences documented.

## Supported environments

- **PK-CLI-020:** v1 supports CPython 3.12 and later minor versions explicitly
  listed in release metadata.
- **PK-CLI-021:** v1 targets current supported Linux, macOS, and Windows on
  x86-64 and ARM64 where CPython and uv support are available; each release
  MUST state its actually tested matrix.
- **PK-CLI-022:** default operation MUST be local and offline after application
  and package installation; network access requires an explicit command or
  authorized configuration.
- **PK-CLI-023:** no command may assume a shell, GNU userland, writable home
  directory, or ambient Git credentials.
- **PK-CLI-024:** root selection resolves an explicit `--root`, then
  `PROCESSKIT_ROOT`, then the nearest ancestor containing `processkit.toml` or
  processkit installed-state metadata; otherwise it uses the current directory
  only for `init` and fails for commands requiring an installation.
- **PK-CLI-025:** root discovery MUST NOT search configured root lists, cross a
  filesystem boundary implicitly, select a descendant, or choose between
  multiple repositories by basename.

## Post-v1 CLI directions

These directions are intentionally outside the v1.0.0 release gate and need
separate accepted contracts before implementation:

- skill authoring, installation, update, enablement, deprecation, and removal;
- provider-neutral prompt assets and their harness-specific slash-command
  projections;
- memory review, promotion, compaction, archival, restoration, retention, and
  pruning, informed by v0 behavior; and
- company-specific processkit distributions carrying organization-wide
  processes, policy, skills, prompts, profiles, and MCP capabilities.

Memory lifecycle design MUST first distinguish durable repository memory from
harness conversation/session context and analyze overlap with harnesses such
as tau. Company-distribution design MUST compare upstream package composition,
private distributions, overlays, and downstream forks, and define provenance,
trust, naming, compatibility, update cadence, and continuous upstream
reconciliation. No particular adaptation mechanism is selected by v1.
