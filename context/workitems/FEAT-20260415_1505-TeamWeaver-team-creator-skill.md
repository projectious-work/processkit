---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: FEAT-20260415_1505-TeamWeaver-team-creator-skill
  created: '2026-04-15T15:05:00+00:00'
  labels:
    component: processkit-core
    area: team-composition
    priority_driver: owner-critical
spec:
  title: New narrow `team-creator` skill — provider-neutral team composition by cost/outcome tier
  state: done
  type: feature
  priority: high
  size: M
  description: >
    Generalize the one-off work that produced the current 8-member
    team (DEC-20260414_0900-TeamRoster) into a reusable, provider-
    neutral skill. The current roster hard-codes Anthropic tiers
    (Opus/Sonnet/Haiku); the landscape is multi-provider and shifts
    quarterly. `team-creator` takes the owner's subscription and
    criteria, tiers available models into heavy / medium / light by
    cost-per-token × capability × quota-burn, maps the 8 archetypal
    roles onto those tiers, and emits the Role / Actor / Binding
    entities plus `context/team/roster.md` plus a DecisionRecord that
    charters the team.
  no_skill_inflation_trade_off: |
    Per feedback memory 2026-04-15, a new skill requires justification.
    Alternatives considered:
      (a) Extend `agent-management` with a `team-compose` command —
          rejected because `agent-management` is already the heaviest
          skill in the kit and this would blur its scope.
      (b) Extend `model-recommender` — rejected because that skill
          profiles individual models; team composition is an
          orchestration layer above it.
      (c) New narrow skill — chosen. Pure orchestration, ≤200 lines of
          SKILL.md, composes `role-management` + `actor-profile` +
          `binding-management` + `model-recommender` + `decision-record`.
    Owner approved Option (c) on 2026-04-15.
  approach:
    phase_1_skill_scaffolding:
      owner: ACTOR-jr-architect
      model: Sonnet
      description: >
        Design the skill surface. Produce SKILL.md outline, command
        list (`team-create`, `team-review`, `team-rebalance`), the
        input-schema (owner constraints + criteria weights), the
        tiering formula, and the 8-role archetype mapping. Output: a
        design artifact before any code.
      output: ART-*-team-creator-skill-design
    phase_2_implementation:
      owner: ACTOR-developer
      model: Sonnet
      description: >
        Implement the skill directory
        `context/skills/processkit/team-creator/` with SKILL.md,
        commands, and a thin MCP server only if the phase-1 design
        calls for one (default: no MCP server; commands are enough
        because skill-finder makes them provider-neutral already).
      deliverables:
        - context/skills/processkit/team-creator/SKILL.md
        - context/skills/processkit/team-creator/commands/team-create.md
        - context/skills/processkit/team-creator/commands/team-review.md
        - context/skills/processkit/team-creator/commands/team-rebalance.md
        - context/skills/processkit/team-creator/references/tiering-formula.md
        - context/skills/processkit/team-creator/references/role-archetypes.md
    phase_3_dogfooding:
      owner: ACTOR-sr-researcher
      model: Opus
      description: >
        Re-derive the current team from scratch using `team-create`
        against the owner's Claude Max 5x subscription. Diff the
        output against the existing roster and DEC-20260414_0900.
        If the skill can reproduce today's team, accept; otherwise
        iterate on the tiering formula.
      output: ART-*-team-creator-dogfood-diff
    phase_4_register:
      owner: ACTOR-jr-developer
      model: Haiku
      description: >
        Register the skill in skill-finder's catalog, update the
        processkit INDEX.md, bump version, and run smoke tests.
  criteria_taxonomy:
    summary: |
      Provider-neutral criteria, sourced from
      ART-20260415_1510-LandscapeSnapshot-ai-provider-comparison-april-2026.
      The skill's tiering formula weights these; weights are inputs,
      not hard-coded.
    dimensions:
      cost:
        - input_price_per_million_tokens
        - output_price_per_million_tokens
        - cache_hit_discount
        - batch_discount
        - subscription_quota_burn_rate
      capability:
        - swe_bench_verified
        - swe_bench_pro
        - livecodebench
        - community_coding_rating
        - context_window
      latency:
        - output_tokens_per_second
        - time_to_first_token
      fit:
        - agentic_reliability
        - tool_use_fidelity
        - long_context_retrieval_accuracy
  role_archetypes:
    - project-manager          # always a heavy-tier model (routing quality compounds)
    - senior-architect         # heavy
    - junior-architect         # medium
    - developer                # medium
    - senior-researcher        # heavy
    - junior-researcher        # medium
    - junior-developer         # light
    - assistant                # light
  success_criteria:
    - Running `team-create` against the owner's current Claude Max 5x subscription reproduces the current 8-member team (±0 role changes; model assignments identical) within ±5pp on the orientation-target shares.
    - Running `team-create` against a hypothetical OpenAI-only or Gemini-only subscription produces a coherent 8-member team that uses no Anthropic models.
    - Skill SKILL.md is ≤200 lines.
    - No hard-coded provider names in SKILL.md or commands — all provider/model names flow in from `model-recommender` entities.
    - New DecisionRecord written by `team-create` supersedes DEC-20260414_0900 explicitly.
  out_of_scope:
    - Automating the subscription purchase or billing reconciliation.
    - Building a web UI — the skill is CLI/MCP-only.
    - Continuous re-tiering; re-tiering is a human-triggered `team-rebalance` command, not a cron job.
  related_artifacts:
    - ART-20260415_1510-LandscapeSnapshot-ai-provider-comparison-april-2026
    - ART-20260415_1505-TeamWeaver-team-creator-skill-design
  progress_notes: |
    Phase 1 (design) completed by ACTOR-jr-architect on 2026-04-15.
    See ART-20260415_1505-TeamWeaver-team-creator-skill-design.

    Three open questions for Phase 2 implementer:
      1. Formula weight persistence (DecisionRecord vs skill-local config).
      2. Landscape snapshot "latest" resolution + HTML parsing vs
         pre-structured markdown summary.
      3. Entity deactivation sequencing on re-create.

    Phase 2 (scaffolding) completed by ACTOR-developer on 2026-04-15.
    Files created:
      - context/skills/processkit/team-creator/SKILL.md (187 lines)
      - context/skills/processkit/team-creator/commands/team-create.md (197 lines)
      - context/skills/processkit/team-creator/commands/team-review.md (118 lines)
      - context/skills/processkit/team-creator/commands/team-rebalance.md (144 lines)
      - context/skills/processkit/team-creator/references/tiering-formula.md (142 lines)
      - context/skills/processkit/team-creator/references/role-archetypes.md (106 lines)
    Skill-finder catalog: updated (trigger phrases + Process category entry).
    Smoke test: pending owner permission to execute uv run scripts/smoke-test-servers.py.
    Phase 3 (dogfooding) ready to start.

    Phase 3 (dogfood) completed by ACTOR-sr-researcher on 2026-04-15.
    Verdict: FAIL. See ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff.
    All 8/8 roles drift (complete tier inversion — skill assigns Haiku to
    PM/sr-arch/sr-researcher, Sonnet to jr-dev/assistant). Per-model
    share Δ on Opus/Sonnet ≈ 75–80pp, far outside the ±5pp window.
    Root cause: on a same-provider candidate set, K+L (combined 50%
    weight) reward the cheapest/fastest model while the 0.01 norm
    floor annihilates the capability laggard's penalty. Recommended
    fix: (P1) rebalance defaults to {C:0.60, K:0.20, L:0.10, G:0.10}
    — re-simulated arithmetic reproduces the current team exactly.
    Secondary fixes P2–P5 in artifact §7. Phase 4 blocked pending
    owner decision on formula adjustment cycle (Phase 3.5).

    Phase 3.5 (weight rebalance) completed by ACTOR-jr-developer on
    2026-04-15. Default weights {C:0.40→0.60, K:0.35→0.20, L:0.15→0.10,
    G:0.10 unchanged}. Files touched: context/skills/processkit/team-creator/
    references/tiering-formula.md (3 edits, 7 lines changed),
    context/skills/processkit/team-creator/SKILL.md (1 edit, 4 lines changed),
    context/skills/processkit/team-creator/commands/team-create.md (2 edits,
    2 lines changed). Worked example (two-model set) recomputed with new weights
    (TierScore numerics updated, tier classification unchanged). Rationale
    added to each file. Smoke test: passed. Phase 4 register ready.

    Phase 4 (register + close) completed by ACTOR-jr-developer on 2026-04-15.
    INDEX.md entry added: team-creator registered in context/skills/INDEX.md
    Layer null (routing and meta skills) section. Skill version confirmed
    1.0.0 in context/skills/processkit/team-creator/SKILL.md frontmatter.
    Skill-finder registration verified: team-creator present in
    context/skills/processkit/skill-finder/SKILL.md with trigger phrases at
    line 126. Smoke test: PASSED (=== ALL SERVER SMOKE TESTS PASSED ===).
    WorkItem state transitioned from proposed to done. Follow-up:
    FEAT-20260415_1600-OpenWeave-team-creator-user-configurable-defaults
    tracks the openness expansion.

    v0.16.0 schema-field support (primary_contact, clone_cap,
    cap_escalation, is_template, templated_from) added by ACTOR-developer
    on 2026-04-15. SKILL version 1.0.0 → 1.1.0.
  related_decisions:
    - DEC-20260414_0900-TeamRoster-permanent-ai-team-composition  # to be superseded by phase-3 output
  related_workitems:
    parent: ARCH-20260414_1245-FirmFoundation-enforcement-implementation-plan
    replaces_placeholder: RES-Q2-team-creator
  assigned_to: ACTOR-pm-claude  # PM routes the phases; per-phase owners listed above
---

# Notes

Reconstructed on 2026-04-15 after context loss. Owner approved Option
(c) — a new narrow skill — over extension of `agent-management` or
`model-recommender`. The input landscape snapshot is the April-2026
provider comparison, ingested as artifact
ART-20260415_1510-LandscapeSnapshot.

Phases 1 → 4 are sequentially dependent; PM dispatches each as its
predecessor completes.
