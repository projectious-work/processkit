---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260517_0822-CleverShore-session-handover
  created: '2026-05-17T08:22:59+00:00'
spec:
  event_type: session.handover
  timestamp: '2026-05-17T08:22:59+00:00'
  summary: Session handover - release finalized and PowerKit idle CPU cause isolated
  actor: TEAMMEMBER-cora
  details:
    session_date: '2026-05-17'
    current_state: 'Main is clean and synced with origin/main at 32b1605. v0.26.14
      was already tagged and published on GitHub with release assets; the additional
      processkit skill library updates were committed and pushed. A high idle CPU
      investigation found tmux/PowerKit status rendering is the main container CPU
      source: status enabled measured about 1.69 cores over 20s, while status disabled
      measured about 0.34 cores over 20s.'
    open_threads:
    - 'In-progress WorkItems from workitem-management: BACK-20260510_0344-MightyWolf-v1-penalty-semantic-hybrid-search;
      BACK-20260510_0344-MerryFox-teammember-slug-engineering-role-coverage; BACK-20260502_0857-SoftWillow-release-readiness-docs-packaging-lane;
      BACK-20260502_0857-SureCrow-tiger-v2-residual-cleanup-lane; BACK-20260502_0857-TidyBear-gateway-doctor-manifest-measurement-lane;
      BACK-20260502_0857-StoutGarnet-full-gateway-daemon-tiger-release-readiness;
      BACK-20260409_1652-WildButter-create-polish-and-deploy.'
    - No blocked WorkItems were returned by workitem-management.
    - PowerKit/tmux idle CPU remains unresolved. Current tmux config uses status 2
      and status-interval 10, with status-format commands invoking aibox-powerkit-render-session
      and three aibox-powerkit-render-list commands across 26 plugins every 10s. Full
      synthetic status repaint samples took 10065ms, 6466ms, and 4383ms.
    - PowerKit line/plugin timings showed no single culprit; most individual plugins
      cost 300-900ms due to repeated bootstrap/theme/options/lifecycle overhead. aibox-status
      --plugin-json itself was fast at about 8ms.
    - 'pk-doctor from earlier in the session had 0 errors, 2 warnings, and 2 actionable
      findings: Codex preauth allowed-tools missing gated by aibox#55, and 2 applied
      migrations are archive candidates.'
    next_recommended_action: 'First, reduce PowerKit idle CPU by changing tmux/PowerKit
      status behavior: either raise status-interval to 30 or 60, remove low-value
      plugins, collapse to one status line, or implement full-line render caching/single-process
      rendering. Re-measure cgroup CPU with status on/off after the change.'
    branch: main
    commit: 32b1605
    stashes: none
    behavioral_retrospective:
    - The user challenged the initial 1.4-core idle reading as too high; further controlled
      measurement confirmed the concern and isolated PowerKit/tmux status rendering
      as the primary source.
    - No skipped tracking promises remain from this wrapup; the open CPU optimization
      thread is captured in this handover.
---
