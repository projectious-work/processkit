# CLEANUP-REQUIRED 2026-04-17: this DecisionRecord was hand-written
# because the processkit MCP servers were not wired (aibox#53).
# Once that issue is fixed and `mcp__processkit-decision-record__record_decision`
# is callable, re-record the same content through the MCP tool to
# pick up schema validation, state-machine enforcement, and the
# automatic event-log entry. This file may be overwritten in place.
---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260417_1800-CapabilityProfileRouting-three-layer-model-selection
  created: '2026-04-17T18:00:00+00:00'
spec:
  title: Adopt a three-layer model-selection architecture — catalog / preferences / role standard sets — and bind roles to capability profiles instead of model SKUs
  state: accepted
  decision: >
    Replace the single `preferences.model = "claude-opus-4-6"` binding
    on each Actor with a three-layer architecture:

    Layer A — **Model catalog** (what exists). Curated registry of
    models the project cares about, with versions, effort tiers, pricing,
    capability scores. Lives inside the `model-recommender` skill
    (`context/skills/processkit/model-recommender/`) and is refreshed
    via Workflow C (`/pk-model-refresh`). Informed by `aibox.toml`'s
    declared providers plus owner-driven additions.

    Layer B — **Project / owner preferences** (what this project can
    use). Subscription tier, available API keys, cost bias, preferred
    ordering, and default thinking policy. Owned by the model-recommender
    skill's `set_config` / `get_config` MCP tools, populated via
    Workflow D (`/pk-model-setup`). No parallel preferences file.

    Layer C — **Role standard sets** (what this role needs). Each
    `Role` entity carries a ranked `model_profiles` array — equivalent
    option-sets keyed by `rank`, each naming provider + family +
    default_version + default_effort + rationale. `rank: 1` is the
    primary; lower ranks are fallbacks when Layer B filters out the
    primary, when rate-limited, or when task specifics favour a
    different option (Computer Use → OpenAI; 2M context → Grok;
    long-document analysis → Gemini Pro; budget-dominant coding →
    DeepSeek V4; default daily work → Anthropic).

    PM routing algorithm (each task): (1) classify task → role.
    (2) Look up role's `model_profiles`. (3) Filter by Layer B's
    active providers. (4) Pick top-ranked surviving profile.
    (5) Propose to owner OR execute with the default. Per-task
    overrides allowed — the PM states the full `provider / family /
    version / effort` in the dispatch log. The owner can invoke
    `/pk-route "<task description>"` to get a recommendation manually
    at any time.

    Schema changes: (1) `Role` gains `model_profiles: array<profile>`.
    (2) `Actor` gains optional `model_profile_override: profile` for
    rare per-actor deviations. (3) The `preferences.model` string
    field on existing actors is deprecated — roles carry the routing
    intent now; Actors stay identity-only unless overriding.
  context: >
    The prior architecture hard-pinned each Actor to one model SKU
    (e.g. `claude-opus-4-6`). Three gaps made this untenable as of
    2026-04-17:

    (a) **Models churn fast.** Opus 4.6 → 4.7 shipped 2026-04-16 with
    a new `xhigh` effort tier and adaptive thinking. GPT-5.4 and 5.3
    coexist with distinct effort tiers. Gemini 3.1 Pro is in preview
    alongside Gemini 2.5 Pro GA. Hard-pinning means rewriting 8 actor
    files every few weeks — and missing per-task effort selection
    entirely.

    (b) **Effort is a separate, per-task lever.** Even with a fixed
    model SKU, the effort tier (low / medium / high / xhigh on Opus;
    minimal / low / medium / high / xhigh on GPT-5) materially changes
    cost and latency. The previous schema had no place for this.

    (c) **Multi-provider is the near-term reality.** This project is
    Anthropic-primary (Claude Max 5x), but GPT-5.4, Gemini 2.5 Pro,
    Grok 4.20 and DeepSeek V4 each have a niche where they dominate
    (Computer Use, long-context cost, 2M context, coding at scale).
    A single-profile-per-actor shape cannot express "use Opus 4.7
    normally but fall back to GPT-5.4 when Anthropic is rate-limited
    or this task specifically needs Computer Use."

    The `model-recommender` skill already implements the Layer A + B
    infrastructure (six-dimension capability scoring, gate dimensions,
    pricing, MCP config tools, four workflows). This decision wires
    Layer C into the Role schema and declares the combined three-layer
    machinery as the canonical routing pipeline.
  rationale: >
    Four reasons. (1) **Absorbs model churn.** Roster updates flow
    through the catalog (Layer A via /pk-model-refresh); Role standard
    sets change only when a role's capability needs change, not on
    every provider rev. (2) **Separates concerns cleanly.** What exists
    (Layer A) is public fact; what the owner can use (Layer B) is
    project-private; what a role needs (Layer C) is a capability
    contract. Each layer has a clear owner and refresh cadence.
    (3) **Expresses alternatives without losing defaults.** A ranked
    list gives the PM an obvious fallback chain while still giving the
    owner a single "just do what you normally do" path on 99% of tasks.
    (4) **Reuses existing infrastructure.** The `model-recommender`
    skill's catalog + config + routing workflows are the natural
    backend for Layers A and B. Building a parallel system would have
    duplicated effort and split the source of truth.
  alternatives:
  - option: Keep the single `preferences.model` string; add a second `preferences.effort` string
    rejected_because: Solves effort selection but not multi-provider fallback. Still requires rewriting every actor on model revs. Provides no structural support for per-task overrides.
  - option: Put the ranked model_profiles on the Actor, not the Role
    rejected_because: Actors derived from templates would each carry a duplicate copy of the same list — edits require fanning out. Role is the capability contract; Actor is identity + rare override.
  - option: Build a separate `context/team/provider-preferences.yaml` and `context/team/model-catalog.yaml`
    rejected_because: The `model-recommender` skill already does both, with MCP tools, six-dimension scoring, pricing data and a Roster Refresh workflow. Parallel infrastructure would split the source of truth and drift.
  - option: Let the PM decide model per task with no per-role defaults
    rejected_because: Pushes the model decision into every turn and every role, which increases coordination cost and loses the "this kind of task usually wants this kind of model" institutional knowledge roles are meant to encode.
  consequences:
  - Role schema gains required `model_profiles` array on all future roles; existing 8 roles migrated in this commit.
  - Actor schema gains optional `model_profile_override`. The deprecated `preferences.model` string on existing actors is left in place for now (no breaking migration); documentation points at the new Role field.
  - `/pk-route`, `/pk-model-setup`, `/pk-model-refresh` (surviving from the model-recommender command trio per DEC-CommandNexus amendment) are the user-facing surface for this architecture. Owner can manually ask "what model/effort should I use for <task>" via `/pk-route <description>` at any time.
  - Session handovers should include the model + effort actuals per-task (not just the Opus / Sonnet / Haiku tier share) so drift against the roster defaults is visible.
  - Drifts the spec for token-budget tracking — the 5 / 85 / 10 Opus / Sonnet / Haiku targets from DEC-TeamRoster still apply, but per-task model/effort choices make the attribution more granular.
  links:
    supersedes_partial:
      - id: DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
        scope: "Model-binding aspect only. Role composition, clone caps, 5/85/10 budget orientation, working protocol all stand."
    related:
      - DEC-20260415_2030-CommandNexus-pk-prefix-namespace-and-command-strategy
    depends_on:
      - "SKILL-model-recommender v1.2.0+ — provides Layer A catalog and Layer B config"
