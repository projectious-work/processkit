---
apiVersion: processkit.projectious.work/v1
kind: WorkItem
metadata:
  id: BACK-20260423_1103-ToughMeadow-pk-doctor-skill-missing
  created: '2026-04-23T11:03:18+00:00'
  updated: '2026-04-23T20:56:00+00:00'
spec:
  title: pk-doctor skill missing commands/ directory — /pk-doctor slash command not
    registered in derived projects
  state: review
  type: bug
  priority: high
  assignee: TEAMMEMBER-cora
  description: '## Report (derived project)


    A derived project reported that `/pk-doctor` is not available despite v0.19.1
    installing the skill.


    - SKILL.md for pk-doctor ships, with `metadata.processkit.commands:` block declaring
    a `pk-doctor` command.

    - Implementation (`scripts/doctor.py`) ships.

    - `commands/` directory is absent — so there is no `commands/pk-doctor.md` for
    the installer''s slash-command registration step to pick up.


    ## Local confirmation


    `ls context/skills/processkit/pk-doctor/` → only `SKILL.md` and `scripts/`. Peer
    skills (status-briefing, model-recommender) ship `commands/pk-*.md`. Audit of
    all processkit skills with `commands:` metadata blocks shows pk-doctor is the
    **only** affected skill — narrow fix.


    Template mirror `context/templates/processkit/v0.19.1/pk-doctor/` confirms the
    gap was present at release time.


    ## Scope


    1. Create `context/skills/processkit/pk-doctor/commands/pk-doctor.md` matching
    the wording/structure of peer command files (short stanza invoking the skill).

    2. Re-mirror into the template tree as part of the next release.

    3. Derived-project repair path: once v0.19.2 ships, installer upgrade should pick
    this up automatically since the per-skill config hash will change — cross-ref
    TrueQuail (BACK-20260423_0829-TrueQuail) which is about exactly this drift-reconciliation
    gap.

    4. Cross-skill audit (already done locally, result: pk-doctor only) should be
    memorialized as a pk-doctor health check: "every skill with a `commands:` metadata
    block has a matching `commands/*.md` file for each entry."


    ## Why


    - Blocks every derived project from running `/pk-doctor` — the skill whose entire
    purpose is surfacing health problems.

    - Fix is minutes of work; shipping it in v0.19.2 avoids a dedicated v0.19.3 patch.

    - Covered by DEC-20260423_1101-SunnyComet-extend-v0-19-2.


    ## Done criteria


    - `commands/pk-doctor.md` exists in `context/skills/processkit/pk-doctor/`.

    - File content mirrors the `commands: [{name: pk-doctor, ...}]` stanza from SKILL.md.

    - Template mirror regenerated (or noted as a release-time step).

    - pk-doctor itself grows a health check for `commands:` metadata ↔ `commands/`
    directory consistency.'
  started_at: '2026-04-23T20:50:16+00:00'
---

## Transition note (2026-04-23T20:50:16+00:00)

Dispatching in parallel with TrueQuail.


## Transition note (2026-04-23T20:56:00+00:00)

Shipped: commands/pk-doctor.md (both trees), new commands_consistency check module (both trees), registry wired, SKILL.md updated. Check runs green for pk-doctor itself. Check also surfaced broader SKILL.md commands-metadata inconsistency across ~11 other skills — filed as follow-up WI BACK-20260423_2055-HappyFinch, NOT in this WI's scope. scripts/check-src-context-drift.sh clean.
