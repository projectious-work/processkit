# Content, packages, and extensions

## Content types

processkit distributes process capability as independently inspectable files:

- EntityType schemas and state machines;
- skills containing instructions, tools, configuration, and references;
- ProcessSpecifications;
- templates and maintained examples;
- policies and validation rules;
- harness-neutral capability metadata;
- harness projections generated from that metadata; and
- documentation tied to the owning content.

## Package manifest

- **PK-PKG-001:** every package MUST have a versioned manifest declaring name,
  version, processkit compatibility, contents, dependencies, conflicts,
  ownership classes, capabilities, and digests.
- **PK-PKG-002:** package dependency resolution MUST be deterministic for a
  pinned release and MUST fail on cycles, absent dependencies, incompatible
  ranges, duplicate ownership, or ambiguous capability providers.
- **PK-PKG-003:** profiles MUST be named selections of packages; they MUST NOT
  duplicate package contents or alter package semantics implicitly.
- **PK-PKG-004:** v1 MUST publish a core-only `standard` profile. The current
  non-kernel concept inventory MAY initially ship in one first-party
  `extended` package while evidence accumulates for smaller durable package
  boundaries. Additional profiles MUST publish an exact resolved manifest.
- **PK-PKG-005:** package and profile selection MUST be previewable without
  filesystem mutation.
- **PK-PKG-006:** optional packages MUST be removable without invalidating
  unrelated kernel entities; references to removed package concepts MUST be
  reported explicitly and MUST NOT be silently coerced into generic records.

## Skills

A skill has one canonical processkit representation. It is not authored once
per harness. Its package contains a harness-neutral manifest and instruction
document plus any declared references, templates, assets, scripts, and MCP
capabilities. Harness-native files are disposable projections of that source.

- **PK-PKG-010:** a skill MUST declare stable identity, version, purpose,
  triggers, inputs, outputs, owned capabilities, dependencies, side effects,
  safety constraints, and progressive-disclosure resources.
- **PK-PKG-011:** skill instructions MUST be provider-neutral; provider or
  harness adapters MAY project them into native discovery formats without
  changing their semantics.
- **PK-PKG-012:** a skill that exposes MCP tools MUST declare those tools in a
  machine-readable capability manifest whose schemas match runtime discovery.
- **PK-PKG-013:** skills MUST declare whether operations are read-only,
  project-mutating, externally mutating, privileged, or destructive.
- **PK-PKG-014:** extension skills MUST NOT impersonate a reserved processkit
  identity or override a core capability without explicit policy.
- **PK-PKG-015:** a canonical skill MUST declare which parts are normative
  semantics and which are explanatory text. A harness adapter MUST preserve
  purpose, triggers, inputs, outputs, safety, side effects, required tools, and
  progressive-disclosure order; formatting and invocation syntax MAY differ.
- **PK-PKG-016:** scripts and MCP tools remain separately executable declared
  capabilities. Project text or generated prompt files MUST NOT silently gain
  executable authority.

## Processes

- **PK-PKG-020:** a ProcessSpecification MUST declare ordered or branching
  steps,
  entry conditions, completion conditions, required capabilities, evidence,
  failure behavior, and resumability.
- **PK-PKG-021:** ProcessSpecifications describe coordination semantics; they
  MUST NOT embed arbitrary executable code.
- **PK-PKG-022:** starting a durable process MUST create a declared execution
  record composed from the canonical ontology, or a declared set of linked
  WorkItems, so execution state is inspectable.
- **PK-PKG-023:** process overrides MUST identify the upstream definition and
  compatibility range they replace.

### Linear reviewed profile

The optional `linear-reviewed` authoring profile applies the useful bounded
patterns of Interpretable Context Methodology (ICM) to Processkit's existing
process model. It is for repeatable, sequential work in which a human may
inspect or edit an artifact between steps. It is not a second execution model.

- **PK-PKG-024:** a `linear-reviewed` ProcessSpecification MUST express each
  step through declared inputs, process intent, outputs, and optional
  checkpoints and audits.
