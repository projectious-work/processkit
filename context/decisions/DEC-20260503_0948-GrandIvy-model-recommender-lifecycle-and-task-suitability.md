---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260503_0948-GrandIvy-model-recommender-lifecycle-and-task-suitability
  created: '2026-05-03T09:48:40+00:00'
spec:
  title: Model Recommender Lifecycle And Task Suitability
  state: accepted
  decision: Model entries stay in the roster while the provider still offers them.
    Routing distinguishes active, legacy, deprecated, retired, and unverified lifecycle
    states, and adds task-class suitability metadata so older or cheaper models can
    remain useful for suitable work instead of being removed from recommendations
    globally.
  context: The model market refresh found that availability, ranking, and task fit
    need to be tracked separately. The user approved implementing a deeper model-recommender
    refresh with broad provider coverage and a 30-50 class task taxonomy.
  rationale: Provider model catalogs now change faster than a single ranked list can
    represent. Lifecycle status prevents accidental deletion of still-callable models,
    while task-class suitability lets routing choose frontier models only where their
    cost and capability are justified.
  consequences: The roster schema gains lifecycle and task suitability metadata. MCP
    query/profile/list outputs should surface lifecycle; routing can filter or rank
    by task class. Retired models should be excluded from active routing but can remain
    in archive/changelog material. Provider claims must be sourced and revisited during
    roster refreshes.
  decided_at: '2026-05-03T09:48:40+00:00'
---
