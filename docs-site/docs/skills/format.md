---
sidebar_position: 2
title: "Skill Package Format"
---

# Skill Package Format

This page summarizes the skill package format. The authoritative source is
[`src/skills/FORMAT.md`](https://github.com/projectious-work/processkit/blob/main/src/skills/FORMAT.md)
in the processkit repo.

## Directory layout

```
src/skills/<skill-name>/
  SKILL.md              ← required — three-level agent instructions
  INDEX.md              ← optional — human-readable overview
  examples/             ← recommended — example outputs
  templates/            ← recommended — YAML frontmatter entity scaffolds
  references/           ← optional — deep-dive reference material
  mcp/                  ← optional — Python MCP server
    server.py
    mcp-config.json
    README.md
```

## Required frontmatter fields

| Field                 | Purpose                                                   |
|-----------------------|-----------------------------------------------------------|
| `apiVersion`          | Always `processkit.projectious.work/v1` at v0.x.          |
| `kind`                | Always `Skill`.                                           |
| `metadata.id`         | `SKILL-<skill-name>`                                      |
| `metadata.name`       | Kebab-case; matches directory name                        |
| `metadata.version`    | Semver, independent of processkit release                 |
| `metadata.created`    | ISO 8601 UTC                                              |
| `spec.description`    | One-sentence summary (shown in listings)                  |
| `spec.category`       | One of the registered categories                          |
| `spec.layer`          | Integer 0–4, or `null` for non-process skills             |

## Optional fields

| Field                 | Purpose                                                        |
|-----------------------|----------------------------------------------------------------|
| `spec.uses`           | Skills this depends on (strictly lower layer for process skills) |
| `spec.provides`       | What the agent gains: primitive kinds, MCP tools, templates    |
| `spec.when_to_use`    | Trigger description for routing                                |
| `spec.replaces`       | ID of a skill this one overrides (for community forks)         |

## Categories

`process`, `language`, `framework`, `infrastructure`, `architecture`,
`design`, `data`, `ai`, `api`, `security`, `observability`, `database`,
`performance`, `meta`.

## The `provides` block

A promise to consumers — what an agent gains by activating this skill:

```yaml
provides:
  primitives: [WorkItem]
  mcp_tools: [create_workitem, transition_workitem, query_workitems]
  templates: [workitem, workitem-bug, workitem-story]
  processes: [backlog-grooming]
```

`aibox lint` cross-checks these against the actual files shipped in the skill.

## MCP server conventions (v0.3.0+)

Skills ship Python MCP servers as standalone scripts with PEP 723 inline
dependencies:

```python
#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp[cli]>=1.0"]
# ///
from mcp.server.fastmcp import FastMCP
server = FastMCP("<skill-name>")
...
if __name__ == "__main__":
    server.run(transport="stdio")
```

Consumers need only Python ≥ 3.10 and `uv` — both already present in aibox
containers.
