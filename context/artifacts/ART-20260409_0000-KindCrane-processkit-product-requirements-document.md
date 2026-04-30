---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260409_0000-KindCrane-processkit-product-requirements-document
  created: 2026-04-09 00:00:00+00:00
spec:
  name: processkit Product Requirements Document
  kind: document
  location: context/artifacts/ART-20260409_0000-KindCrane-processkit-product-requirements-document.md
  format: markdown
  version: 0.7.0
  tags:
  - prd
  - product
  - requirements
---

# Product Requirements Document — processkit

**Status:** Approved
**Owner:** projectious-work
**Last updated:** 2026-04-09

---

## Vision

processkit is a versioned library of process primitives, skills, and
MCP servers for AI-assisted work environments.

It is not tied to any specific methodology, tool, or platform. Its
primitives compose into agile workflows, waterfall projects, research
pipelines, non-software business processes, or anything in between.
A team can use processkit to replace a task tracker, a knowledge
base, or a lightweight BPM tool — or build all three from a single,
forkable source of truth.

processkit is the content layer; the runtime environment (container,
harness, toolchain) is a separate concern. processkit is consumable
by any agent harness or human workflow independently of how the
environment is managed.

The library is deliberately forkable: organisations can maintain a
private fork with custom skills and primitives, consumable by any
downstream tool without changes to the consumer. processkit also
aims to be a curated, trusted catalog of refined skills and MCP
servers — providing as complete a foundation as is practical, so
teams spend time on their domain rather than rebuilding common
tooling.

## Problem statement

AI-assisted teams lack a shared, version-controlled layer for process
artifacts — the work items, decisions, logs, and workflows that give
a project its institutional memory. Tools like Jira, Notion, and
Confluence are closed, not agent-readable in structured form, and not
co-located with the code they describe. The result: agents have no
reliable source of truth for process state; teams context-switch
between tools; and process knowledge is siloed from the repository.

processkit addresses this by treating process artifacts as files in
the repository — versioned, diffable, co-located with the code,
readable by any agent or human without special tooling.

## Goals

**Primary goal:** Make it trivially easy for any team to add a
structured, agent-readable process layer to any repository.

**Secondary goals:**
- Provide a curated, trusted catalog of skills that agents can use
  without building from scratch.
- Enable private forks with zero friction — one config line, no
  downstream changes required in consumers.
- Establish processkit as the lowest common denominator for
  AI-assisted process infrastructure across methodologies and
  providers.

**Non-goals:** See the Non-goals section.

## Target users

| User | What they get from processkit |
|---|---|
| **Solo developer** | A curated set of skills, a minimal primitive set, zero ceremony. |
| **Small team** | Shared process primitives (WorkItem, DecisionRecord, LogEntry) with schema-validated files and default state machines. |
| **Team with a methodology** | Composable package tiers — start with `managed`, upgrade to `software` or `product`, override skills as needed. |
| **AI agent in the project** | MCP servers for mechanical operations (`create_workitem`, `transition_state`, `query_entities`) alongside Markdown instructions for judgment calls. |
| **Skill author** | A clear, multi-artifact package format (SKILL.md + assets + mcp) and a semver release mechanism. |
| **Organisation maintaining a private fork** | One config line to switch the upstream source. Full forkability with no changes required in downstream consumers. |
| **Community contributor** | Any GitHub repo can provide a processkit-compatible skill package. |

## Component map

```
┌──────────────────────────────────────────────┐
│                  processkit                   │
│                                              │
│  src/primitives/   19 schemas +              │
│  src/skills/       state machines            │
│  src/processes/    128+ skills               │
│  src/lib/          12 MCP servers            │
│                    shared Python lib         │
│                                              │
│  releases: semver git tags + tarballs        │
└─────────────────┬────────────────────────────┘
                  │ pinned version
         ┌────────┴────────┐
         │ via aibox sync  │  (or manual install)
         └────────┬────────┘
                  │ installs content
                  ▼
┌─────────────────────────────────────────────────┐
│               Consumer project                   │
│                                                 │
│  AGENTS.md               .mcp.json              │
│  aibox.toml / aibox.lock  .claude/commands/     │
│                                                 │
│  context/                                       │
│  ├── skills/      ← installed from processkit   │
│  ├── schemas/                                   │
│  ├── state-machines/                            │
│  ├── workitems/ ┐                               │
│  ├── decisions/ ├── project entities            │
│  └── logs/      ┘                               │
│          ▲                                      │
│          │ read / write entities                │
│  ┌───────┴────────┐     ┌──────────────────┐   │
│  │  MCP servers   │◀───▶│  Agent harness   │   │
│  │ (uv run *.py)  │ MCP │ (Claude Code, …) │   │
│  └────────────────┘     └──────────────────┘   │
└─────────────────────────────────────────────────┘
```

