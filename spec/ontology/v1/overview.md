# Ontology and content model — overview

Non-normative. The requirements are in `requirements.md`; the interface
catalog is `interfaces.yaml`.

## Owner goal

The owner wants one common language in which a company, its teams, and its
projects define how they work. With it, a user or an agent can express any
process, such as ticket handling, in shared concepts that processkit
validates, stores, and serves (C2). The language must be complete and
versioned, yet processkit must store definitions only, never instances
(C1). Containers and labels must carry the scoping that access control
needs (C7).

## Purpose

The ontology is the common language in which an organization defines how it
works. processkit publishes all 90 concepts, complete and versioned, uses
them for its own content kinds, and lets authors use any concept inside
their standards and process definitions. A ticket-handling
ProcessSpecification, for example, names the WorkItem type it governs, its
StateMachine, its Roles, and its Gates, yet processkit never stores a ticket:
the ontology describes both definitions and instances, and processkit stores
and serves definitions only.

This specification also fixes the envelope every stored item shares
(`apiVersion`, `kind`, `metadata`, `spec`, derived `status`), Containers as
namespaces, typed references, relations, the label-selector grammar used by
the CLI, MCP, and access rules, and how repositories extend the ontology.
processkit keeps JSON files and published JSON Schemas as contracts; RDF,
OWL, SHACL, JSON-LD, and knowledge graphs are not runtime dependencies.

## Boundaries

| Not covered here | Covered by |
|---|---|
| repository layout, declared locations, file formats, serialization, release-owned files | repository-storage@v1 |
| individual content kinds (Standard, ProcessSpecification, Skill, MCPServer, DecisionRecord, Document), their schemas and templates | content-kinds@v1 |
| commands such as `processkit ontology`, `list`, `validate`, exit codes, result envelope | cli@v1 |
| MCP tools such as `ontology`, `list`, `validate`, and resources | mcp-context-serving@v1 |
| the lockfile and resolution of inherited items | inheritance@v1 |
| Roles, `grants-role` Bindings, authenticators, and access decisions that consume selectors and Containers | access-control@v1 |
| path containment and input hardening | security@v1 |
| conversion of v0 content | v0-migration@v1 |

## Governing decisions

- **C1 — Context, not memory:** instances such as tickets, events, and logs
  are never stored, which is why instance concepts are vocabulary only.
- **C2 — The full ontology is the definition language:** all 90 concepts are
  published and classified, and full-inventory coverage is a release gate.
- **C7 — Kubernetes-pattern access control:** Containers scope Bindings and
  labels feed selectors, so visibility is expressed only through access
  control.

## Provenance

