---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260420_1340-QuietLark-adopt-a-three-layer
  created: '2026-04-20T13:40:18+00:00'
spec:
  title: Adopt a three-layer model-selection architecture — catalog / preferences
    / role standard sets — and bind roles to capability profiles instead of model
    SKUs
  state: accepted
  decision: |
    Replace the single `preferences.model = "claude-opus-4-6"` binding on each Actor with a three-layer architecture:

    Layer A — Model catalog (what exists). Curated registry of models the project cares about, with versions, effort tiers, pricing, capability scores. Lives inside the `model-recommender` skill (`context/skills/processkit/model-recommender/`) and is refreshed via Workflow C (`/pk-model-refresh`). Informed by `aibox.toml`'s declared providers plus owner-driven additions.

    Layer B — Project / owner preferences (what this project can use). Subscription tier, available API keys, cost bias, preferred ordering, and default thinking policy. Owned by the model-recommender skill's `set_config` / `get_config` MCP tools, populated via Workflow D (`/pk-model-setup`). No parallel preferences file.

    Layer C — Role standard sets (what this role needs). Each `Role` entity carries a ranked `model_profiles` array — equivalent option-sets keyed by `rank`, each naming provider + family + default_version + default_effort + rationale. `rank: 1` is the primary; lower ranks are fallbacks when Layer B filters out the primary, when rate-limited, or when task specifics favour a different option (Computer Use → OpenAI; 2M context → Grok; long-document analysis → Gemini Pro; budget-dominant coding → DeepSeek V4; default daily work → Anthropic).

    PM routing algorithm (each task): (1) classify task → role. (2) Look up role's `model_profiles`. (3) Filter by Layer B's active providers. (4) Pick top-ranked surviving profile. (5) Propose to owner OR execute with the default. Per-task overrides allowed — the PM states the full provider / family / version / effort in the dispatch log. The owner can invoke `/pk-route "<task description>"` to get a recommendation manually at any time.
  context: 'Re-record of DEC-20260417_1800-CapabilityProfileRouting-three-layer-model-selection
    — originally hand-written on 2026-04-17 because processkit MCP write tools were
    unreachable (aibox#53). The hand-written file carried a CLEANUP-REQUIRED marker
    that pushed YAML frontmatter off line 1 so the index parser skipped it (confirmed:
    get_decision returned "not found" despite the file existing). This re-record restores
    schema validation, state-machine enforcement, and the automatic event-log entry.
    The original hand-written file is deleted in the same turn to avoid duplicate
    entities. Original decision date: 2026-04-17T18:00Z.'
  rationale: Decouples role-to-model binding from specific model SKUs, making provider/model
    churn safe. Lets the PM route tasks based on capability requirements rather than
    hardcoded names. Matches the shape processkit already uses for skill + tool routing
    (capability over SKU).
  deciders:
  - ACTOR-owner
  - ACTOR-pm-claude
  decided_at: '2026-04-20T13:40:18+00:00'
---
