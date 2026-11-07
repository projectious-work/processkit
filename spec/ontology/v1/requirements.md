# Ontology and content model — requirements

This specification defines the processkit v1 ontology: the published,
versioned registry of all 90 concepts with their T/P/D/C class and their
definition-or-instance side, the rules by which the registry is generated
and checked, the common envelope every stored item uses (name, namespace,
labels, annotations, `spec`, and derived `status`), Containers as namespaces,
typed references and relations, the label-selector grammar, the reuse of
external vocabularies, and ontology extensions. It does not define the
individual content kinds, file locations, commands, tools, inheritance, or
access rules; those belong to other specifications and use this one.

Conventions: requirements use EARS; "shall" is mandatory, "should"
recommended, "may" optional; IDs are stable and never reused.

## Purpose

- **PK-PROD-003:** processkit shall publish the complete ontology as a
  versioned definition vocabulary. Instance concepts such as WorkItem, Event,
  and LogEntry shall remain usable as vocabulary inside definitions, and
  processkit shall not store their instances.

## Registry and classification

- **PK-MODEL-001:** processkit shall publish one versioned ontology registry
  containing every concept with its class, side, description, parent
  primitive where applicable, relations, and schema or fragment location.
- **PK-MODEL-002:** processkit shall classify every concept as definition or
  instance. If a concept is used both ways, then the ontology shall either
  split it or document the rule that decides which use is stored.
- **PK-MODEL-003:** processkit shall not persist, serve, or validate content
  whose kind is an instance concept. A definition may reference instance
  concepts by name as vocabulary.
- **PK-MODEL-004:** processkit shall produce the registry, the schemas, and
  the generated reference documentation from one source and shall check them
  for drift.
- **PK-MODEL-005:** processkit shall include every concept of the inventory
  (20 T foundational concepts, 22 P primitives, 24 D discriminators, and 24 C
  compositions, 90 in total) in the published registry with a
  definition-or-instance classification and a schema or fragment. Coverage
  of the full inventory shall be a release gate.
- **PK-MODEL-006:** processkit shall keep concepts from scaling frameworks,
  such as ART, ValueStream, ProgramIncrement, and WSJFEstimate, usable, and
  no processkit content kind or default shall require them.

## Registry generation

- **PK-MODEL-051:** If the ontology source contains a concept with an
  unknown class, a duplicate canonical name, a concept whose declared parent
  is missing, a dependency cycle, a T foundational concept that no generated
  schema consumes, an uncovered discriminator, or a composition with
  unresolved parts, then registry generation shall fail.
  <!-- from governance draft: 13-standard-entity-types.md PK-ENTITY-007 -->
- **PK-MODEL-052:** processkit shall give every T foundational concept one
  canonical schema fragment or registry contract, and every T foundational
  concept shall be exercised by at least one generated P or C schema.
  <!-- from governance draft: 13-standard-entity-types.md PK-ENTITY-006 -->
- **PK-MODEL-053:** processkit shall define every D discriminator as a
  variant of its declared parent P primitive that inherits the parent's
  lifecycle and storage rules, and shall publish fixtures that prove both
  valid specialization and the rejection of invalid mixing.
  <!-- from governance draft: 13-standard-entity-types.md PK-ENTITY-005 -->
- **PK-MODEL-054:** Where a concept is a definition concept, processkit shall
  publish a closed persistent schema for it, and a discriminator of a
  definition primitive shall be a closed variant of the parent's schema.
  Where a concept is an instance concept, processkit shall publish it only
  as a vocabulary fragment and not as a persistent schema, consistent with
  PK-MODEL-003.
  <!-- from governance draft: 13-standard-entity-types.md PK-ENTITY-005
  (closed-schema clause, restricted to definition concepts) -->

## Common envelope

- **PK-MODEL-010:** Every item shall declare `apiVersion`, `kind`,
  `metadata.name`, and `spec`. `metadata.name` shall be unique per kind
  within its namespace and stable across file moves.
- **PK-MODEL-011:** `metadata.namespace` shall name a Container; when it is
  omitted, the item shall belong to the repository's root Container.
  Containers shall form a tree through the Hierarchy relation. If Containers
  form a cycle or a Container names an unknown parent, then processkit shall
  report a validation error.
- **PK-MODEL-012:** `metadata.labels` shall be selectable key/value pairs
  with bounded key and value syntax and a bounded count.
  `metadata.annotations` shall not be selectable and shall not influence
  access decisions.
