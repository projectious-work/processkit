---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260523_0331-CleverHarvest-context-archive-created
  created: '2026-05-23T03:31:46+00:00'
spec:
  event_type: context_archive.created
  timestamp: '2026-05-23T03:31:46+00:00'
  summary: Archived 3 context entities into ARCHIVE-20260523_033140-migration-applied
  subject: ARCHIVE-20260523_033140-migration-applied
  subject_kind: Archive
  actor: processkit-context-archiving
  details:
    archive_path: context/archives/2026/05/ARCHIVE-20260523_033140-migration-applied.tar.gz
    manifest_path: context/archives/2026/05/ARCHIVE-20260523_033140-migration-applied.json
    entity_ids:
    - MIG-20260522T192406
    - MIG-20260515T184054
    - MIG-RUNTIME-20260515T184054
---
