---
sidebar_position: 1
title: "Overview"
---

# Skills — Overview

A **skill** in processkit is a directory containing agent instructions,
examples, entity templates, and optionally a Python MCP server. Skills are
how processkit teaches agents to do things.

## Skill package layout

```
src/skills/<skill-name>/
  SKILL.md              ← three-level agent instructions
  examples/             ← example outputs
  templates/            ← YAML frontmatter entity scaffolds
  references/           ← optional deep-dive material
  mcp/                  ← optional Python MCP server
```

## The three-level principle

Every `SKILL.md` is organized so agents can stop reading as soon as they
have enough context:

| Level   | Content                                                           |
|---------|-------------------------------------------------------------------|
| Level 1 | 1–3 sentences — enough to decide "is this skill relevant?"        |
| Level 2 | Key workflows and common operations — enough to act on typical cases |
| Level 3 | Full reference: edge cases, field-by-field specs, troubleshooting |

Directories contain an `INDEX.md` (Level 0) describing what lives there.

## Frontmatter

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-workitem-management
  name: workitem-management
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "..."
  category: process
  layer: 2
  uses: [event-log, actor-profile]
  provides:
    primitives: [WorkItem]
    mcp_tools: [create_workitem, transition_workitem, query_workitems]
    templates: [workitem, workitem-bug, workitem-story]
  when_to_use: "..."
---
```

See [Skills → Format](./format) for the complete specification.

## v0.2.0 catalog (101 skills)

- **85 migrated from aibox** — technical, language, framework, architecture,
  infrastructure, database, data, AI, security, observability, performance, design
- **16 new process-primitive skills** — one per primitive kind

The migrated skills have `layer: null` (the hierarchy only applies to
process-primitive skills). They were mechanically migrated in v0.2.0 and
will get an explicit three-level rewrite in a later release.

## Where to go next

- [Format](./format) — the full skill package format specification
- [Hierarchy](./hierarchy) — the layered skill graph (`uses:` relationships)
- [Catalog → Process](./catalog/process) — start browsing skills by category
