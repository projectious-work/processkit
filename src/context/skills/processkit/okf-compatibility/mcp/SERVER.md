# OKF Compatibility MCP Server

| Tool | Purpose |
|---|---|
| `export_okf_bundle` | Project canonical entities into a new OKF v0.1 bundle |
| `validate_okf_bundle` | Validate frontmatter and internal Markdown links |

The exporter is a boundary adapter. Canonical processkit state is never read
back from the generated bundle.
