# packages/

Package definitions — bundles of skills, processes, and primitives activated
together. Users pick a package in their `aibox.toml` via
`[context] packages = ["<name>"]`.

**Phase 1 (v0.1.0):** this directory is empty. Package definitions land in Phase 2.6.

## Planned packages

| Package   | Intended use                                | Included                                    |
|-----------|---------------------------------------------|---------------------------------------------|
| minimal   | Lightest footprint, solo work               | event-log, workitem-management              |
| managed   | Default — small team, structured backlog    | minimal + decision-record, standups         |
| software  | Software projects with architecture concern | managed + code skills, architecture         |
| research  | Research projects, data-driven work         | managed + research, documentation           |
| product   | Full product development                    | software + product, security, operations    |

Package files are YAML, listing skill names:

```yaml
apiVersion: processkit.projectious.work/v1
kind: Package
metadata:
  name: minimal
spec:
  description: "Lightest footprint — just the foundation primitives"
  includes:
    skills:
      - event-log
      - workitem-management
```
