---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-scope-management
  name: scope-management
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Manage Scope entities — bounded containers grouping related work (sprint, milestone, project, quarter)."
  category: process
  layer: 2
  uses: [event-log, index-management, id-management]
  provides:
    primitives: [Scope]
    mcp_tools:
      - create_scope
      - get_scope
      - transition_scope
      - list_scopes
    templates: [scope]
  when_to_use: "Use when creating or updating a grouping boundary — sprint, milestone, quarter, project, release — that other entities will reference."
---

# Scope Management

## Level 1 — Intro

A Scope is a named, bounded container that groups related entities — a sprint,
a milestone, a project, a release, a quarter. WorkItems, Processes, and
Bindings reference scopes to say "I apply within this container."

> **MCP server.** This skill ships a self-contained MCP server at
> `mcp/server.py` (PEP 723 script — requires `uv` and Python ≥ 3.10 on
> PATH). Agent harnesses reach its tools by reading a single MCP config
> file at startup, so the contents of `mcp/mcp-config.json` must be merged
> into the harness's MCP config and placed at the harness-specific path
> before this skill is usable. If processkit was installed by an installer,
> that wiring is the installer's responsibility; if processkit was
> installed manually, the project owner must do it by hand.

## Level 2 — Overview

### Kinds of scopes

| kind        | Example                                     |
|-------------|---------------------------------------------|
| `sprint`    | 2-week iteration boundary                   |
| `milestone` | Named delivery target                       |
| `quarter`   | Calendar quarter for OKRs                    |
| `project`   | Long-lived initiative                       |
| `release`   | A specific release version                   |
| `other`     | Custom boundary                             |

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Scope
metadata:
  id: SCOPE-sprint-42
  created: 2026-04-01T00:00:00Z
spec:
  name: "Sprint 42"
  kind: sprint
  state: active
  starts_at: 2026-04-01
  ends_at: 2026-04-14
  description: "Two weeks focused on the lint command and docs-site bootstrap."
  goals:
    - "Ship aibox lint v1"
    - "Publish processkit docs-site"
---
```

### Workflow

1. Pick an ID: `SCOPE-<short-name>` (e.g., `SCOPE-sprint-42`, `SCOPE-q2-2026`).
2. Set `kind` and `state` (`planned`/`active`/`completed`/`cancelled`).
3. Set `starts_at` / `ends_at` for time-bounded scopes.
4. Write goals as concrete, testable bullet points.
5. Save to `context/scopes/`, log `scope.created`.

### Using scopes

Reference via `spec.scope: SCOPE-...` on WorkItems, or use a Binding
(`type: work-scope`) when the scope relationship is temporal and an item
can move in or out of scope during its lifetime.

## Level 3 — Full reference

### Fields

| Field         | Type          | Notes                                             |
|---------------|---------------|---------------------------------------------------|
| `name`        | string        | Human-readable. Shown in listings.                 |
| `kind`        | enum          | `sprint`/`milestone`/`quarter`/`project`/`release`/`other` |
| `state`       | enum          | `planned`/`active`/`completed`/`cancelled`         |
| `starts_at`   | date          | Optional. For time-bounded scopes.                 |
| `ends_at`     | date          | Optional.                                          |
| `goals`       | list[string]  | Concrete outcomes expected.                        |
| `description` | string        | Longer context.                                    |
| `parent`      | string        | Optional parent scope (quarter → sprint).          |

### Nested scopes

A sprint can be nested within a quarter via `spec.parent`. Queries resolve
transitively: "all work in Q2 2026" includes all sprints that sit inside it.

### Closing a scope

When a scope ends:
1. Set `state: completed`.
2. Log `scope.completed`.
3. Do not delete the file — historical WorkItems reference it.
4. Optionally write a retrospective DecisionRecord linked via
   `spec.related_decisions`.
