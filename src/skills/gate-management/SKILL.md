---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-gate-management
  name: gate-management
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Manage Gate entities — validation checkpoints that processes must pass (code review, security scan, tests)."
  category: process
  layer: 3
  uses: [event-log]
  provides:
    primitives: [Gate]
    templates: [gate]
  when_to_use: "Use when defining or updating a checkpoint a process must pass — code review, tests green, security scan, stakeholder approval."
---

# Gate Management

## Level 1 — Intro

A Gate is a validation checkpoint — "code review passed", "tests green",
"security scan clean", "stakeholder signed off". Processes reference gates
to declare what has to be true before a step can complete.

## Level 2 — Overview

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Gate
metadata:
  id: GATE-code-review
  created: 2026-04-06T00:00:00Z
spec:
  name: code-review
  description: "At least one reviewer has approved the change."
  kind: manual           # manual | automated | hybrid
  validator: "A second actor reviews and approves."
  required_roles: [reviewer]
  blocking: true         # if false, gate is advisory only
---
```

### Workflow

1. Pick `GATE-<name>` where name is a short noun phrase.
2. Set `kind`: `manual` (human does it), `automated` (check runs automatically),
   or `hybrid` (both).
3. Describe the `validator` — the concrete check. One or two sentences.
4. List `required_roles` if specific actors must do the validation.
5. Set `blocking: true` for hard gates (cannot proceed), `false` for advisory.

### Gate outcomes

Gates emit LogEntries when they are evaluated:
- `gate.passed` — validation succeeded
- `gate.failed` — validation failed (include failure details)
- `gate.waived` — validation was bypassed (include `details.waived_by` and reason)

## Level 3 — Full reference

### Fields

| Field             | Type          | Notes                                          |
|-------------------|---------------|------------------------------------------------|
| `name`            | string        | Short kebab-case identifier                    |
| `description`     | string        | What this gate checks                          |
| `kind`            | enum          | `manual` / `automated` / `hybrid`              |
| `validator`       | string        | Prose description of the check                 |
| `validator_command` | string      | Optional. CLI command that automates the check |
| `required_roles`  | list[string]  | Roles that can sign off                        |
| `blocking`        | bool          | `true` = cannot proceed if failed              |
| `evidence_required` | bool        | Require a link/artifact in the pass event      |

### Binding gates to processes

Use a Binding (`type: process-gate`) to apply a gate to a specific process,
optionally scoped:

```yaml
kind: Binding
spec:
  type: process-gate
  subject: PROC-release
  target: GATE-security-scan
  scope: SCOPE-project-x
```

This way the same Gate can apply to multiple processes, and the mapping
changes without editing the Gate or Process files.

### Waiving a gate

If a blocking gate is bypassed, log `gate.waived` with `details.waived_by`
(actor ID), `details.reason`, and `details.expires_at`. Do not edit the
Gate definition — the waiver is an event, not a property.
