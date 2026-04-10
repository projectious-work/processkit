---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1840-SteadyLeaf-skills-directory-reorganization
  created: '2026-04-10T18:40:00+00:00'
spec:
  title: Reorganize context/skills/ into 7 category subdirectories
  state: backlog
  type: story
  priority: high
  description: >
    The flat context/skills/ layout (110+ skills) is hard to navigate.
    Reorganize into 7 category subdirectories. processkit/ stays flat (no
    sub-subdirectories at this stage).


    **Target structure:**

    - processkit/   — skills for operating the processkit system itself
    - engineering/  — software design, architecture, backend, languages
    - devops/       — infrastructure, CI/CD, ops, monitoring, incident management
    - data-ai/      — data science, ML, AI/LLM, embeddings
    - product/      — product management, discovery, communication
    - documents/    — document and content authoring
    - design/       — visual, UI, and frontend design
    - _lib/         — internal shared utilities (stays at root, not a public category)


    **Work items:**

    1. Move all SKILL.md directories to the correct category subdir.

    2. Add `category:` field to every SKILL.md YAML frontmatter, matching the
       subdir name.

    3. Update skill-finder to be category-aware (filter by category in agent
       find-mode; expose category in catalog-mode — see BACK-20260410_1840-AmberCliff).

    4. Update any cross-references within SKILL.md files that use relative paths.

    5. Update context/skills/INDEX.md to reflect the new structure.

    6. Verify processkit indexer picks up moved files cleanly (reindex if needed).


    **Prerequisite for:** BACK-20260410_1840-AmberCliff (skill-finder catalog
    extension) which depends on consistent category metadata in frontmatter.
---
