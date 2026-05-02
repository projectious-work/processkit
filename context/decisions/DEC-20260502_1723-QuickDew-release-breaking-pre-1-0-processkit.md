---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260502_1723-QuickDew-release-breaking-pre-1-0-processkit
  created: '2026-05-02T17:23:18+00:00'
spec:
  title: Release breaking pre-1.0 processkit changes as v0.25.0
  state: accepted
  decision: Ship the current breaking processkit release as v0.25.0, not v1.0.0, and
    make the release notes comprehensive enough to explain the daemon, v2 deliverable
    boundary, demotions, release gates, and aibox handover work.
  context: The user approved the release-preparation path after asking whether the
    next release should be major because of the large breaking changes. The repository
    is still pre-1.0, the latest existing tag is v0.24.0, and the current work changes
    the shipped src/context contract substantially.
  rationale: Under SemVer, pre-1.0 projects may use a minor bump for breaking changes.
    A v1.0.0 release would imply a stable compatibility commitment that the project
    is not ready to make. v0.24.0 cannot be reused because it already exists. The
    size and risk of the change require explicit release notes rather than terse bullets.
  alternatives:
  - option: Release as v1.0.0
    reason_not_chosen: The project has not committed to a stable 1.0 compatibility
      contract yet, so this would overstate support expectations.
  - option: Release as v0.24.0
    reason_not_chosen: The v0.24.0 tag already exists and cannot represent the new
      release line.
  - option: Delay release until all downstream aibox reset work is implemented
    reason_not_chosen: Processkit can ship the provider-neutral gateway, release boundary,
      and handover contract while aibox implements its integration and optional reset
      flow against the new release.
  consequences: Release artifacts and provenance must be rebuilt for v0.25.0. The
    changelog and GitHub Release notes must call out breaking behavior and migration
    guidance clearly. Tagging and publishing should only happen from a verified, intentionally
    staged release commit.
  related_workitems:
  - BACK-20260502_0952-SunnyButter-final-release-blockers-aibox-handoff
  - BACK-20260502_0953-ToughWillow-final-release-verification-packaging-prep
  - BACK-20260502_0953-LoyalWillow-aibox-release-handover-document
  decided_at: '2026-05-02T17:23:18+00:00'
---
