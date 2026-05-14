---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260513_1813-PeacefulShell-context-archive-created
  created: '2026-05-13T18:13:12+00:00'
spec:
  event_type: context_archive.created
  timestamp: '2026-05-13T18:13:12+00:00'
  summary: Archived 4 context entities into ARCHIVE-20260513_181306-migration-rejected
  subject: ARCHIVE-20260513_181306-migration-rejected
  subject_kind: Archive
  actor: processkit-context-archiving
  details:
    archive_path: context/archives/2026/05/ARCHIVE-20260513_181306-migration-rejected.tar.gz
    manifest_path: context/archives/2026/05/ARCHIVE-20260513_181306-migration-rejected.json
    entity_ids:
    - MIG-RUNTIME-20260513T180157
    - MIG-20260513T152530
    - MIG-RUNTIME-20260513T152530
    - MIG-DISABLED-HARNESS-STATE
---
