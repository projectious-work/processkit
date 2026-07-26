---
title: processkit v1.0 Start Assessment
description: Scope and risk assessment for starting the v1.0 redesign.
---

# processkit v1.0 Start Assessment

Analyzed: 2026-07-04

Sources considered:

- `processkit-v1.0-rfc-draft.md`
- [processkit v1.0 RFC Analysis](./processkit-v1-rfc-analysis.md)
- [Concept Mapping Briefing Analysis](./concept-mapping-briefing-analysis.md)
- [OKF Compatibility Analysis](./okf-compatibility-analysis.md)
- Google OKF announcement and v0.1 specification
- External survey of adjacent agent, memory, metadata, and coding-agent
  projects

## Judgement

The v1.0 plan is good enough to start, but not as an unconstrained
9-12 month greenfield rebuild.

Start a `v1.0` branch now, but run it as a narrow alpha first:

- prove a small vertical slice before implementing the full ontology
- keep processkit's canonical semantics stricter than OKF
- position processkit as process memory and governance, not as another
  agent runtime
- integrate with external runtimes instead of rebuilding them
- add OKF import/export as a boundary compatibility feature

The plan's direction is strong. Its main risk is scope, not concept.

## Why Start

The market is converging toward exactly the problems processkit is
trying to solve:

- persistent agent context
- local and git-native knowledge
- markdown / frontmatter agent memory
- MCP tool interoperability
- durable work state
- human review and approval gates
- multi-agent role specialization
- observability, lineage, and auditability

The RFC's core differentiators remain valid:

- schema-backed process entities
- lifecycle-aware WorkItems, Decisions, Discussions, Notes, Artifacts,
  Bindings, Gates, Skills, and Logs
- MCP write paths rather than ad hoc file edits
- typed relations instead of prose-only links
- provider-neutral model and role routing
- interface-aware search and query
- structured event history

No surveyed external project fully covers this combination.

## Why Constrain The Start

The RFC's 89-concept ontology is too large to treat as proven before
implementation. It should be validated by usage.

The first alpha should answer:

- Does the new ontology reduce agent confusion in real work?
- Does `query_by_interface` improve routing and retrieval?
- Can existing v0.x history migrate without losing process evidence?
- Can agents create and transition entities reliably through MCP tools?
- Can humans still inspect and review the files directly?
- Can OKF export/import work without weakening internal semantics?

If those are not proven early, a larger rebuild will produce more schema
surface without enough operational proof.

## Concepts To Learn From

These external concepts should influence v1.0 without replacing
processkit's identity.

### OKF: Boundary Format

Learn:

- minimal markdown + YAML interchange
- permissive consumers
- path-readable bundles
- generated `index.md` for progressive disclosure
- plain markdown links for generic graph consumers

Apply:

- OKF exporter and importer
- extension frontmatter preserving processkit IDs and kinds
- OKF validator mode
- generated OKF bundles for publication and exchange

Do not copy:

- path IDs as canonical IDs
- untyped relations as the only graph model
- prose `log.md` as authoritative event history

### Basic Memory / LLM Wiki: Local-First Memory

Learn:

- agents work well with simple, readable markdown memory
- backlinks and lightweight entity extraction are useful
- user-owned files build trust
- MCP access to memory lowers integration friction

Apply:

- keep canonical files inspectable by humans
- improve indexes, backlinks, and local search ergonomics
- expose memory operations through MCP with clear tool metadata
- make agent write paths safe but still low-friction

Do not copy:

- free-form notes as the only data model
- weak lifecycle semantics

### LangGraph / ADK / Microsoft Agent Framework: Runtime Boundaries

Learn:

- durable execution, pause/resume, and human-in-the-loop workflows are
  now table stakes
- agent runtimes increasingly support state, tools, telemetry, and
  multi-agent orchestration
- framework-specific orchestration changes quickly

Apply:

- make processkit easy for those runtimes to use
- define stable MCP tools for work, decisions, gates, and logs
- model approvals and interrupts as first-class process state
- provide runtime-neutral integration examples

Do not copy:

- agent loop orchestration
- provider-specific runtime assumptions

### OpenAI Agents SDK: Handoffs, Guardrails, Tracing

Learn:

- handoffs need explicit target identity and task shape
- guardrails should be auditable process artifacts
- traces are valuable when debugging agent behavior

Apply:

- connect TeamMember / Role routing to handoff metadata
- model guardrails as Gates and policy Bindings
- map traces or summaries into structured LogEntries or Artifacts

Do not copy:

- SDK-specific session state as canonical project memory

### Letta / Mem0: Memory Layering

Learn:

- long-term memory needs summarization, retrieval, and consolidation
- different memory layers serve different retrieval needs
- graph memory can improve multi-hop questions

Apply:

- separate fleeting notes, permanent artifacts, decisions, logs, and
  team-member memory
- add explicit promotion and consolidation workflows
- support graph-aware retrieval over typed entities and Bindings

Do not copy:

- opaque memory stores as the only source of truth
- personalization-first memory as the center of the project model

### DataHub / OpenMetadata / Unity Catalog: Metadata Governance

Learn:

- catalogs win by combining metadata, lineage, ownership, search,
  quality, and governance
- typed metadata supports automation better than prose alone
- enterprise users expect lineage and ownership to be queryable

Apply:

- make ownership, source, provenance, and lifecycle queryable
- add lineage-style relations where process artifacts derive from one
  another
- expose health and quality checks through pk-doctor
- keep metadata extensible without losing validation

Do not copy:

- data-catalog scope as the core product
- centralized service dependency

### OpenLineage: Faceted Extensibility

Learn:

- a small core model plus extension facets can scale across domains
- lineage events benefit from consistent naming and extensible metadata

Apply:

- consider facet-like schema extension points for v1.0 entities
- keep core fields stable while allowing typed extension payloads
- use event metadata to preserve provenance and causal relationships

Do not copy:

- run/job/dataset as processkit's universal core model

### OpenHands / SWE-agent / Copilot Agent / Aider: Coding-Agent Fit

Learn:

- coding agents need repository maps, task context, plans, tests, and
  review loops
- asynchronous agents need durable project state outside chat
- issue-to-PR agents benefit from clear acceptance criteria

Apply:

- make processkit the context substrate for coding agents
- export concise task briefs with related decisions and artifacts
- model acceptance criteria and verification as queryable fields
- preserve branch, PR, test, and review evidence in structured logs

Do not copy:

- code-editing agent behavior
- benchmark chasing as the project goal

## Immediate Plan Improvements

Before full implementation, amend the v1.0 plan with these additions:

1. Add an OKF compatibility acceptance slice.
2. Add a one-project alpha proving a small ontology subset.
3. Define processkit's runtime boundary explicitly.
4. Add a "not building" list:
   agent runtime, vector database, data catalog, OKF-only wiki.
5. Add provenance and lineage requirements.
6. Add handoff / approval / guardrail mapping to Roles, Gates, and Logs.
7. Add graph/backlink ergonomics for human and agent navigation.
8. Add migration proof for existing v0.x entities.
9. Add examples for LangGraph, ADK, OpenAI Agents SDK, and Microsoft
   Agent Framework as consumers.

## Start Condition

Start once the first alpha slice is defined as a vertical proof:

- 10-15 highest-value concepts only
- generated schemas
- MCP create/read/transition path
- interface query
- OKF export
- migration of a small existing corpus
- one real process cycle driven through the new model

That is enough to learn quickly while preserving the RFC's direction.
