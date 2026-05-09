---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1836-TidyAsh-roleslot-primitive-identity-axis-decoupling
  created: '2026-05-09T18:36:59+00:00'
  labels:
    github_issue_parent: 20
    area: team-creator
    cluster: team-model-v2
    epic_sub: SUB-1
    design_artifact_ref: ART-20260509_1836-SmartPanda-team-creator-v2-design
    effort: large
    model_class: deep
    owner_role: ROLE-software-engineer/senior
    blocked_until: open-questions-1-2-3
spec:
  title: 'team-creator v2 SUB-1: RoleSlot primitive + identity-axis decoupling'
  state: backlog
  type: task
  priority: high
  description: 'Foundational sub-item of VastVale (gh#20). Add SCHEMA-roleslot v1.0.0
    to src/context/schemas/. Extend team-manager MCP server with create_role_slot,
    get_role_slot, list_role_slots, fill_role_slot, close_role_slot. Add role-slot-fill
    to binding.yaml known_types. Migration: write RoleSlots derived from current clone_cap;
    back-fill role-slot-fill Bindings. Update get_interlocutor_runtime_binding resolver
    to traverse RoleSlot before falling through 8-layer model-assignment binding precedence.
    Effort: large. Owner role: ROLE-software-engineer/senior. Model class: deep. Depends
    on: nothing. UNBLOCKS: SUB-2, SUB-3, SUB-4. Architectural reference: ART-20260509_1836-SmartPanda-team-creator-v2-design.
    BLOCKED until owner answers open questions 1, 2, 3 (RoleSlot ownership skill;
    v0.16.0 fields cleanup; personality/memory on consultants).'
  parent: BACK-20260509_1318-VastVale-team-creator-v2-5-design-gaps
---
