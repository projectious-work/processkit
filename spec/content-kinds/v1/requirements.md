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

## Process specifications

A ProcessSpecification defines how a kind of work is done, in ontology
terms: which WorkItem type it governs, its StateMachine, the Roles involved,
the Gates on transitions, the Artifacts produced, and the standards and
skills that apply at each step.

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

## Skills

A Skill is a reusable agent capability: instructions, optional reference
files, and metadata. processkit serves skills over MCP instead of copying
them into harness skill directories.

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

## Decision records

A DecisionRecord states why a rule, process, or structure exists. It is a
reviewed document, not an activity log.

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

## Documents

- **PK-DOC-001:** processkit shall require a document source to be declared
  in configuration with a path pattern, a namespace, and labels for every
  matched file. processkit shall not serve Markdown that no document source
  matches.
- **PK-DOC-002:** processkit shall serve a Document's title, path, labels,
  and heading index at level 0, and one heading section at level 2.
  Documents have no rules and no lifecycle.

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
