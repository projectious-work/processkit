---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260518_0952-PluckyCedar-add-typed-mcp-repair-tools-for
  created: '2026-05-18T09:52:33+00:00'
spec:
  title: Add typed MCP repair tools for mutable entity contracts
  state: accepted
  decision: Implement scoped MCP repair/update tools for mutable entity contract failures,
    while preserving append-only or event-sourced entities through migrations/correction
    events rather than generic mutation.
  context: User approved implementation after review of MCP create-without-update
    gaps. Binding and Gate surfaces are the immediate gaps, and codify_eval has a
    multi-entity partial-write risk.
  rationale: 'The create_process_instance bug exposed a broader pattern: pk-doctor
    can detect hard contract errors that agents cannot repair through MCP without
    hand-editing entity files. Mutable entities need typed repair surfaces; immutable
    records should keep explicit migration/correction paths.'
  consequences: Binding and Gate get scoped update tools with schema validation and
    event logging. LogEntry remains append-only. Multi-entity creation should validate
    all required payloads before first write where possible.
  decided_at: '2026-05-18T09:52:33+00:00'
---
