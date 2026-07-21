---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260721_1422-CheerfulSky-use-separate-development-and-integration-branches
  created: '2026-07-21T14:22:51+00:00'
  updated: '2026-07-21T18:15:51+00:00'
spec:
  title: Use separate development and integration branches for v0 and v1 releases
  state: superseded
  decision: Create v0.x-dev from the latest v0 release on main; merge it to main for
    every v0 release and tag there. Rename v1.0 to v1.x-pre-release; create v1.x-dev
    from it; merge v1.x-dev to v1.x-pre-release for every v1 pre-release and tag there.
  context: The prior v0/v1 branch topology allowed release commits and tags to land
    on the wrong development branch, making release provenance ambiguous.
  rationale: Development branches remain writable integration spaces while main and
    v1.x-pre-release provide unambiguous tag provenance for their respective stability
    stages.
  alternatives:
  - option: Use only main and v1.0
    rejected_because: It previously allowed v0 maintenance releases and v1 development
      to mix.
  - option: Tag directly on development branches
    rejected_because: Tags would not identify a verified integration point.
  consequences: Contributors target v0.x-dev or v1.x-dev rather than release branches.
    Stable releases require a reviewed merge to main; pre-releases require a reviewed
    merge to v1.x-pre-release. Branch protections must enforce these paths.
  deciders:
  - ACTOR-owner
  decided_at: '2026-07-21T14:22:51+00:00'
  superseded_by: DEC-20260721_1429-TrustyBison-use-v0-x-release-as-the
---
