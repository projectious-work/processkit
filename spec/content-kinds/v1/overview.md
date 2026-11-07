# Content kinds — overview

Non-normative. The requirements are in `requirements.md`; the observable
interface is in `interfaces.yaml`.

## Purpose

processkit provides the format, validation, location, and serving of
governance content; it never ships an organization's content. This slug
defines the six governance kinds an author or agent writes — Standard,
ProcessSpecification, Skill, MCPServer, DecisionRecord, and Document — what
each must declare, what each disclosure level contains, how content is
validated, and the things processkit refuses to do with each kind: run a
process, execute a skill script, connect to a catalogued server, or write a
decision record on its own.

The kinds let an organization replace the governance part of harness
instruction files and skill directories: always-on standards feed the
connection briefing, and skills, processes, and standards load on demand,
one level at a time.

## Boundaries

This slug does not cover:

- the common envelope (`apiVersion`, `kind`, `metadata`, `status`), the
  ontology registry, Containers, Roles, Bindings, labels, and references —
  `ontology@v1`;
- content locations, file formats, front matter, deterministic
  serialization, and write behavior — `repository-storage@v1`;
- command syntax, `--json` envelopes, and exit codes — `cli@v1`;
- MCP tools, the connection briefing, `get_context` ranking, caching, and
  resources — `mcp-context-serving@v1`;
- overrides, final items, and provenance across upstream repositories —
  `inheritance@v1`;
- access filtering of served items — `access-control@v1`;
- secret redaction and input limits — `security@v1`;
- conversion of v0 skills, decisions, and processes — `v0-migration@v1`.

## Governing decisions

- **C1 — Context, not memory:** processkit defines processes but stores no
  WorkItem instances and runs nothing (PK-PROC-004, PK-PROD-021).
- **C2 — The full ontology is the definition language:** a
  ProcessSpecification is expressed with WorkItem, StateMachine, Role, Gate,
  and Artifact.
- **C3 — Decision records stay:** low-volume reviewed documents linked from
  the standards and processes they justify.
- **C4 — MCP is the agent interface:** skills and standards are served over
  MCP, not copied into harness directories; always-on rules join the
  briefing.
- **C9 — A catalog of trusted MCP servers, not a gateway:** MCPServer
  entries are served and never connected to.

## Provenance

