---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260502_0856-GrandFinch-proceed-with-full-gateway-daemon-and
  created: '2026-05-02T08:56:58+00:00'
  updated: '2026-05-02T08:57:25+00:00'
spec:
  title: Proceed with full gateway daemon and Tiger residual release implementation
  state: accepted
  decision: Proceed with the approved comprehensive plan to complete the full provider-neutral
    processkit gateway daemon implementation, resolve SteadyTiger/SmoothTiger v2 release
    residuals, and prepare the next processkit release with at most three implementation
    agents active in parallel.
  context: The user approved a plan covering streamable-http daemon runtime, stdio
    proxy, lazy catalog/loading, SteadyTiger/SmoothTiger demotion residuals, doctor/manifest/release
    gates, docs, and aibox handoff. The current gateway is an eager stdio server;
    daemon/proxy CLI shapes are reserved but disabled. Release readiness is blocked
    by context/src drift, Tiger residuals, preauth drift, and release gate cleanup.
  rationale: This sequence addresses the original devcontainer memory pressure with
    a real shared daemon while preserving provider neutrality and standalone processkit
    usability. It also prevents a release that advertises v2 daemon/Tiger behavior
    before drift, docs, doctor checks, and packaging are coherent.
  alternatives:
  - option: Ship current eager gateway only
    rejected_because: Does not solve shared daemon memory pressure and docs already
      mark daemon/proxy as future work.
  - option: Make daemon aibox-owned
    rejected_because: Would tightly couple processkit runtime semantics to aibox and
      weaken standalone processkit usability.
  - option: Defer Tiger residuals until after daemon release
    rejected_because: Release readiness checks found v2 demotion/docs/drift issues
      that could confuse consumers of the next processkit release.
  consequences: Implementation will create a second gateway increment with daemon/proxy/lazy
    runtime, Tiger v2 cleanup, and stricter release gates. aibox remains responsible
    for installing/configuring/running the gateway in managed devcontainers, while
    processkit owns gateway semantics and MCP behavior.
  deciders:
  - ACTOR-user
  - ACTOR-codex
  decided_at: '2026-05-02T08:56:58+00:00'
  related_workitems:
  - BACK-20260502_0857-StoutGarnet-full-gateway-daemon-tiger-release-readiness
---
