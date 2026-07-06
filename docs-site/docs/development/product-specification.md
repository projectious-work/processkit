---
title: Product Specification
description: Product definition for processkit v1.0.
---

# Product Specification

## Purpose

processkit v1.0 provides a durable process substrate for agentic
software projects. It gives humans and AI agents a shared project memory
with typed work, decisions, discussions, artifacts, roles, skills,
gates, bindings, and event history.

The product is not an agent runtime. It is the process and memory layer
that agent runtimes, coding agents, and human maintainers can use to
coordinate work safely.

## Primary Users

- Project owners who want inspectable, durable AI-assisted project
  memory.
- Maintainers who need decisions, work, artifacts, and migrations to be
  traceable.
- AI coding agents that need reliable task context and write-safe MCP
  tools.
- Agent runtime integrators that need a provider-neutral process layer.

## Problems To Solve

- Agent sessions lose project context across turns and tools.
- Important decisions and rationale are buried in chat.
- Work state, review state, and acceptance criteria are not consistently
  queryable.
- Multi-agent teams need roles, skills, handoffs, gates, and logs.
- Markdown knowledge is readable but often lacks lifecycle semantics.
- Service-owned metadata systems are less portable than git-backed
  files.

## Product Goals

- Keep project memory file-backed, git-native, and human-inspectable.
- Make process writes happen through validated MCP tools.
- Support typed entities, state machines, and relation queries.
- Implement the RFC's 89-concept T/P/D/C ontology target.
- Preserve auditability through structured event logs.
- Support provider-neutral roles, team members, model routing, and
  skills.
- Export and ingest OKF bundles without weakening canonical semantics.
- Integrate with external agent runtimes instead of replacing them.

## Non-Goals

- Build a general agent runtime.
- Build a vector database.
- Build a general data catalog.
- Make OKF the canonical internal model.
- Replace GitHub, issue trackers, CI, or code review systems.
- Optimize for synthetic coding-agent benchmarks as the product goal.

## Core Workflows

1. Capture work as typed WorkItems with acceptance criteria.
2. Record decisions with context, alternatives, rationale, and
   consequences.
3. Attach artifacts and supporting analysis to work and decisions.
4. Route tasks to roles, team members, skills, and model classes.
5. Apply gates for approval, policy, evaluation, and release checks.
6. Query by interface rather than forcing agents to guess concrete
   entity kinds.
7. Preserve process evidence in structured LogEntries.
8. Export selected knowledge as OKF for open exchange.

## Success Criteria

- A maintainer can understand project state from files and docs without
  replaying chat history.
- An agent can create, transition, and query process entities through MCP
  tools without hand-editing canonical context files.
- A real project cycle can run through the v1.0 alpha model.
- Automated fixture tests cover schema generation, MCP contracts,
  indexing, migrations, and pk-doctor before manual dogfood begins.
- OKF export produces a conformant bundle for public consumption.
- Existing v0.x evidence can migrate or be explicitly preserved.
