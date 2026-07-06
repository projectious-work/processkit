---
title: processkit v1.0 Base Context
description: Baseline context for the processkit v1.0 redesign.
---

# processkit v1.0 Base Context

Created: 2026-07-04

This historical base context was created for the processkit v1.0 redesign.
It was built from the earlier `projectious-work/processkit` repository,
cloned locally at:

- Source URL: https://github.com/projectious-work/processkit
- Analyzed commit: `6a9a175f95c42dd76e23488feca42e3d05526b98`
- Local clone: `/tmp/processkit-original`

The goal is to preserve the proven v0.x product target while creating a
clean basis for processkit v1.0 improvement briefings.

## Current Guiding Briefing

The current guiding briefing is `processkit-v1.0-rfc-draft.md`, analyzed
in the [processkit v1.0 RFC analysis](./processkit-v1-rfc-analysis.md).

Conflict rule:

- preserve the stable product target captured in this base context
- use the v1.0 RFC for ontology, branch, release, schema-composition,
  validation, indexing, and cutover-gate direction
- treat `concept-mapping-2026-05-16.md` as historical input where it
  agrees with the RFC, not as current guidance where it conflicts

## Current Repository Status

At the time of this analysis, the workspace was a fresh
aibox/processkit-derived project scaffold, not yet a rebuilt processkit
source tree.

- `aibox.lock` pins upstream processkit to `v0.27.1`.
- `aibox.toml` enables the processkit core/managed skill surface.
- The workspace currently has no `src/`, `docs-site/`, or implementation
  source tree.
- Indexed processkit entities for WorkItems, DecisionRecords,
  Discussions, and Artifacts are currently empty in this project.
- GitHub auth was available for repository status checks.

Session-start process checks were run before this document was created.
The pending `aibox.lock` backfill migration
`MIG-LOCK-20260703T161218` was applied through migration-management.
After that, active migrations were zero.

`pk-doctor` still reports setup drift that should be tracked separately:

- missing `scripts/check-src-context-drift.sh`
- missing TeamMember tier directories for `cora` and `thrifty-otter`
- missing Claude sub-agent export for `cora`
- stale MCP manifest / server-header / preauth metadata
- one applied migration that is now an archive candidate

These findings are not part of the base-context target itself, but they
are important when this repository starts growing source and release
machinery.

## Stable Product Target

The first processkit version defines processkit as:

> provider-neutral process memory, skills, and MCP tools for agentic
> software projects.

The stable target should not change:

1. processkit is a versioned content and runtime layer for AI-assisted
   projects.
2. It gives agents and humans structured project memory through
   repository files, schemas, skills, state machines, and MCP tools.
3. It is provider-neutral and harness-neutral. Claude, Codex, OpenCode,
   Hermes, Aider, and other harnesses are integration targets, not core
   dependencies.
4. It is a process layer, not a replacement for a harness, runtime
   manager, issue tracker, or model provider.
5. It must remain usable manually, through MCP-capable harnesses, or via
   an external installer such as aibox.
6. It must remain forkable. Organizations can maintain private forks and
   downstream projects can consume those forks without changing their
   own structure.

The original PRD states the primary goal clearly: make it easy for any
team to add a structured, agent-readable process layer to any repository.

## Shipped Deliverable Boundary

The old project made a hard distinction between the processkit
repository's dogfooding context and the content shipped to consumers.
This distinction is foundational and should be preserved.

`src/` in the original repository is a literal mirror of a fresh
consumer project root:

- `src/AGENTS.md` becomes `<project>/AGENTS.md`.
- `src/context/` becomes `<project>/context/`.
- `src/.gitignore.example` is the recommended ignore template.
- `src/.processkit/` is catalog tooling and package metadata; it is not
  installed into consumers as live project context.

The repository-root `context/` in the old project is dogfood project
state. It contains processkit's own WorkItems, Decisions, Artifacts,
logs, migrations, team state, and release history. That content must not
be blindly mirrored into `src/context/`.

The release boundary guard from the original project explicitly allows
dogfood-only directories under root `context/` while forbidding them from
shipping under `src/context/`. In `src/context/`, shipped Artifacts are
model specs and model profiles only; dogfood Decisions, WorkItems,
Discussions, Notes, Logs, Migrations, and Templates do not ship.

## Consumer Usage Model

Consumers can use processkit manually or through a manager.

Manual use:

1. Download a versioned processkit release tarball.
2. Copy the shipped `context/`, `.processkit`, and `AGENTS.md` into the
   consuming project.
3. Configure the harness to launch `processkit-gateway`, or launch
   individual per-skill MCP servers.

aibox-assisted use:

1. `aibox.toml` pins `[processkit] source`, `version`, and `src_path`.
2. aibox fetches the source release, installs selected package tiers, and
   records `aibox.lock`.
3. aibox may configure or supervise runtime files, but processkit remains
   the standalone source for schemas, skills, packages, and MCP runtime.

The old README names three MCP layouts:

