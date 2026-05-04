---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260504_1423-ShinyRiver-add-gpt-5-3-codex-spark
  created: '2026-05-04T14:23:11+00:00'
spec:
  title: Add GPT-5.3-Codex-Spark to fast Codex routing
  state: accepted
  decision: Represent GPT-5.3-Codex-Spark as a first-class OpenAI model candidate
    and include it in fast Codex-oriented code routing for bounded agent side tasks.
  context: The local Codex model catalog exposes slug gpt-5.3-codex-spark, but processkit
    model artifacts and profiles do not currently include it, leaving its separate
    subscription capacity unused by model planning.
  rationale: Spark should be available for low-token, bounded, fast code tasks and
    subagent-style work when the harness can call OpenAI Codex models, while stronger
    models remain preferred for high-risk design, deep implementation, and review.
  consequences: Add a model-spec artifact/projection for GPT-5.3-Codex-Spark, update
    code-fast/profile routing, and keep the model class/effort metadata distinct from
    flagship Codex models.
  related_workitems:
  - BACK-20260504_1422-SmoothWolf-router-sqlite-vec-capacity-spark-release
  decided_at: '2026-05-04T14:23:11+00:00'
---
