---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1840-SteadyLeaf-skills-directory-reorganization
  created: '2026-04-10T18:40:00+00:00'
  updated: '2026-04-11T06:11:32+00:00'
spec:
  title: Reorganize context/skills/ into 7 category subdirectories
  state: done
  type: story
  priority: high
  description: "The flat context/skills/ layout (110+ skills) is hard to navigate.\
    \ Reorganize into 7 category subdirectories. processkit/ stays flat (no sub-subdirectories\
    \ at this stage).\n\n**Target structure:**\n- processkit/   — skills for operating\
    \ the processkit system itself - engineering/  — software design, architecture,\
    \ backend, languages - devops/       — infrastructure, CI/CD, ops, monitoring,\
    \ incident management - data-ai/      — data science, ML, AI/LLM, embeddings -\
    \ product/      — product management, discovery, communication - documents/  \
    \  — document and content authoring - design/       — visual, UI, and frontend\
    \ design - _lib/         — internal shared utilities (stays at root, not a public\
    \ category)\n\n**Work items:**\n1. Move all SKILL.md directories to the correct\
    \ category subdir.\n2. Add `category:` field to every SKILL.md YAML frontmatter,\
    \ matching the\n   subdir name.\n\n3. Update skill-finder to be category-aware\
    \ (filter by category in agent\n   find-mode; expose category in catalog-mode\
    \ — see BACK-20260410_1840-AmberCliff).\n\n4. Update any cross-references within\
    \ SKILL.md files that use relative paths.\n5. Update context/skills/INDEX.md to\
    \ reflect the new structure.\n6. Verify processkit indexer picks up moved files\
    \ cleanly (reindex if needed).\n\n**Prerequisite for:** BACK-20260410_1840-AmberCliff\
    \ (skill-finder catalog extension) which depends on consistent category metadata\
    \ in frontmatter."
  started_at: '2026-04-11T06:11:26+00:00'
  completed_at: '2026-04-11T06:11:32+00:00'
---

## Transition note (2026-04-11T06:11:26+00:00)

Shipped in commit e86ad06.


## Transition note (2026-04-11T06:11:32+00:00)

context/skills/ reorganized into 7 category subdirectories in commit e86ad06.
