# Product definition

## Purpose

processkit is a local-first, provider-neutral AI-agent context and memory
management system for humans and agents working in Git repositories. It turns
repository text files into durable, typed, inspectable memory and provides the
shared ontology through which humans and agents describe work, knowledge,
decisions, evidence, organizations, capabilities, and processes in
conversation.

Its external posture is an agent-native context and workflow layer for durable,
governed project operations. MCP is the primary agent experience; CLI remains
complete for humans, automation, administration, and recovery. The precise
division between agent reasoning and product enforcement is defined in the
[agent-native posture](16-agent-native-posture.md).

One processkit installation belongs to one Git repository representing one
project or coordination scope. Its `context/` is the authoritative shared
process memory of that scope, not the private memory of one agent. Any number
of human, permanent-agent, and ephemeral-agent TeamMembers may participate by
working with ordinary clones, branches, reviews, and merges.

Human-readable Git files are always canonical. Local databases, full-text
indexes, and embedding/vector entries augment retrieval and context assembly,
but remain disposable client-side projections that can be rebuilt from the
repository. processkit also installs, versions, discovers, and governs skills
and MCP servers that let agents understand and safely operate on this context.

The product answers these questions without depending on replay of a chat
history or one model provider's private memory:

1. What project and organizational context should an agent know now?
2. Which durable memories, decisions, evidence, relationships, and history
   support that context?
3. How can a human and an agent express new information in the same ontology?
4. What state are process entities in, and which transitions are valid?
5. Which skill, MCP tool, or process capability should an agent use next?

## Users

- A project owner installs and upgrades a coherent process capability set.
- A human contributor reads and reviews canonical state in Git.
- An AI agent retrieves bounded relevant context, queries durable memory, and
  records or mutates project state through validated tools.
- A process author creates reusable skills, schemas, state machines, and
  process definitions.
- A harness or orchestrator integrates through stable MCP and machine
  contracts without becoming a processkit dependency.
- A portfolio coordinator links work and evidence across repositories without
  treating any single repository as a global mutable database.

## Goals

- **PK-PROD-001:** canonical project process state MUST remain human-readable,
  Git-compatible, and usable without a hosted processkit service.
- **PK-PROD-002:** normal agent writes MUST pass through validated operations
  that enforce schemas, lifecycle rules, ownership, and event recording.
- **PK-PROD-003:** the same public process semantics MUST be available to every
  supported harness through provider-neutral contracts.
- **PK-PROD-004:** installation, upgrade, verification, and removal MUST
  preserve project-owned changes or stop with an explicit conflict.
- **PK-PROD-005:** shipped content and runtime behavior MUST be versioned,
  locally testable, and independently verifiable from release artifacts.
- **PK-PROD-006:** processkit MUST support one repository as one concern while
  allowing explicit references and handoffs between independently owned
  repositories.
- **PK-PROD-017:** one repository MUST have at most one active processkit
  installation and one authoritative context root; nested Git repositories or
  submodules are independent roots and MUST NOT be absorbed implicitly.
- **PK-PROD-018:** a processkit root MUST support multiple human and AI
  participants and MUST NOT imply one repository or one processkit
  installation per agent.
- **PK-PROD-019:** every reference runtime MUST operate locally against one
  selected working copy. A long-lived local MCP daemon MAY serve several
  authorized clients for that working copy, but it is not shared repository
  authority or a second project database. Git synchronization and review
  transfer accepted state between working copies.
- **PK-PROD-007:** project state MUST remain authoritative when indexes,
  caches, generated references, or harness projections are absent.
- **PK-PROD-008:** v1 MUST provide a small mandatory repository-memory kernel.
  Broader organizational, scaling-framework, communication, location,
  planning, and evaluation concepts MUST be supplied through optional
  first-party packages rather than universal core semantics.
- **PK-PROD-009:** processkit MUST assemble bounded, attributable agent context
  from canonical entities and verified derived indexes without treating model
  conversation history as authoritative project memory.
- **PK-PROD-016:** skills and MCP servers MUST be managed as versioned,
  inspectable capabilities with ownership, discovery, configuration,
  compatibility, and verification contracts.
