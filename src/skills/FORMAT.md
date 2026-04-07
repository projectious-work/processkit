---
apiVersion: processkit.projectious.work/v1
kind: Documentation
metadata:
  id: SKILL-FORMAT
  title: "Skill Package Format Specification"
  version: "1.0.0"
spec:
  level: 3
---

# Skill Package Format

## Level 1 — What and why

A **skill** in processkit is a directory, not a single file. It bundles
instructions (SKILL.md), examples, entity templates, and optionally a Python
MCP server into one versioned, composable package. Skills are the primary way
processkit gives agents new capabilities.

## Level 2 — Package layout and frontmatter

### Directory layout

```
src/skills/<skill-name>/
  SKILL.md              ← required — three-level agent instructions
  INDEX.md              ← optional — human-readable overview (Level 0)
  examples/             ← recommended — example outputs (code, entity files, dialog)
    <example>.md
  templates/            ← recommended — YAML entity scaffolds used by this skill
    <entity>.yaml
  references/           ← optional — deep-dive reference material
    <topic>.md
  mcp/                  ← optional — Python MCP server for mechanical tools
    server.py           ← PEP 723 inline deps, STDIO transport, official SDK
    mcp-config.json     ← config fragment merged into consumer's mcp config
    README.md           ← what tools/resources the server provides
```

`<skill-name>` is a kebab-case identifier unique across processkit (and any
community skill packages a project installs).

### SKILL.md frontmatter

Every `SKILL.md` starts with YAML frontmatter:

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-<skill-name>
  name: <skill-name>
  version: "1.0.0"
  created: <iso8601>
spec:
  description: "One-sentence description of what this skill does."
  layer: 2                             # 0..4 — see hierarchy below
  category: process                    # process | language | framework | infrastructure | ...
  uses: [event-log, actor-profile]     # skills this skill depends on (strictly lower layer)
  provides:                            # what an agent gets by activating this skill
    primitives: [WorkItem]             # primitive kinds this skill manages
    mcp_tools: [create_workitem, transition_workitem, query_workitems]
  when_to_use: "Use this skill when the user asks to create, update, or query work items."
---

# <Skill Title>

## Level 1 — Intro (1-3 sentences)

Brief description of the skill's purpose. Just enough for the agent to decide
whether this skill is relevant to the current request.

## Level 2 — Overview

Key concepts, workflows, and the most common operations. Enough for the agent
to act in typical cases without consulting Level 3 or the reference material.

## Level 3 — Full reference

