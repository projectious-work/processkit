---
sidebar_position: 20
title: "Gate"
---

# Gate

A validation checkpoint in a process. Gates define what must be true
before work can proceed. Evaluation results are LogEntries —
`gate.passed`, `gate.failed`, or `gate.waived`.

| | |
|---|---|
| **ID prefix** | `GATE` |
| **State machine** | none |
| **MCP server** | `gate-management` |
| **Skill** | `gate-management` (Layer 3) |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `name` | string (1–100) | Short kebab-case identifier |
| `description` | string | What this gate checks (one sentence) |
| `kind` | enum | `manual` · `automated` · `hybrid` |
| `validator` | string | Prose description of the check (one–two sentences) |

### Optional

| Field | Type | Description |
|---|---|---|
| `validator_command` | string | CLI command for automated/hybrid gates |
| `required_roles` | `ROLE-*[]` | Roles authorised to sign off |
| `blocking` | boolean | `true` = work cannot proceed without passing (default: `true`) |
| `evidence_required` | boolean | `true` = `gate.passed` log must include artifact reference (default: `false`) |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Gate
metadata:
  id: GATE-20260411_0912-SteadyArch-smoke-tests-green
  created: '2026-04-11T09:12:00Z'
spec:
  name: smoke-tests-green
  description: All MCP server smoke tests must pass before tagging a release.
  kind: automated
  validator: Run `uv run scripts/smoke-test-servers.py` — exit 0 required.
  validator_command: uv run scripts/smoke-test-servers.py
  blocking: true
  evidence_required: false
---
```

## Notes

- Gates define *what* to check; the evaluation happens externally (by an
  agent, CI, or human). Log the result with `log_event` using
  `event_type: gate.passed`, `gate.failed`, or `gate.waived`.
- `evaluate_gate` runs the `validator_command` (if set) and logs the
  result in one call.
- Advisory gates (`blocking: false`) surface warnings without halting
  the process.
- Attach gates to concrete v2 surfaces via `workitem-gate` or
  `scope-gate` Bindings. Legacy `process-gate` Bindings are migration-only.
