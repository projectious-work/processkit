---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260502_1814-TallBadger-aibox-release-handover-processkit-v025
  created: '2026-05-02T18:14:52+00:00'
spec:
  name: aibox release handover for processkit v0.25.0
  kind: document
  format: markdown
  version: v0.25.0
  produced_by: BACK-20260502_0953-LoyalWillow-aibox-release-handover-document
  tags:
  - aibox
  - handover
  - internal
  - processkit-v0.25.0
  - mcp-gateway
  produced_at: '2026-05-02T18:14:52+00:00'
---

# aibox Release Handover

This internal handover is for the aibox integration work that follows the
processkit v0.25.0 release.

## MCP gateway daemon

processkit ships `processkit-gateway` as the provider-neutral MCP entry
point. aibox should install the pinned processkit release, start and
stop the gateway in managed devcontainers, and generate harness MCP
configuration that points Claude Code, Codex, OpenCode, Hermes, or other
harnesses at the gateway.

Recommended modes:

- Direct stdio: `serve --transport stdio`
- Daemon: `serve --transport streamable-http --host 127.0.0.1 --port 8000 --path /mcp`
- Stdio-only harness bridge: `stdio-proxy --url http://127.0.0.1:8000/mcp`
- Lazy daemon startup: generate `catalog --write`, then set
  `PROCESSKIT_GATEWAY_IMPORT_MODE=lazy-catalog`

The gateway is not a Claude, Codex, or aibox daemon. It is a processkit
MCP gateway. aibox owns deployment, supervision, generated harness config,
doctor wiring, and user-facing configuration knobs.

## Optional reset path

The harder reset path should be optional. The normal upgrade path remains
the current migration flow.

aibox should expose the harder reset as an opt-in mode of `aibox apply` or
`aibox reset`, with an explicit user decision before any destructive
rewrite of `context/`.

Recommended flow:

1. Export project memory from the current tree: decisions, artifacts,
   discussions, logs, notes, workitems, bindings, scopes, gates, roles,
   team members, and migration records.
2. Bootstrap a fresh `context/` tree from the new processkit release.
3. Generate a migration/import manifest that maps old IDs, references,
   schemas, and state-machine fields to the new release contract.
4. Re-import preserved project memory with updated references and schema
   fields.
5. Leave an auditable migration record describing the reset and import.
6. Preserve user-owned harness config while replacing processkit-managed
   generated MCP blocks.

processkit provides the release contract, migration semantics, doctor
checks, MCP manifest, and gateway. aibox owns the reset UX, temporary
storage, fresh bootstrap, import choreography, and rollback story.

## SteadyTiger updates

The release treats `Metric`, `Model`, `Process`, `Schedule`, and
`StateMachine` as legacy migration-source kinds, not shipped v2 entity
primitives. aibox should not assume these schemas or directories exist
under `src/context/` in new processkit releases.

Integration implications:

- Preserve existing project `context/models/` and `context/processes/`
  only as migration-source state.
- Do not re-create removed v2 schemas during sync.
- Treat `model-assignment` Bindings as references to model-recommender
  roster/profile IDs, not first-class Model entities.
- Treat task-router `process_override` as `legacy-v1` compatibility data.

## SmoothTiger updates

SmoothTiger/SmoothRiver v2 keeps durable facts in existing entity
primitives and uses projection skills for runtime files. aibox should
continue to preserve project memory while allowing generated files,
manifests, and harness blocks to be refreshed from the new processkit
release.

Relevant release-facing checks:

- `scripts/check-src-context-drift.sh --release-deliverable`
- `release_audit.py --tree=src-context`
- `pk-doctor` categories for MCP manifest drift, server headers,
  migrations, and v2 contracts
- `scripts/measure-mcp-gateway.py`
- `scripts/smoke-test-servers.py`

## References

- Plan: `ART-20260502_0952-WiseGarnet-approved-final-release-blocker-plan`
- Decision: `DEC-20260502_0952-KeenCrane-proceed-with-final-release-blocker-plan`
- Gateway docs: `docs-site/docs/mcp-servers/harness-compatibility.md`
- v2 contract docs: `docs-site/docs/reference/v2-contracts.md`
- Release gate: `scripts/check-src-context-drift.sh --release-deliverable`
- Release audit: `context/skills/processkit/release-audit/scripts/release_audit.py --tree=src-context`
