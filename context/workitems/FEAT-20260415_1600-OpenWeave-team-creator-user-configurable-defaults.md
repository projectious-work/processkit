---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: FEAT-20260415_1600-OpenWeave-team-creator-user-configurable-defaults
  created: '2026-04-15T16:00:00+00:00'
  labels:
    component: processkit-core
    area: team-composition
    priority_driver: owner-critical
spec:
  title: team-creator openness — user- and agent-configurable models, weights, classes, and role→class bindings
  state: proposed
  type: feature
  priority: medium
  size: M
  description: >
    Today's `team-creator` (FEAT-TeamWeaver) ships strong defaults —
    default model ladder, default formula weights, fixed tier
    thresholds (≥0.70 heavy / 0.40–0.69 medium / <0.40 light), and
    fixed role→class archetype pins. The owner has flagged that
    derived projects / downstream users will have legitimate reasons
    to override any of these four layers (e.g. a latency-critical
    project weights L far higher; a research lab pins more roles to
    heavy; an edge deployment has a completely different accessible
    model set). This WorkItem opens all four layers to manual and
    agent-driven override, while keeping the kit's defaults
    unchanged for first-time users.
  layers_to_open:
    layer_1_default_models:
      current: >
        The landscape summary artifact is the only model source, and
        its contents are curated quarterly by the kit maintainers.
      open_by: >
        Allow derived projects to ship their own landscape-summary
        artifact (same schema, different tag suffix) and point
        `team-create --landscape-artifact` at it. Agent-driven: a
        `landscape-curator` skill (out of scope here) could regenerate
        the summary from provider APIs.
    layer_2_weights:
      current: >
        CLI flag `--weight-overrides` already accepts a JSON blob.
        Defaults (C=0.60 post-Phase-3.5, K=0.20, L=0.10, G=0.10) live
        in `references/tiering-formula.md`.
      open_by: >
        Persist per-project weight overrides in a new optional
        DecisionRecord `DEC-*-TeamWeights` that `team-create` reads on
        startup. Agent-driven: a PM/sr-architect can propose a weight
        change via `decision-record-write` and future runs pick it up.
    layer_3_tier_thresholds:
      current: >
        Hardcoded thresholds (≥0.70, 0.40–0.69, <0.40) in
        `references/tiering-formula.md`. Phase 1 design explicitly
        locked these as non-overridable for auditability.
      open_by: >
        Relax the lock: allow thresholds to be overridden in the same
        `DEC-*-TeamWeights` record, but require the DecisionRecord to
        document the reason (mandatory `rationale:` field). Auditability
        preserved via the DecisionRecord itself.
    layer_4_role_class_pins:
      current: >
        Hardcoded in `references/role-archetypes.md`. PM/sr-arch/
        sr-researcher pinned heavy; jr-dev/assistant pinned light;
        others medium. Override-when rules exist but only for narrow
        cases.
      open_by: >
        Allow derived projects to supply a `role-archetypes.yaml`
        override file that remaps pins. `team-create` validates the
        override against an archetype schema and refuses assignments
        that violate the clone-cap or PM-uniqueness invariants.
  success_criteria:
    - A derived project can override any of the four layers without patching kit files.
    - Each override produces an audit trail (DecisionRecord amendment or artifact reference).
    - Kit defaults remain unchanged; first-time users see identical behaviour to the FEAT-TeamWeaver baseline.
    - The existing Phase 3 dogfood test continues to PASS with kit defaults (regression gate).
    - A new dogfood test demonstrates a latency-weighted override (L=0.50, K=0.20, C=0.25, G=0.05) producing a visibly different team on the same landscape — proves the override surface actually moves the output.
  agent_driven_path:
    description: >
      The four override surfaces must be discoverable by agents, not
      just humans. Phase 2 of this WorkItem should add a trigger
      phrase table to skill-finder so an agent can resolve requests
      like "the user values latency more" or "pin senior-architect
      to medium for this project" into the correct override layer
      without the owner naming the layer explicitly.
  out_of_scope:
    - Building the `landscape-curator` skill (separate WorkItem if we decide to automate snapshot refresh).
    - UI for editing weights — override is file-based / CLI / MCP tool only.
    - Cross-project weight sharing / synchronization.
  related_workitems:
    depends_on: FEAT-20260415_1505-TeamWeaver-team-creator-skill  # this wave must land first
    parent: ARCH-20260414_1245-FirmFoundation-enforcement-implementation-plan
  related_artifacts:
    - ART-20260415_1545-TeamWeaver-team-creator-dogfood-diff
    - ART-20260415_1505-TeamWeaver-team-creator-skill-design
    - ART-20260415_1600-OpenWeave-openweave-skill-design
  progress_notes: |
    Phase 1 (design spike) completed by ACTOR-jr-architect on 2026-04-15.
    See ART-20260415_1600-OpenWeave-openweave-skill-design.

    Key design choices:
      - Layer 1 (models): 3-level precedence with landscape-summary-project tag.
      - Layer 2 (weights): new DEC-*-TeamWeights record, discovered by tag.
      - Layer 3 (thresholds): co-located with weights in same DEC (causally coupled).
      - Layer 4 (role pins): context/team/role-archetypes.yaml, delta-default.
      - Trigger phrases designed for all 4 layers (skill-finder additive entries).

    Top open questions for Phase 2:
      1. Can index-management query arbitrary spec.* fields, or tag-only?
      2. Eager vs lazy role-archetypes.yaml validation.
      3. team-rebalance handling of TeamWeights DEC newer than governing team DEC.
  assigned_to: ACTOR-pm-claude  # PM sequences; per-layer implementers TBD
---

# Notes

Opened 2026-04-15 after Phase 3 dogfood revealed that the first-wave
defaults work for the owner's current subscription but are not
portable. The four-layer openness design came from owner feedback:
"derived projects/users should adapt models, weightings, classes,
and role→class bindings either manually or with agents." Start after
FEAT-TeamWeaver's Phase 4 closes (i.e. once defaults are proven stable
on the owner's subscription).
