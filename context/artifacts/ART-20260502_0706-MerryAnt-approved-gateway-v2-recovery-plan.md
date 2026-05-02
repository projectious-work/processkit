---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260502_0706-MerryAnt-approved-gateway-v2-recovery-plan
  created: '2026-05-02T07:06:16+00:00'
spec:
  name: Approved implementation plan - processkit gateway and SmoothRiver v2 recovery
  kind: document
  format: markdown
  version: '1.0'
  owner: TEAMMEMBER-thrifty-otter
  produced_by: ACTOR-codex
  tags:
  - implementation-plan
  - processkit-gateway
  - mcp
  - SmoothRiver
  - SmoothTiger
  - v2
  - parallel-lanes
  produced_at: '2026-05-02T07:06:16+00:00'
---

# Approved implementation plan - processkit gateway and SmoothRiver v2 recovery

## Context

The owner approved a reconstructed plan after the prior environment crash lost the working plan. The plan combines two tracks:

1. Reduce managed devcontainer memory pressure by moving processkit MCP exposure from one Python interpreter per MCP server per harness toward a single provider-neutral processkit MCP gateway.
2. Finish the SmoothRiver/SmoothTiger v2 recovery in `src/`, preserving the accepted split-track rule: `src/` moves to v2/no-shim deliverables, while the live `context/` tree remains a staged runtime/migration source unless changed through approved processkit migrations.

## Confirmed current state

- `aggregate-mcp` already exists and re-exports per-skill MCP tools through one FastMCP process.
- `aggregate-mcp` currently imports all per-skill `server.py` modules eagerly, so it reduces process count but not idle module memory.
- MCP Python SDK supports stdio, SSE, and Streamable HTTP; Streamable HTTP is the preferred production direction in the SDK docs.
- v2 foundations are partially present: v2 frontmatter/entity shape, schema validation, Metric demotion to `Artifact{kind=metric-spec}`, SmoothRiver artifact/binding/log vocabularies, migration source-version semantics, Hook inbox helpers, AgentCard/eval/security projection stubs, and `pk-doctor` `v2_contracts`.
- Incomplete v2 demotions remain: Model, Process, Schedule, and StateMachine still exist as first-class source primitives under `src/context/`.
- Documentation is behind the implementation: MCP server count, v1 examples, primitive docs, pk-doctor docs, and projection docs need updates.

## Gateway direction

Build in stages:

1. Aggregate quick win: make aibox/harness config able to register `processkit-aggregate-mcp` instead of granular per-skill servers.
2. Gateway daemon: add a long-lived `processkit-gateway` process exposing one processkit MCP surface, preferably over local Streamable HTTP.
3. Stdio bridge: for harnesses without HTTP MCP support, provide a tiny stdio adapter that forwards to the local gateway.
4. Lazy registry: advertise tool metadata without importing every tool module; import per-skill modules on first tool call, retain hot modules, and evict only where safe.
5. Permission and concurrency: preserve tool annotations and enforce processkit permission metadata inside the gateway; serialize mutating tools with a single-writer lock.

## Parallel implementation lanes

### Lane 1 - Gateway runtime

Write scope: `src/context/skills/processkit/aggregate-mcp/`, new gateway files under a gateway/aggregate skill scope, related MCP config docs.

Deliverables:
- Aggregate mode config option and docs.
- Gateway prototype with local Streamable HTTP transport where feasible.
- Stdio bridge design/prototype for stdio-only harnesses.
- Lazy tool registry design that avoids FastMCP private internals where possible.
- Gateway health and tool inventory surface.

### Lane 2 - Schema and v2 demotions

Write scope: `src/context/schemas/`, `src/context/models/`, `src/context/processes/`, `src/context/state-machines/`, `src/context/skills/_lib/processkit/`.

Deliverables:
- Complete Model demotion to `Artifact{kind=model-spec}` or model-recommender configuration, with no hidden v1/v2 shim.
- Complete Process demotion to `Artifact{kind=process-definition}` plus `WorkItem{kind=process-instance|process-step}`.
- Complete Schedule demotion to `Artifact{kind=schedule-rule}` plus `Binding{type=time-window}`.
- Reconcile StateMachine treatment with `Schema{kind=state-machine}` or explicitly document the remaining loader-only exception.
- Fix vocabulary enforcement gaps such as `Migration.kind`.

### Lane 3 - MCP semantics

Write scope: affected processkit MCP servers and shared semantics, including model-recommender, artifact-management, binding-management, note-management, migration-management, index-management.

Deliverables:
- Update server APIs to the v2 demoted model/process/schedule/state-machine contract.
- Keep write paths MCP-owned and schema/state-machine validated.
- Preserve processkit/aibox responsibility split: processkit owns runtime semantics, aibox owns deployment/configuration.
- Confirm aggregate/gateway surface matches the intended per-skill tool surface and does not accidentally expose unconfigured servers.

### Lane 4 - Doctor and tests

Write scope: `src/context/skills/processkit/pk-doctor/scripts/`, tests, smoke scripts, release-audit checks.

Deliverables:
- Add/finish v2 guardrails for demoted primitives and closed vocabularies.
- Add gateway/aggregate parity and health checks.
- Add checks for stale docs/manifests where practical.
- Keep `uv run scripts/smoke-test-servers.py` green.

### Lane 5 - Docs

Write scope: `docs-site/`, relevant `src/context/skills/processkit/*/SKILL.md` and `mcp/SERVER.md` docs.

Deliverables:
- Update MCP overview for aggregate/gateway modes and correct server count.
- Replace stale v1 primitive examples with v2/no-shim examples.
- Add user-facing pages for Hook inbox, AgentCard projection, eval-gate authoring, security projections, and `pk-doctor v2_contracts`.
- Update migration docs for split-track v2 recovery.

### Lane 6 - Integration

Write scope: main-session owned only.

Deliverables:
- Review and integrate worker patches.
- Regenerate manifests and provenance where required.
- Run smoke tests and targeted docs build/test.
- Ensure no accidental hand-edit migration of live `context/` entities outside MCP-approved records.

## Sequencing

1. Persist plan and acceptance in processkit.
2. Create lane WorkItems.
3. Start read/write worker lanes with disjoint scopes.
4. Integrate in the main session.
5. Verify with doctor, smoke tests, and docs build.

## First verification gates

- `pk-doctor --category=schema_vocabulary,v2_contracts,mcp_config_drift,server_header_drift`
- `uv run scripts/smoke-test-servers.py`
- docs build from `docs-site`
- aggregate/gateway tool inventory compared with per-skill MCP config manifest
