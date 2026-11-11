# Content kinds — overview

Non-normative. The requirements are in `requirements.md`; the observable
interface is in `interfaces.yaml`.

## Owner goal

The owner wants an organization to write its governance once, as reviewed
files, and have every agent load exactly the part a task needs: standards,
processes, skills, trusted MCP servers, decisions, and documents
(PK-PROD-010, C3, C4). The content kinds must be precise enough that an
agent can draft them from natural language and processkit can validate
them, yet processkit must stay a definition and serving layer: it never runs
a process, a skill, a gate, or a catalogued server, and it stores no
instances (C1, C2, C9). The kinds replace the governance part of harness
instruction files and skill directories without locking authors into one
vendor's format.

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
- command syntax, `-o json` envelopes, and exit codes — `cli@v1`;
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
| `schemas/v1/standard.schema.json`, `schemas/v1/mcp-server.schema.json` | `schemas/` (extended when resolving open items; see below) |
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

### Gap rows drafted as agent proposals

Drafted because they fit C1 and C2; accepted by owner 2026-11-11
(#212):

- **Gap row 6** (governance draft 04, PK-PKG-024 to PK-PKG-026): a
  `linear` shape of ProcessSpecification (PK-PROC-011) and per-state
  intent and classified inputs (PK-PROC-012). It is a constrained
  StateMachine, not a second execution model, so it keeps PK-PROC-001 and
  C2. Not drafted: PK-PKG-027 to PK-PKG-029 (execution records, step
  completion proof, rendered stage views), because processkit stores no
  instances and generates no projections (C1, C4).
- **Gap row 8, Gate only** (governance draft 13, PK-ENTITY-050 and
  PK-ENTITY-052): the Gate field contract (PK-PROC-009) and the outcome and
  waiver vocabulary (PK-PROC-010). Not drafted: PK-ENTITY-051 (append-only
  evaluation events), because gate evaluations are instances (C1).

## Resolved open items

| Item | Resolution | Basis |
|---|---|---|
| OPEN-content-kinds-01 | `schemas/skill.schema.json` for `skill.json` with every Skill field; templates `examples/skill.template.json` and `.md`; level contents in `levels` (PK-CONT-013) | owner decision: #213 finding 5 (schema); agent proposal (fields) |
| OPEN-content-kinds-02 | `schemas/process-specification.schema.json`, template, and worked example; extra structural checks (PK-PROC-007); level 1 outline and level 2 state in `levels` | owner decision: #213 finding 5 (schema); agent proposal (fields) |
| OPEN-content-kinds-03 | `schemas/decision-record.schema.json`; every field in front matter, `date` as `YYYY-MM-DD`, body as section `notes` (PK-DEC-005); `supersedes` and its checks (PK-DEC-006) | owner decision: #213 finding 5 (schema); agent proposal (fields; follows repository-storage@v1 front matter rule) |
| OPEN-content-kinds-04 | `[[document-sources]]` with `pattern`, `namespace`, `labels`, `summary`, `triggers`, patterns against the repository root (PK-DOC-003); name, title, summary, and triggers derivation (PK-DOC-004); heading index and ids (PK-DOC-005); `schemas/document.schema.json` and `document-sources.schema.json` | owner decision: #213 finding 5 (schema); agent proposal (keys; follows repository-storage@v1 pattern root) |
| OPEN-content-kinds-05 | PK-CONT-002 governs: `triggers` required in `mcp-server.schema.json`; summary 1..600 and triggers rules for every kind (PK-CONT-014); DecisionRecord declares both; Documents take them from front matter or the source | agent proposal (conventional alignment of the schema with the requirement) |
| OPEN-content-kinds-06 | `cli@v1` diagnostic shape; code table in `errors`; `constraint` is the schema keyword location (PK-CONT-017); invalid items shown without `spec` (PK-CONT-018); draft scope (PK-CONT-022) | agent proposal (reuses cli@v1 diagnostic schema) |
| OPEN-content-kinds-07 | attribution members in `attribution`, using `ontology@v1` status; version is `spec.version` or the content digest (PK-CONT-016) | agent proposal |
| OPEN-content-kinds-08 | `ontology@v1` owns the envelope metadata schema; the copy here stays byte-identical and changes only by copying | agent proposal |
| OPEN-content-kinds-09 | built-in secret patterns in `secret_patterns` plus operator `redaction.patterns` of `cli@v1` (PK-CAT-005) | agent proposal |
| OPEN-content-kinds-10 | exact, case-sensitive `kind` values for MCP; case-insensitive name, plural, or short name for the CLI TYPE, owner decision 2026-11-11 (#212), CLI style B (PK-CONT-019); templates per kind, `content-kinds.no-template` for Document (PK-CONT-020) | agent proposal |
| OPEN-content-kinds-11 | `read-only`, `project-mutating`, `externally-mutating`, `privileged`, `destructive`; one field with the highest class (PK-SKILL-011) | agent proposal |
| OPEN-content-kinds-12 | typed references that must resolve; dependencies target Skill or Standard (PK-SKILL-012) | agent proposal |
| OPEN-content-kinds-13 | `spec.parts` in `skill.json` per file; `SKILL.md` required; unlisted files explanatory (PK-SKILL-013) | agent proposal (follows repository-storage@v1: skill.json authoritative) |
| OPEN-content-kinds-14 | script when under `scripts/` or starting with `#!`; result `{path, script, encoding, content}` (PK-SKILL-014); Agent Skills format target without a version (PK-SKILL-015) | agent proposal |
| OPEN-content-kinds-15 | `upstreams` on role `server` fails; unknown gateway upstream is a warning (PK-CAT-006) | agent proposal |
| OPEN-content-kinds-16 | the `section` argument with the state id; section keys per kind (PK-CONT-015) | agent proposal |
| (PK-INH-012 override effects) | `spec.overrides.effect` `replace` or `amend` with `addRules` and `ruleLevels` in the Standard schema (PK-STD-006, PK-STD-007); `final` and `replace` overrides for ProcessSpecification, Skill, and MCPServer (PK-CONT-023) | owner decision: #213 assignment (content-kinds owns `standard.schema.json`); agent proposal (shape) |
| (gap row 4) | Skill metadata made concrete in `skill.schema.json`; optional `spec.agent` with persona, model class, and evaluation cases (PK-SKILL-016) | owner decision: standards v2.2.0 applicability record (owner plan); agent proposal (fields) |
