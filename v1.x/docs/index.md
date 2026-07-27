# Introduction

LLMS index: [llms.txt](/processkit/v1.x/llms.txt)

---

# processkit

**processkit is a provider-neutral process layer for AI-assisted
software projects.**

It gives agents structured project memory, reusable domain skills, and
validated MCP tools. The practical effect is simple: agents can read and
write durable work items, decisions, notes, artifacts, migrations, and
other project records through explicit contracts instead of loose files
and provider-specific conventions.

processkit is designed to be used directly by MCP-capable harnesses or
installed by an environment manager. aibox is one supported managed
installer, not a runtime dependency.

## What ships

- **140 skills** across engineering, product, research, data, design,
  documents, devops, and processkit operations.
- **25 MCP server entry points** for entity management, search, routing,
  release checks, projections, and gateway access.
- **16 shipped project-memory schemas** for durable v2 entities such as
  WorkItem, DecisionRecord, Artifact, Note, LogEntry, Migration, Actor,
  Role, Binding, Scope, Gate, Discussion, and related primitives.
- **5 package tiers**: `minimal`, `managed`, `software`, `research`,
  and `product`.
- **A provider-neutral MCP gateway** that can expose processkit through
  one stdio server, one streamable HTTP daemon, or a stdio proxy.

## Design goals

processkit separates process semantics from harness behavior:

- The **schemas** define durable project memory.
- The **skills** describe repeatable workflows and domain gotchas.
- The **MCP tools** validate writes, enforce state transitions, and keep
  the context searchable.
- The **gateway** gives harnesses one processkit entry point without
  knowing about Claude, Codex, OpenCode, Hermes, Aider, or any other
  provider-specific runtime.

That split keeps processkit forkable, installable by hand, and usable by
multiple harnesses. Integrations can automate install and lifecycle, but
they do not own the processkit contracts.

## How to use it

The direct path is:

