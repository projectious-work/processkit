---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260429_1329-DeepDove-github-issue-closed
  created: '2026-04-29T13:29:47+00:00'
spec:
  event_type: github.issue.closed
  timestamp: '2026-04-29T13:29:47+00:00'
  summary: 'Closed GitHub issue #13 after verifying provenance stamping is current.'
  actor: system
  subject: projectious-work/processkit#13
  subject_kind: github_issue
  details:
    repo: projectious-work/processkit
    issue: 13
    evidence:
    - scripts/build-release-tarball.sh runs scripts/stamp-provenance.sh --check "$VERSION"
      before staging release tarballs
    - v0.23.1 tag src/PROVENANCE.toml has generated_for_tag = "v0.23.1"
    - current src/PROVENANCE.toml has generated_for_tag = "v0.23.1"
    note: v0.23.1 GitHub Release has no uploaded tarball assets to inspect.
---
