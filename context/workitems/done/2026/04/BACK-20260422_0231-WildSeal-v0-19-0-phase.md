---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260422_0231-WildSeal-v0-19-0-phase
  created: '2026-04-22T02:31:23+00:00'
  updated: '2026-04-22T05:31:31+00:00'
spec:
  title: v0.19.0 Phase 1 — New schemas (team-member, model, binding extensions) +
    .gitignore.example bundle
  state: done
  type: task
  priority: high
  assignee: ACTOR-sr-architect
  description: |
    Foundational schemas for v0.19.0.

    **Deliverables**
    - `context/schemas/team-member.yaml` (new; replaces actor.yaml) with fields: type, name, slug, default_role, default_seniority, personality{communication_style, voice, archetype_blend, boundaries, declared_expertise}, memory{enabled, tiers, consolidation_cadence, importance_threshold, decay_enabled}, relationships, exportable, export_policy{include, exclude, redact_sensitivity}, active, joined_at, left_at.
    - `context/schemas/model.yaml` (new) with fields: provider, family, versions[{version_id, released_at, status, deprecated_at, successor, context_window, max_output, pricing_usd_per_1m}], efforts_supported, dimensions{reasoning, engineering, speed, breadth, reliability, governance}, modalities, access_tier, status_page_url, equivalent_tier.
    - Update `context/schemas/role.yaml` to v2: strip seniority from slugs; remove embedded `model_profiles[]` (moved to bindings). Seniority becomes a pure ordinal tag with ladder `junior → specialist → expert → senior → principal`.
    - Extend binding-type catalog with `model-assignment` type.
    - Ship `.gitignore.example` at processkit repo root bundling all proposed ignores (team-members/*/private/, any other pending ones).
    - Memory file frontmatter convention: tier, source, sensitivity, confidence, importance, created, last_reinforced, scope.

    **Done when**
    - All schemas validate against pk-doctor.
    - `.gitignore.example` exists and is referenced from AGENTS.md.
    - Dual-tree mirror clean (src/ matches context/).
  started_at: '2026-04-22T02:37:35+00:00'
  completed_at: '2026-04-22T05:31:31+00:00'
---

## Transition note (2026-04-22T02:37:35+00:00)

Starting v0.19.0 Phase 1: drafting team-member.yaml, model.yaml, role.yaml v2, binding extension, and .gitignore.example.


## Transition note (2026-04-22T05:31:27+00:00)

Phase 1 complete: team-member.yaml (new), model.yaml (new), role.yaml v2 (strip seniority + remove model_profiles), binding.yaml v1.1 (model-assignment conditional schema) all written to context/ and src/context/. .gitignore.example shipped at repo root. 8 files validate as YAML + structure; dual-tree mirror clean.


## Transition note (2026-04-22T05:31:31+00:00)

Self-review complete: schema YAML parses clean, required spec/spec_schema fields present, dual-tree diff clean. Ready for Phase 2 (team-manager skill).
