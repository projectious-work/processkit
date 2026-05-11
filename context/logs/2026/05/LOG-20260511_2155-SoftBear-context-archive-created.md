---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260511_2155-SoftBear-context-archive-created
  created: '2026-05-11T21:55:06+00:00'
spec:
  event_type: context_archive.created
  timestamp: '2026-05-11T21:55:06+00:00'
  summary: Archived 4 context entities into ARCHIVE-20260511_215500-migration-applied
  subject: ARCHIVE-20260511_215500-migration-applied
  subject_kind: Archive
  actor: processkit-context-archiving
  details:
    archive_path: context/archives/2026/05/ARCHIVE-20260511_215500-migration-applied.tar.gz
    manifest_path: context/archives/2026/05/ARCHIVE-20260511_215500-migration-applied.json
    entity_ids:
    - MIG-RUNTIME-20260511T213352
    - MIG-RUNTIME-20260511T212429
    - MIG-RUNTIME-20260510T151433
    - MIG-RUNTIME-DRIFT-20260510T151433
---
