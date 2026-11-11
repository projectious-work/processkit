# Content kinds — requirements

This specification defines the governance content kinds processkit
validates, locates, and serves: Standard, ProcessSpecification, Skill,
MCPServer (trusted MCP server catalog entry), DecisionRecord, and Document.
It states what each kind must declare, what belongs to each disclosure
level, how content is validated, and what processkit must never do with a
kind (run a process, run a skill script, connect to a catalogued server, or
write a decision record). It does not define the common envelope and
ontology (`ontology@v1`), file locations and serialization
(`repository-storage@v1`), command syntax (`cli@v1`), MCP tools and context
assembly (`mcp-context-serving@v1`), or inheritance (`inheritance@v1`).

Conventions: requirements use EARS; "shall" is mandatory, "should" is
recommended, "may" is optional; requirement IDs are stable and never reused.

## Disclosure levels

Every kind is served in the following levels, so an agent loads only what a
task needs:

| Level | Content | Typical size |
|---|---|---|
| 0 | name, title, summary, triggers, applicability, labels | one line per item |
| 1 | level 0 plus the item's binding core: rules, process outline, skill instructions, server entry | tens of lines |
| 2 | one named section in full | as authored |

- **PK-CONT-001:** processkit shall define, for every content kind, which
  content belongs to each disclosure level. A level-0 listing shall not
  include rule text or section bodies. A level-1 read shall not include
  section bodies.
- **PK-CONT-002:** processkit shall require every item to declare a
  `summary` of bounded length and `triggers` that describe when the item
  applies. These fields are what an agent sees before deciding to load more.
- **PK-CONT-003:** processkit shall include in every served result the
  item's kind, name, version, source repository and path, content digest,
  and validation status, so an agent can cite exactly what it applied.
- **PK-CONT-004:** processkit shall require an item's applicability to be
  declared by project-defined profiles such as `cli`, `library`, `service`,
  or `documentation`, by labels, or by both. processkit shall treat profile
  names as vocabulary the repository declares, not as a fixed list.
- **PK-CONT-013:** processkit shall serve each kind at each disclosure
  level with exactly the members that `interfaces.yaml` lists for the kind
  under `levels`. A level-2 result shall also carry the kind's level-0
  members.
  <!-- agent proposal: OPEN-content-kinds-01, -02, -03, -04 -->
- **PK-CONT-014:** processkit shall require, for every kind, a `summary` of
  1 to 600 characters and `triggers` as a list of at least one unique string
  of 1 to 200 characters. This includes MCPServer entries, DecisionRecords,
  and Documents.
  <!-- agent proposal: OPEN-content-kinds-05 -->
- **PK-CONT-015:** When a caller requests one section at level 2,
  processkit shall find the section by the kind's section key in
  `interfaces.yaml` `sections`. If the item has no section with that key,
  then processkit shall fail with `content-kinds.unknown-section` and shall
  return no section.
  <!-- agent proposal: OPEN-content-kinds-16 -->
- **PK-CONT-016:** processkit shall carry the facts of PK-CONT-003 in the
  members that `interfaces.yaml` lists under `attribution`. The version of
  a Standard, ProcessSpecification, or Skill shall be its `spec.version`.
  The version of an MCPServer entry, DecisionRecord, or Document shall be
  its content digest; the `spec.version` of an MCPServer entry is the
  version of the catalogued server.
  <!-- agent proposal: OPEN-content-kinds-07 -->
- **PK-CONT-021:** processkit shall require every item to declare
  `spec.applicability`, at least one label, or both. If an item declares
  neither, then validation shall fail with
  `content-kinds.applicability-missing`. If an item names a profile that is
  not `*` and that is not known to the repository (the top-level key
  `profiles` of `processkit.toml` and those of locked upstreams,
  mcp-context-serving@v1 PK-MCP-090), then validation shall fail with
  `content-kinds.undeclared-profile`.
  <!-- agent proposal: PK-CONT-004 (profiles as repository vocabulary) -->

## Standards

A Standard is a versioned rule set, for example a branching, security, or
documentation standard. Its structure is the published schema
`schemas/standard.schema.json`; its template is
`examples/standard.template.json`.

- **PK-STD-001:** processkit shall require a Standard to declare title,
  version, lifecycle status, owner, summary, triggers, applicability, and an
  ordered list of rules. processkit shall require each rule to carry a
  stable identifier, an RFC 2119 level, and its text.
- **PK-STD-002:** processkit shall keep a Standard's detailed guidance in
  named sections that are retrievable one at a time. Sections may use
  Markdown. Rules and applicability shall stay structured fields.
