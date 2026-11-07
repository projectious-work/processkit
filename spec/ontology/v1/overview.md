# Ontology and content model — overview

Non-normative. The requirements are in `requirements.md`; the interface
catalog is `interfaces.yaml`.

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
left open for inherited Containers (OPEN-ontology-10); PK-ENTITY-150's
"core discriminators Team and Project" is replaced by the six Container
discriminators of the v1 inventory, consistent with PK-MODEL-006.

## Open questions

Mirrors `interfaces.yaml` `open`.

- **OPEN-ontology-01:** registry file name, location, serialization, entry
  field names, and version format.
- **OPEN-ontology-02:** diagnostic codes for each validation, selector, and
  generation failure.
- **OPEN-ontology-03:** Container `spec` schema (field names, owner type,
  parent expression, lifecycle states, discriminator declaration).
- **OPEN-ontology-04:** name of the implicit root Container and whether it
  may be declared explicitly.
- **OPEN-ontology-05:** shape and placement of `status` in results.
- **OPEN-ontology-06:** whether `!=` and `notin` match items without the
  key; whitespace, empty sets, empty selector, quoting.
- **OPEN-ontology-07:** unit, base, and result field of the selector error
  position.
- **OPEN-ontology-08:** the definition-or-instance side of each of the 90
  concepts.
- **OPEN-ontology-09:** meaning of "uncovered discriminator" and "invalid
  mixing".
- **OPEN-ontology-10:** whether upstream Containers count as known and are
  included in duplicate-name checks.
- **OPEN-ontology-11:** names and paths of the extension metaschemas and how
  a namespace owner is declared.
- **OPEN-ontology-12:** location of the relation-type registry and the
  relation types shipped in v1.