## Core requirements

### R1 — Entity file format is stable and versioned

Every primitive entity is a Markdown file with YAML frontmatter
conforming to the format defined in `src/primitives/FORMAT.md`. The
`apiVersion` field is locked at `processkit.projectious.work/v1`
through v1.x. A breaking change bumps to `v2` and requires a
migration path.

### R2 — 19 primitives as universal building blocks

processkit ships schemas, default state machines, and management
skills for 19 primitives: WorkItem, LogEntry, DecisionRecord,
Artifact, Role, Process, StateMachine, Category, CrossReference,
Gate, Metric, Schedule, Scope, Constraint, Context, Discussion,
Actor, Binding, Migration.

These are framework-agnostic building blocks present in every serious
process methodology. processkit does not impose a methodology on top
of them.

### R3 — Skills are multi-artifact packages

A skill is a directory:

```
src/skills/<skill-name>/
  SKILL.md          ← instructions (Intro/Overview/Gotchas/Full ref)
  assets/           ← YAML scaffolds, reference docs, examples
  mcp/              ← optional Python MCP server (PEP 723 + uv)
    server.py
    mcp-config.json
    SERVER.md
  commands/         ← optional provider-specific command adapters
```

Skills declare dependencies via `metadata.processkit.uses` in their
frontmatter. The dependency graph is strictly downward across five
layers (0–4).

### R4 — Skills conform to the processkit skill format

