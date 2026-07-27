# OKF Compatibility MCP Server

| Tool | Purpose |
|---|---|
| `export_okf_bundle` | Project canonical entities into a new OKF v0.1 bundle |
| `import_okf_bundle` | Plan or apply a lossless producer-profile import |
| `validate_okf_bundle` | Validate frontmatter and internal Markdown links |

The exporter is a boundary adapter. Canonical processkit state is never read
back from the generated bundle.
