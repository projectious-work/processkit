---
name: process-management
description: |
  Manage Process entities — declarative sequences of steps with roles, gates, and a definition of done. Use when defining a reusable workflow — code review, release, incident response, onboarding — that the project wants to run consistently.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-process-management
    version: "1.0.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 3
    uses:
      - skill: event-log
        purpose: Log events to keep the audit trail accurate after every write.
      - skill: role-management
        purpose: Resolve Role IDs when entities need role-based assignment.
      - skill: gate-management
        purpose: Evaluate gate conditions before allowing transitions.
    provides:
      primitives: [Process]
      templates: [process]
---

# Process Management

## Intro

A Process is a declarative definition of a workflow: a sequence of steps,
the roles involved, the gates that must pass, and the definition of done.
processkit does NOT execute processes — agents and humans do. processkit
just defines them.

## Overview

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Process
metadata:
  id: PROC-code-review
  created: 2026-04-06T00:00:00Z
spec:
  name: code-review
  description: "Review a pull request before merge."
  triggers: [pr.opened, pr.review-requested]
  roles: [developer, reviewer]
  steps:
    - name: author-self-check
      role: developer
      uses_skill: code-review
      description: "Author runs the self-review checklist."
    - name: peer-review
      role: reviewer
      uses_skill: code-review
      description: "A different actor reviews the diff and leaves comments."
      gates: [GATE-no-blocking-comments]
    - name: approval
      role: reviewer
      description: "Reviewer approves the PR."
      gates: [GATE-code-review-passed]
    - name: merge
      role: developer
      description: "Author merges after approval and CI pass."
      gates: [GATE-ci-passed, GATE-code-review-passed]
  definition_of_done: "PR merged with at least one approval, all CI gates passed."
---
```

### Workflow

1. Pick `PROC-<name>`.
2. List `triggers` — events that kick off the process.
3. List required `roles`.
4. Define `steps` in order. Each step names the actor role, optional skill,
   description, and gates.
5. Write a clear `definition_of_done`.
6. Save to `context/processes/`.

### Running a process

An agent running a process:
1. Detects the trigger.
2. Walks the steps in order.
3. For each step, performs the action (often guided by `uses_skill`).
4. Validates gates at each step — logs `gate.passed` / `gate.failed`.
5. Logs `process.step.started` / `process.step.completed`.
6. Exits when the last step completes or a blocking gate fails.

## Full reference

### Fields

| Field                | Type          | Notes                                              |
|----------------------|---------------|----------------------------------------------------|
| `name`               | string        | kebab-case identifier                              |
| `description`        | string        | One sentence                                       |
| `triggers`           | list[string]  | Event types that start the process                 |
| `roles`              | list[string]  | Role names involved                                |
| `steps`              | list[object]  | Ordered list; see below                            |
| `definition_of_done` | string        | The acceptance criterion for the whole process     |
| `parallel`           | bool          | Default false; true = steps run in parallel        |
| `retryable`          | bool          | Can the process be re-run if it fails?             |

### Step object

```yaml
- name: <step-name>
  role: <role-name>         # who performs this step
  description: <one-sentence>
  uses_skill: <skill-name>  # optional — skill that guides execution
  inputs: [<entity-ref>]    # optional — what this step needs
  outputs: [<entity-ref>]   # optional — what this step produces
  gates: [<gate-id>]        # optional — gates that must pass
  on_failure: <action>      # halt | retry | skip | escalate
```

### Parallel vs sequential

Default is sequential. Set `parallel: true` to run steps concurrently when
they are independent. For conditional branching, write multiple processes
and trigger them conditionally rather than embedding complex logic.

### Scoping a process

Use a Binding (`type: process-scope`) to apply a process to a specific
project or team:

```yaml
kind: Binding
spec:
  type: process-scope
  subject: PROC-code-review
  target: SCOPE-project-x
```

### No workflow engine

processkit does not ship an engine that executes processes. The Process
definition is a contract between the definition and whoever runs it. Agents
are the default runners; automation can take over specific steps.
