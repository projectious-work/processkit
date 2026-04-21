---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260414_0930-ReliableReach-processkit-enforcement-research
  legacy_id: BACK-20260414_0930-ReliableReach-processkit-enforcement-research
  created: '2026-04-14T09:30:00+00:00'
  labels:
    component: processkit-core
    area: enforcement
    priority_driver: owner-critical
spec:
  title: Research report — why agents ignore processkit, and provider-neutral leverage points
  state: completed
  type: spike
  priority: critical
  description: >
    Produce a research-with-confidence report answering: where do agents
    (Claude Code + OpenAI Codex CLI first, Cursor / OpenCode / Continue /
    Aider as follow-up) actually attend to instructions — prose
    (AGENTS.md / CLAUDE.md), tool-schemas (re-injected every turn), MCP
    tool descriptions, hooks (pre-tool / post-tool), or slash-commands?
    Rank evidence by confidence. Produce 3–5 leverage points that would
    raise processkit adoption across harnesses; split each into
    "works everywhere by design" vs "needs a per-harness adapter".
    Store the report as a processkit Artifact under context/artifacts/.
  related_decisions:
    - DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
  assigned_to: ACTOR-sr-researcher
  owner_note: >
    Kickoff for the three-question improvement plan agreed 2026-04-14.
    Blocks RES-Q2 (team-creator) and FEAT-Q3 (session-onboarding skill).
---

## Progress

- 2026-04-14T12:30Z — Sr Researcher (Opus) delivered report.
  Artifacts:
    - ART-20260414_1230-ReachReady-processkit-enforcement-research.md
      (full 8–15 page report with confidence labels)
    - ART-20260414_1230-ReachReady-processkit-enforcement-research.summary.md
      (one-page executive summary)
  Top 3 leverage points (see summary): (1) ship a pre-merged MCP
  config at install time; (2) SessionStart + UserPromptSubmit hook
  re-injecting a compliance contract; (3) move the 1% rule into MCP
  tool descriptions for `route_task`, `create_workitem`,
  `record_decision`, etc. PM's "tools > prose" hypothesis supported
  (with nuance). Owner's "~70 lines" threshold is folklore in its
  literal form but the underlying context-rot mechanics are real and
  cited. Ready for Sr Architect handoff.
  State → completed.
