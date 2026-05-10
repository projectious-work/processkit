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
  updated: '2026-05-10T03:46:08+00:00'
spec:
  title: 'team-creator v2 SUB-1: RoleSlot primitive + identity-axis decoupling'
  state: done
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
  started_at: '2026-05-09T21:27:36+00:00'
  completed_at: '2026-05-10T03:46:08+00:00'
---

## Transition note (2026-05-09T21:27:36+00:00)

Wave 4 SUB-1 dispatch — TEAMMEMBER-finn (ROLE-software-engineer/senior) on Sonnet 4.5. Foundational RoleSlot primitive + identity-axis decoupling. Working on a fresh branch off main; PR #24 (the cluster work-down) is the immediate ancestor for context, but SUB-1 lands as a separate PR.


## Transition note (2026-05-09T21:42:45+00:00)

SUB-1 Phase A shipped on Sonnet 4.5 senior. SCHEMA-roleslot v1.0.0 (165 lines); binding.yaml gains role-slot-fill type; _lib/processkit indexes RoleSlot; team-manager MCP server gains 5 tools (create_role_slot, get_role_slot, list_role_slots, fill_role_slot, close_role_slot) + _roleslot_pre_step resolver hook (purely additive, 8 layers untouched); migration 20260509_2139_0.25.8-to-0.26.0.md (state=pending, full-feasibility rollback). 11 new tests, 68/68 pass on both src/ and context/ trees. NOTABLE FINDING: v0.16.0 fields (clone_cap, cap_escalation, is_template, templated_from, primary_contact) are NOT in schemas — they were already removed. The doc cleanup falls naturally to SUB-2 (LuckyWren) which deletes the archetype-Role write step. RoleSlot.default_model_profile surfaces in resolver response but is NOT yet wired to Layer 8 of model-recommender — deeper change deferred (out of "do not reshape 8 layers" scope). Branch: feat/sub-1-roleslot-primitive (off feat/gh-issue-cluster-2026-05-09, PR #24).


## Transition note (2026-05-10T03:46:08+00:00)

Shipped to main on 2026-05-09 via PR #27; closing per v0.26.0 release prep.
