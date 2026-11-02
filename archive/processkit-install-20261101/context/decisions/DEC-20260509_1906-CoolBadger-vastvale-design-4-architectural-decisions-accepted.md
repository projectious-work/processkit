---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260509_1906-CoolBadger-vastvale-design-4-architectural-decisions-accepted
  created: '2026-05-09T19:06:10+00:00'
spec:
  title: VastVale design — 4 architectural decisions accepted
  state: accepted
  decision: 'Owner accepts all four architect recommendations from ART-20260509_1836-SmartPanda
    design synthesis: (Q1) RoleSlot primitive ships INSIDE the existing team-manager
    skill, NOT as a new slot-management skill. (Q2) v0.16.0 capacity fields (clone_cap,
    cap_escalation, is_template, templated_from, primary_contact) are REMOVED cleanly
    from Role/TeamMember schemas at v2.2.0 after a one-minor-version deprecation window;
    primary_contact=true semantics migrate to RoleSlot.rank=1. (Q3) Consultants use
    the SAME TeamMember schema as persistent members; type=consultant + engaged_for
    + engagement_window are the only differentiators; export_policy.include defaults
    to [persona, card] only to prevent memory leakage between engagements. (Q5) Budget
    unit-cost source: LIVE model-recommender.get_pricing call at charter time, snapshot
    the resolved value into slot_projections[].unit_cost_usd; pk-team-review recomputes
    actuals against live pricing at review time so drift captures both volume AND
    price changes.'
  context: Asked at SUB-1 dispatch boundary. Q1/Q2/Q3 unblock SUB-1 (BACK-TidyAsh
    — RoleSlot primitive); Q5 unblocks SUB-4 (BACK-SwiftReef — budget projection).
    Q4 (auto-deactivate consultants on Scope close) and Q6 (ROLE-assistant archetype
    target) were NOT asked because their recommendations were unambiguous and unblocking;
    defer if owner wants to push back.
  rationale: 'Owner judgment: each recommendation aligned with established project
    values — no skill inflation (Q1, matches feedback_no_skill_inflation memory);
    minimize long-term schema dead weight (Q2); single-source-of-truth for identity
    (Q3); maximum drift visibility for capacity planning (Q5). Architect''s recommendations
    were all default-acceptable; no contrarian path warranted further investigation.'
  consequences: |
    SUB-1 (TidyAsh) becomes dispatch-eligible. SUB-3 (RapidLily) and SUB-4 (SwiftReef) inherit SUB-1's schema-shape decisions. SUB-2 (LuckyWren) only blocked on Q6 which is ambient. Implementation order remains: SUB-1 → SUB-2 → SUB-3 → SUB-4. SUB-5 (MerryPlum) shipped this turn.</consequences>
    <parameter name="deciders">["TEAMMEMBER-thrifty-otter"]
  related_workitems:
  - BACK-20260509_1318-VastVale-team-creator-v2-5-design-gaps
  - BACK-20260509_1836-TidyAsh-roleslot-primitive-identity-axis-decoupling
  - BACK-20260509_1837-RapidLily-consultant-type-engagement-window-resolver
  - BACK-20260509_1837-SwiftReef-budget-projection-charter-drift-detection
  decided_at: '2026-05-09T19:06:10+00:00'
---
