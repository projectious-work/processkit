---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1049-KeenCrane-add-docs-content-from
  created: '2026-04-10T10:49:35+00:00'
spec:
  title: Add docs content from aibox to WildButter docs-site
  state: backlog
  type: task
  priority: high
  description: '5 content blocks from aibox docs belong in processkit''s own docs-site
    (source: aibox/move-to-processkit/docs-content/processkit-docs-content.md).


    Content to migrate:

    1. Package composition table with "Best for" descriptions (minimal/managed/software/research/product)

    2. Package composition references — what each tier composes and why the tiers
    exist

    3. Skill catalogue browsing instructions (GitHub links, release assets, local
    context/ path)

    4. "processkit not yet deployed" placeholder → replace with real docs links once
    site is live

    5. "Why this split?" rationale — reusable content, forkable catalog, independent
    release cadence, smaller aibox


    These blocks currently live in aibox''s docs as stand-ins. Once WildButter ships,
    aibox docs should link to processkit rather than duplicating this content.'
  parent: BACK-20260409_1652-WildButter-create-polish-and-deploy
---
