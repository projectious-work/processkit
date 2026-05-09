---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1317-NobleLeaf-rebalance-compliance-contract-sentiment-to-positive
  created: '2026-05-09T13:17:41+00:00'
  labels:
    github_issue: 18
    area: compliance
    cluster: agent-dispatch
  updated: '2026-05-09T14:04:05+00:00'
spec:
  title: Rebalance compliance contract sentiment to positive imperatives (gh#18)
  state: review
  type: task
  priority: high
  description: 'Triaged from GH #18. Current `compliance-contract.md` has 9 negative
    imperatives, 0 positive scheduled actions; agents pattern-match the whole block
    as "things-to-avoid" and skip positive guidance buried in skill bodies. Proposals:\n1.
    Aim for ~50/50 positive/negative imperative balance\n2. Add explicit session-start
    positive checks (e.g. "call get_active_interlocutor before any briefing")\n3.
    Visually/lexically separate `<positive-actions>` from `<rules>`\n4. Audit existing
    rules for negative→positive rewrites (action-first phrasing)\n\nWidely-observed
    LLM pattern, not Claude-specific. Pairs with gh#17 (which positive imperatives
    to add) and gh#19 (Claude Code surface).'
  started_at: '2026-05-09T13:57:10+00:00'
---

## Transition note (2026-05-09T13:57:10+00:00)

Wave 3a dispatch — ephemeral ROLE-ai-research-scientist/senior on Opus 4.7 picking it up. Brief includes WildPanda P1 placeholder marker requirement, ≤60-line cap, ~50/50 balance target.


## Transition note (2026-05-09T14:04:05+00:00)

Contract rewrite landed. 50 lines (under 60 cap). 5 sections: On session start / Tool routing / Entity writes / Decisions / Prohibitions. 10 positive : 4 negative imperatives (skews more positive than 50/50; agent justified as matching the WorkItem's "name desired behaviors first" framing). All 10 original rules preserved. WildPanda P1 placeholder at line 12: `&lt;!-- TODO(WildPanda P1): sub-agent-dispatch clause --&gt;`. Both trees byte-identical. Note: per DaringRaven rec 4 decision, this 50-line full contract will become the canonical reference; the per-turn hook will inject a 3+1-line slim version against this same file (or a derived slim file) — implementation TBD in Wave 3c.
