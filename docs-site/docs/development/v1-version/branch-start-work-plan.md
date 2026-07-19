---
title: Branch Start Work Plan
description: Phase plan for beginning the processkit v1.0 branch.
---

# Branch Start Work Plan

This plan turns the v1.0 documentation set into branch-start execution
work. Phase 0 and Phase 1 are intentionally concrete; later phases are
rougher and should be refined as evidence arrives.

## Phase 0 - Branch Foundation

Goal: make the `v1.0` branch buildable, testable, and clearly separated
from v0.x maintenance.

Backlog:

- Freeze the branch contract and backport policy in docs.
- Add a visible branch banner or README note explaining that `v1.0` is
  the rebuild line.
- Decide the initial source layout for `context/schemas/src/`, `_generated/`,
  schema renderer tests, and fixture projects.
- Add a minimal fixture-project layout for `empty-project`,
  `alpha-project`, `migration-v0-project`, `adversarial-project`, and
  `art-project`.
- Define the command surface for schema rebuild, validation, MCP smoke,
  index rebuild, and docs build.
- Establish manual local release-audit commands that do not depend on
  aibox or GitHub Actions.
- Record any accepted deviations from the RFC before implementation
  starts.

Exit criteria:

- The branch builds docs.
- The planned source/test directories exist.
- The first schema-generation and fixture-test commands are documented.

## Phase 1 - Ontology And Schema Generation

Goal: turn the documented 89-concept ontology into generated schema
contracts and prove deterministic generation.

Backlog:

- Create the canonical ontology registry with class, name, description,
  parent, discriminator, interface, lifecycle, and migration note fields.
- Scaffold `src/context/schemas/src/` with T fragments, primitive schemas,
  discriminator overlays, and composition templates.
- Implement the Jinja + YAML renderer.
- Implement merge strategies for `replace`, `concat`, and `name-merge`.
- Commit `_generated/*.yaml` output and golden render fixtures.
- Add strict/tolerant validation-mode metadata per kind.
- Add schema contract tests for valid and invalid fixtures.
- Add the `regenerate_schemas(kinds: list | None)` MCP shape or a local
  implementation shim if the MCP server is not ready yet.

Exit criteria:

- Full and partial schema regeneration are deterministic.
- The generated schema tree is committed.
- The alpha ontology subset has generated schemas and validation tests.

## Phase 2 - Tooling Parity

Goal: make the generated schemas usable through MCP and local tools.

Backlog:

- Build shared MCP helpers for schema loading, validation,
  state-machine checks, atomic writes, event emission, and index upsert.
- Port alpha create/read/transition tools to generated schemas.
- Add Python signature to draft-2020-12 JSON Schema consistency tests.
- Expose validation mode through MCP.
- Add state-machine fixtures for valid transitions, invalid transitions,
  guard failures, and terminal states.
- Keep per-domain tool ownership while allowing gateway aggregation.
- Define a shared remediation descriptor schema for doctor findings.
- Validate every executable remediation against the installed gateway tool
  catalog and input schema.
- Add a structured policy-exception resolver with scope, fingerprint,
  decision, and review metadata.

Exit criteria:

- Alpha entity writes happen through MCP helpers.
- Tool signatures and JSON Schemas match.
- State-machine and validation-mode tests pass.
- Every actionable alpha finding has an executable or formally recognized
  disposition.

## Phase 3 - Indexing And Corpus Migration

Goal: migrate representative v0 data and prove that read-side behavior
matches the new ontology.

Backlog:

- Extend the SQLite/FTS5 index with schema-declared interfaces.
- Implement `query_by_interface` for at least `Record` and `Versioned`.
- Index typed Binding edges, provenance, ownership, hierarchy, and event
  subjects.
- Build v0-to-v1 migration adapters for the alpha corpus.
- Implement declarative migration drafting, planning, and execution with
  source-hash preconditions and recovery journals.
- Support bounded operations for path moves, field updates, entity renames,
  reference rewrites, and archival.
- Preserve predecessor/successor links, durable ID aliases, and unknown-field
  reports without silently rewriting append-only logs.
- Measure field loss and orphan rates.
- Add index drift detection and `reindex` recovery tests.

Exit criteria:

- A representative v0 fixture corpus migrates without manual aibox
  steps.
- Interface queries return mixed-kind results correctly.
- Migration reports are deterministic and actionable.
- Migration-backed doctor findings can be planned, executed, and rechecked
  cleanly through the shipped gateway.

## Phase 4 - Skills, Agents, And Runtime Surfaces

Goal: make skills and agent-facing instructions use the v1.0 model.

Backlog:

- Update skill metadata and trigger guidance to v1.0 ontology language.
- Remove v0 primitive assumptions from write-side skill instructions.
- Add canned agent scenarios covering work, decisions, risks, gates,
  roles, skills, artifacts, and migrations.
- Update gateway, per-domain MCP, and harness compatibility docs.
- Add malformed-output measurements for scenario runs.
- Keep aibox as an adapter path, not a core test dependency.

Exit criteria:

- Canned scenarios pass with malformed output below the acceptance
  threshold.
- Skills use MCP write paths for canonical entities.
- Runtime docs describe gateway and per-domain modes consistently.

## Phase 5 - First-ART Validation

Goal: prove the rebuild with a production-shaped ART cycle.

Backlog:

- Model Portfolio, ValueStream, ART, Team, Scope, RoleSlot, and
  TeamMember structures.
- Run PI planning with objectives, risks, dependencies, capacity, and
  committed WorkItems.
- Execute the cycle through MCP transitions and gates.
- Capture demo evidence, Measurements, Outcomes, Decisions, and
  inspect-and-adapt follow-up.
- Record friction, interpretation drift, missing concepts, and missing
  tool affordances.
- Review the first-ART evidence before rc promotion.

Exit criteria:

- The first-ART pilot completes planning, execution, demo, and
  inspect-and-adapt.
- pk-doctor reports no blocking errors on the pilot corpus.
- Human reviewers can inspect the same state through files and docs.

## Phase 6 - Cutover Preparation

Goal: prepare `v1.0.0` without calendar-driven release pressure.

Backlog:

- Verify all strict gate criteria through A5.
- Produce reproducible release artifacts from a clean checkout.
- Publish migration and downstream adoption guidance.
- Finalize v0.x maintenance and LTS policy.
- Record the cutover decision.
- Prepare merge strategy from `v1.0` to `main`.

Exit criteria:

- No known blocker remains for final `v1.0.0` cutover.
- The cutover decision is recorded.
- Docs and release artifacts are published and reproducible.

## Phase 7 - Post-cutover Stabilisation

Goal: stabilize the v1 line after release.

Backlog:

- Observe the minimum 14-day stabilization window.
- Track and triage critical regressions.
- Exercise downstream migration support.
- Verify release integrity, provenance, docs publication, and package
  installation.
- Run index rebuild, drift recovery, MCP smoke, sensitive-data, and
  adversarial pk-doctor fixtures.
- Validate one v0.x LTS slow-adopter scenario if needed.

Exit criteria:

- Stabilization findings are closed, tracked, or accepted.
- Release integrity and adversarial fixture checks pass.
- v1.x becomes the normal development line after cutover.
