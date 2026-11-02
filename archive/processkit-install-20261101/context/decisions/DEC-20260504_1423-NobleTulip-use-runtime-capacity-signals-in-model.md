---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260504_1423-NobleTulip-use-runtime-capacity-signals-in-model
  created: '2026-05-04T14:23:02+00:00'
spec:
  title: Use runtime capacity signals in model planning
  state: accepted
  decision: Add a provider-neutral runtime-capacity concept to model planning so agents
    can incorporate subscription or quota signals when recommending model effort,
    model class, and parallelism.
  context: Codex exposes subscription/usage information interactively via /status,
    and Claude Code exposes session cost or reset-limit signals in documented interactive
    flows, but neither is reliably available today as a stable processkit MCP input.
  rationale: Capacity should be modeled as optional observed data rather than guessed
    from provider pricing. When available, remaining quota/reset windows can drive
    concrete planning changes such as using fast models, limiting subagents, warning
    about large tasks, or waiting for reset.
  consequences: Model-recommender should accept explicit runtime-capacity observations,
    expose planning guidance, and stay conservative when capacity data is unknown
    or low-confidence.
  related_workitems:
  - BACK-20260504_1422-SmoothWolf-router-sqlite-vec-capacity-spark-release
  decided_at: '2026-05-04T14:23:02+00:00'
---
