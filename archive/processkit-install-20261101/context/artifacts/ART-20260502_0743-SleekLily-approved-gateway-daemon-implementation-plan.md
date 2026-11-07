---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260502_0743-SleekLily-approved-gateway-daemon-implementation-plan
  created: '2026-05-02T07:43:32+00:00'
spec:
  name: Approved processkit gateway daemon implementation plan
  kind: document
  format: markdown
  owner: ACTOR-codex
  tags:
  - processkit
  - mcp
  - gateway
  - daemon
  - architecture
  - approved-plan
  produced_at: '2026-05-02T07:43:32+00:00'
---

Approved plan for provider-neutral processkit MCP gateway daemon. Architecture: keep per-skill stdio MCP servers as canonical compatibility mode; keep aggregate-mcp as one-process stdio bridge; add processkit-gateway as provider-neutral runtime; add stdio proxy so stdio-only harnesses can connect to shared daemon; keep aibox as installer/supervisor only. Lanes: 1 Gateway Runtime: new processkit-gateway skill plus shared _lib/processkit/gateway registry, naming, loader, session, permissions modules; list_gateway_tools; preserve aggregate naming/collision behavior. 2 Daemon And Stdio Proxy: processkit-gateway serve --transport streamable-http, serve --transport stdio, stdio-proxy --url; PID/socket/port handling; health endpoint; stale daemon recovery; non-aibox startup. 3 Aggregate Compatibility: refactor aggregate-mcp to reuse gateway internals; preserve list_aggregate_tools and opt-in config; no server/tool renames. 4 Harness Compatibility: docs/config examples for Claude/Codex stdio proxy, OpenCode, Hermes; Aider limitation documented; mode matrix per-skill|aggregate|daemon-proxy. 5 Doctor Manifest Drift: mcp_gateway doctor check; mcp_config_drift accepts intentional gateway/proxy mode; manifest records gateway/proxy metadata; guard against starting both granular and gateway configs unintentionally. 6 Verification Benchmarks: focused gateway pytest, JSON-RPC stdio proxy smoke, full smoke integration, process count/RSS benchmark. 7 Docs Release: gateway architecture docs, non-aibox usage, aibox boundary, security/session model, release compatibility notes. Constraints: do not remove per-skill stdio servers; do not make aibox required; do not expose tools globally without per-connection policy; delegate entity validation to canonical per-skill tools; daemon session state must be explicit rather than PID-based. Verification gates: uv run scripts/smoke-test-servers.py; uv run src/context/skills/processkit/pk-doctor/scripts/doctor.py --no-log; npm --prefix docs-site run build; focused gateway pytest; uv run scripts/measure-mcp-gateway.py.
