---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260504_0557-AmberStream-session-handover
  created: '2026-05-04T05:57:44+00:00'
spec:
  event_type: session.handover
  timestamp: '2026-05-04T05:57:16Z'
  summary: Session handover - v0.25.3 provider-neutral model-profile routing released
  actor: ACTOR-codex
  subject: v0.25.3
  subject_kind: release
  details:
    session_date: '2026-05-04'
    current_state: processkit v0.25.3 has been implemented, committed, pushed, tagged,
      and published. The release adds provider-neutral model-profile artifacts, rewires
      Role/TeamMember model bindings through profiles, keeps concrete ModelSpec artifacts
      provider/model-named, adds resolver runtime provider gates for supported harnesses,
      and extends pk-doctor checks for profile hygiene and direct model pins. GitHub
      Release v0.25.3 is live with tarball assets attached; final pk-doctor passed
      with 0 ERROR / 0 WARN and release_integrity verified all 35 local v* tags have
      GitHub Releases. The working tree is clean.
    open_threads:
    - 'Existing in-progress epic BACK-20260502_0857-StoutGarnet-full-gateway-daemon-tiger-release-readiness
      remains open with its three lane stories: BACK-20260502_0857-SoftWillow-release-readiness-docs-packaging-lane,
      BACK-20260502_0857-SureCrow-tiger-v2-residual-cleanup-lane, and BACK-20260502_0857-TidyBear-gateway-doctor-manifest-measurement-lane.'
    - Existing in-progress docs epic BACK-20260409_1652-WildButter-create-polish-and-deploy
      remains open.
    - New model-routing implementation WorkItem BACK-20260503_1829-SoundSeal-provider-neutral-model-profile-routing
      was created for the accepted architecture; it should be reviewed for whether
      to transition to done after any desired post-release audit.
    - bwrap namespace failures still occur for some sandboxed shell commands. User
      delegated that issue to aibox; processkit release work used escalated reruns
      where necessary.
    - 'aibox responsibility follow-up remains: aibox should surface runtime provider
      access/entitlements so processkit model-profile expansion can use accurate available_providers
      rather than only harness inference.'
    next_recommended_action: 'Run a short post-release audit of v0.25.3 from a fresh
      checkout or downstream aibox sync path: install the release tarball, confirm
      model-profile artifacts arrive in src/context/artifacts, confirm Cora/Role bindings
      resolve through ModelProfile under both Codex and a non-Codex harness configuration,
      then close or transition BACK-20260503_1829-SoundSeal-provider-neutral-model-profile-routing
      if the audit is clean.'
    branch: main
    commit: 953f10f
    working_tree: clean
    stash: none
    release:
      tag: v0.25.3
      url: https://github.com/projectious-work/processkit/releases/tag/v0.25.3
      asset_sha256: 30e03e8f7ea08edfeee3c2c5224dd2734389679033387ead783e6ee2c1ac8048
    verification:
    - 'pk-doctor --no-log: 0 ERROR / 0 WARN'
    - 'pk-doctor --category=release_integrity: all 35 local v* tags have GitHub Releases'
    - 'scripts/check-src-context-drift.sh --release-deliverable: passed'
    - 'release_audit.py --tree=src-context: 0 ERROR / 0 WARN'
    - 'resolver/default-binding tests: 35 passed'
    - 'model-recommender MCP filter tests: 21 passed'
    - 'model migration tests: 20 passed'
    - 'release-audit tests: 26 passed'
    - 'uv run scripts/smoke-test-servers.py: passed'
    behavioral_retrospective:
    - 'User corrected the model artifact filename principle: concrete ModelSpec files
      may include provider/model names, but actors, roles, team members, and model-profile
      indirections must not. This is now encoded in docs, schemas, bindings, and pk-doctor
      checks.'
    - 'The release checksum/provenance loop required multiple amend/rebuild passes.
      Final state is stable: committed checksum matches dist/processkit-v0.25.3.tar.gz.sha256.'
    - One optional model-recommender MCP test was initially run without its declared
      mcp/httpx dependencies and failed with ModuleNotFoundError; rerun with declared
      dependencies passed. Future sessions should use the server script dependency
      set for those tests.
---
