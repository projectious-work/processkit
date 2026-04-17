# Team roster

This is the permanent AI team for the processkit project. It is the
companion narrative to the `Role` / `Actor` / `Binding` entities under
`context/roles/`, `context/actors/`, and `context/bindings/`.

**Governing decisions:**
- `DEC-20260414_0900-TeamRoster-permanent-ai-team-composition` — role composition, clone caps, budget orientation.
- `DEC-20260417_1800-CapabilityProfileRouting-three-layer-model-selection` — model binding via three-layer architecture (catalog / preferences / role standard sets).

Load this file at session start whenever a task needs routing.

## Model-selection architecture (three layers)

Model choice is a function of three layers — PM evaluates them in order
on every routing decision:

**Layer A — Model catalog** (*what exists*). Curated registry of models
the project tracks. Lives inside the `model-recommender` skill and is
refreshed via `/pk-model-refresh`. Covers Anthropic, OpenAI, Google,
xAI, DeepSeek — driven by `aibox.toml` declared providers plus owner
additions.

**Layer B — Project / owner preferences** (*what this project can use*).
Subscriptions, API keys, cost bias, preferred provider ordering. Owned
by the model-recommender skill's `set_config` / `get_config` MCP tools,
configured via `/pk-model-setup`.

**Layer C — Role standard sets** (*what this role needs*). Each Role
entity carries a ranked `model_profiles` array (see the "Members"
table below for the defaults). Rank 1 is the primary; lower ranks are
fallbacks.

**PM routing algorithm (per task):**
1. Classify task → role.
2. Load the role's `model_profiles`.
3. Filter by Layer B's active providers.
4. Pick the top-ranked surviving profile.
5. Execute by default, or propose alternatives when task specifics
   favour a lower-ranked option (e.g. Computer Use → OpenAI; 2M context
   → Grok; long-document analysis → Gemini; budget-dominant coding →
   DeepSeek).

Owner can manually invoke `/pk-route "<task description>"` at any time
to get a recommendation. Per-task overrides stated in the dispatch log:
PM calls out the full `provider / family / version / effort` chosen.

## Members

| Role | Actor | Primary default (rank 1) | Fallbacks (rank 2+) | Invoke when… |
|---|---|---|---|---|
| project-manager | ACTOR-pm-claude | Anthropic claude-opus 4.7 @ medium | OpenAI gpt-5 5.4 @ high | Default session agent. Owns every request, routes, reviews, argues back. |
| senior-architect | ACTOR-sr-architect | Anthropic claude-opus 4.7 @ high | OpenAI gpt-5 5.4 @ high; xAI grok 4.20 @ high | Large feature design, cross-subsystem diagnosis, schema / API changes. |
| junior-architect | ACTOR-jr-architect | Anthropic claude-sonnet 4.6 @ medium | OpenAI gpt-5 5.4 @ medium | Single-module design, moderate refactors, bounded architectural Q&A. |
| developer | ACTOR-developer | Anthropic claude-sonnet 4.6 @ medium | DeepSeek v4; OpenAI gpt-5 5.4 @ medium | Feature implementation / bug fixes against a written plan. |
| senior-researcher | ACTOR-sr-researcher | Anthropic claude-opus 4.7 @ high | Google gemini-pro 2.5 @ medium; OpenAI gpt-5 5.4 @ high | Open-ended / high-stakes research, multi-source synthesis, trade-offs. |
| junior-researcher | ACTOR-jr-researcher | Anthropic claude-sonnet 4.6 @ low | Google gemini-flash 2.5 @ medium | Bounded research: one topic, few sources, summaries, comparison tables. |
| junior-developer | ACTOR-jr-developer | Anthropic claude-haiku 4.5 | DeepSeek v4 | Well-specified single-file edits, mechanical refactors, obvious fixes. |
| assistant | ACTOR-assistant | Anthropic claude-haiku 4.5 | Google gemini-flash-lite 2.5 | Summaries, list ordering, admin chores, routine formatting. |

Full `model_profiles` arrays live in each role file under
`context/roles/`. Rationale strings for each fallback option are
documented there.

## Routing heuristic (PM decision table)

