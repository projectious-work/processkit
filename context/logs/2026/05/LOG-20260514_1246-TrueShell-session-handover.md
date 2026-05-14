---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260514_1246-TrueShell-session-handover
  created: '2026-05-14T12:46:58+00:00'
spec:
  event_type: session.handover
  timestamp: '2026-05-14T12:46:58+00:00'
  summary: Session handover — v0.26.7 patch release published and follow-up release
    hardening filed
  actor: ACTOR-codex
  details:
    session_date: '2026-05-14'
    current_state: processkit v0.26.7 has been published from main and tagged at 8a1ab48.
      The release includes semantic ID vocabulary allocation, id-management support
      for tagged pools and high-volume three-word allocation, pk-doctor id vocabulary
      checks, recorded decisions, and the completed implementation WorkItem. The clean
      tarball was built from a detached worktree at the v0.26.7 tag, the GitHub release
      assets were uploaded, and the downloaded checksum verified. The working tree
      remains dirty with many pre-existing unrelated context/aibox/doc changes; these
      were deliberately left untouched.
    open_threads:
    - BACK-20260514_1246-FluentDove-harden-release-tarball-dirty-tree is newly filed
      in backlog to make release packaging refuse or avoid dirty-checkout artifacts.
    - 'In-progress WorkItems from workitem-management: BACK-20260510_0344-MightyWolf-v1-penalty-semantic-hybrid-search;
      BACK-20260510_0344-MerryFox-teammember-slug-engineering-role-coverage; BACK-20260502_0857-SoftWillow-release-readiness-docs-packaging-lane;
      BACK-20260502_0857-SureCrow-tiger-v2-residual-cleanup-lane; BACK-20260502_0857-TidyBear-gateway-doctor-manifest-measurement-lane;
      BACK-20260502_0857-StoutGarnet-full-gateway-daemon-tiger-release-readiness;
      BACK-20260409_1652-WildButter-create-polish-and-deploy.'
    - Blocked WorkItems query returned none.
    - The checkout has many unrelated uncommitted modifications/deletions/untracked
      files, including aibox.toml, aibox.lock, context migration/archive/log/workitem
      movement, deleted broad skill trees, and preauth/manifest changes. Treat these
      as user or prior-session work; do not revert without an explicit request.
    next_recommended_action: Start by triaging the dirty working tree and the pending
      context/migration/archive changes before starting new release work. If continuing
      release hardening, pick up BACK-20260514_1246-FluentDove and update scripts/build-release-tarball.sh
      so release artifacts are produced only from the intended clean tag/source tree.
    branch: main
    commit: 8a1ab48
    stash: No stashes reported by git stash list.
    behavioral_retrospective:
    - The release flow initially built an unsafe v0.26.7 tarball from a dirty main
      checkout. I discarded that artifact, rebuilt from a clean detached worktree,
      verified the published checksum, and filed BACK-20260514_1246-FluentDove so
      the release script can prevent recurrence.
    - The GitHub release notes were first created with literal newline escapes. I
      corrected the release body with gh release edit and verified the rendered notes.
    - No pending user-approved design decision from this turn remains unrecorded;
      the accepted vocabulary/RAG architecture decisions were already recorded earlier
      in the session.
---
