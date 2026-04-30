---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260415_2030-CommandNexus-pk-prefix-namespace-and-command-strategy
  created: '2026-04-15T20:30:00+00:00'
spec:
  title: Adopt `/pk-<verb>` as the processkit command namespace; ship commands only
    for processkit-owned capabilities
  state: accepted
  decision: |
    (1) Every slash command processkit ships — now and going forward — uses the `/pk-<verb>` prefix. No unprefixed processkit commands. (2) processkit commands wrap processkit skills AND fill cross- harness gaps. For lifecycle commands not uniformly built-in across all major harnesses (Claude Code, Codex CLI, Cursor, OpenCode, Aider), processkit ships its own `/pk-<verb>`. Two delivery surfaces: (2a) **Skill-driven** — the command invokes a processkit skill.
         Used for planning, release, research, meta commands.
    (2b) **AGENTS.md-driven** — the command reads a structured
         `<!-- pk-commands -->` YAML block in AGENTS.md and executes
         the project's declared command. Used for build, test, lint,
         fmt — project-specific tools that vary per repo but whose
         ergonomic availability should be uniform across harnesses.
    The earlier exclusion of build/test/lint/deploy is REVERSED per owner decision on 2026-04-16 after a cross-harness built-in matrix showed 4 of 5 harnesses ship zero build/test coverage. See DISC-20260416_0800-CommandScope for the full discussion. (3) Long-form commands (`/workitem-management-create`, `/release-semver-prepare`) remain as aliases indefinitely — no deprecation pressure. `/pk-<verb>` is an additive ergonomic surface, not a replacement. (4) When community convention converges on an unprefixed short verb (e.g. `/release`, `/retro`), users who want it pull a thin local alias (`.claude/commands/release.md` → invoke `/pk-release`). aibox may ship an opt-in alias pack, but processkit itself does not ship unprefixed aliases.
  context: |
    v0.17.0 is processkit's first release that adds ergonomic short slash commands on top of the existing 25 `<skill>-<verb>` long-form commands. A strategy review was run on 2026-04-15 via RES-CommandCompass (ART-20260415_1830), which confirmed that (a) the community has converged on short top-level verbs (`/standup`, `/release`, `/decide`, `/onboard`, `/test`, `/deploy`), and (b) processkit already provides the capability behind ~90% of those verbs but hides it behind long-form names invisible from `/` autocomplete.
    The owner flagged that without an explicit namespace strategy, we risk (i) colliding with harness built-ins (Claude Code ships `/team-onboarding`, `/review`, `/security-review`, `/insights`, `/statusline`), (ii) colliding with user-local customisations, and (iii) over-promising by shipping wrappers over project tools processkit doesn't actually own.
  rationale: |
    Four cross-cutting reasons.
    (1) Namespace collision avoidance. `/pk-resume` will never clash with a harness built-in or a user's own `/onboarding.md`.
    (2) Scope honesty. `/pk-release` is opinionated about the processkit release flow (CHANGELOG + PROVENANCE + tag + smoke test). Shipping `/release` unprefixed would falsely promise processkit can release any project.
    (3) Ergonomic discoverability preserved. Users who want bare `/release` create a 3-line local alias file; aibox can ship an opt-in alias pack. processkit does not force the decision.
    (4) Strategic brand signal. Over time `/pk-` becomes a recognisable namespace: "this command runs the processkit- canonical version of the flow." That signal compounds as the kit grows.
  alternatives:
  - option: Blanket cover community verbs unprefixed (e.g. /release, /retro).
    rejected_because: Collides with harness built-ins and user-local commands; over-promises
      scope; forces processkit into project- tooling territory it does not own.
  - option: Dual-ship — every command exists as both /pk-<verb> and /<verb>.
    rejected_because: Doubles the surface area, creates two aliases users must keep
      in sync, and still triggers collision concerns for the unprefixed form. No ergonomic
      gain over the 3-line local alias.
  - option: Ship unprefixed short verbs only for commands with no harness-builtin
      collision.
    rejected_because: Inconsistent mental model ("is this one pk- or not?"); demands
      the kit track harness-builtin evolution; breaks down the first time a harness
      ships a new built-in.
  consequences:
  - All future processkit commands adopt `/pk-<verb>`.
  - processkit DOES ship `/pk-build`, `/pk-test`, `/pk-lint` as AGENTS.md-driven commands
    (reads a structured YAML block in AGENTS.md, executes the project's declared command).
    Reversed 2026-04-16 after cross-harness matrix showed 4/5 harnesses ship zero
    build/test coverage. `/pk-deploy` deferred to v0.18.0.
  - If a new capability is added as a processkit skill, its short alias ships as `/pk-<verb>`
    with the skill.
  - Long-form `<skill>-<verb>` commands stay as aliases; no deprecation pressure on
    either direction.
  - aibox may ship an opt-in alias pack for users who want unprefixed community-verb
    access; this is explicitly aibox's concern, not processkit's.
  supersedes: []
  superseded_by: null
  related:
  - ART-20260415_1830-CommandCompass-processkit-slash-command-inventory-and-proposal
  - ART-20260415_2000-ShadowCount-rail5-marker-calibration
  - BACK-20260415_1700-QuietLedger-rail5-auto-decision-capture-implementation
  - DISC-20260416_0800-CommandScope-v017-command-strategy-session
  v017_command_scope:
    ship:
    - /pk-resume    (morning-briefing-generate)     — session start
    - /pk-status    (standup-context-write)         — mid-session status
    - /pk-standup   (alias of /pk-status)           — community-naming alias
    - /pk-wrapup    (session-handover-write)        — session end
    - /pk-note      (note-management-capture)       — fleeting capture + Zettelkasten
      link suggestion
    - /pk-discuss   (discussion-management-start)   — multi-turn engagement
    - /pk-research  (research-with-confidence-investigate)
    - /pk-release   (release-semver-prepare)
    - /pk-publish   (release-semver-publish)
    - /pk-test      (AGENTS.md-driven)              — reads pk-commands.test from
      AGENTS.md
    - /pk-build     (AGENTS.md-driven)              — reads pk-commands.build from
      AGENTS.md
    - /pk-lint      (AGENTS.md-driven)              — reads pk-commands.lint from
      AGENTS.md
    - /pk-review    (skill-driven)                  — processkit code-review
    bug_fix:
    - FEAT-XS — tool_use / tool_result / isCompactSummary / isSidechain filter in
      decision_markers transcript reader (from ART-ShadowCount §9).
    defer_to_v018:
    - /pk-groom    (context-grooming-run)
    - /pk-retro    (retrospective skill — must be designed + built first)
    - FEAT-M — LLM-classifier variant for Rail 5 Lever 1
    dropped_from_v017:
    - /pk-decide   (decisions are conversational; Rail 5 shadow-mode + long-form /decision-record-write
      cover it; revisit after LLM-classifier lands)
    - '/pk-onboard  (split into /pk-resume + /pk-wrap + /pk-status per owner feedback:
      three distinct moments, not one)'
    - /pk-capture  (superseded by /pk-note + /pk-discuss)