Edge cases, complete field specs, rare workflows, error modes. This section
can be long; the agent only reads it when Level 2 doesn't answer the question.
```

### Frontmatter fields

| Field                 | Required | Purpose                                                  |
|-----------------------|----------|----------------------------------------------------------|
| `apiVersion`          | yes      | Always `processkit.projectious.work/v1` at v0.x.         |
| `kind`                | yes      | Always `Skill`.                                          |
| `metadata.id`         | yes      | `SKILL-<skill-name>`.                                    |
| `metadata.name`       | yes      | Kebab-case name — must match directory name.             |
| `metadata.version`    | yes      | Semver. Independent of processkit's release version.     |
| `metadata.created`    | yes      | ISO 8601 UTC.                                            |
| `spec.description`    | yes      | One-sentence summary. Shown in skill listings.           |
| `spec.layer`          | yes      | Integer 0–4. See hierarchy below.                        |
| `spec.category`       | yes      | One of the registered categories. See below.             |
| `spec.uses`           | no       | List of skills this depends on. Strictly lower layer.    |
| `spec.provides`       | no       | What the agent gains: primitive kinds, MCP tools, etc.   |
| `spec.when_to_use`    | recommended | Trigger description — helps agent routing.            |
| `spec.replaces`       | no       | For customized community forks: ID of the skill this overrides. |

### Skill hierarchy

Skills reference lower-layer skills via `uses:`. The graph is a DAG; cycles are
validation errors.

| Layer | Role                      | Examples                                                       |
|-------|---------------------------|----------------------------------------------------------------|
| 0     | Foundation                | event-log                                                      |
| 1     | Primitive management      | role-management, actor-profile                                 |
| 2     | Core entity management    | workitem-management, decision-record, scope-management         |
| 3     | Process orchestration     | process-management, gate-management, schedule-management       |
| 4     | Cross-cutting concerns    | discussion-management, metrics-management                      |

Technical and language skills (e.g. `python-best-practices`, `fastapi-patterns`)
do not fit this hierarchy — they are category `language`, `framework`, etc.,
with `layer: null`.

### Categories

The category field groups skills in the docs-site and in `aibox skill list`:

`process`, `language`, `framework`, `infrastructure`, `architecture`,
`design`, `data`, `ai`, `api`, `security`, `observability`, `database`,
`performance`, `meta`.

## Level 3 — Full reference

### The three-level principle in SKILL.md

Agents read skills top-down and stop as soon as they have enough context.
Structure each SKILL.md so that:

- **Level 1** answers "should I use this skill at all?" — 1 to 3 sentences.
- **Level 2** answers "how do I do the common thing?" — key workflows, typical
  invocations, default behavior. Roughly 1–3 screens.
- **Level 3** answers "what about the edge case?" — full field-by-field
  reference, rare transitions, interop with other skills, troubleshooting.

Level 3 may be further subdivided (e.g. a `references/` directory for
deep-dive topics). The index MCP server (Phase 3) exposes level-aware queries
so agents can fetch just the level they need.

### The `provides` block

`spec.provides` is a promise to consumers. It lists:

```yaml
provides:
  primitives:           # primitive kinds this skill creates/manages
    - WorkItem
  mcp_tools:            # tool names exposed by the MCP server (if any)
    - create_workitem
    - transition_workitem
    - query_workitems
  templates:            # entity template names shipped in templates/
    - workitem
    - workitem-bug
    - workitem-story
  processes:            # process names this skill implements (if any)
    - backlog-grooming
```

A consumer's `aibox lint` cross-checks `provides.primitives` against the
`kind` values in the directory's `templates/`, and `provides.mcp_tools`
against the server's `list_tools()` response.

### examples/

Each example is a Markdown file demonstrating a complete good output for a
realistic task. Examples are NOT tests — they are patterns. The skill points
the agent at the nearest example when Level 2 gives a hint like "see the
create-feature example for the full flow."

Naming convention: `<action>-<subject>.md` — e.g. `create-feature.md`,
`transition-to-review.md`, `link-related-decisions.md`.

### templates/

Each template is a complete YAML frontmatter entity (no body) that the skill
(or its MCP server) uses as a scaffold for new entities. Templates should
include sensible defaults and leave `TODO` markers where the agent must fill
in context-specific values.

```yaml
# templates/workitem.yaml
---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-TODO           # MCP server replaces with generated ID
  created: TODO           # MCP server replaces with current timestamp
spec:
  title: TODO             # agent fills in
  state: backlog
  type: task
  priority: medium
---
```

### mcp/

When a skill ships an MCP server:

- `server.py` uses the official Python MCP SDK via PEP 723 inline deps:
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
- `mcp-config.json` is the fragment merged into the consumer's mcp config:
  ```json
  {
    "mcpServers": {
      "<skill-name>": {
        "command": "uv",
        "args": ["run", "context/skills/<skill-name>/mcp/server.py"]
      }
    }
  }
  ```
- `README.md` documents: tools provided, resources exposed, required
  environment, known limitations.

### Versioning

`metadata.version` is per-skill semver, independent of processkit's overall
release version. A skill's version bumps when its behavior or interface
changes. The processkit release tag (e.g. `v0.2.0`) is a coordinated snapshot
of all skill versions at a point in time.

### Overriding skills in community packages

A community skill package (installed via `aibox process install <git-url>`)
can override a processkit-shipped skill by setting `spec.replaces: <skill-name>`.
The consumer project sees the community skill at `<skill-name>`; the original
is shadowed. This is the extension mechanism for forking or customizing
opinionated defaults without monkey-patching.
