---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: ARCH-20260414_1245-FirmFoundation-enforcement-implementation-plan
  created: '2026-04-14T12:45:00+00:00'
  labels:
    component: processkit-core
    area: enforcement
    priority_driver: owner-critical
spec:
  title: Implementation plan — processkit enforcement (hooks + acknowledge-contract hybrid)
  state: in-progress
  type: architecture
  priority: critical
  description: >
    Consume the Sr Researcher's report
    (ART-20260414_1230-ReachReady) and design the implementation.
    Approach agreed with owner: wire hook-based enforcement on
    harnesses that support it (Claude Code, Codex CLI), layer a
    provider-neutral acknowledge_contract() MCP tool on top. Also
    produce a responsibility split: what is processkit's job vs
    what belongs in aibox (installer, sync, harness wiring).
    Output: developer-sized WorkItems, a DecisionRecord locking
    the list of MCP tools getting in-description 1%-rule text,
    and a list of issues to file upstream to aibox.
  related_artifacts:
    - ART-20260414_1230-ReachReady-processkit-enforcement-research
    - ART-20260414_0935-AuditSurface-mcp-enforcement-surface
  related_decisions:
    - DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
  assigned_to: ACTOR-sr-architect
  blocks:
    - FEAT-Q3-session-onboarding   # not yet filed
    - RES-Q2-team-creator          # not yet filed
---
