---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260517_1504-TenderPath-scope-processkit-issue-adaptations-to-processkit
  created: '2026-05-17T15:04:42+00:00'
spec:
  title: Scope processkit issue adaptations to processkit-owned policy
  state: accepted
  decision: Accept the processkit adaptation for legacy runtime migration IDs, keep
    binding filename policy strict with rename guidance, and avoid processkit changes
    that encode aibox-specific responsibility.
  context: 'Follow-up to analysis of GitHub issues #60, #61, and #62 received on 2026-05-17.
    User accepted recommendation (1), rejected relaxing policy for (2), and constrained
    (3) to avoid tying processkit to aibox.'
  rationale: The accepted direction is to adapt processkit where processkit owns diagnostic
    policy, but not to relax canonical binding filename rules. Historical role-slot-fill
    binding files should be renamed through an explicit data-fix path with doctor
    warnings and advice. For MCP manifest absence, processkit should only fix release/packaging
    or diagnostic behavior that is processkit-owned; any aibox installer or derived-project
    responsibility should be tracked in the aibox project instead of adding aibox-specific
    coupling to processkit.
  alternatives:
  - option: Relax doctor policy for historical role-slot-fill bindings
    status: rejected
    reason: Would weaken canonical filename policy where explicit data repair is preferred.
  - option: Add aibox-specific special cases inside processkit
    status: rejected
    reason: Creates cross-project coupling outside processkit responsibility.
  consequences: 'Implementation planning should update #60 recommendations to preserve
    warnings and provide migration/rename advice. #61 should be split by responsibility:
    verify processkit release payload contains the manifest and file an aibox issue
    if the installer/derived install path drops or fails to consume it.'
  decided_at: '2026-05-17T15:04:42+00:00'
---
