---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260426_1529-TidyLynx-extend-v0-23-0
  created: '2026-04-26T15:29:25+00:00'
spec:
  title: 'Extend v0.23.0 scope: add TidyGrove + NobleBrook + AmberCliff + BraveMeadow'
  state: accepted
  decision: |
    Add four small backlog items to the v0.23.0 batch on top of the four already done (CalmArch, RapidDaisy, VastLark, SolidWolf):

    - BACK-20260409_1830-TidyGrove — Release audit skill (validate entity files, skills, structure pre-tag).
    - BACK-20260409_1738-NobleBrook — Skill DAG validator (cycle + layer-constraint checks).
    - BACK-20260410_1840-AmberCliff — skill-finder catalog query mode (user-facing discovery).
    - BACK-20260410_1049-BraveMeadow — Verify owner-profiling reference files (observable-signals.md + interview-protocol.md).

    Implementation will be parallelized via four subagents at sonnet tier (matches the team-roster 85% Sonnet allocation), one per WI, working concurrently. Files touched are largely disjoint (release-audit/ new, pk-doctor/ check, skill-finder/ extension, owner-profiling/ verification) so merge risk is low.

    Release flow stays the same as v0.22.1: bump aibox.lock processkit pin → CHANGELOG entry → stamp src/PROVENANCE.toml → commit → tag → push → gh release create → gh release view verify.
  context: DEC-20260426_1214-SoundLark fixed the v0.22.1/v0.23.0 release shape with
    v0.23.0 floored at CalmArch + RapidDaisy + VastLark + SolidWolf and "additions
    TBD" pending owner grooming. Owner has now finished grooming and selected four
    additional cheap-to-ship items, all of which independently de-risk future releases
    (release-audit + skill-DAG validator) or close known docs/scaffolding gaps (skill-finder
    catalog mode, owner-profiling reference files).
  rationale: Each of the four items is small, self-contained, and theme-coherent with
    the existing v0.23.0 batch ("data quality + scaffolding + governance"). TidyGrove
    and NobleBrook materially reduce future-release risk — both pre-tag validation,
    exactly the kind of safety net that would have caught FierceWren-class bugs earlier.
    AmberCliff is a docs/UX win that uses already-shipped MCP infrastructure (no new
    MCP server). BraveMeadow is a verification-only task that closes a documented
    gap. Bundling them now avoids release-fragmentation drag; Sonnet-tier parallel
    implementation keeps cost and Opus-context low.
  alternatives:
  - option: Ship v0.23.0 with the original four only
    rejected_because: Owner judged that adding four cheap items still leaves the release
      focused and meaningfully reduces future-release risk via the two new validators.
  - option: Add larger items (SureHeron CI harness, BoldVale FTS5)
    rejected_because: Both are bigger investments; folding them in would inflate the
      release scope and delay the tag. Reserved for v0.24.0.
  consequences: v0.23.0 ships 8 items instead of 4, but each is small. Four parallel
    subagents are dispatched concurrently; merge conflicts are not expected because
    target dirs are disjoint. Pre-tag pk-doctor must remain green — any new check
    from NobleBrook or TidyGrove that flags on the existing tree must be fixed in
    the same release or its WARN/INFO surface explained in CHANGELOG.
  related_workitems:
  - BACK-20260409_1830-TidyGrove-release-audit-skill-validate
  - BACK-20260409_1738-NobleBrook-skill-dag-validator-cycle
  - BACK-20260410_1840-AmberCliff-skill-finder-catalog-extension
  - BACK-20260410_1049-BraveMeadow-verify-and-complete-owner
  decided_at: '2026-04-26T15:29:24+00:00'
---
