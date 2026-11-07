---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260514_0841-ActiveGrove-implement-rag-assisted-id-vocabulary
  created: '2026-05-14T08:41:28+00:00'
  labels:
    area: id-management
    architecture: rag-assisted-allocation
    decision:
    - DEC-20260514_0834-AlertShell-adopt-tagged-vocabulary-pools-and-high
    - DEC-20260514_0841-FairOasis-use-rag-assisted-allocation-for-semantic
  updated: '2026-05-14T08:52:05+00:00'
spec:
  title: Implement RAG-assisted ID vocabulary allocation
  state: done
  type: task
  priority: medium
  description: |
    Plan:
    1. Add a structured vocabulary registry for tagged adjective and noun pools plus allocation modes.
    2. Extend id generation to select palettes from entity kind, stable subtype, and ID intent text while preserving backward-compatible formats.
    3. Add lexical-token extraction/reservation support so human shorthand can be checked globally, not only by full ID per kind.
    4. Reuse index-management sqlite/sqlite-vec primitives for semantic ID intent and vocabulary ranking rather than adding a disconnected vector store.
    5. Add pk-doctor and test coverage for palette capacity, ambiguous shorthand, blocked words, and high-volume three-token modes.
    6. Update id-management documentation and mirror shipped src/context changes as needed.
  started_at: '2026-05-14T08:41:37+00:00'
  completed_at: '2026-05-14T08:52:05+00:00'
---

## Transition note (2026-05-14T08:41:37+00:00)

Starting implementation of the accepted RAG-assisted ID vocabulary allocation plan.


## Transition note (2026-05-14T08:51:47+00:00)

Implementation complete; focused tests and id_vocabulary doctor check pass.


## Transition note (2026-05-14T08:52:05+00:00)

Implementation complete and verified with focused pytest, id-management validation import smoke, py_compile, and pk-doctor --category=id_vocabulary.
