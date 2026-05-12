---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260512_0532-ZestfulRobin-context-archive-created
  created: '2026-05-12T05:32:59+00:00'
spec:
  event_type: context_archive.created
  timestamp: '2026-05-12T05:32:59+00:00'
  summary: Archived 2 context entities into ARCHIVE-20260512_053252-migration-rejected
  subject: ARCHIVE-20260512_053252-migration-rejected
  subject_kind: Archive
  actor: processkit-context-archiving
  details:
    archive_path: context/archives/2026/05/ARCHIVE-20260512_053252-migration-rejected.tar.gz
    manifest_path: context/archives/2026/05/ARCHIVE-20260512_053252-migration-rejected.json
    entity_ids:
    - MIG-20260512T052703
    - MIG-RUNTIME-20260512T052703
---