The PM classifies each incoming request on two axes — **kind** and
**complexity** — and routes accordingly. When two roles are plausible,
pick the cheaper model; escalate only if the first pass is weak.
Effort-tier downgrade (Opus-high → Opus-medium → Opus-low) is the
first cost lever before considering a model swap.

| Kind ↓ / Complexity → | Small | Medium | Large |
|---|---|---|---|
| Research / analysis | junior-researcher | junior-researcher | senior-researcher |
| Architecture / design | junior-architect | junior-architect | senior-architect |
| Implementation / bug fix | junior-developer | developer | developer (with senior-architect plan) |
| Admin / formatting / summarisation | assistant | assistant | assistant (fan-out) |
| Routing / devil's advocate / owner dialogue | project-manager | project-manager | project-manager |

**Complexity rule of thumb.** Small = one file, clear spec. Medium = one
module / single subsystem. Large = multi-module, unclear boundaries, or
high blast radius.

## Cloning policy

- Default: 1 instance per role.
- Up to 5 parallel clones per role: PM-approved, no owner sign-off.
- 6 or more: owner approval required, recorded in the session log.
- PM is never cloned (single routing identity).

Per `agent-management` guidance, only fan out when the PM has verified
subtasks are provably independent (different files, different modules).

## Token-budget orientation

Driven by the owner's Anthropic Claude Max 5x subscription. Published
weekly allowances roughly indicate Opus ≈15–35 h/week and Sonnet
≈140–280 h/week under typical assumptions; heavy interactive use burns
the Opus allowance materially faster.

Orientation targets (not hard limits):

| Tier | Target share of session effort |
|---|---|
| Opus (PM, senior-architect, senior-researcher) | ≈ 5 % |
| Sonnet (junior-architect, developer, junior-researcher) | ≈ 85 % |
| Haiku (junior-developer, assistant) | ≈ 10 % |

**PM drift-flagging rule.** When session share deviates more than ±10pp
from a target, the PM surfaces it to the owner with the driving task
mix (e.g. "this week was architecture-heavy — Opus ran at 18%; want to
rebalance next week?"). Do not auto-throttle; the owner decides.

**Effort-tier attribution.** Session handovers should break down time
by model + effort, not just tier (e.g. "Opus @ high: 40 min;
Opus @ medium: 20 min; Sonnet @ medium: 3 h 20 min"). Effort is the
primary cost lever within a model.

## Working protocol

1. Owner states a request to the PM.
2. PM classifies (kind + complexity), checks skill-finder / `route_task`
   when applicable, picks the role + clone count.
3. PM drafts success criteria before dispatch. For large tasks, a
   senior-architect or senior-researcher plan precedes implementation.
4. PM states the model + effort choice for the dispatch (default from
   role's `model_profiles` rank 1 unless overriding — override cases
   logged with reason).
5. Assigned role does the work, returns artifacts with a structured
   handoff (see `agent-management` SKILL).
6. PM reviews against success criteria, plays devil's advocate on
   weak points, returns to the owner.
7. PM logs decisions via `decision-record` (`/pk-dec`) and tracks open
   work via `workitem-management` (`/pk-work`) as appropriate.

## Changing the team

Team composition is governed by a DecisionRecord. To add, remove, or
retier a role:

1. Open a Discussion (`/pk-discuss`) proposing the change.
2. On owner approval, write a new `DecisionRecord` (`/pk-dec`) that
   supersedes `DEC-20260414_0900-TeamRoster-permanent-ai-team-composition`
   (role composition) and/or
   `DEC-20260417_1800-CapabilityProfileRouting-three-layer-model-selection`
   (model binding).
3. Create the new Role / Actor / Binding entities; deactivate (not
   delete) superseded ones by setting `active: false` and `left_at`.
4. Update this roster doc.

## Refreshing the model roster

When a new model version ships (e.g. Opus 4.7 → 4.8, GPT-5.4 → 5.5):

1. Run `/pk-model-refresh` to update Layer A (catalog).
2. Review Layer C (role `model_profiles`) — do any `default_version`
   strings need bumping? Does the new version unlock a reshuffle of
   ranks (e.g. promoting a new provider that just became competitive)?
3. If Layer C changes are material, record a new DecisionRecord
   (`/pk-dec`).
