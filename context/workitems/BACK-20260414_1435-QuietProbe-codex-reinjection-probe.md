---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260414_1435-QuietProbe-codex-reinjection-probe
  legacy_id: BACK-20260414_1435-QuietProbe-codex-reinjection-probe
  created: '2026-04-14T14:35:00+00:00'
  labels:
    component: codex
    area: enforcement
spec:
  title: Probe Codex CLI AGENTS.md re-injection behaviour and record findings
  state: done
  type: spike
  priority: medium
  size: S
  description: >
    The research report (ART-20260414_1230-ReachReady §6) leaves open
    whether Codex CLI re-injects AGENTS.md each turn or only at session
    start. This determines whether hooks are primary or secondary
    priority on Codex. Run a one-shot empirical probe and record the
    finding.
  inputs:
    - /workspace/context/artifacts/ART-20260414_1230-ReachReady-processkit-enforcement-research.md  (§6)
    - https://developers.openai.com/codex/guides/agents-md
    - https://github.com/openai/codex  (source; inspect if docs are ambiguous)
  method: |
    1. Insert a distinctive sentinel string (e.g. "SENTINEL-20260414-QuietProbe-A7F3") into AGENTS.md.
    2. Start a Codex CLI session. In turn 1, do unrelated work that does not reference the sentinel.
    3. Over turns 2–20, gradually fill context with unrelated tool calls.
    4. At turn 20, ask Codex verbatim: "What is the value of SENTINEL-20260414-QuietProbe-A7F3 in AGENTS.md?"
    5. Record whether Codex can recall the sentinel. If yes → AGENTS.md is still accessible (re-injected or retained); if no → compacted away.
    6. Repeat with a modified sentinel after turn 10 to test whether Codex sees mid-session edits.
  deliverables:
    - context/artifacts/ART-<DATE>-<WORD>-codex-reinjection-probe.md — findings with method, evidence, confidence label, and recommendation (hooks primary vs secondary for Codex).
  success_criteria:
    - Artifact exists, registered via create_artifact so the index picks it up.
    - Finding carries an explicit confidence label (Confirmed / Likely / Possible).
    - Recommendation section explicitly answers: "Do Codex hooks remain primary priority for enforcement, or can AGENTS.md carry the load?"
    - If the finding is Possible only, follow-up probes are listed.
  out_of_scope:
    - Changing any enforcement wiring based on the finding — that is a follow-up WorkItem.
  related_artifacts:
    - ART-20260414_1230-ReachReady-processkit-enforcement-research
    - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
    - ART-20260414_1500-ClearSignal-codex-agents-md-reinjection-probe
  assigned_to: ACTOR-junior-researcher
  parent: BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan
---
