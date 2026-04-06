# skills/

Multi-artifact skill packages. Each skill is a directory containing instructions
(SKILL.md), examples, templates, and optionally a Python MCP server.

**Phase 1 (v0.1.0):** this directory is empty. Skills are migrated in Phase 2.

## Skill package layout

```
<skill-name>/
  SKILL.md              ← three-level instructions (Level 1: 1-3 sentences;
                          Level 2: key workflows; Level 3: full reference)
  examples/             ← example outputs showing what good looks like
  templates/            ← YAML frontmatter templates for entity scaffolding
  mcp/                  ← Python MCP server (optional)
    server.py           ← uses official MCP SDK via PEP 723 inline deps
    mcp-config.json     ← config snippet merged into consumer's mcp.json
    README.md           ← what tools/resources this server provides
```

See the full skill format spec in `skills/FORMAT.md` (added in Phase 2.1).

## Skill hierarchy (Phase 2)

Skills reference lower-layer skills via `uses:` in frontmatter. Strictly downward.

```
Layer 0: event-log (foundation)
Layer 1: role-management, actor-profile
Layer 2: workitem-management, decision-record, scope-management
Layer 3: process-management, gate-management, schedule-management
Layer 4: discussion-management, metrics-management
```
