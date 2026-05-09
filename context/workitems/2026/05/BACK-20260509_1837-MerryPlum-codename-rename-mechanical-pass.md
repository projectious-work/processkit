---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1837-MerryPlum-codename-rename-mechanical-pass
  created: '2026-05-09T18:37:22+00:00'
  labels:
    github_issue_parent: 20
    area: team-creator
    cluster: team-model-v2
    epic_sub: SUB-5
    design_artifact_ref: ART-20260509_1836-SmartPanda-team-creator-v2-design
    effort: small
    model_class: fast
    owner_role: ROLE-technical-writer/specialist
  updated: '2026-05-09T19:06:13+00:00'
spec:
  title: 'team-creator v2 SUB-5: codename rename pass (mechanical)'
  state: review
  type: chore
  priority: low
  description: 'Sub-item of VastVale (gh#20). Mechanical search-and-replace in context/skills/processkit/team-creator/SKILL.md
    and likely also commands/, references/, chartering DecisionRecord template. Targets:
    ''OpenWeave'' → ''team-creator override layers''; ''OpenWeave layers 1-4'' → ''override
    layers 1-4''; ''TeamWeaver Phase 3 dogfood'' → ''the 2026-04-15 internal review''
    (keep ART-20260415_1545 ID stable, rename display title only). DEC ID codename
    suffixes (BraveFalcon, LoyalComet, etc.) NOT renamed (immutable refs); add one-line
    gloss on first use. No schema change, no architectural decision. Effort: small.
    Owner role: ROLE-technical-writer/specialist. Model class: fast (Haiku). Depends
    on: nothing — parallel-safe. Architectural reference: ART-20260509_1836-SmartPanda-team-creator-v2-design
    §"Gap 2 — Codename rename".'
  parent: BACK-20260509_1318-VastVale-team-creator-v2-5-design-gaps
  started_at: '2026-05-09T18:40:30+00:00'
---

## Transition note (2026-05-09T18:40:30+00:00)

Wave 4 SUB-5 dispatch — ephemeral ROLE-technical-writer/specialist on Haiku 4.5. Mechanical rename, parallel-safe, no dependency on the 6 open questions.


## Transition note (2026-05-09T19:06:13+00:00)

Wave 4 SUB-5 shipped on Haiku. 12 total replacements across 2 mirror trees: SKILL.md (4×2), references/tiering-formula.md (1×2), references/team-weights-decision-schema.md (1×2). All "OpenWeave" surfaces collapsed to plain phrasing; "TeamWeaver Phase 3 dogfood" → "the 2026-04-15 internal review". DEC IDs and ART-20260415_1545-TeamWeaver-* preserved (immutable refs). diff -r clean, no uncertainties flagged.
