---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260410_1840-SunnyLily-library-expert-skills-concept
  created: '2026-04-10T18:40:00+00:00'
  updated: '2026-04-30T12:39:50+00:00'
spec:
  title: Library expert skills — concept spike, template, and pilot batch
  state: done
  type: story
  priority: medium
  description: |
    Concept spike and pilot for StackOverflow-style library expert skills: self-contained problem → solution format with real code examples baked in. Covers two skill types: (a) tech-stack recommender, (b) per-library expert.

    **Step 1 — Audit existing library skills:**
    Read and evaluate reflex-python and pandas-polars (both exist) against the concept criteria. What works, what is missing, what should carry over into the new template. These are the baseline.

    **Step 2 — Exploit existing research:**
    Read and synthesize: - NOTE-20260410_1046-SteadyTiger (skill marketplace landscape — quality
      patterns, best practices from 40K+ skills analysis)
    - NOTE-20260410_1046-RapidPeak (skills quality audit — current gaps, the
      "thin tier" analysis, checklist template)

    Extract: what distinguishes high-quality library skills from thin ones, what the market shows is in demand vs underserved.

    **Step 3 — Sharpen RAG integration:**
    Define the RAG stance: baked-in examples are primary (offline-first, no retrieval latency). RAG is an optional augmentation layer for: - Current-version docs when the skill's examples are version-pinned older - Finding answers outside the baked-in recipe set
    Specify how a library skill signals to the agent when to reach for the rag-engineering skill vs use what is baked in. Document in the template.

    **Step 4 — Define the library skill template:**
    Required frontmatter: - `library_version: "X.Y"` — version the examples are pinned to - `library_homepage:` — canonical docs URL - Standard category (engineering/ or data-ai/ etc.)
    Required content structure: - Intro: one-liner on the library, when to use it - Choosing section (if alternatives exist): decision table - Recipes: 5–15 blocks, each with:
      - **Problem** headline (short, searchable: "Group by and aggregate",
        "Read Parquet with schema enforcement")
      - **Solution** code block (syntactically correct, copy-pasteable, minimal)
      - Optional: one-line "Watch out" note for common pitfalls
    - Reference links to official docs sections

    **Step 5 — Library-skill builder component:**
    Extend or create a dedicated section in skill-builder for researching and building library skills. Workflow: (1) verify library_version, (2) identify the 10 most common use-case patterns from docs + Stack Overflow, (3) write recipe blocks, (4) version-pin frontmatter, (5) verify code correctness. This can operate as a sub-invocation of skill-builder or as a standalone research-and-build skill.

    **Step 6 — Pilot batch (5 skills):**
    After template is defined and builder process works: - pandas-polars — upgrade existing to new template (add version pins, expand
      recipes to 10+)
    - reflex-python — same upgrade - great-tables — new skill (Python table rendering library) - pydantic — new skill (data validation) - httpx — new skill (async HTTP)

    **Step 7 — Tech-stack recommender skill (type a):**
    Separate lighter skill — reasons about which libraries to choose for a given problem domain and language. Does not contain usage recipes. References library expert skills by name for hand-off. Covers: Python data stack, Python web/API stack, Python AI/ML stack as initial domains.
  started_at: '2026-04-30T11:03:42+00:00'
  completed_at: '2026-04-30T12:39:50+00:00'
---

## Transition note (2026-04-30T11:03:42+00:00)

Started library expert concept work: added skill-builder library-expert template and RAG escalation stance. Existing-skill audits and pilot batch remain open.


## Transition note (2026-04-30T12:39:50+00:00)

Implemented library-expert template, skill-builder workflow guidance, skill-reviewer audit checks, and skill-finder discoverability. Validation passed.


## Transition note (2026-04-30T12:39:50+00:00)

Implemented library-expert template, skill-builder workflow guidance, skill-reviewer audit checks, and skill-finder discoverability. Validation passed.
