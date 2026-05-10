---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260509_1318-KindSpruce-pk-doctor-add-v1-entity-drift
  created: '2026-05-09T13:18:20+00:00'
  labels:
    github_issue: 22
    area: pk-doctor
    cluster: v1-drift
  updated: '2026-05-10T03:46:03+00:00'
spec:
  title: 'pk-doctor: add v1_entity_drift check (gh#22)'
  state: done
  type: task
  priority: medium
  description: 'Triaged from GH #22. No pk-doctor check surfaces stale v1-frontmatter
    entities in directories where v2 successors exist. aibox v0.25.6 has 3,450 v1
    files; concerning slice: 72 v1 workitems, 33 v1 decisions, 9 v1 actors (whole
    dir superseded by team-members/), 9 v1 process files (superseded by Scope+Gate).\n\nNew
    check `v1_entity_drift` in `context/skills/processkit/pk-doctor/scripts/checks/`:\n-
    Walk `context/<dir>/*.md` for registered entity directories\n- For files with
    `apiVersion: ...v1`, look up v2 successor in table (Actor→TeamMember; Process→Scope+Gate;
    StateMachine→lifecycle; Model→Artifact model-spec)\n- WARN per file when successor
    exists; INFO for immutable dirs (logs/, migrations/applied/)\n- `--fix`: interactively
    call `apply_migration` for matching v1→v2 Migration, or propose creating one\n\nPrereq:
    gh#23 (doc gap) — `v2_contracts.py`/`context_hygiene.py`/`schema_vocabulary.py`
    may already cover parts of this; document them first to know.'
  started_at: '2026-05-09T13:48:40+00:00'
  completed_at: '2026-05-10T03:46:03+00:00'
---

## Transition note (2026-05-09T13:48:40+00:00)

Wave 2 dispatch — TEAMMEMBER-finn (SE/senior) on Sonnet 4.5. FierceIvy (gh#23) prereq satisfied; doc of v2_contracts/context_hygiene/schema_vocabulary now available so finn can scope v1_entity_drift to avoid duplication.


## Transition note (2026-05-09T13:53:53+00:00)

v1_entity_drift check landed (~265 lines incl. successor/entity-dir/immutable-prefix tables). Registered in checks/__init__.py after v2_contracts. SKILL.md bullet added. Both trees mirrored (diff -r clean modulo __pycache__). On this repo expect ~0 WARNs (dogfood is already v2) + 1 aggregate INFO v1.immutable-bucket; on aibox v0.25.6 should surface the 72 v1 workitems / 33 decisions / 9 actors / 9 processes as WARNs. No tests added (no per-check pattern exists in pk-doctor). Smoke-checked via py_compile only — sandbox blocked runtime import of pyyaml. Worth a quick `--category=v1_entity_drift` real run before merge.


## Transition note (2026-05-10T03:46:03+00:00)

Shipped to main on 2026-05-09 via PR #24; closing per v0.26.0 release prep.
