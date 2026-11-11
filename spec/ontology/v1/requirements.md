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

- **PK-MODEL-055:** processkit shall publish the registry as one JSON
  document named `ontology-registry.json`. The document shall validate
  against `schemas/ontology-registry.schema.json`. It shall carry the
  ontology version as a semantic version `MAJOR.MINOR.PATCH`, and it shall
  list concepts and relation types sorted by name. The first v1 release
  shall publish ontology version `1.0.0`.
  <!-- agent proposal: OPEN-ontology-01 -->
- **PK-MODEL-056:** processkit shall give each concept the side listed for
  it in `interfaces.yaml` `inventory`. Every T foundational concept shall
  be on the definition side and shall be published as a schema fragment,
  not as a closed persistent schema. Every D discriminator shall have the
  side of its parent primitive.
  <!-- agent proposal: OPEN-ontology-08 -->
- **PK-MODEL-057:** When a user runs `processkit api-resources`, the
  processkit CLI shall return the registry document with the concepts and
  relation types of every valid OntologyExtension in the effective item set
  added. When a user runs `processkit explain TYPE`, the processkit CLI
  shall return the one concept entry whose name equals TYPE, compared
  without regard to case, or, if TYPE is a kind's plural or short name
  (cli@v1 PK-CLI-049), the entry named by that kind. If no concept has
  that name, then the processkit CLI shall fail with the diagnostic code
  `ontology.unknown-concept`. The MCP `ontology` tool shall return the same
  data for the same input.
  <!-- agent proposal: OPEN-ontology-01; changed by owner decision:
       2026-11-11 (#212), CLI style B -->

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

- **PK-MODEL-058:** If registry generation fails, then the generator shall
  exit with a non-zero status and shall report, for each failure, the
  diagnostic code listed in `interfaces.yaml` `generation` and the
  canonical name of the concept concerned.
  <!-- agent proposal: OPEN-ontology-02 -->
- **PK-MODEL-059:** A D discriminator shall be uncovered when its parent's
  schema does not admit it as a variant, or when the release lacks at least
  one positive and one negative fixture for it. A parent's schema shall
  admit a discriminator by listing its name in the parent's `discriminator`
  field. The Binding primitive shall instead admit its discriminators
  through the relation types of the registry, in `spec.relation`.
  <!-- agent proposal: OPEN-ontology-09 -->
- **PK-MODEL-060:** A negative discriminator fixture shall show invalid
  mixing. Invalid mixing is an item that names a discriminator of another
  parent, names more than one discriminator, or carries a field that only
  another discriminator of the same parent defines. Validation of each
  negative fixture shall fail.
  <!-- agent proposal: OPEN-ontology-09 -->

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
- **PK-MODEL-075:** The reservation of PK-MODEL-013 shall apply to the exact
  prefix `processkit.projectious.work/` only. Keys under a subdomain, such
  as the v0 annotation keys `v0.processkit.projectious.work/<pointer>` that
  v0-migration@v1 writes, shall not be reserved.
  <!-- agent proposal: reconciliation with v0-migration@v1 -->
- **PK-MODEL-014:** Authored content shall live in `spec`. processkit shall
  report validation result, content digest, source path, provenance, and
  other derived facts as `status`, and authored content shall not set them.
- **PK-MODEL-015:** If an item contains an unknown field and the owning
  schema declares no extension map for that position, then validation shall
  fail. Extension fields shall be namespaced and shall not redefine ontology
  fields.
- **PK-MODEL-016:** Whenever absent, null, empty, and default values have
  different semantics, the schema shall distinguish them.

- **PK-MODEL-061:** If validation finds a condition listed in
  `interfaces.yaml` `errors`, then processkit shall report a diagnostic
  with the code listed for that condition, the file, and the JSON pointer
  of the offending value, in the diagnostic shape of cli@v1. The CLI and
  the MCP server shall report the same codes for the same content.
  <!-- agent proposal: OPEN-ontology-02 -->
- **PK-MODEL-062:** processkit shall report `status` as an object that
  validates against `schemas/status.schema.json`. Single-item results
  (`processkit get TYPE NAME`, `processkit describe`, and the MCP `get` and
  `explain` tools) shall include the full `status`. Entries of list and
  context results (`processkit get TYPE`, `processkit get context`, and the
  MCP `list` and `get_context` tools) shall include `status` in the
  reduced shape `$defs/listStatus` of that schema, which carries the
  attribution facts of content-kinds@v1 PK-CONT-003 without diagnostics or
  references.
  <!-- agent proposal: OPEN-ontology-05; changed by owner decision:
       2026-11-11 (#212), CLI style B -->
- **PK-MODEL-063:** An extension map shall be an object member named
  `extensions`. Every key of an extension map shall have the form
  `<dns-prefix>/<name>`. The Container schema shall declare an extension
  map at `spec.extensions`.
  <!-- agent proposal: OPEN-ontology-11 -->

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

- **PK-MODEL-064:** A Container shall validate against
  `schemas/container.schema.json`. The parent shall be the typed reference
  `spec.parent`. The discriminator shall be `spec.discriminator`. The
  lifecycle shall be `spec.lifecycle`, and it shall not change naming,
  selection, validation, or access.
  <!-- agent proposal: OPEN-ontology-03 -->
- **PK-MODEL-065:** The root Container shall be named `root`. It shall exist
  even when the repository declares no Container named `root`. A
  repository may declare it explicitly, and then it shall have no parent.
  A Container without `spec.parent` shall be a child of the root Container.
  A Container shall not declare `metadata.namespace`.
  <!-- agent proposal: OPEN-ontology-04 -->
- **PK-MODEL-066:** The known Containers shall be the root Container and
  the Containers of the effective item set, which includes Containers from
  locked upstream repositories (inheritance@v1). PK-MODEL-047 shall apply
  to the Containers that one repository declares itself. A local Container
  with the same name as an inherited Container shall be handled as
  inheritance@v1 PK-INH-011 and PK-INH-014 define.
  <!-- agent proposal: OPEN-ontology-10 -->

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

- **PK-MODEL-067:** processkit shall accept exactly the selectors that the
  grammar in `interfaces.yaml` `selectors.grammar` derives. An empty
  selector, or one of spaces only, shall match every item. Quoted values
  and empty value sets shall be invalid.
  <!-- agent proposal: OPEN-ontology-06 -->
- **PK-MODEL-068:** An inequality requirement (`key!=value`) and a set
  exclusion requirement (`key notin (a,b)`) shall match an item that does
  not have the key.
  <!-- agent proposal: OPEN-ontology-06 -->
- **PK-MODEL-069:** When processkit rejects a selector, it shall report the
  diagnostic code `ontology.invalid-selector` with the member `offset`. The
  offset shall be the 0-based index, in Unicode code points, of the first
  character that cannot continue a valid selector. If the selector ends
  too early, then the offset shall be the selector's length in code points.
  If a token is well formed but exceeds a length bound, then the offset
  shall be the index of the token's first character.
  <!-- agent proposal: OPEN-ontology-07 -->

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

- **PK-MODEL-070:** processkit shall ship the relation types listed in
  `interfaces.yaml` `relations.types` in the registry member
  `relationTypes`. A Binding shall name its relation type in
  `spec.relation`. If a Binding names an unknown relation type, an endpoint
  that the relation type does not allow, or more targets than its
  cardinality allows, then validation shall fail.
  <!-- agent proposal: OPEN-ontology-12 -->
- **PK-MODEL-071:** A reference of the form `<kind>/<name>` shall resolve to
  the item of that kind and name in the root Container, or to the Container
  or OntologyExtension of that name.
  <!-- agent proposal: OPEN-ontology-10 -->

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
- **PK-MODEL-072:** A repository shall declare extensions in items of kind
  `OntologyExtension` that validate against
  `schemas/ontology-extension.schema.json`. The namespace shall be
  `spec.namespace`, and the namespace owner shall be `spec.namespaceOwner`.
  An OntologyExtension shall not declare `metadata.namespace`.
  <!-- agent proposal: OPEN-ontology-11 -->
- **PK-MODEL-073:** If an added concept, discriminator, relation type, or
  content kind has a name equal to a published name, compared without
  regard to ASCII case, then validation shall fail. If two extensions in
  the effective item set add the same name, then validation shall fail.
  <!-- agent proposal: OPEN-ontology-11 -->
- **PK-MODEL-074:** If a local OntologyExtension declares a namespace that
  an inherited OntologyExtension declares, then validation shall fail.
  <!-- agent proposal: OPEN-ontology-11 -->
- **PK-MODEL-076:** Every content kind that an OntologyExtension adds shall
  declare `plural` and `shortName`, each a lowercase string that matches
  `^[a-z][a-z0-9]*$`, as the type names of cli@v1 PK-CLI-049. If the kind's
  name, plural, or short name equals, compared without regard to ASCII
  case, the name, plural, or short name of another kind of the release
  (cli@v1 `type_names`) or of another extension kind in the effective item
  set, or the reserved word `context`, then validation shall fail with
  `ontology.extension-type-name-taken`. A kind name equal to a published
  name shall be reported as PK-MODEL-073 states.
  <!-- agent proposal: owner decision 2026-11-11 (#212), CLI style B -->
