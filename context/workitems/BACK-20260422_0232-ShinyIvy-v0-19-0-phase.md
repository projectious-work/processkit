---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260422_0232-ShinyIvy-v0-19-0-phase
  created: '2026-04-22T02:32:11+00:00'
  updated: '2026-04-22T06:24:16+00:00'
spec:
  title: 'v0.19.0 Phase 5 — Binding infrastructure: model-assignment type, 8-layer
    resolution precedence, default binding pack'
  state: done
  type: task
  priority: high
  assignee: ACTOR-developer
  description: 'Wire up bindings so (role + seniority) × (model + version + effort)
    routing is declarative.


    **Binding type: `model-assignment`**

    - subject: Role | TeamMember | ProjectScope

    - target: Model

    - conditions: {seniority?, rank?, effort_floor?, effort_ceiling?, version_pin?,
    blocked?, provider_preference?, cost_bias?, cost_cap?}


    **Resolution precedence (high → low)**

    1. Task-pinned override (short-circuit on `task_hints.model_pin`)

    2. Team-member preference (TeamMember→Model bindings)

    3. Project veto (ProjectScope→Model with blocked:true — hard filter)

    4. Capability filter (task_hints requirements vs model modalities)

    5. Role+seniority ranking (Role→Model with conditions.seniority)

    6. Role default ranking (Role→Model without seniority)

    7. Project bias (cost_bias, provider_preference — reorder, don''t filter)

    8. Shim fallback (role.default_model or system default; emits warning)


    **Tie-breakers within same rank**: project-preferred provider, lower cost, more
    recent GA, higher reliability score.


    **Edge cases**: effort clamping, version pin resolution, stale-binding skip, explain
    mode trace, resolution cache keyed on (role, seniority, team_member, scope, hints_hash)
    invalidated by binding/model events.


    **Default binding pack** shipped at `context/skills/processkit/model-recommender/default-bindings/`
    — sensible starter mappings any new processkit project can import; users override.


    **Done when**

    - `resolve_bindings_for(role, seniority, team_member, scope, task_hints)` implemented
    and tested.

    - `pk explain-routing` command available for debugging.

    - Default binding pack validates against schemas.

    - Dogfood: routing returns same answers as today for the 8 original roles (regression
    baseline).'
  started_at: '2026-04-22T06:07:24+00:00'
  completed_at: '2026-04-22T06:24:16+00:00'
---

## Transition note (2026-04-22T06:07:24+00:00)

Starting Phase 5: implementing 8-layer resolver, model-assignment binding type support, default binding pack, and pk explain-routing CLI. Delegated to background agent.


## Transition note (2026-04-22T06:19:06+00:00)

Phase 5 complete: 789-LOC resolver.py (8-layer precedence with cache, effort clamping, tie-breakers, shim fallback), 25 pytest tests passing, 30-binding default pack at default-bindings/MANIFEST.yaml, resolve_model + explain_routing MCP tools added to model-recommender server, /pk-explain-routing slash command. binding-management needed no changes (freeform conditions pass through). Dual-tree clean.
