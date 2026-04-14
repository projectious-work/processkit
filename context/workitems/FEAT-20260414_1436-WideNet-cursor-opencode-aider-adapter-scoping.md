---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: FEAT-20260414_1436-WideNet-cursor-opencode-aider-adapter-scoping
  created: '2026-04-14T14:36:00+00:00'
  labels:
    component: harness-adapters
    area: enforcement
spec:
  title: Scope processkit-side content requirements for Cursor / OpenCode / Aider adapters
  state: done
  type: research
  priority: low
  size: S
  description: >
    For the three follow-up harnesses named in the research report,
    produce a capability matrix (prose surface / MCP / hooks) and
    decide what, if anything, processkit must ship beyond the canonical
    compliance contract to support them. Every installer / wiring step
    identified here becomes an aibox issue, not processkit work.
  inputs:
    - /workspace/context/artifacts/ART-20260414_1230-ReachReady-processkit-enforcement-research.md  (§4.3)
    - /workspace/context/artifacts/ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan.md  (§1.6, §2.5)
    - https://docs.cursor.com/context/rules
    - https://opencode.ai/docs/rules/
    - https://aider.chat/docs/usage/conventions.html
  deliverables:
    - context/artifacts/ART-<DATE>-<WORD>-cursor-opencode-aider-capability-matrix.md — one-page matrix per harness covering prose surface, MCP client, hook points, known limitations.
    - One GitHub issue body drafted (NOT filed) per harness needing an aibox-side adapter, appended to the artifact.
  success_criteria:
    - Capability matrix artifact is registered via create_artifact.
    - Each harness has an explicit answer to "Does processkit need to ship a new file, or is the canonical compliance-contract.md sufficient?"
    - At least three aibox-issue bodies drafted (one per harness) unless a harness is found to need no adapter at all; in that case the artifact documents why.
  out_of_scope:
    - Filing the aibox issues (owner decision).
    - Building any adapter code in processkit. If a harness needs processkit content that does not yet exist, scope a follow-up WorkItem — do not implement it in this one.
  related_artifacts:
    - ART-20260414_1230-ReachReady-processkit-enforcement-research
    - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
    - ART-20260414_1545-SharpGrid-follow-up-harness-capability-matrix
  assigned_to: ACTOR-junior-researcher
  parent: ARCH-20260414_1245-FirmFoundation-enforcement-implementation-plan
  progress_notes: |
    2026-04-14 — Research complete. Capability matrix produced as
    ART-20260414_1545-SharpGrid-follow-up-harness-capability-matrix.
    Key findings: Cursor gained hook support (v1.7, Oct 2025) — issue
    #47 needs splitting into rules/MCP and hooks wiring; sessionStart
    context injection is buggy on Cursor. Aider has no MCP client and
    no hooks — prose-only ceiling confirmed. OpenCode MCP hooks bypass
    bug (#2319) makes structural enforcement impossible until upstream
    fix. Five issue draft bodies produced (A–E). No processkit-side
    new files needed; all work is aibox installer work.
---
