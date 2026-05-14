---
apiVersion: processkit.projectious.work/v2
kind: WorkItem
metadata:
  id: BACK-20260410_1840-SleekSky-theme-creator-skill
  created: '2026-04-10T18:40:00+00:00'
spec:
  title: Create theme-creator skill — color theory, palette generation, Radix-style
    scales
  state: backlog
  type: story
  priority: medium
  description: |
    New skill: theme-creator. Deeply specialized color skill, separate from but coordinating with brand-design (StoutCrow / BACK-20260410_1050-StoutCrow).

    **Scope:**
    1. Deep internet research (web search) on how major color tools work — Coolors,
       ColorMagic, Designs.ai Colormatcher, Adobe Color, Paletton, Colormind,
       PaletteMaker — covering generation algorithms, harmony models, psychology
       annotation, and accessibility checks. Findings inform the baked-in knowledge.

    2. Color theory foundations: color wheel models (RYB, RGB, HSL, OKLCH),
       harmony rules (monochromatic, complementary, analogous, triadic,
       split-complementary, tetradic), contrast principles, WCAG accessibility.

    3. Color psychology per-hue reference: meaning and communication intent for
       each major hue family (trust/authority → blue, energy/warmth → orange, etc.)
       baked in as a decision table.

    4. Palette output formats the skill can generate:

       a. Brand palette: 2–7 brand colors (primary and secondary are part of this
          range, not additional). On top of the brand colors: one neutral/gray
          (with compatible tones) and three semantic colors ok/warning/error
          (with compatible tones). Total output varies by requested brand color count.

       b. 12-step Radix-style scale (per Radix UI Colors specification):
          full 12-step scale, with-alpha variant, grayscale variant.

    5. Annotated output: every swatch in every palette gets a role label +
       psychological rationale (why this color, what it communicates, how to use it).

    6. Tool landscape awareness: knows when to recommend Coolors, Adobe Color,
       Paletton, etc. for specific user needs (the research from step 1 becomes
       embedded knowledge).


    **Relationship to StoutCrow:** brand-design covers brand identity holistically (logo, typography, voice, visual language). theme-creator is the color-specialist sub-skill. brand-design invokes theme-creator for the color subsystem.

    Use skill-builder. Add to design category (post-reorganization).
---