- **PK-STD-003:** A Standard may reference other standards, processes,
  decisions, and URLs, and may declare `supersedes`. If a reference in a
  Standard does not resolve, then processkit shall report a validation
  error.
- **PK-STD-004:** processkit shall define the Standard kind as a composition
  over the ontology's Policy primitive.
- **PK-STD-005:** A Standard may be marked always-on. Where a Standard is
  marked always-on, processkit shall contribute its rules to the level-0
  briefing; always-on standards replace the governance part of harness
  instruction files.
- **PK-STD-006:** A Standard that overrides an inherited Standard shall
  declare `spec.overrides.effect` as `replace` or `amend`. With `replace`,
  the Standard shall be complete. With `amend`, the Standard's `spec` shall
  contain only `overrides`. inheritance@v1 PK-INH-051 defines how processkit
  applies each effect.
  <!-- agent proposal: inheritance@v1 PK-INH-012 override effects
       (assignment: content-kinds owns standard.schema.json) -->
- **PK-STD-007:** If an amending override names in `ruleLevels` a rule that
  the upstream Standard does not have, then validation shall fail with
  `content-kinds.override-unknown-rule`. If a rule in `addRules` has the id
  of a rule of the upstream Standard, then validation shall fail with
  `content-kinds.override-duplicate-rule`.
  <!-- agent proposal: inheritance@v1 PK-INH-012 override effects -->

## Process specifications

A ProcessSpecification defines how a kind of work is done, in ontology
terms: which WorkItem type it governs, its StateMachine, the Roles involved,
the Gates on transitions, the Artifacts produced, and the standards and
skills that apply at each step. Its structure is the published schema
`schemas/process-specification.schema.json`; its template is
`examples/process-specification.template.json`, and
`examples/process-specification.example.json` is the worked ticket-handling
example.

- **PK-PROC-001:** processkit shall require a ProcessSpecification to
  declare title, version, status, owner, summary, triggers, the governed
  WorkItem type, a StateMachine with states and transitions, and the Roles
  that may perform each transition.
- **PK-PROC-002:** A ProcessSpecification may declare Gates on transitions,
  Artifacts required or produced per state, and references to the
  standards, skills, and MCP servers that apply per state.
- **PK-PROC-003:** When processkit validates a ProcessSpecification,
  processkit shall check that every state is reachable, that terminal
  states are declared, that every transition names an existing Role, and
  that every referenced item resolves.
- **PK-PROC-004:** processkit shall not create, store, or track instances of
  the governed WorkItem type. A ProcessSpecification may name the external
  system that holds instances, such as an issue tracker.
- **PK-PROC-005:** processkit shall serve a ProcessSpecification as a whole
  at level 1 and per state at level 2, so an agent working on one ticket in
  state `triaged` loads only what that state requires.
- **PK-PROC-006:** processkit shall publish a schema and a template for
  ProcessSpecification. The processkit documentation shall include a worked
  ticket-handling example created from a natural-language description.
- **PK-PROD-021:** processkit shall not execute or track processes. It
  defines them; harnesses, trackers, forges, and orchestrators run them.
- **PK-PROC-007:** When processkit validates a ProcessSpecification,
  processkit shall also check that `initial` and the `from` and `to` of
  every transition name a declared state, that state ids are unique, and
  that no terminal state has an outgoing transition.
  <!-- agent proposal: OPEN-content-kinds-02 -->
