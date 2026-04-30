---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260420_1340-StoutLeaf-decision-re-recorded
  created: '2026-04-20T13:40:47+00:00'
spec:
  event_type: decision.re-recorded
  timestamp: '2026-04-20T13:40:47+00:00'
  summary: Re-recorded DEC-20260417_1800-CapabilityProfileRouting-three-layer-model-selection
    via record_decision MCP as DEC-20260420_1340-QuietLark-adopt-a-three-layer. Original
    hand-written file deleted to avoid duplicate entities. CLEANUP-REQUIRED marker
    resolved.
  actor: ACTOR-pm-claude
  subject: DEC-20260420_1340-QuietLark-adopt-a-three-layer
  subject_kind: DecisionRecord
  details:
    superseded_file: DEC-20260417_1800-CapabilityProfileRouting-three-layer-model-selection.md
    original_decision_date: '2026-04-17T18:00:00Z'
    reason: Original file had CLEANUP-REQUIRED comment on line 1 pushing YAML frontmatter
      off line 1; index parser skipped it (get_decision returned not-found). Re-recorded
      through MCP to restore schema validation + event-log auto-entry.
---
