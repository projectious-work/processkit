# Team roster

This is the permanent AI team for the processkit project. It is the
companion narrative to the `Role` / `Actor` / `Binding` entities under
`context/roles/`, `context/actors/`, and `context/bindings/`, and it is
governed by `DEC-20260414_0900-TeamRoster-permanent-ai-team-composition`.

Load this file at session start whenever a task needs routing.

## Members

| Role | Actor | Model tier | Invoke when… |
|---|---|---|---|
| project-manager | ACTOR-pm-claude | Opus 4.6 | Default session agent. Owns every incoming request, routes, reviews, and argues back. |
| senior-architect | ACTOR-sr-architect | Opus 4.6 | Large new feature design, cross-subsystem bug diagnosis, schema / API-contract / state-machine changes. |
| junior-architect | ACTOR-jr-architect | Sonnet 4.6 | Single-module design, moderate refactors, architectural Q&A with bounded blast radius. |
| developer | ACTOR-developer | Sonnet 4.6 | Feature implementation and bug fixes against a written plan. |
| senior-researcher | ACTOR-sr-researcher | Opus 4.6 | Open-ended or high-stakes research, multi-source synthesis, trade-off analysis. |
| junior-researcher | ACTOR-jr-researcher | Sonnet 4.6 | Bounded research: one topic, a handful of sources, summarisation, comparison tables. |
| junior-developer | ACTOR-jr-developer | Haiku 4.5 | Well-specified single-file edits, mechanical refactors, obvious bug fixes. |
| assistant | ACTOR-assistant | Haiku 4.5 | Summarising texts, ordering lists, admin chores, routine formatting. |

## Routing heuristic (PM decision table)

The PM classifies each incoming request on two axes — **kind** and
**complexity** — and routes accordingly. When two roles are plausible,
pick the cheaper model; escalate only if the first pass is weak.

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

## Working protocol

1. Owner states a request to the PM.
2. PM classifies (kind + complexity), checks skill-finder / `route_task`
   when applicable, and picks the role + clone count.
3. PM drafts success criteria before dispatch; for large tasks, a
   senior-architect or senior-researcher plan precedes implementation.
4. Assigned role does the work, returns artifacts with a structured
   handoff (see `agent-management` SKILL).
5. PM reviews against success criteria, plays devil's advocate on
   weak points, and returns to the owner.
6. PM logs decisions via `decision-record` and tracks open work via
   `workitem-management` as appropriate.

## Changing the team

Team composition is governed by a DecisionRecord. To add, remove, or
retier a role:

1. Open a Discussion (`discussion-management`) proposing the change.
2. On owner approval, write a new `DecisionRecord` that supersedes
   `DEC-20260414_0900-TeamRoster-permanent-ai-team-composition`.
3. Create the new Role / Actor / Binding entities; deactivate (not
   delete) superseded ones by setting `active: false` and `left_at`.
4. Update this roster doc.
