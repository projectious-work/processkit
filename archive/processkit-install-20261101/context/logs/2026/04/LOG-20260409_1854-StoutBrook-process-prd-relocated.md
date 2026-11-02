---
apiVersion: processkit.projectious.work/v2
kind: LogEntry
metadata:
  id: LOG-20260409_1854-StoutBrook-process-prd-relocated
  created: '2026-04-09T18:54:18+00:00'
spec:
  event_type: process.prd_relocated
  timestamp: '2026-04-09T18:54:18+00:00'
  summary: PRD moved to context/artifacts/ as ART-kind-crane, missing sections added
  actor: ACTOR-claude
  subject: ART-20260409_0000-KindCrane-processkit-product-requirements-document
  subject_kind: Artifact
  details:
    from: context/PRD.md
    to: context/artifacts/prd-processkit-2026-04-09.md
    added_sections:
    - status header
    - problem statement
    - goals
    - non-functional requirements
    - split dependencies/open questions
    - appendix
---
