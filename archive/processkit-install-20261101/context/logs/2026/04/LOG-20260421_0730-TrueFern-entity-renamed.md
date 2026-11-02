---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260421_0730-TrueFern-entity-renamed
  created: '2026-04-21T07:30:05+00:00'
spec:
  event_type: entity.renamed
  timestamp: '2026-04-21T07:30:05+00:00'
  summary: Renamed context/processes/code-review.md -> context/processes/PROC-code-review.md
    (and src/ mirror) to match canonical metadata.id prefix. pk-doctor Phase 2 filename
    rename.
  actor: PROC-code-review
  subject: PROC-code-review
  subject_kind: Process
  details:
    old_path: context/processes/code-review.md
    new_path: context/processes/PROC-code-review.md
    mirror_old: src/context/processes/code-review.md
    mirror_new: src/context/processes/PROC-code-review.md
---