- **PK-PKG-025:** inputs MUST classify content as accepted `instruction`,
  stable `reference`, or per-run `working` context and MUST identify exact
  entities, artifacts, files, sections, queries, or previous-step outputs.
- **PK-PKG-026:** the profile MUST support ordered steps only. Branching,
  concurrent scheduling, dynamic agent coordination, and unattended retry
  policy require the general ProcessSpecification contract or an external
  orchestrator.
- **PK-PKG-027:** Processkit EntityTypes, execution records, transitions,
  gates, evidence, provenance, and result contracts remain authoritative.
  Folder numbering, file presence, or human-readable projection layout MUST
  NOT independently prove step completion, approval, freshness, or success.
- **PK-PKG-028:** Processkit MAY render a provider-neutral, human-readable
  stage view with `Inputs`, `Process`, `Outputs`, `Checkpoints`, and `Audits`.
  The rendering MUST carry source provenance and MUST be disposable or
  reconciled through the normal ownership contract.
- **PK-PKG-029:** intermediate outputs MUST remain ordinary inspectable and
  editable project artifacts. A later step MUST consume their current
  revision through a declared input and preserve enough provenance to
  distinguish agent output, human revision, approval, and staleness.

## Governance standards

A governance standard is a structured, versioned rule set that a company,
team, or project defines for its own work: for example a branching, security,
or documentation standard. processkit provides the format, validation,
storage location, and MCP serving. It does not define or ship the content of
any organization's standards.

A repository that governs a company or team installs processkit and keeps its
standards as canonical files. An implementation repository may install
processkit and keep project-level standards the same way. Each standard is
one JSON document validated against the published
[`standard.schema.json`](../../schemas/v1/standard.schema.json); the published
[`standard.template.json`](../../templates/v1/standard.template.json) is the
starting point an author or agent fills in.

- **PK-STD-001:** processkit MUST publish a versioned JSON Schema for
  governance standards and a matching JSON template that validates against it.
  The schema and template are release-owned; the standards written from them
  are project-owned.
- **PK-STD-002:** a governance standard MUST declare a stable identifier,
  title, version, lifecycle status, owner, a short `summary`, `triggers` that
  describe when it applies, applicability by profile, and an ordered list of
  normative `rules`. Each rule MUST carry a stable identifier, an RFC 2119
  level, and its text.
- **PK-STD-003:** detailed guidance MUST live in named `sections` so readers
  can retrieve one section without loading the whole standard. Sections MAY
  use Markdown text; rules and applicability MUST remain structured fields.
- **PK-STD-004:** governance standards MUST be stored under the configured
  context directory at `standards/<standard-id>.json`. Other locations MUST be
  declared in project configuration; processkit MUST NOT discover standards by
  scanning arbitrary repository paths.
- **PK-STD-005:** `processkit standard validate` and `processkit verify` MUST
  validate every standard against the installed schema version and report the
  exact file, field, and rule. An invalid standard MUST NOT be served as
  valid; other valid standards remain available with the failure reported.
- **PK-STD-006:** a project MUST be able to declare which profiles apply to
  itself, such as `cli`, `library`, `service`, or `documentation`. Profile
  names are project-defined vocabulary validated against the profiles the
  project declares, not a fixed processkit list.
- **PK-STD-007:** standards MUST be able to reference other standards by
  identifier and MAY declare `supersedes`. References MUST be validated;
  a dangling reference is a verification error.
- **PK-STD-008:** the standards surface is read-only over MCP in v1. Creating
  or changing a standard is an ordinary reviewed file change validated by
  `processkit standard validate`.
- **PK-STD-009:** a standard is modelled as a composition over the kernel
  `Policy` primitive so it can take part in relations, lifecycle, and events
  without a separate ontology concept.

### Progressive disclosure

Serving a standard has three levels so agents load only what a task needs:

| Level | Content | Typical size |
|---|---|---|
| 0 | identifier, title, `summary`, `triggers`, applicability | one line per standard |
| 1 | level 0 plus all `rules` and the section index | tens of lines |
| 2 | one named section in full | as authored |

