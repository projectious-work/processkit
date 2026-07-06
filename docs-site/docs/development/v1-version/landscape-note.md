---
title: Landscape Note
description: Adjacent projects and concepts processkit should learn from.
---

# Landscape Note

## Positioning

processkit v1.0 is not trying to replace agent runtimes, memory
databases, coding agents, or data catalogs. It should be the process
substrate those systems can use.

Its strongest position is:

> provider-neutral process memory and governance for agentic software
> projects.

## Adjacent Areas

### OKF

[OKF](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)
validates markdown plus YAML frontmatter as an agent-readable exchange
format. processkit should support OKF import/export, generated indexes,
and permissive boundary consumption.

processkit should not copy OKF's path IDs, untyped links, or prose-only
logs as canonical semantics.

### Local Markdown Memory

Projects such as
[Basic Memory](https://github.com/basicmachines-co/basic-memory) and LLM
wiki patterns show that agents and humans benefit from simple, local,
readable markdown knowledge.

processkit should learn from their ergonomics: backlinks, readable
files, simple search, and low-friction MCP access.

processkit should keep stronger lifecycle and relation semantics.

### Agent Runtimes

[LangGraph](https://github.com/langchain-ai/langgraph),
[Google ADK](https://adk.dev/),
[OpenAI Agents SDK](https://openai.github.io/openai-agents-python/), and
[Microsoft Agent Framework](https://github.com/microsoft/agent-framework)
provide orchestration, tools, handoffs, sessions, tracing, and
human-in-the-loop behavior.

processkit should integrate with them through stable MCP tools and
runtime-neutral examples. It should not own the agent loop.

### Memory Layers

[Letta](https://github.com/letta-ai/letta) and
[Mem0](https://github.com/mem0ai/mem0) show the importance of long-term
memory, retrieval, summarization, and consolidation.

processkit should distinguish fleeting notes, permanent artifacts,
decisions, logs, and team-member memory. Promotion and consolidation
should be explicit process actions.

### Metadata Governance

[DataHub](https://github.com/datahub-project/datahub),
[OpenMetadata](https://github.com/open-metadata/OpenMetadata),
[Unity Catalog](https://github.com/unitycatalog/unitycatalog), and
[OpenLineage](https://github.com/OpenLineage/OpenLineage) show the value
of typed metadata, lineage, ownership, governance, and quality checks.

processkit should make ownership, provenance, lineage, and quality
queryable without turning into a data catalog.

### Coding Agents

[OpenHands](https://github.com/OpenHands/OpenHands),
[SWE-agent](https://github.com/SWE-agent/SWE-agent),
[GitHub Copilot Agent](https://github.com/features/copilot), and
[Aider](https://github.com/Aider-AI/aider) need durable task context,
acceptance criteria, related decisions, test evidence, and review
history.

processkit should make those inputs easy to retrieve and those outputs
easy to record.

## Concepts To Adopt

- boundary compatibility with OKF
- local-first markdown ergonomics
- explicit handoffs and approvals
- guardrails as auditable Gates
- traces and summaries as structured evidence
- memory promotion workflows
- typed provenance and lineage
- acceptance criteria as queryable fields
- runtime-neutral integration examples

## Concepts To Avoid

- replacing agent runtimes
- replacing data catalogs
- treating vector memory as the source of truth
- reducing typed relations to prose links
- making path names the canonical identity model
