---
sidebar_position: 28
title: "Process"
---

# Process

A declarative workflow definition — a sequence of steps, the roles
involved, the gates that must pass, and the definition of done.
processkit defines processes; agents and humans execute them.

| | |
|---|---|
| **ID prefix** | `PROC` |
| **State machine** | none |
| **MCP server** | none |
| **Skill** | `process-management` (Layer 3) |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `name` | string | Kebab-case identifier |
| `description` | string | One-sentence summary |
| `steps` | object[] | Ordered list of steps (see below) |
| `definition_of_done` | string | Acceptance criterion for the whole process |

### Optional

| Field | Type | Description |
|---|---|---|
| `triggers` | string[] | Event types that kick off the process |
| `roles` | string[] | Role names involved |
| `parallel` | boolean | `true` = steps run in parallel (default: `false`) |
| `retryable` | boolean | `true` = process can re-run on failure (default: `true`) |

### Step fields

| Field | Type | Description |
|---|---|---|
| `name` | string | Required — step identifier |
| `role` | string | Role responsible for this step |
| `description` | string | What the step does |
| `uses_skill` | string | Skill ID the agent invokes |
| `inputs` | string[] | Inputs expected at this step |
| `outputs` | string[] | Outputs produced |
| `gates` | `GATE-*[]` | Gates that must pass before proceeding |
| `on_failure` | enum | `halt` · `retry` · `skip` · `escalate` |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Process
metadata:
  id: PROC-20260411_0918-SureElm-code-review
  created: '2026-04-11T09:18:00Z'
spec:
  name: code-review
  description: Review a pull request before merge.
  triggers: [pr.opened, pr.review-requested]
  roles: [developer, reviewer]
  steps:
    - name: author-self-check
      role: developer
      uses_skill: code-review
    - name: peer-review
      role: reviewer
      uses_skill: code-review
      gates: [GATE-no-blocking-comments]
    - name: merge
      role: developer
      gates: [GATE-ci-passed, GATE-code-review-passed]
  definition_of_done: PR merged with approval and CI green.
---
```

## Notes

- processkit does **not execute** processes. The agent (or human) walks
  the steps and logs progress via `log_event`.
- Gate references in steps are pointers to Gate entities — create the
  Gate first, then reference its ID.
- Formal process definitions (`bug-fix`, `code-review`,
  `feature-development`, `release`) are planned as shipped YAML files
  in a future release.
