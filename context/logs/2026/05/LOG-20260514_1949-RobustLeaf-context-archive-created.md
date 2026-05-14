---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260514_1949-RobustLeaf-context-archive-created
  created: '2026-05-14T19:49:24+00:00'
spec:
  event_type: context_archive.created
  timestamp: '2026-05-14T19:49:24+00:00'
  summary: Archived 2 context entities into ARCHIVE-20260514_194917-migration-applied
  subject: ARCHIVE-20260514_194917-migration-applied
  subject_kind: Archive
  actor: processkit-context-archiving
  details:
    archive_path: context/archives/2026/05/ARCHIVE-20260514_194917-migration-applied.tar.gz
    manifest_path: context/archives/2026/05/ARCHIVE-20260514_194917-migration-applied.json
    entity_ids:
    - MIG-20260514T193936
    - MIG-RUNTIME-20260514T193936
---
