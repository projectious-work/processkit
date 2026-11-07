---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260414_1500-BaselinePulse-enforcement-adoption-baseline-metrics
  legacy_id: BACK-20260414_1500-BaselinePulse-enforcement-adoption-baseline-metrics
  created: '2026-04-14T15:00:00+00:00'
  labels:
    component: processkit-core
    area: enforcement
    priority_driver: measurement
spec:
  title: Capture pre-enforcement baseline metrics for processkit adoption in derived
    projects
  state: done
  type: spike
  priority: medium
  description: |
    Before the enforcement wave (CleanCharter / InkStamp / RightPath / LoudBell / SteadyHand) lands in a release, capture a baseline of how often agents currently invoke processkit surfaces in derived projects. Without this, we cannot later claim the enforcement work improved adoption — we will only have vibes.
    Scope (bounded — 1–2 hours Jr Researcher): 1. Pick 2 derived projects that consume processkit today (owner
       will name them; default candidates: aibox itself and one
       private consumer).
    2. For the last ~20 agent sessions in each (look at
       context/events/ log entries and git history for entity writes),
       count:
         - sessions where route_task was invoked before the first
           create_* / transition_* / record_* call
         - sessions where create_workitem / create_artifact /
           record_decision were called at all
         - sessions where hand-edits under context/ happened without
           a corresponding MCP tool call in the same window
         - sessions where log_event entries followed state changes
    3. Produce an Artifact with the counts per project plus a single
       aggregated rate (e.g. "route_task-before-write: 12/40 = 30%").
       No commentary on causes — this is the before-picture only.

    Out of scope: changing anything, designing better metrics, comparing across harnesses. The same counts will be re-run after the enforcement wave ships to produce the after-picture.
  related_artifacts:
  - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
  - ART-20260414_1230-ReachReady-processkit-enforcement-research
  related_decisions:
  - DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list
  assigned_to: ACTOR-jr-researcher
  linked_artifacts:
  - ART-20260414_1515-BaselinePulse-enforcement-baseline-metrics
  progress_notes: |
    2026-04-14T15:15Z — Baseline complete. Data source: context/logs/2026/04/ (70 log entries) + git history (94 commits). Session proxy: commit clusters. 16 sessions identified; 7 had entity writes. Key counts: M1 route_task-before- write 0/3 (0%); M2 create-* called at all 5/7 (71%); M3 hand-edits without MCP 2/16 (12.5%); M4 log_event after state-changes ~55-60%. Confidence low-medium across all four due to voluntary log_event. Second project not accessible — owner must name one before release. No commit per WI instructions.
  owner_note: |
    Owner approved adding baseline metrics so the A/B the research report recommends (research §6 row 4) can be run with a real before-picture. Should land before the enforcement release is cut.
---