- **PK-MODEL-013:** The key prefix `processkit.projectious.work/` shall be
  reserved. Authored content shall not set reserved keys.
- **PK-MODEL-014:** Authored content shall live in `spec`. processkit shall
  report validation result, content digest, source path, provenance, and
  other derived facts as `status`, and authored content shall not set them.
- **PK-MODEL-015:** If an item contains an unknown field and the owning
  schema declares no extension map for that position, then validation shall
  fail. Extension fields shall be namespaced and shall not redefine ontology
  fields.
- **PK-MODEL-016:** Whenever absent, null, empty, and default values have
  different semantics, the schema shall distinguish them.

## Containers

- **PK-MODEL-046:** A Container shall be an organizational scope with a
  name, a title, an owner, an optional parent through the Hierarchy relation,
  and a lifecycle. A Container may carry one of the Container discriminators
  of the inventory; a Container without a discriminator represents a company
  or another organizational unit.
  <!-- from governance draft: 13-standard-entity-types.md PK-ENTITY-150
  (PK-ENTITY-151 rename-on-mutation dropped: v1 has no MCP writes) -->
- **PK-MODEL-047:** If two Containers in one repository declare the same
  name, then processkit shall report a validation error.
  <!-- from governance draft: 17-resources-identity-and-access.md PK-RES-020 -->
- **PK-MODEL-048:** If an item's `metadata.namespace` names an unknown
  Container, then validation of that item shall fail and processkit shall
  not serve the item.
  <!-- from governance draft: 17-resources-identity-and-access.md PK-RES-021 -->
- **PK-MODEL-049:** Namespace membership shall not change an item's authored
  content or semantics; it shall scope naming, selection, and access only.
  <!-- from governance draft: 17-resources-identity-and-access.md PK-RES-022 -->
- **PK-MODEL-050:** processkit shall express visibility restrictions only
  through labels and access control as defined by access-control@v1, as the
  contract of the Visibility foundational concept. processkit shall not add
  a separate taint-like mechanism that hides items outside access control.
  <!-- from governance draft: 17-resources-identity-and-access.md PK-RES-007 -->

## Label selectors

- **PK-MODEL-044:** processkit shall support label selectors with equality
  (`key=value`), inequality (`key!=value`), set membership
  (`key in (a,b)`), set exclusion (`key notin (a,b)`), existence (`key`),
  and non-existence (`!key`) requirements, combined by comma as logical AND.
  <!-- from governance draft: 17-resources-identity-and-access.md PK-RES-005 -->
- **PK-MODEL-045:** The processkit CLI and the MCP server shall parse
  selectors with one grammar. If a selector is invalid, then processkit
  shall reject it and report the exact position of the error.
  <!-- from governance draft: 17-resources-identity-and-access.md PK-RES-005 -->

## Relations and references

- **PK-MODEL-020:** A relation shall declare its type, subject, target, and
  optional scope or validity bounds. A relation type shall define direction,
  cardinality, endpoint constraints, and inverse.
- **PK-MODEL-021:** References shall use typed names, `<kind>/<name>` or
  `<kind>/<namespace>/<name>`. Filenames and Markdown links shall not be
  identity.
- **PK-MODEL-022:** When a reference targets an inherited item, processkit
  shall resolve it through the inheritance lock and shall carry the upstream
  identity in results.
- **PK-MODEL-023:** If a reference cannot be resolved, then processkit shall
  keep it visible as unresolved, and validation shall fail where the owning
  schema requires the reference.

## Standards reuse

- **PK-MODEL-030:** Generic descriptive metadata should follow Dublin Core
  Terms where the meaning fits exactly, and provenance should follow the W3C
  PROV model where the meaning fits.
- **PK-MODEL-031:** processkit may offer an exported JSON-LD or other
  semantic-web projection later. Where such a projection is offered, it shall
  be generated from the registry and shall not become a second source.

## Extensions

- **PK-MODEL-040:** A repository may add namespaced concepts,
  discriminators, relation types, and content kinds. Such additions shall
  validate against the published extension metaschemas and shall declare
  their namespace owner.
- **PK-MODEL-041:** Extensions shall not redefine published concepts. An
  inheriting repository may use an upstream extension; its namespace owner
  shall remain the upstream repository.
- **PK-MODEL-042:** An addition to the published ontology shall demonstrate
  need across at least two unrelated domains, shall declare its class and
  side, and shall provide compatibility and migration treatment.
- **PK-MODEL-043:** processkit's own repositories shall use the published
  ontology and schemas only and shall not define private concepts.