- **PK-STD-010:** MCP and CLI MUST serve each level separately. A level-0
  listing MUST NOT include rule text or section bodies; a level-1 read MUST
  NOT include section bodies.
- **PK-STD-011:** listing and applicability queries MUST filter by the
  project's declared profiles and MUST report which standards were excluded
  and why.
- **PK-STD-012:** every served result MUST carry the standard identifier,
  version, source path, and content digest so an agent can cite the exact
  rule it applied.

### Future hierarchies

Roadmap item PK1-P6 plans standards inherited from pinned upstream processkit
repositories, for example company to team to project. Its contract must keep
upstream content read-only, record provenance, make local overrides explicit
and reviewable, and never create shared mutable authority. Until that contract
exists, every served standard belongs to the selected repository.

## Extension model

- **PK-PKG-030:** projects MAY add namespaced EntityTypes, relation types,
  skills, processes, policies, and packages under project-owned paths.
- **PK-PKG-031:** extensions MUST validate against published extension
  metaschemas and MUST declare their namespace owner.
- **PK-PKG-032:** extension loading order MUST be deterministic and explicit;
  directory traversal order MUST NOT affect behavior.
- **PK-PKG-033:** processkit MUST offer conformance commands that validate an
  extension without installing it into a real project.
- **PK-PKG-034:** extension failures MUST be isolated and attributed; one
  invalid optional extension MUST NOT silently disable unrelated core checks.
- **PK-PKG-035:** executable plugins are outside the default v1 extension
  model. If introduced later, they require a separate trust, sandbox, signing,
  and compatibility contract.

## Harness projections

A harness adapter maps the canonical skill and capability catalogs to one
documented harness contract: discovery paths, instruction wrappers, command
aliases, MCP configuration, and supported metadata. Adapters do not own skill
semantics.

- **PK-PKG-040:** one canonical capability catalog MUST generate supported
  harness configuration and command/skill projections.
- **PK-PKG-041:** projection generation MUST preserve user-owned configuration
  or stop with a conflict; generated files MUST carry provenance.
- **PK-PKG-042:** harness absence MUST NOT prevent package installation,
  verification, CLI use, or manual MCP configuration.
- **PK-PKG-043:** adding a harness adapter MUST NOT change core entity or
  process semantics.
- **PK-PKG-044:** each adapter MUST publish a support matrix. If a harness
  cannot represent a required skill constraint, generation MUST report the
  loss and verification MUST fail when that projection is required by policy.
- **PK-PKG-045:** `init` MAY detect supported harnesses and include their
  projections in its installation plan, but MUST NOT install every known
  adapter implicitly. Explicitly configured or selected targets take
  precedence over detection.
- **PK-PKG-046:** one plan MAY contain several harness targets. Applying it
  MUST generate all selected projections from the same canonical catalog and
  record adapter versions and source digests, allowing one repository to
  support several harnesses without maintaining several skill sources.
- **PK-PKG-047:** selected harness targets and adapter options MUST be
  declarative desired state in project configuration. Projection files and
  merged harness MCP configuration are observed state; deleting or changing
  them creates detectable drift rather than changing the desired catalog.

## Future organizational distributions

Organizations may eventually publish a governed processkit adaptation that
preselects or adds mandatory profiles, processes, policies, skills, prompts,
and MCP capabilities for their developers. The organization-specific
distribution is not part of the v1 contract.

Its future design must preserve upstream processkit identity and provenance,
distinguish upstream and organization-owned content, support private
distribution and authenticated installation, declare compatibility with an
exact upstream range, and provide a continuous update and conflict-resolution
path. A downstream Git fork requiring indefinite manual merges is one option
to evaluate, not the assumed product model.

Roadmap item PK1-P6 covers the first concrete step in this direction: an MCP
gateway for trusted organization MCP servers and inherited governance
standards. It does not change the v1 contract until it is specified and
accepted.
