# roadmap.yaml

## Fields

| Field | Required | Meaning |
|---|---|---|
| `schemaVersion` | yes (top level) | version of this file format |
| `groups[].id`, `groups[].title` | yes | outcome area or release theme |
| `items[].id` | yes | stable, unique; never reused, survives renames and regrouping |
| `items[].title` | yes | short, outcome-oriented name |
| `items[].summary` | yes | user or operator outcome, not a component name |
| `items[].status` | yes | `idea` · `planned` · `in_progress` · `done` · `shipped` · `cancelled` |
| `items[].kind` | no | `feature` (default) or `phase` for an ordered delivery phase |
| `items[].target` | no | release, milestone, or date — only if it will be maintained |
| `items[].dependencies` | no | IDs of prerequisite items |
| `items[].issues` | no | ticket references |
| `items[].decisions` | no | ADR references |
| `items[].devNote` | when non-trivial and `done` or `shipped` | path under `dev-notes/` |
| `items[].release` | when `shipped` | release version |
| `items[].rationale` | when `cancelled` | why, or a decision reference |

Projects may add fields; they never redefine these fields or statuses.

## Example

```yaml
schemaVersion: 1
groups:
  - id: onboarding
    title: First-run experience
    items:
      - id: RM-12
        title: Guided first upload
        summary: New users upload and classify their first document without help.
        status: shipped
        release: 2.4.0
        issues: [PROJ-101]
        devNote: dev-notes/RM-12-guided-first-upload.md
      - id: RM-13
        title: Bulk import
        summary: Users import a whole folder in one step.
        status: in_progress
        dependencies: [RM-12]
        target: 2.6.0
      - id: RM-20
        title: Offline mode
        summary: Users keep working without a connection.
        status: idea
```
