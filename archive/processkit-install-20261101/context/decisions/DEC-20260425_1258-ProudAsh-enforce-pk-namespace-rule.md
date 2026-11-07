---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260425_1258-ProudAsh-enforce-pk-namespace-rule
  created: '2026-04-25T12:58:49+00:00'
spec:
  title: Enforce /pk- namespace rule on release-semver and research-with-confidence
    SKILL.md commands metadata
  state: accepted
  decision: Revert the `metadata.processkit.commands[]` blocks in `context/skills/devops/release-semver/SKILL.md`
    and `context/skills/product/research-with-confidence/SKILL.md` (and their `src/context/`
    mirrors) to declare /pk-prefixed names — `pk-release`, `pk-publish`, `pk-research`
    — matching the canonical files already present in `commands/`. Delete the 6 untracked
    duplicate non-namespaced files (3 in each skill's `commands/` dir × 2 skills,
    plus their `.claude/commands/` mirrors).
  context: pk-doctor surfaced 4 drift WARNs caused by 6 untracked command files (`release-semver-prepare.md`,
    `release-semver-publish.md`, `research-with-confidence-investigate.md`) that exist
    in `context/skills/.../commands/` and `.claude/commands/` but have no `src/context/`
    mirror. Investigation showed these duplicates were spawned because the two SKILL.md
    `metadata.processkit.commands[]` blocks declare verbose, non-`pk-`-prefixed names.
    The canonical aliases (`pk-release`, `pk-publish`, `pk-research`) already exist
    in `src/context/skills/.../commands/` and conform to the project's documented
    namespace rule.
  rationale: 'Project memory rule (project_pk_command_namespace): "all processkit
    slash commands ship as /pk-<verb>; commands wrap processkit skills only, never
    project tooling." Mirroring the new files would entrench the violation; the right
    fix is at the metadata source so the next installer/auto-fill pass produces /pk-*
    files instead.'
  alternatives:
  - option: Mirror the untracked files into src/context/ to silence the drift WARNs
    reason_rejected: Entrenches the namespace-rule violation and creates two parallel
      command surfaces.
  - option: Delete the dupes only, leave SKILL.md metadata as-is
    reason_rejected: The next installer/auto-fill run that reads metadata.commands[]
      would re-create the same dupes — does not fix the root cause.
  - option: Update the namespace rule itself to allow verbose skill-prefixed command
      names
    reason_rejected: Owner has a stated preference encoded in memory; would require
      a discussion, not a unilateral change.
  consequences: 'Drift WARNs clear on next pk-doctor run. Future skill authors must
    use /pk-<verb> names in `metadata.processkit.commands[]`. Worth considering: a
    pk-doctor check that flags any `commands[].name` that does not start with `pk-`
    for processkit-tier (and dependent-tier) skills.'
  decided_at: '2026-04-25T12:58:49+00:00'
---