| Baseline source (#197) | Carried here |
|---|---|
| `04-governance-content.md` intro, "Progressive disclosure" | Disclosure levels, PK-CONT-001 to PK-CONT-004 |
| `04-governance-content.md` "Standards" | PK-STD-001 to PK-STD-005 |
| `04-governance-content.md` "Process specifications" | PK-PROC-001 to PK-PROC-006 |
| `04-governance-content.md` "Skills" | PK-SKILL-001 to PK-SKILL-004 |
| `04-governance-content.md` "Trusted MCP server catalog" | PK-CAT-001 to PK-CAT-004 |
| `04-governance-content.md` "Decision records" | PK-DEC-001 to PK-DEC-004 |
| `04-governance-content.md` "Documents" | PK-DOC-001, PK-DOC-002 |
| `04-governance-content.md` "Validation" | PK-CONT-010 to PK-CONT-012 |
| `01-product-definition.md` "Goals", "Non-goals", "Content" | PK-PROD-010, PK-PROD-021; kind/ontology mapping |
| `03-repository-and-files.md` "Layout" | file paths in `interfaces.yaml` (informative; owned by `repository-storage@v1`) |
| `06-cli.md`, `07-mcp-and-context-assembly.md` | operation signatures in `interfaces.yaml` (informative; owned by `cli@v1`, `mcp-context-serving@v1`) |
| `11-verification-and-release.md` "Acceptance journeys" 2 and 3 | journeys 1 and 2 |
| `schemas/v1/standard.schema.json`, `schemas/v1/mcp-server.schema.json` | `schemas/` (unchanged copies) |
| `templates/v1/standard.template.json`, `templates/v1/mcp-server.template.json` | `examples/` (unchanged copies) |

The "Organizational scope and access" paragraph of chapter 4 (Containers,
Roles, Bindings under `context/ontology/`) belongs to `ontology@v1` and
`access-control@v1`.

### Gap items carried

From tag `archive/processkit-v1-governance-standards`, file
`spec/doc/v1/04-content-packages-and-extensions.md` (the assignment named
`04-governance-content.md`; that file does not exist on the tag):

| New ID | Old ID(s) | Content |
|---|---|---|
| PK-SKILL-005 | PK-PKG-010 | inputs and outputs |
| PK-SKILL-006 | PK-PKG-010 | dependencies |
| PK-SKILL-007 | PK-PKG-010, PK-PKG-013 | side-effect class (five classes) |
| PK-SKILL-008 | PK-PKG-010, PK-PKG-015 | safety constraints |
| PK-SKILL-009 | PK-PKG-015 | required MCP servers ("required tools") |
| PK-SKILL-010 | PK-PKG-015 | normative versus explanatory parts |

Not carried, because they conflict with #197:

- PK-PKG-012 (skill-exposed MCP tools): the MCP tool set is fixed by the
  release, and skills contain no code processkit runs.
- PK-PKG-015, second sentence (harness adapters preserving semantics):
  processkit generates no harness projections (C4, PK-PROD-023).
- PK-PKG-010 "owned capabilities": tied to the package/capability model
  that #197 removed; identity, version, purpose (summary), triggers, and
  progressive-disclosure resources are already in PK-SKILL-001 and
  PK-SKILL-002.

The skill metadata declarations are information served to agents, like
MCPServer `sideEffects`; processkit does not enforce or execute them.

## Open questions

Mirrors `open` in `interfaces.yaml`.

- **OPEN-content-kinds-01:** `skill.json` has no schema or template; field
  names and constraints for all Skill metadata, including the gap fields.
- **OPEN-content-kinds-02:** ProcessSpecification has no schema or template
  although PK-PROC-006 requires both; field names and level 0/1 contents.
- **OPEN-content-kinds-03:** DecisionRecord has no schema or template;
  front matter fields, date format, supersession link, level contents.
- **OPEN-content-kinds-04:** document source keys in `processkit.toml`,
  heading index shape, section addressing, level 1 contents.
- **OPEN-content-kinds-05:** PK-CONT-002 requires `summary` and `triggers`
  on every item, but the MCPServer schema makes `triggers` optional and
  DecisionRecord and Document declare neither; summary bound for unschemed
  kinds.
- **OPEN-content-kinds-06:** diagnostic field names and codes; how an
  invalid item is reported in results.
- **OPEN-content-kinds-07:** result field names for the attribution facts,
  and the meaning of "version" per kind.
- **OPEN-content-kinds-08:** both schemas `$ref`
  `resource-metadata.schema.json`; a copy of the `ontology@v1` schema is
  carried here. Which slug owns future envelope changes?
- **OPEN-content-kinds-09:** where secret patterns are configured; any
  default set.
- **OPEN-content-kinds-10:** KIND tokens for CLI and MCP; `processkit new`
  for kinds without a template.
- **OPEN-content-kinds-11:** spelling of the five skill side-effect
  classes versus the three MCPServer values; per operation or highest.
- **OPEN-content-kinds-12:** whether skill dependencies and required MCP
  servers are resolved references that fail validation when dangling.
- **OPEN-content-kinds-13:** how a Skill marks normative versus explanatory
  parts, compatibly with Agent Skills.
- **OPEN-content-kinds-14:** how scripts are identified and labelled;
  target Agent Skills format version.
- **OPEN-content-kinds-15:** `upstreams` on a non-gateway entry; whether
  gateway upstream names must resolve.
- **OPEN-content-kinds-16:** how a process state is addressed at level 2.
