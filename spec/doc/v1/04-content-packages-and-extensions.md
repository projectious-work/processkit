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
- **PK-PKG-004:** the initial profiles are `minimal`, `managed`, `product`,
  `research`, and `software`; each MUST publish an exact resolved manifest.
- **PK-PKG-005:** package and profile selection MUST be previewable without
  filesystem mutation.

## Skills

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

Provider-neutral prompt assets and slash-command projections are a post-v1
package capability. A future contract must separate canonical prompt purpose,
inputs, outputs, safety, and versioning from provider- or harness-specific
command syntax.

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

- **PK-PKG-040:** one canonical capability catalog MUST generate supported
  harness configuration and command/skill projections.
- **PK-PKG-041:** projection generation MUST preserve user-owned configuration
  or stop with a conflict; generated files MUST carry provenance.
- **PK-PKG-042:** harness absence MUST NOT prevent package installation,
  verification, CLI use, or manual MCP configuration.
- **PK-PKG-043:** adding a harness adapter MUST NOT change core entity or
  process semantics.

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
