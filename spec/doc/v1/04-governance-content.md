# Governance content

processkit provides the format, validation, location, and serving of
governance content. It never ships an organization's content. Each kind has a
published JSON Schema and a template that an author or agent fills in.

## Progressive disclosure

Every kind is served in levels so an agent loads only what a task needs.

| Level | Content | Typical size |
|---|---|---|
| 0 | name, title, summary, triggers, applicability, labels | one line per item |
| 1 | level 0 plus the item's binding core: rules, process outline, skill instructions, server entry | tens of lines |
| 2 | one named section in full | as authored |

- **PK-CONT-001:** every kind MUST define what belongs to each level. A
  level-0 listing MUST NOT include rule text or section bodies; a level-1
  read MUST NOT include section bodies.
- **PK-CONT-002:** every item MUST declare a `summary` of bounded length and
  `triggers` describing when it applies. These are what an agent sees before
  deciding to load more.
- **PK-CONT-003:** every served result MUST carry kind, name, version, source
  repository and path, content digest, and validation status, so an agent can
  cite exactly what it applied.
- **PK-CONT-004:** applicability MUST be declared by project-defined profiles
  such as `cli`, `library`, `service`, or `documentation`, by labels, or both.
  Profile names are vocabulary the repository declares, not a fixed list.

## Standards

A standard is a versioned rule set: for example a branching, security, or
documentation standard. Schema:
[`standard.schema.json`](../../schemas/v1/standard.schema.json); template:
[`standard.template.json`](../../templates/v1/standard.template.json).

- **PK-STD-001:** a standard MUST declare title, version, lifecycle status,
  owner, summary, triggers, applicability, and an ordered list of rules. Each
  rule MUST carry a stable identifier, an RFC 2119 level, and its text.
- **PK-STD-002:** detailed guidance MUST live in named sections retrievable
  one at a time. Sections MAY use Markdown; rules and applicability MUST stay
  structured fields.
- **PK-STD-003:** a standard MAY reference other standards, processes,
  decisions, and URLs, and MAY declare `supersedes`. A dangling reference is
  a validation error.
- **PK-STD-004:** a standard is a composition over the Policy primitive.
- **PK-STD-005:** a standard MAY be marked `always-on`. Always-on standards
  contribute their rules to the level-0 briefing and replace the governance
  part of harness instruction files.

## Process specifications

A process specification defines how a kind of work is done, in ontology
terms: which WorkItem type it governs, its StateMachine, the Roles involved,
the Gates on transitions, the Artifacts produced, and the standards and
skills that apply at each step.

- **PK-PROC-001:** a ProcessSpecification MUST declare title, version, status,
  owner, summary, triggers, the governed WorkItem type, a StateMachine with
  states and transitions, and the Roles that may perform each transition.
- **PK-PROC-002:** a process MAY declare Gates on transitions, Artifacts
  required or produced per state, and references to the standards, skills,
  and MCP servers that apply per state.
- **PK-PROC-003:** validation MUST check that every state is reachable, that
  terminal states are declared, that every transition names an existing
  Role, and that every referenced item resolves.
- **PK-PROC-004:** processkit MUST NOT create, store, or track instances of
  the governed WorkItem type. A process MAY name the external system that
  holds instances, such as an issue tracker.
- **PK-PROC-005:** a process MUST be servable as a whole at level 1 and per
  state at level 2, so an agent working on one ticket in state `triaged`
  loads only what that state requires.
- **PK-PROC-006:** processkit MUST publish a schema and a template for
  ProcessSpecification, and the documentation MUST include a worked
  ticket-handling example created from a natural-language description.

## Skills

A skill is a reusable agent capability: instructions, optional reference
files, and metadata. processkit serves skills over MCP instead of copying
them into harness skill directories.

- **PK-SKILL-001:** a skill MUST consist of `SKILL.md` and `skill.json`
  metadata with name, version, summary, triggers, and applicability.
- **PK-SKILL-002:** level 1 is the body of `SKILL.md`; additional files in the
  skill directory are level 2 and MUST be retrievable one at a time.
- **PK-SKILL-003:** skills MUST NOT contain executable code that processkit
  runs. Scripts in a skill are content returned to the agent, labelled as
  such.
- **PK-SKILL-004:** the `SKILL.md` format SHOULD stay compatible with the
  published Agent Skills format so existing skills can be adopted unchanged.

## Trusted MCP server catalog

A governing repository can publish the MCP servers it trusts, including an
external MCP gateway. Schema:
[`mcp-server.schema.json`](../../schemas/v1/mcp-server.schema.json);
template: [`mcp-server.template.json`](../../templates/v1/mcp-server.template.json).

- **PK-CAT-001:** processkit MUST NOT connect to, forward to, proxy, or invoke
  a catalogued server. The catalog is information for agents and people.
- **PK-CAT-002:** an entry MUST declare a pinned version, transport, highest
  side-effect class, owner, lifecycle status, and authentication mode. Remote
  transports MUST use HTTPS; stdio entries MUST name a package coordinate,
  never a shell command line.
- **PK-CAT-003:** entries MUST NOT contain credential values, and validation
  MUST fail on fields that match configured secret patterns.
- **PK-CAT-004:** an entry with role `gateway` MAY list the catalogued servers
  it fronts. processkit MUST NOT infer trust in a server from its presence
  behind a gateway.

## Decision records

A decision record states why a rule, process, or structure exists. It is a
reviewed document, not an activity log.

- **PK-DEC-001:** a DecisionRecord MUST declare title, status (`proposed`,
  `accepted`, `superseded`, `rejected`), date, deciders, context, decision,
  and consequences, and MAY declare alternatives.
- **PK-DEC-002:** standards and processes MAY reference the decisions that
  justify them; serving a rule MUST be able to include those references.
- **PK-DEC-003:** an accepted decision MUST NOT be rewritten in meaning.
  Changing it requires a new decision that supersedes it.
- **PK-DEC-004:** decision records are written by authors through reviewed
  file changes. processkit MUST NOT create a decision record as a side
  effect of another command.

## Documents

- **PK-DOC-001:** a document source MUST be declared in configuration with a
  path pattern, a namespace, and labels for every matched file. Markdown that
  no source matches MUST NOT be served.
- **PK-DOC-002:** level 0 is title, path, labels, and heading index; level 2
  is one heading section. Documents have no rules and no lifecycle.

## Organizational scope and access

Containers, Roles, and Bindings are ontology content stored under
`context/ontology/`. Containers are the namespaces of all other items.
Roles and Bindings also carry access rules, see
[Identity and access control](08-identity-and-access.md).

## Validation

- **PK-CONT-010:** `processkit validate` MUST validate every item against the
  schema of its declared `apiVersion` and report file, JSON pointer, and
  violated constraint.
- **PK-CONT-011:** an invalid item MUST NOT be served as valid. Other valid
  items remain available, and the invalid item is reported in results that
  would have included it.
- **PK-CONT-012:** validation MUST be available for draft content passed as
  input, without writing files, through both CLI and MCP.