Baseline (`spec/doc/v1`, #197):

- `02-ontology.md`, all sections (role of the ontology, T/P/D/C classes,
  inventory, common envelope, relations, standards reuse, extensions):
  PK-MODEL-001 to PK-MODEL-006, PK-MODEL-010 to PK-MODEL-016, PK-MODEL-020
  to PK-MODEL-023, PK-MODEL-030, PK-MODEL-031, PK-MODEL-040 to
  PK-MODEL-043.
- `01-product-definition.md`, Goals: PK-PROD-003.
- Inventory names, class contracts, the envelope example, and the side
  examples are carried into `interfaces.yaml`.
- `schemas/v1/resource-metadata.schema.json` is copied unchanged into
  `schemas/`.
- Context only: `03-repository-and-files.md` (`context/ontology/`),
  `04-governance-content.md` (organizational scope), `06-cli.md` and
  `07-mcp-and-context-assembly.md` (observation points),
  `08-identity-and-access.md` (selector use in Role rules).

Gap items carried from tag `archive/processkit-v1-governance-standards`:

| New ID | Source | Note |
|---|---|---|
| PK-MODEL-044, PK-MODEL-045 | 17-resources-identity-and-access.md PK-RES-005 | selector grammar; one parser; exact error position |
| PK-MODEL-046 | 13-standard-entity-types.md PK-ENTITY-150 | Container fields; PK-ENTITY-151 dropped (rename-on-mutation; v1 has no MCP writes) |
| PK-MODEL-047 | PK-RES-020 | duplicate Container names (cycles and unknown parents were already PK-MODEL-011) |
| PK-MODEL-048 | PK-RES-021 | unknown Container fails and is not served (root default already PK-MODEL-011) |
| PK-MODEL-049 | PK-RES-022 | namespace never changes semantics |
| PK-MODEL-050 | PK-RES-007 | visibility only through labels and access control |
| PK-MODEL-051 | PK-ENTITY-007 | generation failure conditions |
| PK-MODEL-052 | PK-ENTITY-006 | T-concept fragments and consumption |
| PK-MODEL-053 | PK-ENTITY-005 | discriminator variants and fixtures |
| PK-MODEL-054 | PK-ENTITY-005 | closed persistent schemas for definition concepts only; instance concepts stay fragments (PK-MODEL-003) |

Adjustments for compatibility with #197: the draft's "kernel" terminology,
`list_resources`/`get_resource` operations, and resource URIs are not
carried (owned by other slugs); PK-RES-020's "in the same repository" is
resolved for inherited Containers by PK-MODEL-066; PK-ENTITY-150's
"core discriminators Team and Project" is replaced by the six Container
discriminators of the v1 inventory, consistent with PK-MODEL-006.

## Resolved open items

All former `open` items of `interfaces.yaml` are answered. Each answer is
an agent proposal for owner review at freeze; requirements carry an
`<!-- agent proposal: ... -->` marker and catalog entries
`basis: agent-proposal`.

| Item | Resolution | Basis |
|---|---|---|
| OPEN-ontology-01 | Registry `ontology-registry.json`, JSON, release-owned, published at the schema base URL; fields in `schemas/ontology-registry.schema.json`; `ontologyVersion` semantic version, first value `1.0.0`; `ontology list` and `show` semantics (PK-MODEL-055, PK-MODEL-057). | agent proposal |
| OPEN-ontology-02 | Lowercase dot-separated codes with the `ontology.` prefix for every validation, selector, and generation condition (`interfaces.yaml` `errors`, `generation`); diagnostic shape from cli@v1 (PK-MODEL-058, PK-MODEL-061). | agent proposal |
| OPEN-ontology-03 | `schemas/container.schema.json`: `spec.title`, `spec.owner` (string), `spec.parent` (`Container/<name>`), `spec.discriminator`, `spec.lifecycle` (`proposed`, `active`, `retired`, informational), `spec.extensions` (PK-MODEL-064). | agent proposal |
| OPEN-ontology-04 | The root Container is `root`; implicit unless declared; declared without parent; parentless Containers are its children; Containers have no `metadata.namespace` (PK-MODEL-065). | agent proposal |
| OPEN-ontology-05 | `schemas/status.schema.json` (`validation`, `digest`, `source`, `provenance`, `references`, `uncommitted`). Single-item results carry the full status. List and context entries carry `$defs/listStatus`, the attribution facts of content-kinds@v1 PK-CONT-003 (PK-MODEL-062). | agent proposal |
| OPEN-ontology-06 | `!=` and `notin` match items without the key (Kubernetes convention, consistent with J7); exact EBNF; spaces allowed around operators; empty selector matches all; quotes and empty sets invalid (PK-MODEL-067, PK-MODEL-068). | agent proposal |
| OPEN-ontology-07 | Member `offset`, 0-based, in Unicode code points, rules for early end and over-long tokens (PK-MODEL-069). | agent proposal |
| OPEN-ontology-08 | Side of all 90 concepts in `interfaces.yaml` `inventory` (68 definition, 22 instance); T on the definition side as fragments; D takes its parent's side (PK-MODEL-056). | agent proposal |
| OPEN-ontology-09 | Uncovered: parent schema does not admit it, or a positive or negative fixture is missing; invalid mixing defined; fixtures under `fixtures/discriminators/<name>/` (PK-MODEL-059, PK-MODEL-060). | agent proposal |
| OPEN-ontology-10 | Upstream Containers in the effective item set are known; PK-MODEL-047 covers one repository's own Containers; local-versus-inherited names follow inheritance@v1 PK-INH-011 and PK-INH-014 (PK-MODEL-066). Unqualified references resolve in the root Container (PK-MODEL-071). | agent proposal |
| OPEN-ontology-11 | One metaschema, `schemas/ontology-extension.schema.json`, for items of kind `OntologyExtension`; owner in `spec.namespaceOwner`; redefinition and namespace-taken rules; extension maps `extensions` with `<dns-prefix>/<name>` keys (PK-MODEL-063, PK-MODEL-072 to PK-MODEL-074). | agent proposal |
| OPEN-ontology-12 | Relation types live in the registry member `relationTypes`; v1 ships the seven Binding discriminators as relation types plus `grants-role` (access-control@v1) (PK-MODEL-070). | agent proposal |

Notes for the owner review:

- PK-MODEL-056 publishes T foundational concepts, which are on the
  definition side, as fragments. This reads PK-MODEL-054's closed
  persistent schema as applying to P, D, and C definition concepts, in
  line with the T class contract ("without independent persistence").
- Storage locations for items of an extension content kind are not stated
  by repository-storage@v1.
