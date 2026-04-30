---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260414_1434-RightPath-agents-md-compliance-header
  legacy_id: BACK-20260414_1434-RightPath-agents-md-compliance-header
  created: '2026-04-14T14:34:00+00:00'
  labels:
    component: agents-md
    area: enforcement
spec:
  title: Re-layer AGENTS.md with a compliance-contract header block (canonical + scaffolding)
  state: done
  type: story
  priority: medium
  size: S
  description: |
    Move the compliance-contract body to the top of AGENTS.md inside a versioned marker block so the primacy region carries the rules. No further trimming — position is the binding constraint, not size, per the research report. Edit both /workspace/AGENTS.md (rendered project file) and /workspace/src/AGENTS.md (scaffolding template).
  inputs:
  - /workspace/context/artifacts/ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan.md  (§1.5)
  - /workspace/AGENTS.md
  - /workspace/src/AGENTS.md
  - depends-on: BACK-20260414_1430-CleanCharter-compliance-contract-canonical-source
  deliverables:
  - Updated /workspace/AGENTS.md with the header block.
  - Updated /workspace/src/AGENTS.md with the same block (token-compatible with its
    {{PLACEHOLDER}} scheme).
  marker_shape: |
    <!-- pk-compliance-contract v1 BEGIN -->
    ... verbatim body of context/skills/processkit/skill-gate/assets/compliance-contract.md ...
    <!-- pk-compliance-contract v1 END -->
  success_criteria:
  - The block appears immediately after the AGENTS.md title (within the first 40 lines),
    not buried mid-document.
  - The block contents match the canonical compliance-contract.md byte-for-byte (excluding
    the version marker line that lives in the contract itself).
  - All existing AGENTS.md content is preserved below the block; no trimming beyond
    removing duplicate rule phrasings now covered verbatim in the block.
  - The scaffolding template at src/AGENTS.md uses the same BEGIN/END markers so aibox
    can substitute or re-sync the block.
  - '`grep -c "1% rule" AGENTS.md` returns >=1; the literal string is present.'
  out_of_scope:
  - Editing AGENTS.md for any reason other than the header insertion and minimal de-duplication.
  - Any change under context/templates/ (read-only mirror).
  related_artifacts:
  - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
  assigned_to: ACTOR-developer
  parent: BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan
  progress_notes:
  - date: '2026-04-14'
    actor: ACTOR-developer
    note: |
      Inserted <!-- pk-compliance-contract v1 BEGIN/END --> block verbatim from context/skills/processkit/skill-gate/assets/compliance-contract.md (real file, CleanCharter had already landed) immediately after the title line in both /workspace/AGENTS.md and /workspace/src/AGENTS.md. All existing content preserved below the block. State transitioned backlog→done.
---
