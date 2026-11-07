# Skill Management MCP Server

| Tool | Purpose |
|---|---|
| `create_skill` | Create a minimal draft Skill package |
| `get_skill` | Read and validate one projected Skill |
| `update_skill` | Update non-lifecycle manifest fields |
| `transition_skill` | Apply a governed Skill state transition |
| `list_skills` | List projected Skill packages |

The server treats `SKILL.md` as canonical storage and indexes a synthetic
`Skill` projection for interface-aware reads.