- `processkit-gateway`: preferred provider-neutral entry point.
- Per-skill MCP servers: canonical granular compatibility surface.
- `aggregate-mcp`: legacy compatibility bridge.

The gateway is additive. It must not replace per-skill servers as the
canonical validation and compatibility surface.

## Package Tiers

The original package model has five tiers:

- `minimal`: foundation for solo developers and small side projects.
- `managed`: recommended default for small teams with backlog and
  process cadence.
- `software`: managed plus architecture, infrastructure, security,
  performance, database, and observability skills.
- `research`: managed plus data, ML, AI, and research-authoring skills.
- `product`: software plus design, framework, product, and broader
  end-to-end product-development skills.

Packages compose through `spec.extends`; consumers can add or remove
specific skills through config overrides.

## Entity and Contract Model

The stable entity model is Markdown files with YAML frontmatter:

- `apiVersion`
- `kind`
- `metadata`
- `spec`
- body content where appropriate

The v2 direction is intentionally breaking and explicit. The historical
decisions rejected long-term v1/v2 compatibility shims. v1 contexts are
migration sources; after migration, v2 schemas and index semantics are
authoritative.

Important v2 contract points:

- Unknown kinds, stale primitive assumptions, and ad hoc event/type
  vocabulary should fail validation.
- `Metric`, `Model`, `Process`, `Schedule`, and `StateMachine` are
  legacy v1 migration-source kinds, not shipped v2 entity primitives.
- Process definitions are Artifacts plus process-instance WorkItems.
- Schedule semantics use `Binding(type=time-window)`.
- Runtime state-machine YAML files are implementation contracts, not
  user-authored StateMachine entities.
- Hook inbox items are Notes with `spec.inbox`.
- Agent cards and security policies are Artifact-backed projections.
- Eval gates produce eval-spec Artifacts, paired Gates, policy/application
  Bindings, and calibration LogEntries.

## MCP and Indexing Principles

The old project converged on these operational rules:

- Agents read entities through `index-management`, not raw filesystem
  scraping.
- Agents write entities through management MCP tools so schema
  validation, state-machine enforcement, index updates, and event logs
  happen consistently.
- `index-management` is the read-side foundation.
- `id-management` is the write-side ID foundation.
- Entity search uses SQLite FTS5, with optional sqlite-vec semantic
  search and hybrid search.
- Broad health checks and release checks should return structured JSON
  so agents can route findings instead of re-parsing prose.

The original release had 30 MCP server files under `src/context/skills`.
Most are processkit management servers; one additional shipped server was
`devops/repo-management`.

## Provider and Model Neutrality

Provider neutrality is a core invariant, not a convenience.

The old decisions establish:

- processkit skills, commands, MCP tools, and doctor findings must not
  require or invoke aibox host commands from inside derived project
  containers.
- aibox and other managers may install, supervise, or provide runtime
  signals, but processkit remediation surfaces stay generic.
- Role and TeamMember model assignments bind to provider-neutral
  `Artifact(kind=model-profile)` artifacts by default.
- Concrete `Artifact(kind=model-spec)` artifacts may encode provider and
  model names because they describe real provider models.
- Runtime access gates expand profiles into concrete candidates.
- Direct Role/TeamMember bindings to concrete ModelSpec artifacts are
  explicit pins or compatibility cases.

This is the design line that lets a processkit project move between
Codex, Claude Code, Gemini CLI, Aider, Cursor, Copilot, OpenCode,
Hermes, and future harnesses without rewriting its process memory.

## Team and Role Model

The old project introduced persistent TeamMembers, Roles, RoleSlots, and
Bindings to support repeatable multi-agent collaboration:

- Roles define responsibilities.
- TeamMembers represent named humans or AI personas.
- Bindings connect actors, roles, model profiles, scopes, and other
  addressable surfaces.
- RoleSlots decouple identity and capacity planning from concrete people
  or model invocations.
- Sub-agent dispatch should route through `route_task` first and use the
  recommended TeamMember/model class when available.

The workspace had processkit TeamMember remnants from installation, but
`pk-doctor` reported missing tier directories and one missing Claude
sub-agent export. Treat that as setup hygiene, not as the future team
model.

## Release and Migration Model

The first processkit version treated releases as deliberate versioned
content, not silent syncs.

Stable release expectations:

- `src/PROVENANCE.toml` maps shipped files to the tag where each last
  changed.
- `scripts/processkit-diff.sh` compares tagged versions and classifies
  added, removed, changed, and unchanged files.
- Installers write explicit Migration documents for upgrades.
- Users and agents review migrations before applying them.
- Migration flow is `pending` -> `in-progress` -> `applied`.
- Release tarballs are built reproducibly from `src/`.
- Release packaging runs a release-boundary guard, release audit,
  provenance freshness check, MCP preauth validation, and checksum
  generation.

The old release process guarded against a known failure mode: dogfood
context had changed while `src/context/` did not receive corresponding
shippable changes. The new version should preserve a guard that makes
that drift visible.

## Documentation Surface

