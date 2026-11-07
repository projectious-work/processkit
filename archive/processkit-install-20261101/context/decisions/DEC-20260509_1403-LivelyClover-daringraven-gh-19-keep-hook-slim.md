---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260509_1403-LivelyClover-daringraven-gh-19-keep-hook-slim
  created: '2026-05-09T14:03:49+00:00'
spec:
  title: 'DaringRaven (gh#19): keep hook, slim contract; reject rec 1 migration'
  state: accepted
  decision: Reject DaringRaven rec 1 (migrate compliance contract from per-turn UserPromptSubmit
    hook to once-per-session compliance-refresh skill). Accept rec 4 (keep the per-turn
    hook but slim the contract injected on every prompt to 3 absolute non-negotiables
    + 1 positive-actions reference). Recs 2, 3, 5, 6, 7 proceed as planned.
  context: DaringRaven (gh#19) recommendation 1 was flagged in ART-DeepSpruce as needing
    explicit owner approval before implementation, not just at the WorkItem boundary.
    Asked at NobleLeaf-dispatch time so the answer is in by Wave 3c kickoff.
  rationale: 'Owner judgment: load-bearing nature of the contract makes once-per-session
    loading too risky (long sessions can compress the contract out of effective context,
    leading to silent mid-session compliance drift). Slim-but-persistent injection
    preserves the safety floor while reclaiming most of the per-turn token tax.'
  consequences: 'Wave 3c scope: implement rec 4 (slim hook) instead of rec 1 (migrate).
    Slim target: 3 non-negotiables (acknowledge_contract on session start; route_task
    before write-side tools; find_skill before domain work) + 1 positive-actions reference.
    Full positive-actions content stays in compliance-contract.md (NobleLeaf 50-line
    version) but is loaded by reference, not pasted on every turn. Implementation
    must define the slim/full split mechanism (separate file, marker-based extraction,
    or section anchors).'
  deciders:
  - TEAMMEMBER-thrifty-otter
  related_workitems:
  - BACK-20260509_1317-DaringRaven-make-processkit-regulations-louder-in-claude
  - BACK-20260509_1317-NobleLeaf-rebalance-compliance-contract-sentiment-to-positive
  decided_at: '2026-05-09T14:03:49+00:00'
---
