---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260510_0740-WildBrook-context-archive-created
  created: '2026-05-10T07:40:53+00:00'
spec:
  event_type: context_archive.created
  timestamp: '2026-05-10T07:40:53+00:00'
  summary: Archived 9 context entities into ARCHIVE-20260510_074047-migration-applied
  subject: ARCHIVE-20260510_074047-migration-applied
  subject_kind: Archive
  actor: processkit-context-archiving
  details:
    archive_path: context/archives/2026/05/ARCHIVE-20260510_074047-migration-applied.tar.gz
    manifest_path: context/archives/2026/05/ARCHIVE-20260510_074047-migration-applied.json
    entity_ids:
    - MIG-LOCK-20260509T112052
    - MIG-RUNTIME-20260509T112052
    - MIG-RUNTIME-20260508T132832
    - MIG-RUNTIME-20260508T083035
    - MIG-RUNTIME-20260507T191658
    - MIG-RUNTIME-20260506T021335
    - MIG-20260505T165732
    - MIG-RUNTIME-20260505T165731
    - MIG-RUNTIME-20260504T145520
---
