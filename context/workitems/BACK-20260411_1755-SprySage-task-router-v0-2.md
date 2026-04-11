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
spec:
  title: 'task-router v0.2: embedding scoring + cheap-model escalation'
  state: backlog
  type: story
  priority: medium
  description: "Extend `processkit-task-router` v0.1 with two v0.2 capabilities:\n\
    \n1. **Embedding-based scoring** — replace Phase 2 token-overlap scoring with\n\
    \   cosine similarity over pre-computed tool description embeddings. Improves\n\
    \   match quality for paraphrased or domain-shifted task descriptions where\n\
    \   vocabulary overlap is low.\n\n2. **Cheap-model escalation** — when `confidence\
    \ < 0.5` (routing_basis ==\n   \"needs_llm_confirm\"), optionally call a fast/cheap\
    \ model (e.g. Haiku for\n   Anthropic, Flash for Gemini) to disambiguate between\
    \ `candidate_tools[]`\n   before returning the result. This is the MasRouter cascaded-controller\n\
    \   pattern applied to processkit: lightweight proxy network makes routing\n \
    \  decision without burning the main model's context.\n\n   Requires: model-class\
    \ configuration per derived project (see companion\n   backlog item on model-class\
    \ routing). The escalation call is optional and\n   gated by a config flag so\
    \ projects without cheap-model access degrade\n   gracefully to returning `needs_llm_confirm`.\n\
    \nAcceptance criteria:\n- Phase 2 scoring uses embeddings when an embedding model\
    \ is configured\n- `route_task()` accepts optional `allow_llm_escalation: bool`\
    \ param\n- When escalation enabled and confidence &lt; 0.5, cheap model call made\n\
    - Smoke test covers embedding path and escalation path\n- Graceful degradation\
    \ when neither embedding nor escalation is configured"
---