- **PK-PROD-029:** MCP, CLI, and future adapters MUST call one interface-
  neutral application core and preserve equivalent domain semantics wherever
  capabilities overlap.
- **PK-PROD-030:** agents MUST be able to discover typed applicability,
  authority requirements, permitted next actions, and recovery state without
  parsing console prose or treating entity content as executable policy.

## Non-goals

- **PK-PROD-010:** processkit MUST NOT run language models, own an agent loop,
  schedule autonomous teams, or replace a harness or orchestrator.
- **PK-PROD-011:** processkit MUST NOT replace Git hosting, issue trackers,
  code review, CI systems, chat, secrets managers, or artifact stores.
- **PK-PROD-012:** processkit MUST NOT require a central database, cloud
  account, projectious.work service, aibox, or a specific AI provider.
- **PK-PROD-013:** processkit MUST NOT encode a single scaling framework,
  organizational method, or model vendor as its universal ontology.
- **PK-PROD-014:** processkit MUST NOT make every Markdown file an entity or
  claim that unstructured documentation has lifecycle semantics.
- **PK-PROD-015:** processkit v1 MUST NOT provide portfolio-wide distributed
  transactions or pretend cross-repository operations are atomic.
- **PK-PROD-028:** processkit MUST NOT create branches, commits, pull
  requests, issues, discussions, merges, pushes, or fetches as implicit side
  effects. Humans, agents, harnesses, and forge adapters own those workflows.

## Product boundary

processkit owns:

- contracts for process entities, relations, transitions, and events;
- reusable process content and its packaging metadata;
- local installation and reconciliation of processkit-owned files;
- validated CLI and MCP operations;
- derived local indexes and generated harness projections;
- context discovery, retrieval, ranking, and bounded context assembly;
- local full-text and embedding/vector projections derived from canonical
  repository content;
- versioned skills and MCP server capability manifests, installation, and
  verification;
- compatibility, migration, verification, and diagnostic behavior.

The consuming repository owns:

- its entities and their meaning within the declared contracts;
- local policies, extensions, accepted overrides, and private content;
- Git history, review, retention, backup, and publication;
- authorization to mutate the repository;
- credentials and external-system integrations.

The harness or orchestrator owns agent identity bootstrap, model execution,
prompts outside shipped skills, conversation and runtime memory, heartbeat,
task scheduling, agent isolation, cost control, and cross-agent coordination.
Company modelling, teams-of-teams orchestration, simulation, message delivery,
and portfolio views belong to products such as Kaits, which consume
processkit contracts without becoming repository authority.

## Required user journeys

- **PK-PROD-020:** a new user MUST be able to install a pinned release into a
  disposable Git repository, verify it, start MCP, and create/read/transition
  a WorkItem without aibox.
- **PK-PROD-021:** an existing project MUST be able to preview an update,
  inspect every planned file action and conflict, apply it atomically within
  documented limits, and verify the result.
- **PK-PROD-022:** an agent MUST be able to discover an applicable skill,
  query the relevant entities, perform an allowed mutation, and observe the
  resulting event without raw filesystem discovery.
- **PK-PROD-023:** a maintainer MUST be able to rebuild all derived indexes
  and projections from canonical files.
- **PK-PROD-024:** a project with local extensions MUST be able to distinguish
  upstream-owned, locally modified, project-owned, and generated paths.
- **PK-PROD-025:** a failed or interrupted mutation MUST leave either the
  previous valid state or explicit recovery evidence; it MUST NOT claim
  transactionality beyond what was achieved.
- **PK-PROD-026:** a project MUST be able to export a sanitized, bounded
  handoff bundle and record an external reference without surrendering local
  ownership or exposing private context by default.
- **PK-PROD-027:** a user MUST be able to validate, create or compose, query,
  relate, and inspect every concept installed by the selected package set
  through its declared schema and interfaces.
- **PK-PROD-031:** processkit MUST reuse the smallest best-fitting subset of
  established semantic terms where doing so prevents duplicate design. V1
  MUST NOT require a general RDF store, ontology reasoner, linked-data export,
  or support for a broad external ontology catalog.
