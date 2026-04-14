---
apiVersion: processkit.projectious.work/v1
kind: DecisionRecord
metadata:
  id: DEC-20260414_0900-TeamRoster-permanent-ai-team-composition
  created: '2026-04-14T09:00:00+00:00'
spec:
  title: Establish a permanent eight-member AI team with model-tier-aware task routing
  state: accepted
  decision: >
    Model the project's working group as eight Role / Actor / Binding
    triples under `context/roles/`, `context/actors/`, and
    `context/bindings/`, plus a plain-language roster at
    `context/team/roster.md`. Members: project-manager (Opus),
    senior-architect (Opus), junior-architect (Sonnet), developer
    (Sonnet), senior-researcher (Opus), junior-researcher (Sonnet),
    junior-developer (Haiku), assistant (Haiku). The project manager
    routes every incoming request; Opus work targets ≈5% of session
    effort, Sonnet ≈85%, Haiku ≈10%. A role may be "cloned" up to 5
    parallel instances without owner re-approval; beyond 5 requires
    explicit owner sign-off.
  context: >
    Owner operates on an Anthropic Claude Max 5x subscription with
    asymmetric per-model weekly allowances (Opus ≈15–35 hours/week,
    Sonnet ≈140–280 hours/week on typical traffic patterns; heavy
    interactive use burns the Opus allowance materially faster). To
    stay within budget while still applying strong reasoning where it
    matters, the team must (a) route by complexity-to-model fit, not
    by convenience, and (b) cap parallel fan-out so coordination cost
    does not exceed benefit. processkit already provides the Role /
    Actor / Binding primitives and the agent-management skill — this
    decision composes them into a permanent team definition.
  rationale: >
    Four cross-cutting reasons. (1) Matching task complexity to the
    cheapest capable model is the highest-leverage cost lever on any
    token-metered plan. (2) processkit's agent-management skill already
    recommends pipelines capped at 3–4 parallel agents; 5 is a modest
    extension the owner is willing to pay for when a task genuinely
    parallelizes. (3) Splitting each responsibility into a Role
    (descriptive) + Actor (identity + model pin) + Binding (assignment
    + scope) keeps the team definition queryable via
    `index-management` and survives model-tier relabeling without
    rewriting history. (4) A project-manager role that also plays
    devil's advocate versus the owner and the rest of the team is the
    single highest-impact addition — every other role benefits from
    its scepticism and routing decisions.
  alternatives:
  - option: Freeform prose in AGENTS.md describing the team
    rejected_because: Not queryable; drifts in long sessions; cannot scope
      or time-bound assignments; loses audit trail.
  - option: A single generalist agent that picks its own model per turn
    rejected_because: Pushes routing into every turn; loses specialisation;
      makes budget tracking impossible.
  - option: Hard quota enforcement on Opus / Sonnet / Haiku share
    rejected_because: Task mix varies (heavy research weeks vs heavy
      implementation weeks). Orientation targets preserve flexibility;
      PM flags drift only when it is material (>10pp off).
  consequences:
  - All future task-assignment guidance references the role IDs defined here.
  - Session handovers include a budget-share snapshot (Opus / Sonnet / Haiku actuals vs targets).
  - Clone requests above 5 must be recorded as an owner-approved exception in the session log.
  supersedes: []
  superseded_by: null
  related:
    - SKILL-agent-management
    - SKILL-role-management
    - SKILL-actor-profile
    - SKILL-binding-management
---

# Permanent AI team composition

This decision record is the charter for the team defined under
`context/roles/`, `context/actors/`, `context/bindings/`, and
`context/team/roster.md`. See the roster doc for routing heuristics and
the clone-allocation policy.
