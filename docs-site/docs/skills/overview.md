---
sidebar_position: 1
title: "Overview"
---

# Skills — Overview

A **skill** in processkit is a directory containing agent instructions,
examples, assets, and optionally a Python MCP server. Skills are how processkit
gives agents domain-specific intelligence — not just instructions, but the
conventions, gotchas, and decision rules of a domain expert.

## Skill package layout

```
src/skills/<skill-name>/
  SKILL.md              ← agent instructions (Intro / Overview / Gotchas / Full reference)
  examples/             ← example outputs
  assets/               ← templates, reference data, reusable artifacts
  references/           ← optional deep-dive material (keeps SKILL.md under 5 000 words)
  scripts/              ← optional helper scripts
  mcp/                  ← optional Python MCP server
```

## The four-section structure

Every `SKILL.md` is organized so agents can stop reading as soon as they
have enough context:

| Section            | Content                                                                |
|--------------------|------------------------------------------------------------------------|
| **Intro**          | 1–3 sentences — enough to decide "is this skill relevant?"             |
| **Overview**       | Key workflows and common operations — enough to act on typical cases   |
| **Gotchas**        | 7 agent-specific failure modes — where agents most often go wrong      |
| **Full reference** | Edge cases, field-by-field specs, troubleshooting                      |

The Gotchas section is the highest-signal content: 7 provider-neutral failure
modes, each with a bold title, the specific failure pattern, and the specific
countermeasure.

## Frontmatter

Skills follow the [Anthropic Agent Skills spec](https://anthropic.com/). Each
`SKILL.md` opens with YAML frontmatter:

```yaml
---
name: workitem-management
description: |
  Creates, transitions, and queries WorkItems — the task-tracking primitive
  in processkit. Use when managing backlog items, updating work item state,
  or querying items by status, owner, or priority.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-workitem-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 2
    uses:
      - skill: event-log
        purpose: "records state transitions as auditable log entries"
    provides:
      primitives: [WorkItem]
      mcp_tools: [create_workitem, transition_workitem, query_workitems]
      assets: [workitem, workitem-bug, workitem-story]
---
```

See [Skills → Format](./format) for the complete specification.

## v0.18.0 catalog (130+ skills)

| Category | Count | Examples |
|---|---|---|
| Engineering (language, framework, architecture, infra, security) | ~70 | python-best-practices, fastapi-patterns, terraform-basics |
| Process-primitive | ~32 | workitem-management, decision-record, artifact-management, task-router, skill-gate |
| Document / asset creation | 4 | docx-authoring, pptx-authoring, xlsx-modeling, pdf-workflow |
| Meta-cognitive | 4 | research-with-confidence, devils-advocate, board-of-advisors, status-briefing |
| Role-specific | 4 | prd-writing, user-research, data-storytelling, legal-review |
| Data, design, AI/ML | ~23 | data-science, excalidraw, rag-engineering, llm-evaluation |

All skills are **Pattern 5 (domain-specific intelligence)**: they encode
what an expert in the domain carries in their head — conventions, gotchas,
and decision rules — so the agent reasons like a specialist, not a generalist.

## Browsing the skill catalog

Three ways to find skills:

**On GitHub** — Browse the source tree directly:
[`src/context/skills/`](https://github.com/projectious-work/processkit/tree/main/src/context/skills/)
is organized into 7 category subdirectories (`processkit/`,
`engineering/`, `devops/`, `data-ai/`, `product/`, `documents/`,
`design/`). Each skill directory contains a `SKILL.md` with the full
description, gotchas, and reference.

**From a release tarball** — Every GitHub release includes a
`processkit-vX.Y.Z.tar.gz` with all `src/` content. Download and unpack
to inspect or diff skills without cloning the full repo. Release assets
live at:
[github.com/projectious-work/processkit/releases](https://github.com/projectious-work/processkit/releases)

**In a project using aibox** — After `aibox init`, skills are installed
under `context/skills/processkit/<skill-name>/SKILL.md` in the project
root. The `task-router` MCP server's `route_task(task_description)` call
returns the matching skill, any project-specific process override, and the
recommended MCP tool in a single call. `skill-finder` (`find_skill`,
`list_skills`) is called internally by `task-router` and remains available
directly. The index-management MCP server's `search_entities` tool can
query skill metadata from the SQLite index.

## Where to go next

- [Format](./format) — the full skill package format specification
- [Hierarchy](./hierarchy) — the layered skill graph (`uses:` relationships)
- [Catalog → Process](./catalog/process) — start browsing skills by category