The first version had two user-facing documentation surfaces:

- root docs such as `docs/harness-claude-code.md`
- Docusaurus docs under `docs-site/`

The most important stable docs topics are:

- installation and harness setup
- package tiers and skill catalog
- API version policy
- migration model
- v2 contracts
- ID formats
- privacy tiers
- gateway and MCP layouts

At the time of capture, the workspace did not yet have the current
Docusaurus development section. Treat that statement as historical.

## Current Gap Summary

Compared with the original processkit repository, this project currently
has:

- processkit runtime context installed under root `context/`
- aibox config and lock data
- devcontainer/runtime scaffolding
- this base-context document

It does not yet have:

- `src/` deliverable tree
- `src/context/` schemas, state machines, skills, model artifacts, roles,
  bindings, and TeamMember defaults
- package definitions under `src/.processkit/packages`
- release scripts and verification scripts
- docs-site user documentation
- changelog, contribution guide, or release packaging flow
- processkit v1.0-specific WorkItems, Decisions, or Artifacts describing the
  rebuild roadmap

## Base-Context Readiness Audit

This first phase is complete enough for the next briefing document.

| Requirement | Evidence | Status |
|---|---|---|
| Clone/analyze original repository | `/tmp/processkit-original` at commit `6a9a175f95c42dd76e23488feca42e3d05526b98` | Done |
| Capture target that should not change | Stable Product Target, Consumer Usage Model, Entity and Contract Model | Done |
| Analyze old `context/` decisions/artifacts | Evidence Index lists PRD and high-signal DecisionRecords | Done |
| Analyze old `src/` source deliverable | Shipped Deliverable Boundary, Package Tiers, MCP and Indexing Principles | Done |
| Analyze user-facing docs | Documentation Surface plus reference-doc evidence list | Done |
| Capture initial v1.0 workspace status | Current Repository Status and Current Gap Summary | Done |
| Verify process health before handoff | active migrations: zero; `pk-doctor` findings summarized above | Done |

Open items are intentionally deferred until the incoming briefing is
reviewed:

- creating processkit v1.0-specific WorkItems or DecisionRecords
- choosing which old skills or runtime code to import versus redesign
- rebuilding `src/`, `docs-site/`, release scripts, or MCP runtime code
- resolving unrelated installed-context hygiene findings from `pk-doctor`

## Improvement Surface for Later Briefing

The next briefing can change how the new implementation is built, but it
should do so against these preserved targets:

- keep processkit provider-neutral and host-orchestrator-neutral
- keep the shipped deliverable boundary explicit
- keep entity writes validated through MCP, not hand-edited context files
- keep migrations explicit and reviewable
- keep gateway additive rather than replacing per-skill canonical servers
- keep model routing provider-neutral through profiles
- keep docs and release checks first-class
- keep dogfood project context separate from consumer deliverables

Likely redesign areas for processkit v1.0:

- simplify the source layout without losing the consumer mirror invariant
- reduce prompt/runtime overhead of the skill and MCP surfaces
- make package selection and command projection easier to reason about
- strengthen release and migration tests from the start
- define processkit v1.0-specific WorkItems/Decisions after the incoming
  briefing document is reviewed
- decide whether to import, regenerate, or redesign each old skill family
  rather than copying the whole first-version catalog wholesale

## Evidence Index

Primary evidence from the original repository:

- `README.md`: product promise, install model, MCP layouts, current status
- `ART-20260409_1854-KindCrane-processkit-product-requirements-document`:
  original approved PRD
- `src/INDEX.md`: shipped deliverable boundary and mirror invariant
- `src/.processkit/packages/*.yaml`: package tiers and composition
- `docs/harness-claude-code.md`: harness behavior and compliance payloads
- `docs-site/docs/reference/apiversion-policy.md`: apiVersion rules
- `docs-site/docs/reference/migration.md`: version migration model
- `docs-site/docs/reference/v2-contracts.md`: v2 entity/projection rules
- `docs-site/docs/reference/id-formats.md`: ID prefix and format policy
- `docs-site/docs/reference/privacy.md`: privacy tiers and private dirs
- `src/context/skills/processkit/processkit-gateway/SKILL.md`: gateway
  architecture
- `src/context/skills/processkit/index-management/SKILL.md`: read-side
  index foundation
- `scripts/check-src-context-drift.sh`: release boundary guard
- `scripts/build-release-tarball.sh`: release packaging flow
- `scripts/smoke-test-servers.py`: MCP smoke workflow

High-signal historical decisions:

- `DEC-20260430_1416-SmoothTiger-adopt-breaking-v2-implementation-plan-for`
- `DEC-20260501_1739-ProudCrane-adopt-smoothtiger-informed-split-track-v2`
- `DEC-20260502_0743-CoolFjord-adopt-provider-neutral-processkit-gateway-daemon`
- `DEC-20260503_1829-LoyalComet-route-roles-and-team-members-through`
- `DEC-20260515_1232-GentleLantern-keep-processkit-host-orchestrator-neutral`
