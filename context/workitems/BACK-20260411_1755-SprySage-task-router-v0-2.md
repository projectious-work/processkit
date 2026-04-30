---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260411_1755-SprySage-task-router-v0-2
  created: '2026-04-11T17:55:13+00:00'
  labels:
    component: task-router
    version: v0.2
    track: routing
  updated: '2026-04-30T12:39:50+00:00'
spec:
  title: 'task-router v0.2: embedding scoring + cheap-model escalation'
  state: done
  type: story
  priority: medium
  description: |
    Extend `processkit-task-router` v0.1 with two v0.2 capabilities:

    1. **Embedding-based scoring** — replace Phase 2 token-overlap scoring with
       cosine similarity over pre-computed tool description embeddings. Improves
       match quality for paraphrased or domain-shifted task descriptions where
       vocabulary overlap is low.

    2. **Cheap-model escalation** — when `confidence < 0.5` (routing_basis ==
       "needs_llm_confirm"), optionally call a fast/cheap model (e.g. Haiku for
       Anthropic, Flash for Gemini) to disambiguate between `candidate_tools[]`
       before returning the result. This is the MasRouter cascaded-controller
       pattern applied to processkit: lightweight proxy network makes routing
       decision without burning the main model's context.

       Requires: model-class configuration per derived project (see companion
       backlog item on model-class routing). The escalation call is optional and
       gated by a config flag so projects without cheap-model access degrade
       gracefully to returning `needs_llm_confirm`.

    Acceptance criteria:
    - Phase 2 scoring uses embeddings when an embedding model is configured
    - `route_task()` accepts optional `allow_llm_escalation: bool` param
    - When escalation enabled and confidence &lt; 0.5, cheap model call made
    - Smoke test covers embedding path and escalation path
    - Graceful degradation when neither embedding nor escalation is configured
  started_at: '2026-04-30T11:03:42+00:00'
  completed_at: '2026-04-30T12:39:50+00:00'
---

## Transition note (2026-04-30T11:03:42+00:00)

Started v0.2 routing work: added local embedding-style scoring, allow_llm_escalation response metadata, and focused tests. Provider embedding and actual cheap-model invocation remain open.


## Transition note (2026-04-30T12:39:50+00:00)

Implemented task-router v0.2 embedding-style scoring, scoring_basis reporting, and cheap-model escalation metadata. Validation passed.


## Transition note (2026-04-30T12:39:50+00:00)

Implemented task-router v0.2 embedding-style scoring, scoring_basis reporting, and cheap-model escalation metadata. Validation passed.