---

# Notes

This decision emerged from a 2026-04-15 working conversation between
the owner and ACTOR-pm-claude (Opus) after the CommandCompass research
landed. The owner explicitly requested the conversation be recorded
as a DecisionRecord so the strategic rationale survives any future
`/clear` or context loss.

## Summary of the decision process

- CommandCompass (ART-20260415_1830) surfaced 7 proposed must/should-
  ship commands and three open questions.
- Owner pushed back on naming (wanted namespace clarity),
  on `/pk-decide` (wrong shape for conversational decisions), and
  asked for a command-strategy clarification.
- Three options considered: A (pk-prefix only, processkit-owned
  only), B (blanket unprefixed), C (dual-ship). Option A chosen.
- Session-start / session-end / mid-status decomposed into three
  distinct commands (`/pk-resume`, `/pk-wrap`, `/pk-status`) reflecting
  three real moments, not one onboarding event.
- Capture-moment split into `/pk-note` (one-way fleeting) and
  `/pk-discuss` (two-way structured engagement) — two primitives,
  two commands.

## Decisions bundled into this record

1. `/pk-<verb>` is the processkit command namespace. Exclusive.
2. processkit commands wrap processkit skills — not project tooling.
3. v0.17.0 command set: 9 aliases + 1 bug fix as listed above.
4. v0.18.0 defer list as listed above.
5. Dropped from v0.17.0: `/pk-decide`, `/pk-onboard`, `/pk-capture`.
6. Long-form commands stay as aliases indefinitely.
7. `/pk-standup` ships as a community-naming alias of `/pk-status`.