- **PK-PROC-009:** processkit shall require a Gate to declare an id, a
  title, its kind (`approval` or `check`), a validator description, and the
  Roles with authority over its outcome. A Gate may declare whether it
  blocks the transition, the evidence its outcome must cite, and the Roles
  that may waive it.
  <!-- agent proposal: gap row 8, accepted by owner 2026-11-11 (#212) -->
- **PK-PROC-010:** processkit shall not evaluate a Gate, record a Gate
  outcome, or store a waiver. The outcomes of a Gate are `passed`,
  `failed`, and `waived`; a waiver states authority, reason, scope, and an
  expiry or review condition. The external instance system records them.
  <!-- agent proposal: gap row 8, accepted by owner 2026-11-11 (#212) -->
- **PK-PROC-011:** Where a ProcessSpecification declares `shape` `linear`,
  processkit shall require its states to form one ordered chain:
  `initial` is the first state in `states`, every transition goes from a
  state to the next state in `states`, every state except the last has
  exactly one transition, and only the last state is terminal. If the
  states do not form this chain, then validation shall fail with
  `content-kinds.process-not-linear`.
  <!-- agent proposal: gap row 6, accepted by owner 2026-11-11 (#212) -->
- **PK-PROC-012:** A state of a ProcessSpecification may declare its intent
  and its inputs. processkit shall require each input to declare its class
  (`instruction`, `reference`, or `working`) and a description. An input
  may name a typed reference or an artifact. If an input or a Gate's
  evidence names an artifact that no state of the process declares, then
  validation shall fail with `content-kinds.process-unknown-artifact`.
  <!-- agent proposal: gap row 6, accepted by owner 2026-11-11 (#212) -->

## Skills

A Skill is a reusable agent capability: instructions, optional reference
files, and metadata. processkit serves skills over MCP instead of copying
them into harness skill directories. The structure of `skill.json` is the
published schema `schemas/skill.schema.json`; the templates are
`examples/skill.template.json` and `examples/skill.template.md`.

- **PK-SKILL-001:** processkit shall require a Skill to consist of
  `SKILL.md` and `skill.json` metadata that declares name, version, summary,
  triggers, and applicability.
- **PK-SKILL-002:** processkit shall serve the body of `SKILL.md` as the
  Skill's level 1. processkit shall treat additional files in the skill
  directory as level 2 and shall make them retrievable one at a time.
- **PK-SKILL-003:** processkit shall not run executable code contained in a
  Skill. When processkit returns a script contained in a Skill, processkit
  shall return it to the agent as content, labelled as a script.
- **PK-SKILL-004:** The `SKILL.md` format should stay compatible with the
  published Agent Skills format, so existing skills can be adopted
  unchanged.
- **PK-SKILL-005:** processkit shall require a Skill's metadata to declare
  the skill's inputs and outputs.
  <!-- from governance draft: 04-content-packages-and-extensions.md
       PK-PKG-010 -->
- **PK-SKILL-006:** processkit shall require a Skill's metadata to declare
  the skill's dependencies.
  <!-- from governance draft: 04-content-packages-and-extensions.md
       PK-PKG-010 -->
- **PK-SKILL-007:** processkit shall require a Skill's metadata to declare
  whether the skill's operations are read-only, project-mutating,
  externally mutating, privileged, or destructive.
  <!-- from governance draft: 04-content-packages-and-extensions.md
       PK-PKG-010, PK-PKG-013 -->
- **PK-SKILL-008:** processkit shall require a Skill's metadata to declare
  the skill's safety constraints.
  <!-- from governance draft: 04-content-packages-and-extensions.md
       PK-PKG-010, PK-PKG-015 -->
- **PK-SKILL-009:** processkit shall require a Skill's metadata to declare
  the MCP servers the skill requires.
  <!-- from governance draft: 04-content-packages-and-extensions.md
       PK-PKG-015 -->
- **PK-SKILL-010:** processkit shall require a Skill to declare which of its
  parts are normative semantics and which are explanatory text.
  <!-- from governance draft: 04-content-packages-and-extensions.md
       PK-PKG-015 -->
- **PK-SKILL-011:** processkit shall require `spec.sideEffects` of a Skill
  to state the highest side-effect class of the skill's operations, as one
  of `read-only`, `project-mutating`, `externally-mutating`, `privileged`,
  or `destructive`, listed in ascending order.
  <!-- agent proposal: OPEN-content-kinds-11 -->
- **PK-SKILL-012:** processkit shall treat every entry of
  `spec.dependencies` (a Skill or a Standard) and of
  `spec.requiredMcpServers` (an MCPServer) as a typed reference. If such a
  reference does not resolve, then validation shall fail.
  <!-- agent proposal: OPEN-content-kinds-12 -->
- **PK-SKILL-013:** processkit shall read a Skill's normative and
  explanatory parts from `spec.parts` in `skill.json`, never from
  `SKILL.md`. processkit shall require `spec.parts` to list `SKILL.md` and
  shall treat a file that is not listed as explanatory. If a listed path
  does not exist in the skill directory, then validation shall fail with
  `content-kinds.skill-part-missing`.
  <!-- agent proposal: OPEN-content-kinds-13 -->
- **PK-SKILL-014:** processkit shall label a skill file as a script if its
  path in the skill directory starts with `scripts/` or its content starts
  with the two bytes `#!`. processkit shall return an additional skill file
  with its `path`, `script` label, `encoding`, and `content`.
  <!-- agent proposal: OPEN-content-kinds-14 -->
- **PK-SKILL-015:** processkit shall validate a skill directory in the
  Agent Skills format (`SKILL.md` with front matter `name` and
  `description`, and optional `scripts/`, `references/`, and `assets/`
  directories) when only `skill.json` is added. processkit shall not
  require front matter in `SKILL.md` and shall not require a change to it.
  <!-- agent proposal: OPEN-content-kinds-14 -->
- **PK-SKILL-016:** A Skill may declare in `spec.agent` a persona Document,
  a model class, and evaluation cases. processkit shall serve these fields
  at level 1 as information. processkit shall not run a model or an
  evaluation.
  <!-- agent proposal: gap row 4 (owner plan in the standards v2.2.0
       applicability record) -->

## Trusted MCP server catalog

A governing repository can publish the MCP servers it trusts, including an
external MCP gateway, as MCPServer entries. Their structure is the published
schema `schemas/mcp-server.schema.json`; the template is
`examples/mcp-server.template.json`.

- **PK-CAT-001:** processkit shall not connect to, forward to, proxy, or
  invoke a catalogued server. The catalog is information for agents and
  people.
- **PK-CAT-002:** processkit shall require an MCPServer entry to declare a
  pinned version, transport, highest side-effect class, owner, lifecycle
  status, and authentication mode. processkit shall require a remote
  transport to use HTTPS. processkit shall require a stdio entry to name a
  package coordinate and shall not accept a shell command line in its place.
- **PK-CAT-003:** An MCPServer entry shall not contain credential values. If
  a field of an MCPServer entry matches a configured secret pattern, then
  processkit validation shall fail.
- **PK-CAT-004:** An MCPServer entry with role `gateway` may list the
  catalogued servers it fronts. processkit shall not infer trust in a server
  from its presence behind a gateway.
- **PK-CAT-005:** processkit shall check every string value of an
  MCPServer entry, including its metadata, against the built-in secret
  patterns in `interfaces.yaml` and against the operator's
  `redaction.patterns` (`cli@v1`). If a value matches, then validation
  shall fail with `content-kinds.secret-in-catalog-entry`, and the
  diagnostic shall not contain the value.
  <!-- agent proposal: OPEN-content-kinds-09 -->
- **PK-CAT-006:** If an MCPServer entry with role `server` declares
  `upstreams`, then validation shall fail with
  `content-kinds.upstreams-not-allowed`. If a name in the `upstreams` of a
  gateway entry matches no MCPServer entry, then processkit shall report
  the warning `content-kinds.upstream-not-catalogued` and shall serve the
  gateway entry.
  <!-- agent proposal: OPEN-content-kinds-15 -->

## Decision records

A DecisionRecord states why a rule, process, or structure exists. It is a
reviewed document, not an activity log. The structure of its front matter
is the published schema `schemas/decision-record.schema.json`; its
template is `examples/decision-record.template.md`.

- **PK-PROD-010:** processkit shall keep decision records as reviewed
  governance documents and shall make them linkable from the standards and
  processes they justify.
- **PK-DEC-001:** processkit shall require a DecisionRecord to declare
  title, status (`proposed`, `accepted`, `superseded`, or `rejected`), date,
  deciders, context, decision, and consequences. A DecisionRecord may
  declare alternatives.
- **PK-DEC-002:** Standards and process specifications may reference the
  DecisionRecords that justify them. When processkit serves a rule,
  processkit shall be able to include those references.
- **PK-DEC-003:** An accepted DecisionRecord shall not be rewritten in
  meaning. A change to an accepted decision shall be made by a new
  DecisionRecord that supersedes it.
- **PK-DEC-004:** processkit shall not create a DecisionRecord as a side
  effect of another command. Authors write decision records through
  reviewed file changes.
- **PK-DEC-005:** processkit shall require every field of a
  DecisionRecord, including context, decision, and consequences, in its
  front matter, with `date` as an ISO 8601 calendar date `YYYY-MM-DD`.
  processkit shall serve the Markdown body only as the level-2 section
  `notes`.
  <!-- agent proposal: OPEN-content-kinds-03 -->
- **PK-DEC-006:** A DecisionRecord that replaces others shall name them in
  `spec.supersedes`. If a named record does not have status `superseded`,
  then validation shall fail with `content-kinds.supersession-status`. If a
  record has status `superseded` and no record names it in `supersedes`,
  then processkit shall report the warning
  `content-kinds.supersession-missing`.
  <!-- agent proposal: OPEN-content-kinds-03 -->

## Documents

A Document is a Markdown file that a declared document source matches. The
front matter keys processkit reads are in `schemas/document.schema.json`;
the document source table is in `schemas/document-sources.schema.json`.

- **PK-DOC-001:** processkit shall require a document source to be declared
  in configuration with a path pattern, a namespace, and labels for every
  matched file. processkit shall not serve Markdown that no document source
  matches.
- **PK-DOC-002:** processkit shall serve a Document's title, path, labels,
  and heading index at level 0, and one heading section at level 2.
  Documents have no rules and no lifecycle.
- **PK-DOC-003:** processkit shall read document sources from the
  `[[document-sources]]` tables of `processkit.toml`, with the keys
  `pattern`, `namespace`, and `labels`, and the optional keys `summary` and
  `triggers`. processkit shall resolve patterns against the repository root
  with the syntax of `schemas/document-sources.schema.json`. If a file
  matches more than one document source, then validation shall fail with
  `content-kinds.document-source-overlap`.
  <!-- agent proposal: OPEN-content-kinds-04 -->
- **PK-DOC-004:** processkit shall take a Document's name from front matter
  `name`, else from the file name without `.md`. processkit shall take its
  title from front matter `title`, else from the first level-1 heading,
  else from the name. processkit shall take its summary and triggers from
  front matter, else from the document source. If a Document then has no
  summary or no triggers, then validation shall fail with
  `content-kinds.document-missing-field`. If two Documents in one namespace
  have the same name, then validation shall fail with
  `content-kinds.document-name-collision` for both.
  <!-- agent proposal: OPEN-content-kinds-04, OPEN-content-kinds-05 -->
- **PK-DOC-005:** processkit shall build a Document's heading index from
  its ATX and setext headings as CommonMark 0.31.2 defines them, and shall
  give each heading the id, level, and title that `interfaces.yaml`
  `heading_index` defines. A heading section shall extend from its heading
  to the next heading of the same or a smaller level number, or to the end
  of the file.
  <!-- agent proposal: OPEN-content-kinds-04 -->

## Validation

- **PK-CONT-010:** When `processkit validate` runs, processkit shall
  validate every item against the schema of the item's declared
  `apiVersion` and shall report the file, JSON pointer, and violated
  constraint of every violation.
- **PK-CONT-011:** If an item is invalid, then processkit shall not serve it
  as valid, shall keep other valid items available, and shall report the
  invalid item in results that would have included it.
- **PK-CONT-012:** processkit shall validate draft content passed as input,
  without writing files, through both the processkit CLI and the MCP
  server.
- **PK-CONT-017:** processkit shall report every validation failure that
  this specification defines as a `cli@v1` diagnostic with category
  `validation` (unless `interfaces.yaml` `errors` states another category),
  the code from `interfaces.yaml` `errors`, `file`, `pointer`, and
  `constraint`. For a schema violation, `constraint` shall be the absolute
  keyword location in the published schema.
  <!-- agent proposal: OPEN-content-kinds-06 -->
- **PK-CONT-018:** If an item is invalid, then processkit shall show it in
  a result that would have included it with its kind, name, namespace, and
  attribution only, with validation outcome `invalid` and its diagnostics,
  and without its `spec` members.
  <!-- agent proposal: OPEN-content-kinds-06 -->
- **PK-CONT-019:** processkit shall accept as the KIND operand of the CLI
  and as the `kind` argument of the MCP tools exactly the `kind` value of a
  content kind, compared case-sensitively. If the value names no kind,
  then processkit shall fail with `content-kinds.unknown-kind`.
  <!-- agent proposal: OPEN-content-kinds-10 -->
- **PK-CONT-020:** When `processkit new KIND NAME` runs, processkit shall
  plan the files of the kind's published template at the kind's location,
  with the template's placeholder name replaced by NAME. If the kind has no
  published template, then processkit shall fail with
  `content-kinds.no-template`. If NAME does not match the name syntax of
  `ontology@v1`, then processkit shall fail with
  `content-kinds.invalid-name`.
  <!-- agent proposal: OPEN-content-kinds-10 -->
- **PK-CONT-022:** When processkit validates draft content passed as input,
  processkit shall validate the draft as one item of the given kind: its
  schema, its references, and its cross-field rules. processkit shall skip
  the checks that need other files of the same item, such as Skill parts,
  and shall report `-` as the diagnostic `file`.
  <!-- agent proposal: OPEN-content-kinds-06 -->
- **PK-CONT-023:** A ProcessSpecification, Skill, or MCPServer entry may
  declare `spec.final` and a `spec.overrides` with effect `replace`, in the
  shape a Standard uses. processkit shall apply them as `inheritance@v1`
  defines for final items and overrides.
  <!-- agent proposal: inheritance@v1 OPEN-inheritance-04 (kinds other
       than Standard) -->