---

## Narrative

This decision closes a loop that's been open since the initial team-roster
commit on 2026-04-14. That commit defined 8 roles and pinned each to a
model tier (opus / sonnet / haiku) with a specific SKU in
`preferences.model`. It worked for two weeks. Then three things broke
the shape:

1. **2026-04-16 — Anthropic ships Opus 4.7** with adaptive thinking and
   the new `xhigh` effort tier. The string `claude-opus-4-6` in every
   senior actor becomes immediately outdated.

2. **Owner observation 2026-04-17** — the existing schema has no place
   for effort tiers. Opus runs ~25% of session effort in the last session
   (vs. 5% target) because PM dispatch didn't know it could downgrade
   Opus-medium-turns-with-adaptive-thinking to Opus-low. Single-string
   binding obscures the available cost lever.

3. **Owner constraint surfaced 2026-04-17** — this project is Anthropic-
   primary but multi-provider access is the plausible near-term state.
   GPT-5.4, Gemini 2.5 Pro, Grok 4.20, DeepSeek V4 each dominate a
   niche. The PM needs a ranked "equivalent options" list per role, not
   a single SKU binding.

The three-layer architecture is lifted directly from the owner's
framing in the 2026-04-17 session: generally-available catalog (A) →
project preferences (B) → role standard sets (C). The insight that
(A) and (B) already exist as `model-recommender` infrastructure — and
this decision should wire into it rather than build parallel files —
collapsed the scope from "large schema + 3 new YAML files" to "1 field
on Role, 1 optional field on Actor, populate 8 role files, document."

Implementation landed in a single commit alongside the Phase 4
consolidation that retired 10 legacy slash commands and promoted 13 new
/pk-* commands, including the three model-recommender commands that
now form the user-facing surface for this architecture.