Every skill package conforms to the
[Agent Skills standard](https://agentskills.io/specification) and
to the processkit-specific extensions defined in
`src/skills/FORMAT.md`. This covers: frontmatter fields (`name`,
`description`, `metadata.processkit.*`), four required body sections
in order (Intro, Overview, Gotchas, Full reference), the three-level
depth convention within those sections, command adapter hygiene when
commands are declared, and MCP tool annotation requirements when an
MCP server is shipped. The format is versioned alongside the library.

### R5 — MCP servers as the mechanical-correctness path

For each primitive that benefits from programmatic operations,
processkit ships a Python MCP server using PEP 723 inline
dependencies (requires only Python ≥ 3.10 and `uv`). MCP servers
give agents two paths to the same operation:

- **Probabilistic:** the agent edits files directly following
  SKILL.md. Always valid.
- **Mechanical:** the agent calls an MCP tool that validates against
  the schema and state machine. Guaranteed correct.

Both are first-class. MCP is not required.

### R6 — Package tiers for progressive adoption

| Package | Intended use |
|---|---|
| minimal | Lightest footprint, solo work |
| managed | Default — small team, structured backlog |
| software | Software projects with architecture concern |
| research | Research / data-driven projects |
| product | Full product development |

### R7 — Git tags and release tarballs as the release mechanism

processkit releases via semver git tags. Each release produces a
reproducible tarball (`dist/processkit-<version>.tar.gz`) with a
sha256 sidecar, uploaded as a GitHub release asset. Consumers pin a
specific tag and download the tarball via its sha256-verified URL.
No custom registry, no server infrastructure, no runtime
dependencies beyond the repo.

### R8 — Index as a processkit MCP server

The SQLite index lives in a processkit-owned MCP server
(`index-management`). The runtime environment does only structural
validation (apiVersion, kind, metadata.id present). Schema knowledge
stays inside processkit, where it belongs.

### R9 — Provider independence

processkit is provider-independent at every layer. The canonical
agent entry point is `AGENTS.md` (open standard), not any
provider-specific file. Skills, schemas, state machines, and
processes install to provider-neutral paths (`context/skills/`,
`context/schemas/`, etc.). Provider-specific adapters (e.g. command
files for Claude Code) are generated at install time from
provider-neutral declarations in SKILL.md frontmatter and live in
provider-specific directories. No processkit-shipped content
references a specific AI provider by name in its canonical form.

### R10 — Documentation site

processkit ships a Docusaurus site (`docs-site/`) as the canonical
reference for the entity format, all 19 primitives, the skill
catalog, MCP tool reference, process templates, and package tiers.

## Non-functional requirements

- **Portability:** All content installs to provider-neutral paths.
  No dependency on a specific AI provider or container system.
- **Offline-first:** MCP servers run locally via `uv run`. No
  external network calls required for core operations.
- **Minimal footprint:** The minimal package tier installs with no
  build step. Dependency resolution handled by `uv` on first run.
- **Backward compatibility:** `apiVersion` is stable within a major
  version. Field additions are non-breaking; removals require a
  version bump.
- **Privacy by default:** Entity files support a `privacy` field
  (`public`, `project-private`, `user-private`). User-private
  content lives under `context/**/private/` and is gitignored.

## Non-goals

- **Enterprise governance.** No RBAC, no signed commits, no
  compliance enforcement.
- **Container infrastructure.** No Dockerfiles or container images.
- **CLI surface.** processkit is consumed, not run.
- **Workflow execution engine.** processkit defines processes
  declaratively. Agents and humans execute them.
- **Deterministic event enforcement.** LogEntries are agent-written
  (probabilistic). No tamper-evident log infrastructure.
- **Non-MCP programmatic interfaces.** Not REST, not gRPC, not
  direct imports.

## Success metrics

| Metric | Status | Target |
|---|---|---|
| Entity files parse-validate clean | Manual today | Release audit skill validates compliance before each tag |
| MCP server coverage | 12 servers shipped | All lifecycle primitives have an MCP server |
| Skill dependency graph: 0 cycles | Not yet validated | Automated via `scripts/validate-skill-dag.py` |
| Docs site: every primitive + skill has a page | Not done | Full coverage at v1.0 |
| Consumer time-to-first-entity | Not measured | First WorkItem in < 2 min from install |
| Dogfooding | ✅ Done | Maintained |
| Package tiers defined and testable | 5 tiers defined | Covered by smoke-test suite |

## Milestones

**Shipped:** v0.1.0–v0.7.0 — entity format, skill migration, MCP
servers, 19 primitives, skill commands, model-recommender.

**v1.0 criteria:**
- Stable `apiVersion` (no breaking changes planned beyond src/
  restructure already in backlog)
- Full docs-site coverage
- All lifecycle primitives have MCP servers
- Automated validation: DAG check + release audit skill
- src/ → target-root mirror restructure complete

No date commitments. Cadence is driven by open workitems.

## Glossary

| Term | Definition |
|---|---|
| **Primitive** | A core entity type with a JSON schema, default state machine, and management skill (e.g. WorkItem, DecisionRecord). |
| **Skill** | A multi-artifact package (SKILL.md + assets + optional MCP server) that instructs an agent how to perform a domain task. |
| **Package tier** | A named bundle of skills for a common use case (minimal, managed, software, research, product). |
| **Layer** | A dependency rank for process-primitive skills (0–4). Skills only depend on equal or lower layers. |
| **Binding** | A time-scoped, attributed relationship between two entities. |
| **Process** | A formal `kind: Process` entity defining a repeatable workflow with steps, roles, gates, and definition-of-done. |
| **MCP server** | A Python script (PEP 723, launched via `uv run`) exposing processkit operations as MCP tools. |

## Dependencies and constraints

**Technical constraints:**
- Python ≥ 3.10 and `uv` required in any environment running MCP
  servers.
- processkit lib is not a published PyPI package — sys.path injected
  via `_find_lib()`.
- Consumers require a git client or tarball download capability to
  install processkit.

**External dependencies:**
- aibox — the primary install vehicle (optional; manual install is
  supported).
- GitHub — release tarball hosting.

## Open questions

| Question | Status |
|---|---|
| src/ → target-root mirror restructure (BACK-grand-lily) | Filed, not started |
| Release audit skill (BACK-tidy-grove) | Filed, not started |
| Docs-site first public deploy | Not yet scheduled |

## Appendix

- `AGENTS.md` — canonical agent entry point and working norms
- `src/primitives/FORMAT.md` — entity file format spec
- `src/skills/FORMAT.md` — skill package format spec
- `src/skills/INDEX.md` — full skill catalog
- `docs-site/` — user-facing documentation (not yet deployed)
- Related decisions: `context/decisions/`
- Open workitems: query via `query_workitems(state="backlog")`
