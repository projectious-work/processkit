---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260502_0952-WiseGarnet-approved-final-release-blocker-plan
  created: '2026-05-02T09:52:29+00:00'
spec:
  name: Approved final release blocker implementation plan
  kind: spec
  format: markdown
  tags:
  - release-readiness
  - mcp-gateway
  - aibox-handoff
  - steadytiger
  - smoothtiger
  produced_at: '2026-05-02T09:52:29+00:00'
---

Approved plan for final processkit release blocker resolution. Lane 1: replace raw src/context dogfood drift as a release blocker with a deliverable-focused release gate that classifies deliverable, dogfood-only, generated-managed, and legacy-migration-source paths. Lane 2: update release audit for src/context v2 deliverables and fix processkit-gateway skill audit shape. Lane 3: finalize Model/Process/Metric demotion contract, keep demoted primitives out of shipped src/context, and classify live context legacy state as migration source; review task-router compatibility behavior. Lane 4: define aibox reset handoff as an optional harder reset path, recommended as an opt-in mode of aibox apply or aibox reset. Normal current migrations remain the default path. The optional reset should export project memory/context, bootstrap a fresh context tree from the processkit release, generate a migration/import manifest, restore preserved content with updated refs/schemas, leave an audit record, and preserve user-owned harness config while replacing processkit-managed blocks. Lane 5: run final release prep: smoke, pytest, doctor, docs build, measurement, provenance, tarball, checksum. Final lane: write an aibox handover document covering Lane 4, MCP daemon integration, SteadyTiger updates, SmoothTiger updates, and references needed for the new processkit release. Implementation uses at most three parallel agents; mutating processkit writes remain in the main session.
