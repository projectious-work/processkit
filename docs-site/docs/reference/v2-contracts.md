---
sidebar_position: 5
title: "v2 Contracts"
---

# v2 Contracts

SmoothTiger/SmoothRiver v2 keeps durable facts in existing entity
primitives and uses projection skills for runtime files. The source of
truth remains processkit context; generated files are checked against
that source.

`Metric`, `Model`, `Process`, `Schedule`, and `StateMachine` are legacy
v1 migration-source kinds, not shipped v2 entity primitives. Model
selection uses model-recommender roster/configuration data. Process
definitions are Artifacts plus process-instance WorkItems. Schedule
semantics use `Binding(type=time-window)`. Runtime state-machine YAML
files remain implementation contracts, not user-authored StateMachine
entities.

## Hook inbox

Hook inbox items are Notes with `spec.inbox`. The `note-management` MCP
server owns the lifecycle:

- `prepare_hook_inbox_dirs`
- `capture_inbox_item`
- `claim_inbox_item`
- `complete_inbox_item`
- `fail_inbox_item`

Valid injection modes are `interrupt`, `ambient`, and `next-cycle`.
They belong on `Binding(type=triage-classification)` records.

## AgentCard

Agent cards are Artifact-backed projections. Store the canonical source
as an Artifact with `spec.kind: agent-card`, then use the `agent-card`
MCP server's `project_agent_card` tool to render the public JSON file.
`spec.projection_path` and `spec.projection_checksum` let validation
detect missing or stale projections.

## Eval gates

The `eval-gate-authoring` MCP server turns observed run outputs into:

- `Artifact(spec.kind=eval-spec)`
- a paired `Gate`
- policy/application Bindings
- calibration LogEntries for LLM-as-judge evals

Use `collect_run_outputs`, `codify_eval`, `calibrate_judge`, and
`bind_eval_to_runs`. LLM judge eval specs are expected to have a
calibration log before they are treated as enforceable gates.

## Security projections

Security policy sources are Artifacts. The `security-projections` MCP
server emits runtime policy files from those Artifacts:

- `project_agent_ids_rule` renders Agent-IDS JSON rules.
- `project_tetragon_tracing_policy` renders Tetragon-style YAML
  tracing policies.

Keep the Artifact as the reviewable source and treat generated policy
files as projections.

## pk-doctor `v2_contracts`

`pk-doctor` includes a `v2_contracts` check for v2 workflow and
projection guardrails. It currently checks:

- process-instance WorkItems reference a process definition.
- time-window Bindings include `conditions.recurrence_rule`.
- cost-policy Artifacts are bound through budget-application Bindings.
- policy supersedes chains point at known policy Artifacts.
- LLM-as-judge eval-spec Artifacts have calibration logs.
- agent-card projections exist and match recorded checksums.
- hook inbox injection modes are valid and scoped to
  triage-classification Bindings.
- claimed inbox Notes older than 24 hours are reported as orphan risks.

Run it through the normal doctor command:

```bash
uv run context/skills/processkit/pk-doctor/scripts/doctor.py
```
