---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260514_1246-FluentDove-harden-release-tarball-dirty-tree
  created: '2026-05-14T12:46:41+00:00'
  labels:
    source: pk-wrapup
    release: v0.26.7
spec:
  title: Harden release tarball build against dirty working tree artifacts
  state: backlog
  type: task
  priority: medium
  description: During the v0.26.7 release, the first tarball build was run from a
    dirty main checkout and regenerated release files using unrelated local changes.
    The artifact was discarded and rebuilt from a clean detached worktree at the tag,
    but scripts/build-release-tarball.sh should make this harder to do accidentally.
    Evaluate adding a dirty-tree guard, a tag/worktree build mode, or a clear refusal
    unless the source tree exactly matches the release tag; keep dist output reproducible
    and verify provenance from the same tree used for packaging.
---
