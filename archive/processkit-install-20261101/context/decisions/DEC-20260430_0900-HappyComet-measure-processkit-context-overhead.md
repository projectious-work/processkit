---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260430_0900-HappyComet-measure-processkit-context-overhead
  created: '2026-04-30T09:00:51+00:00'
  updated: '2026-04-30T09:20:29+00:00'
spec:
  title: Measure processkit context overhead with checkpoints
  state: accepted
  decision: Extend context-consumption measurement with user-created checkpoints and
    reports that attribute observed processkit-owned payload changes between two checkpoint
    labels, while clearly separating local estimates from provider-billed token usage.
  context: The existing context_consumption feature reports static processkit footprint.
    The user accepted a design for measuring processkit overhead during a session
    or between two user-chosen checkpoints.
  rationale: Checkpoint snapshots make the feature actionable during real work without
    requiring provider-specific billing telemetry. Exact provider-billed incremental
    tokens remain unavailable unless the harness/provider exposes reliable usage data,
    so reports must label local token counts as estimates and distinguish observed
    processkit payloads from counterfactual overhead.
  alternatives:
  - option: Use provider tokenizers or billing APIs only
    reason_rejected: Not provider-neutral and unavailable in many harnesses.
  - option: Keep only static footprint reporting
    reason_rejected: Does not answer session-level or checkpoint-level overhead questions.
  - option: Add an MCP tool for every measurement operation
    reason_rejected: Additional MCP schema surface increases the context footprint
      being measured.
  consequences: Implement a local checkpoint/report CLI and documentation. Store lightweight
    snapshots under processkit state, avoid sending content to external tokenizers,
    and keep reports provider-neutral with optional future integration for harness
    usage telemetry.
  decided_at: '2026-04-30T09:00:51+00:00'
  related_workitems:
  - BACK-20260430_0918-MightySwan-add-context-consumption-checkpoint-reports
---
