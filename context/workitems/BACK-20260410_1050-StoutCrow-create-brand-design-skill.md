---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1050-StoutCrow-create-brand-design-skill
  created: '2026-04-10T10:50:00+00:00'
spec:
  title: Create brand-design skill — W3C DTCG tokens, logo system, brand voice
  state: backlog
  type: story
  priority: medium
  description: brand-design skill does not exist in src/context/skills/ or context/skills/.
    Full spec in NOTE-20260410_1046-NobleComet (sourced from aibox/move-to-processkit/research/brand-design-skills-2026-03.md).
    Spec covers W3C DTCG JSON as source of truth, Style Dictionary for multi-format
    output, logo system (7 variants), color system (OKLCH), typography, brand voice,
    social card templates. Use skill-builder. Add to product package tier. Update
    skill-finder.

    Color subsystem is handled by a separate specialist skill — theme-creator
    (BACK-20260410_1840-SleekSky). brand-design should invoke theme-creator for
    palette and scale generation rather than embedding color theory directly.
---
