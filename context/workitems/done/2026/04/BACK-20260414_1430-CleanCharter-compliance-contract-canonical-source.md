---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260414_1430-CleanCharter-compliance-contract-canonical-source
  legacy_id: BACK-20260414_1430-CleanCharter-compliance-contract-canonical-source
  created: '2026-04-14T14:30:00+00:00'
  labels:
    component: skill-gate
    area: enforcement
spec:
  title: Write the canonical processkit compliance-contract.md under skill-gate/assets/
  state: done
  progress_notes: |
    Created context/skills/processkit/skill-gate/assets/compliance-contract.md (33 lines). Leading <!-- pk-compliance v1 --> marker on line 1. All nine seed rules from §1.1 are present: route_task-first, 1%-rule/skill-finder, same-turn entity creation, MCP-not-hand-edit writes, index-management reads, log-after-state-change, record_decision on accepted recommendation, no-templates-edit, no-hand-edit-harness-config. Rules 1 and 7 from the seed (route_task and skill-finder) are kept as separate rules matching the original seed's intent; no rules dropped or new categories added.
  type: story
  priority: high
  size: S
  description: |
    Create the single versioned source of truth for the processkit compliance contract. Every other enforcement rail (hooks, acknowledge_contract() MCP tool, AGENTS.md header) reads from this one file. 15–30 lines of imperative, stand-alone rules.
  inputs:
  - /workspace/context/artifacts/ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan.md
  - /workspace/context/skills/processkit/skill-gate/SKILL.md
  - /workspace/AGENTS.md  (§ "Project-specific notes" for seed rules)
  deliverables:
  - context/skills/processkit/skill-gate/assets/compliance-contract.md
  success_criteria:
  - File exists at the exact path above.
  - First non-blank line is "<!-- pk-compliance v1 -->" — version marker for hook
    scripts.
  - File is 15–30 lines of prose, each rule on its own line, imperative voice, no
    subheadings beyond "##".
  - Contract covers all eight seed rules listed in §1.1 of the plan artifact.
  - No external links in the body — the file must stand alone when pasted into a hook's
    stdout or a tool response.
  - File is valid UTF-8, LF line endings, hard-wrapped at 80 columns.
  out_of_scope:
  - Wiring the file into any hook or MCP tool (separate WorkItems).
  - Editing AGENTS.md (separate WorkItem: RightPath).
  related_artifacts:
  - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
  related_decisions:
  - DEC-20260414_1430-SteelLatch-enforcement-mcp-tool-description-list
  assigned_to: ACTOR-developer
  parent: BACK-20260414_1245-FirmFoundation-enforcement-implementation-plan
---
