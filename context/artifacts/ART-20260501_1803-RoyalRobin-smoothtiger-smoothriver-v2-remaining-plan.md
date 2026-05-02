---
apiVersion: processkit.projectious.work/v1
kind: Artifact
metadata:
  id: ART-20260501_1803-RoyalRobin-smoothtiger-smoothriver-v2-remaining-plan
  created: '2026-05-01T18:03:41+00:00'
spec:
  name: SmoothTiger SmoothRiver remaining v2 implementation plan
  kind: document
  location: context/artifacts/ART-SmoothTiger-SmoothRiver-remaining-v2-implementation-plan.md
  format: markdown
  version: '1.0'
  tags:
  - SmoothTiger
  - SmoothRiver
  - v2
  - implementation-plan
  - src
  produced_at: '2026-05-01T18:03:41+00:00'
---

Approved on 2026-05-01. Plan to finish SmoothTiger/SmoothRiver v2 gaps in src while live context remains v1. Lanes: 1) baseline contracts and checklist, 2) primitive demotion for Model, Process, Schedule, and indexed StateMachine while keeping Metric demoted, 3) MCP and skill refactor for model-recommender, process-management, schedule-management, state-machine-management, and missing Binding helpers, 4) pk-doctor validation and tests for demoted primitive surfaces and SmoothRiver checks, 5) migration docs/assets for schema-extension/data-fix and v1-to-v2 demoted representation, 6) docs cleanup removing contradictory primitive references, 7) security/cost/eval/projection follow-through, 8) parallel worker implementation with disjoint scopes, 9) integration verification: py_compile, targeted pytest, smoke-test-servers, docs build, git diff --check, and final SmoothRiver checklist audit.
