# Application and lifecycle

## Distribution

The reference implementation is installed as a Python application with
`uv tool install processkit==<exact-version>` or an equivalent isolated Python
application installer. Releases publish a wheel, source distribution, source
archive, checksums, SBOM, and signature or attestation material.

- **PK-CLI-000:** the installed CLI is `processkit`; `pk` MAY be supplied as a
  documented alias. All repository commands accept `--root`, where root means
  exactly one repository working copy rather than its `context/` directory.

## Command surface

| Command | Purpose |
|---|---|
| `processkit version` | Report product, source, runtime, and contract versions. |
| `processkit help` | Show stable command help. |
| `processkit list KIND` | List installed `skills`, `ontology`, `packages`, `profiles`, `mcp-servers`, `harness-adapters`, or another declared catalog kind. |
| `processkit show KIND NAME` | Describe one catalog entry and its source, version, compatibility, and enabled state. |
| `processkit init [--harness TARGET...]` | Convenience form of `plan install` for an uninitialized repository; it creates a reviewable plan and does not apply it. |
| `processkit plan OPERATION` | Preview install, update, reconcile, profile, adapter, or removal changes. |
| `processkit apply --plan PLAN` | Apply an exact reviewed plan. |
| `processkit verify` | Verify ownership, contracts, projections, and derived state. |
| `processkit doctor [--reconcile]` | Diagnose and optionally apply bounded safe repairs. |
| `processkit migrate plan|apply|verify` | Operate an explicit contract or data migration through reviewed phases. |
| `processkit index status|rebuild` | Inspect or rebuild disposable lexical, semantic, and vector indexes. |
| `processkit generate TARGET` | Regenerate declared schemas, documentation, or manifests that do not require installation reconciliation. |
| `processkit entity get ID` | Read one canonical entity by typed ID or exact repository-relative path. |
| `processkit entity list [TYPE]` | List entities with state, scope, relation, and pagination filters. |
| `processkit entity search QUERY` | Run lexical, semantic, or hybrid retrieval with explicit method and filters. |
| `processkit entity create TYPE` | Create an entity from structured input through its declared operation. |
| `processkit entity update ID` | Update fields allowed by the entity contract. |
| `processkit entity transition ID STATE` | Apply a declared lifecycle transition. |
| `processkit entity link SUBJECT RELATION TARGET` | Create a validated relation or Binding. |
| `processkit entity supersede OLD NEW` | Supersede historical state without silent rewriting. |
| `processkit entity archive ID` | Apply the entity's declared archival operation. |
| `processkit event list` | Query canonical domain events by subject, actor, type, outcome, and time. |
| `processkit context assemble` | Assemble bounded attributed context from one repository for a supplied task. |
| `processkit skill find|route` | Find an applicable skill or route a task through installed policy. |
| `processkit harness detect|verify` | Detect applicable harnesses and verify generated projections; the general catalog lists adapters. |
| `processkit handoff export|import` | Export or import a bounded cross-repository handoff without remote mutation. |
| `processkit mcp serve --stdio` | Serve the configured MCP capability set over standard input/output. |
| `processkit mcp serve --http` | Run the same repository-bound MCP application as a long-lived authenticated loopback daemon. |
| `processkit mcp proxy` | Bridge a harness's stdio connection to the configured local daemon. |
| `processkit package validate` | Validate a package or extension in isolation. |

- **PK-CLI-009:** the generic entity, event, context, skill, and handoff
  command groups are mandatory v1 surfaces. EntityType- and skill-specific
  convenience aliases MAY be added after their contracts are stable, but use
  the same application services and machine envelopes.
- **PK-CLI-013:** `list` MUST be read-only and return canonical identity,
  version, source package, installation status, enabled state where
  applicable, and compatibility metadata in text and versioned machine form.
- **PK-CLI-014:** listable kinds MUST derive from the installed ontology and
  capability catalogs. The CLI MUST NOT maintain a second hard-coded catalog
  that can drift from MCP discovery or package manifests.
- **PK-CLI-015:** products exposing a local MCP server MUST use the common
  command shape `<product> mcp serve --stdio`. Product-specific root and
  capability options MAY extend this shape without renaming the command.
- **PK-CLI-016:** CLI and MCP need not use identical names, but every
  repository read or mutation available through both adapters MUST resolve to
  the same application operation and produce equivalent outcomes, events,
  authorization checks, and recovery behavior.
- **PK-CLI-017:** structured input MUST be accepted from a versioned JSON or
  YAML document through an explicit file or standard input. Repeated `--set`
  flags MAY support simple interactive use but MUST NOT define a second data
  model or silently coerce ambiguous values.
- **PK-CLI-018:** every data-bearing command MUST support a versioned machine
  result. Text output is a human projection and MUST NOT be the only way to
  recover IDs, revisions, diagnostics, events, or recovery state.
- **PK-CLI-019:** entity mutation commands modify only the selected working
  copy. They MUST NOT stage, commit, branch, merge, push, open a pull request,
  or contact a Git forge unless a separately named future adapter command is
  explicitly invoked.
- **PK-CLI-027:** stdio is the universal v1 MCP baseline. V1 also supports an
  optional local daemon over authenticated loopback HTTP and a lightweight
  stdio proxy. Remote, unauthenticated, and hosted endpoints are outside v1.
- **PK-CLI-028:** harness projection changes use the ordinary lifecycle:
  `processkit plan adapter --harness TARGET...` followed by
  `processkit apply --plan PLAN`. `TARGET` is data resolved through the adapter
  catalog; v1 MUST NOT add a different top-level command per harness.
- **PK-CLI-029:** `processkit init --harness detected` MAY include every
  confidently detected supported harness in the initial plan. With no harness
  selection it MUST leave projections unconfigured and report the exact plan
  command to add them later.
- **PK-CLI-030:** `processkit plan reconcile` MUST compare the complete
  declared repository configuration with observed installed packages,
  profiles, harness adapters, generated projections, ownership state, and
  derived-state generations. Applying its reviewed plan converges only those
  processkit-owned or mergeable surfaces whose preconditions still match.
- **PK-CLI-031:** `processkit plan adapter --harness TARGET...` MAY propose
  both the declarative configuration change and its resulting projections.
  Once accepted configuration names those targets, ordinary `plan reconcile`,
  `apply`, and `verify` MUST be sufficient for later automation; callers do
  not need harness-specific imperative commands.

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
- **PK-CLI-026:** an invocation MUST report an error when `--root` names the
  context directory instead of the repository root unless the implementation
  can unambiguously normalize it to the owning repository and reports the
  normalized root before mutation.

## Post-v1 CLI directions

These directions are intentionally outside the v1.0.0 release gate and need
separate accepted contracts before implementation:

- harness conversation-memory review or synchronization; repository entity
  archival is already part of the v1 entity surface;
- company-specific processkit distributions carrying organization-wide
  processes, policy, skills, prompts, profiles, and MCP capabilities.

Memory lifecycle design MUST first distinguish durable repository memory from
harness conversation/session context and analyze overlap with harnesses such
as tau. Company-distribution design MUST compare upstream package composition,
private distributions, overlays, and downstream forks, and define provenance,
trust, naming, compatibility, update cadence, and continuous upstream
reconciliation. No particular adaptation mechanism is selected by v1.
