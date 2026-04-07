# Product Requirements Document — processkit

Derived from [aibox DISC-002](https://github.com/projectious-work/aibox/blob/main/context/discussions/DISC-002-aibox-refocus.md). This PRD codifies processkit's scope as the **content layer** of the aibox ecosystem.

## Vision

**processkit is the versioned content layer for AI-assisted work environments.** Where aibox provides the containerized runtime, processkit provides everything that runs inside it: the 18 process primitives, the skills that let agents do useful work, the process templates that structure projects, and the MCP servers that give agents mechanical correctness on top of probabilistic reasoning.

The explicit analogy: `aibox` is to AI work environments as `uv` is to Python environments — it sets up the box. `processkit` is what goes *in* the box.

By splitting content from infrastructure, both sides can evolve at their natural pace: the CLI and container story stabilize, while primitives, skills, and MCP tools iterate rapidly against real-world use.

## Target users

| User                        | What they get from processkit                                                                 |
|-----------------------------|-----------------------------------------------------------------------------------------------|
| **Solo developer**          | A curated set of skills installed into their project, a minimal primitive set, zero ceremony. |
| **Small team**              | Shared process primitives (WorkItem, DecisionRecord, LogEntry) with schema-validated files and a default state machine.                                                           |
| **Team with a methodology** | Composable package tiers — start with `managed`, upgrade to `software` or `product`, override skills as needed.                                                                         |
| **AI agent in the project** | MCP servers for mechanical operations (`create_workitem`, `transition_state`, `query_entities`) alongside markdown instructions for judgment calls.                                    |
| **Skill author**            | A clear, multi-artifact package format (SKILL.md + examples + templates + mcp) and a semver release mechanism (git tags).                                                                        |
| **Community contributor**   | Any GitHub repo can provide a processkit-compatible skill package, installable via `aibox process install <git-url>`.                                                                       |

processkit is explicitly **not** for enterprise governance (RBAC, signed commits, compliance enforcement). See Non-goals.

## Core requirements

### R1 — Entity file format is stable and versioned

Every primitive entity is a Markdown file with YAML frontmatter following the shape:

```yaml
apiVersion: processkit.projectious.work/v1
kind: <Kind>
metadata:
  id: <PREFIX>-<id>
  created: <iso8601>
  updated: <iso8601>
  labels: { ... }
spec:
  ...
```

The format is defined in `src/primitives/FORMAT.md` and enforced structurally by `aibox lint`. Full schema validation happens in a processkit-owned MCP server (not in aibox CLI) — this keeps schema evolution self-contained.

**apiVersion policy:** `processkit.projectious.work/v1` throughout v0.x and v1.x. A breaking change bumps to `v2` and triggers an `aibox migrate` path.

### R2 — 18 primitives as universal building blocks

processkit ships schemas, default state machines, and management skills for the 18 primitives identified in DISC-001 §3 and refined in DISC-002:

WorkItem, LogEntry, DecisionRecord, Artifact, Role, Process, StateMachine, Category, CrossReference, Gate, Metric, Schedule, Scope, Constraint, Context, Discussion, Actor, Binding.

These are framework-agnostic — they appear in every serious process methodology (SAFe, PMBOK, CMMI, Scrum, Kanban). processkit does not impose a methodology on top of them.

**Rule on relationships:** if a relationship has scope, time, or its own attributes → use a `Binding` entity. Otherwise → use a cross-reference field in frontmatter.

### R3 — Skills are multi-artifact packages

A skill is a directory, not a single file:

```
src/skills/<skill-name>/
  SKILL.md              ← three-level instructions (Level 1/2/3)
  examples/             ← example outputs
  templates/            ← YAML frontmatter entity scaffolds
  mcp/                  ← optional Python MCP server (PEP 723 + uv)
    server.py
    mcp-config.json
    README.md
```

Skills declare dependencies via a `uses:` field in their frontmatter. The dependency graph is strictly downward:

```
Layer 0: event-log (foundation)
Layer 1: role-management, actor-profile
Layer 2: workitem-management, decision-record, scope-management
Layer 3: process-management, gate-management, schedule-management
Layer 4: discussion-management, metrics-management
```

### R4 — Three-level instructions

All SKILL.md and FORMAT.md documents follow three levels of detail:

- **Level 1** (1–3 sentences): enough for the agent to decide whether to keep reading.
- **Level 2**: key concepts and workflows — enough to act in common cases.
- **Level 3**: full reference — edge cases, field-by-field specs, examples.

Directories contain an `INDEX.md` (**Level 0**): what lives here and why.

### R5 — MCP servers as mechanical-correctness path

For each foundation skill that benefits from programmatic operations, processkit ships a Python MCP server using the official SDK with PEP 723 inline dependencies. The container requires only Python ≥ 3.10 and `uv` (both already present in aibox images).

MCP servers give agents two paths to the same operation:

- **Probabilistic path**: the agent edits files directly following SKILL.md instructions. Always valid.
- **Mechanical path**: the agent calls an MCP tool (`create_workitem`, `transition_state`, ...) that validates against the schema and state machine. Guaranteed correct.

Both are first-class. MCP is not required.

### R6 — Package tiers for progressive adoption

processkit ships opinionated package tiers bundling skills for common use cases:

| Package   | Intended use                                 |
|-----------|----------------------------------------------|
| minimal   | Lightest footprint, solo work                |
| managed   | Default — small team, structured backlog    |
| software  | Software projects with architecture concern |
| research  | Research/data-driven projects                 |
| product   | Full product development                     |

A consumer selects a tier via `[context] packages = ["<name>"]` in `aibox.toml`. Overrides (`[skills] include/exclude`) allow fine-tuning.

### R7 — Git tags as the release mechanism

processkit releases via semver git tags. `aibox init` consumes a specific tag. This means:

- No custom package registry, no server infrastructure, no runtime dependencies.
- Community skill packages use the same pattern — any GitHub repo with a `package.yaml` and a tag is installable via `aibox process install <git-url>`.
- Version pinning is the interop contract between aibox and processkit. Both sides pin; upgrades are deliberate.

### R8 — Index as a processkit MCP server

The SQLite index (parse frontmatter, build tables, serve queries) lives in a processkit-owned MCP server (`src/skills/index-management/mcp/`). aibox CLI does only structural validation (`apiVersion`, `kind`, `metadata.id` present). This keeps schema knowledge out of the CLI and inside processkit, where it belongs.

### R9 — Dogfooding

processkit is itself developed using aibox. Its `.devcontainer/` and (eventually, once aibox-side consumption logic lands and we close the loop) its `context/` are scaffolded via `aibox init` pinned to a specific aibox version. The dogfooding loop is resolved by version pinning on both sides; see R7. The install layout is provider-neutral — nothing lands under `.claude/`.

### R10 — Documentation site

processkit ships a Docusaurus site (`docs-site/`) published to GitHub Pages. The site is the canonical reference for:

- The entity file format and apiVersion policy
- The 18 primitives and their schemas
- The skill catalog (with filtering by category and layer)
- The MCP tool reference for each skill that ships a server
- Process templates (code-review, release, incident-response, ...)
- Package tier definitions

Documentation currently living in the aibox docs-site that belongs to processkit (context system, skill catalog, process packages) migrates here.

## Non-goals

Explicitly **out of scope** for processkit:

- **Enterprise governance.** No RBAC enforcement, no signed commits, no certificate-based authorization, no verification manifests, no per-file authorization policy. DISC-001 research is preserved in the aibox repo for whatever governance platform eventually needs it.
- **Container infrastructure.** processkit does not define Dockerfiles or container images. That is aibox.
- **CLI surface.** processkit is consumed, not run. There is no `processkit` command.
- **Workflow execution.** processkit defines processes declaratively. Agents and humans execute them. processkit does not include a workflow engine.
- **Deterministic event enforcement.** Per DISC-002, LogEntries are all probabilistic (agent-written). There is no second deterministic event source inside processkit. If an enterprise needs tamper-evident event logs, that is the governance platform's job.
- **Bundled non-MCP tooling.** MCP is the only programmatic tool interface processkit supports. Not REST, not gRPC, not direct imports.

## Success metrics

| Metric                              | Target                                                        |
|-------------------------------------|---------------------------------------------------------------|
| Entity files parse-validate clean   | 100% of shipped entity files lint-pass on every commit        |
| Foundation skills have MCP coverage | 5+ foundation skills ship working MCP servers by v0.3.0       |
| Package tiers exercised             | 5 package tiers defined and covered by end-to-end tests       |
| Skill dependency graph              | 0 cycles in `uses:` graph (validated in Phase 5)              |
| Docs site coverage                  | Every primitive and every shipped skill has a docs page       |
| Consumer time-to-first-entity       | `aibox init` → created first WorkItem in < 2 minutes          |
| Dogfooding                          | processkit's own context/ uses processkit primitives by v0.3.0 |

## Release plan

See [DISC-002 §16 — Implementation Plan](https://github.com/projectious-work/aibox/blob/main/context/discussions/DISC-002-aibox-refocus.md#16-implementation-plan) for the five-phase rollout.

| Tag    | Contents                                                                |
|--------|-------------------------------------------------------------------------|
| v0.1.0 | Foundation — format spec, 3 schemas (WorkItem/LogEntry/DecisionRecord), 2 state machines. **Shipped.** |
| v0.2.0 | Skill migration — 85 aibox skills migrated, 16 new process skills, packages, docs site. |
| v0.3.0 | MCP servers operational — 5 foundation servers + SQLite index.          |
| v1.0.0 | First stable release — all primitives, all MCP servers, full docs.      |
