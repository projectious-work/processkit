# Product definition

> **Non-normative documentation** (moved from `spec/doc/v1/` in #206).
> The normative contract is the specifications under
> [`spec/`](../../spec/); see [the v1 overview](README.md). Requirements
> that moved into a specification are listed here by ID only.

## Purpose

processkit is a provider-neutral framework for agent context in an
organization. It gives companies, teams, and projects a common ontology in
which to define how they work, lets them author that governance content as
structured, validated files in Git repositories, composes it across a
hierarchy of repositories, and serves it to any AI agent over MCP,
personalized for the caller.

processkit manages context, not memory. It stores what an organization has
decided and defined: standards, process definitions, skills, trusted MCP
servers, decision records, and documents. It does not record what happens
while work is done. Instances such as tickets, events, logs, session
transcripts, and agent memories belong to the harness, the issue tracker, the
code forge, and Git history.

The target is that processkit's MCP server replaces the governance part of
harness instruction files and skill directories. A harness keeps assembling
its system prompt and remains responsible for memory, conversation history,
and code-base context; it obtains organizational rules, processes, skills,
and approved MCP servers from processkit. A project's harness configuration
then needs little more than the processkit MCP server entry.

The ontology is the product's common language, not processkit's private
storage model. A user can describe a process in natural language, for example
ticket handling, and an agent expresses it with ontology concepts such as
WorkItem, StateMachine, Role, Gate, and Binding. processkit validates the
result as a structured process definition, stores it in the governing
repository, and serves it company-wide.

The product answers these questions for a human or an agent:

1. Which standards, processes, skills, and MCP servers apply to me and to
   this task now?
2. Which rules must I follow, and where exactly is each rule defined?
3. How is this process defined: which roles, states, transitions, gates, and
   artifacts does it have?
4. Why does a rule exist, and which decision introduced or changed it?
5. Which level of the organization defines a rule, and which level overrides
   it?

## Content

| Kind | Purpose | Ontology |
|---|---|---|
| `Standard` | rules an organization defines for its work | composition over `Policy` |
| `ProcessSpecification` | a process defined in ontology terms | composition |
| `Skill` | a reusable agent capability | primitive |
| `MCPServer` | a trusted MCP server or gateway entry | refinement of `Service` |
| `DecisionRecord` | why a rule or process exists | composition |
| `Document` | governed Markdown, such as guides and handbooks | composition over `Artifact` |
| `Container`, `Role`, `Binding` | organizational scope and access | primitives |

## Repository roles

- A **governing repository** holds the standards, processes, skills, catalog,
  and decisions of a company, business unit, or team. It is usually served to
  many readers through the shared server.
- A **project repository** inherits governance content from one or more
  governing repositories and may add project-level content. It is usually
  served locally to the agents working in it.
- Governing repositories may inherit from other governing repositories,
  forming a tree of organizational levels.

## Users

- A governance owner defines and maintains a level's standards and processes.
- An author, human or agent, writes and revises governance content from
  published schemas and templates.
- An AI agent asks for the context that applies to its task and receives a
  bounded, attributed, personalized answer.
- An operator runs a shared server and connects it to the organization's
  identity infrastructure.
- A project owner chooses which governing repositories a project inherits
  from and at which pinned versions.

## Goals

- `PK-PROD-001`: normative in
  [`repository-storage@v1`](../../spec/repository-storage/v1/requirements.md).
- **PK-PROD-002:** processkit MUST ship the ontology, schemas, templates,
  validation, composition, and serving. It MUST NOT ship or define any
  organization's governance content.
- `PK-PROD-003`: normative in
  [`ontology@v1`](../../spec/ontology/v1/requirements.md).
- `PK-PROD-004`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).
- `PK-PROD-005`: normative in
  [`cli@v1`](../../spec/cli/v1/requirements.md).
- `PK-PROD-006`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).
- `PK-PROD-007`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).
- `PK-PROD-008`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).
- `PK-PROD-014`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).
- `PK-PROD-009`: normative in
  [`inheritance@v1`](../../spec/inheritance/v1/requirements.md).
- `PK-PROD-010`: normative in
  [`content-kinds@v1`](../../spec/content-kinds/v1/requirements.md).
- `PK-PROD-011`: normative in
  [`access-control@v1`](../../spec/access-control/v1/requirements.md).
- `PK-PROD-012`: normative in
  [`cli@v1`](../../spec/cli/v1/requirements.md).
- **PK-PROD-013:** processkit's own repositories MUST be governed with the
  published ontology and schemas only.

## Non-goals

- `PK-PROD-020`: normative in
  [`repository-storage@v1`](../../spec/repository-storage/v1/requirements.md).
- `PK-PROD-021`: normative in
  [`content-kinds@v1`](../../spec/content-kinds/v1/requirements.md).
- `PK-PROD-022`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).
- `PK-PROD-023`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).
- **PK-PROD-024:** processkit MUST NOT run language models, own an agent
  loop, or replace a harness, issue tracker, code forge, CI system, or
  secrets manager.
- `PK-PROD-025`: normative in
  [`mcp-context-serving@v1`](../../spec/mcp-context-serving/v1/requirements.md).
- `PK-PROD-026`: normative in
  [`inheritance@v1`](../../spec/inheritance/v1/requirements.md).

## Product boundary

| processkit owns | Others own |
|---|---|
| ontology, schemas, templates, validation | the content of an organization's standards and processes |
| composition across governing repositories | Git hosting, review, and merge |
| per-caller context assembly and MCP serving | agent memory, sessions, and conversation history |
| governance context: rules, processes, skills, approved servers | system-prompt assembly and code-base context |
| access decisions for the shared server | identity providers and certificate authorities |
| the trusted MCP server catalog | MCP gateways and the catalogued servers |
| process definitions | process execution, tickets, events, and evidence |
