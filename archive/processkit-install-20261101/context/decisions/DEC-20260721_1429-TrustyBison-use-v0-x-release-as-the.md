---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260721_1429-TrustyBison-use-v0-x-release-as-the
  created: '2026-07-21T14:29:27+00:00'
  updated: '2026-07-21T18:15:51+00:00'
spec:
  title: Use v0.x-release as the v0 integration and tagging branch
  state: accepted
  decision: 'Create v0.x-release from main at v0.27.6, then create v0.x-dev from v0.x-release.
    Put all v0 work on v0.x-dev. For every v0 release, merge v0.x-dev into v0.x-release,
    prepare and validate the release there, and create the v0.x.y tag there. Then
    merge v0.x-release into main so the exact tagged release is reachable from main.
    Keep the accepted v1 approach: rename v1.0 to v1.x-pre-release, branch v1.x-dev
    from it, merge v1.x-dev into v1.x-pre-release for prerelease tags.'
  context: 'The earlier branch strategy placed v0 releases directly on main. The user
    refined it after the v0.27.6 cleanup: main should receive finalized v0 releases
    only after they are tagged from a dedicated release branch.'
  rationale: This separates active maintenance from release integration, makes the
    tagging authority explicit, and keeps main as a clean, published-history branch
    without repeating the prior mixed-line tagging problem.
  alternatives:
  - option: Tag v0 releases directly from v0.x-dev
    outcome: Rejected because a development branch should not be the release authority.
  - option: Continue releasing directly from main
    outcome: Superseded because main would again mix release integration with active
      maintenance.
  consequences: Protect v0.x-release and main; disallow direct commits to either.
    Stable v0 tags originate only on v0.x-release and must be merged into main immediately
    after tagging. Define an analogous promotion rule for the eventual v1 GA release.
  decided_at: '2026-07-21T14:29:27+00:00'
  supersedes: DEC-20260721_1422-CheerfulSky-use-separate-development-and-integration-branches
---
