---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260502_0856-BoldCedar-approved-full-daemon-tiger-release-plan
  created: '2026-05-02T08:56:48+00:00'
spec:
  name: Approved full daemon and Tiger residual release implementation plan
  kind: document
  format: markdown
  version: '1.0'
  owner: ACTOR-codex
  tags:
  - processkit
  - mcp
  - gateway
  - daemon
  - SteadyTiger
  - SmoothTiger
  - release-plan
  - approved-plan
  produced_at: '2026-05-02T08:56:48+00:00'
---

Approved plan for completing the full processkit gateway daemon implementation and next release readiness. Goal: finish real daemon/proxy runtime, lazy loading/catalog, SteadyTiger/SmoothTiger v2 residuals, doctor/manifest/release gates, docs, and aibox handoff. Batch 1: implement streamable-http daemon, stdio proxy, runtime/session policy while preserving eager stdio. Batch 2: split tool catalog from implementation import, implement lazy execution and hot-module cache/idle eviction, preserve aggregate and per-skill compatibility. Batch 3: resolve v2 residuals: Model demotion, Process demotion and task-router process override behavior, Schedule and StateMachine demotion docs/skills, binding docs consistency, projection/eval/cost/security/Hook inbox coverage. Batch 4: extend pk-doctor, manifest, measurement, drift, preauth, aibox handoff, and release gates. Batch 5: update docs and prepare release with smoke tests, focused pytest, full doctor, release audit, docs build, drift check, manifest regeneration, provenance stamp, tarball build, checksum verification. Team model: at most three agents active at once; main session owns processkit writes, integration, transitions, release tagging, and final verification. Acceptance: daemon HTTP mode works; stdio proxy works without importing backing servers; lazy mode avoids importing all per-skill MCP servers at startup; eager gateway, aggregate, and per-skill modes still pass; Tiger residuals are resolved or explicitly documented as migration-only; all release gates pass.
