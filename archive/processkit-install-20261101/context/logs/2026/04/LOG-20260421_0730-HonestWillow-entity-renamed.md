---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260421_0730-HonestWillow-entity-renamed
  created: '2026-04-21T07:30:03+00:00'
spec:
  event_type: entity.renamed
  timestamp: '2026-04-21T07:30:03+00:00'
  summary: Renamed context/processes/release.md -> context/processes/PROC-release.md
    (and src/ mirror) to match canonical metadata.id prefix. pk-doctor Phase 2 filename
    rename.
  actor: PROC-release
  subject: PROC-release
  subject_kind: Process
  details:
    old_path: context/processes/release.md
    new_path: context/processes/PROC-release.md
    mirror_old: src/context/processes/release.md
    mirror_new: src/context/processes/PROC-release.md
---