1. Download a release tarball from
   [GitHub Releases](https://github.com/projectious-work/processkit/releases).
2. Copy the shipped `context/`, `.processkit/`, and `AGENTS.md` files
   into your project.
3. Register `processkit-gateway` or selected per-skill MCP servers with
   your harness.
4. Ask the agent to use processkit tools for entity reads and writes.

Managed installers can do those steps for you. For example, aibox can
fetch a pinned processkit release, choose a package tier, write harness
MCP configuration, and supervise a gateway daemon in a devcontainer.

## Where to go next

- [Getting Started](./getting-started/overview) explains the manual and
  managed install paths.
- [MCP Servers](./mcp-servers/overview) explains gateway, daemon,
  stdio-proxy, aggregate, and per-skill layouts.
- [Primitives](./primitives/overview) explains the project-memory
  entity model.
- [Skills](./skills/overview) explains the skill package format and
  catalog.
- [Packages](./packages/overview) explains the five package tiers.
- [v2 Contracts](./reference/v2-contracts) explains the current
  deliverable boundary and demoted legacy primitives.

## Current status

The current release line is pre-1.0. Breaking changes may still land in
minor releases, and the changelog calls them out explicitly.

`v0.25.0` is a breaking pre-1.0 release. It completes the
SmoothTiger/SmoothRiver v2 deliverable boundary, adds the
provider-neutral `processkit-gateway`, removes legacy first-class
primitive schemas from the shipped `src/context/` surface, and turns the
release checks into executable gates.

---

Section pages:

- [apiVersion Policy](/processkit/v1.x/docs/reference/apiversion-policy/)
- [Overview](/processkit/v1.x/docs/getting-started/overview/)
- [Overview](/processkit/v1.x/docs/mcp-servers/overview/)
- [Overview](/processkit/v1.x/docs/packages/overview/)
- [Overview](/processkit/v1.x/docs/primitives/overview/)
- [Overview](/processkit/v1.x/docs/processes/overview/)
- [Overview](/processkit/v1.x/docs/skills/overview/)
- [Entity File Format](/processkit/v1.x/docs/primitives/format/)
- [Harness Compatibility](/processkit/v1.x/docs/mcp-servers/harness-compatibility/)
- [ID Formats](/processkit/v1.x/docs/reference/id-formats/)
- [Installing](/processkit/v1.x/docs/getting-started/installing/)
- [minimal](/processkit/v1.x/docs/packages/minimal/)
- [Process Skills](/processkit/v1.x/docs/skills/catalog/process/)
- [Skill Package Format](/processkit/v1.x/docs/skills/format/)
- [managed](/processkit/v1.x/docs/packages/managed/)
- [Skill Hierarchy](/processkit/v1.x/docs/skills/hierarchy/)
- [State Machines](/processkit/v1.x/docs/primitives/state-machines/)
- [Version Migration](/processkit/v1.x/docs/reference/migration/)
- [Your First Entity](/processkit/v1.x/docs/getting-started/first-entity/)
- [Language Skills](/processkit/v1.x/docs/skills/catalog/language/)
- [Privacy Tiers](/processkit/v1.x/docs/reference/privacy/)
- [Relationships](/processkit/v1.x/docs/primitives/relationships/)
- [software](/processkit/v1.x/docs/packages/software/)
- [Infrastructure Skills](/processkit/v1.x/docs/skills/catalog/infrastructure/)
- [research](/processkit/v1.x/docs/packages/research/)
- [v2 Contracts](/processkit/v1.x/docs/reference/v2-contracts/)
- [Architecture Skills](/processkit/v1.x/docs/skills/catalog/architecture/)
- [product](/processkit/v1.x/docs/packages/product/)
- [Design & Visual Skills](/processkit/v1.x/docs/skills/catalog/design/)
- [Data & Analytics Skills](/processkit/v1.x/docs/skills/catalog/data/)
- [AI & ML Skills](/processkit/v1.x/docs/skills/catalog/ai-ml/)
- [API & Integration Skills](/processkit/v1.x/docs/skills/catalog/api/)
- [WorkItem](/processkit/v1.x/docs/primitives/workitem/)
- [LogEntry](/processkit/v1.x/docs/primitives/logentry/)
- [Security Skills](/processkit/v1.x/docs/skills/catalog/security/)
- [DecisionRecord](/processkit/v1.x/docs/primitives/decisionrecord/)
- [Observability Skills](/processkit/v1.x/docs/skills/catalog/observability/)
- [Artifact](/processkit/v1.x/docs/primitives/artifact/)
- [Database Skills](/processkit/v1.x/docs/skills/catalog/database/)
- [Note](/processkit/v1.x/docs/primitives/note/)
- [Actor](/processkit/v1.x/docs/primitives/actor/)
- [Role](/processkit/v1.x/docs/primitives/role/)
- [Binding](/processkit/v1.x/docs/primitives/binding/)
- [Scope](/processkit/v1.x/docs/primitives/scope/)
- [Discussion](/processkit/v1.x/docs/primitives/discussion/)
- [Gate](/processkit/v1.x/docs/primitives/gate/)
- [Migration](/processkit/v1.x/docs/primitives/migration/)
- [Schedule](/processkit/v1.x/docs/primitives/schedule/)
- [Constraint](/processkit/v1.x/docs/primitives/constraint/)
- [Category](/processkit/v1.x/docs/primitives/category/)
- [CrossReference](/processkit/v1.x/docs/primitives/cross-reference/)
- [Context](/processkit/v1.x/docs/primitives/context-entity/)
- [Process](/processkit/v1.x/docs/primitives/process-entity/)
- [StateMachine](/processkit/v1.x/docs/primitives/statemachine/)
- [Installer and releases](/processkit/v1.x/docs/installer/): Standalone installation, trust, compatibility, and integrations.
- [](/processkit/v1.x/docs/mcp-servers/claude-code/)
- [Development](/processkit/v1.x/docs/development/): Active planning documents for processkit evolution.
- [Framework & SEO Skills](/processkit/v1.x/docs/skills/catalog/framework/)
- [Performance Skills](/processkit/v1.x/docs/skills/catalog/performance/)
