---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260421_0730-EagerBird-entity-renamed
  created: '2026-04-21T07:30:07+00:00'
spec:
  event_type: entity.renamed
  timestamp: '2026-04-21T07:30:07+00:00'
  summary: Renamed context/processes/feature-development.md -> context/processes/PROC-feature-development.md
    (and src/ mirror) to match canonical metadata.id prefix. pk-doctor Phase 2 filename
    rename.
  actor: PROC-feature-development
  subject: PROC-feature-development
  subject_kind: Process
  details:
    old_path: context/processes/feature-development.md
    new_path: context/processes/PROC-feature-development.md
    mirror_old: src/context/processes/feature-development.md
    mirror_new: src/context/processes/PROC-feature-development.md
---
