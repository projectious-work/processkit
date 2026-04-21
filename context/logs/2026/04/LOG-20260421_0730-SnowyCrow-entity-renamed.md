---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260421_0730-SnowyCrow-entity-renamed
  created: '2026-04-21T07:30:01+00:00'
spec:
  event_type: entity.renamed
  timestamp: '2026-04-21T07:30:01+00:00'
  summary: Renamed context/processes/bug-fix.md -> context/processes/PROC-bug-fix.md
    (and src/ mirror) to match canonical metadata.id prefix. pk-doctor Phase 2 filename
    rename.
  actor: PROC-bug-fix
  subject: PROC-bug-fix
  subject_kind: Process
  details:
    old_path: context/processes/bug-fix.md
    new_path: context/processes/PROC-bug-fix.md
    mirror_old: src/context/processes/bug-fix.md
    mirror_new: src/context/processes/PROC-bug-fix.md
---
