---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260415_1830-CommandCompass-processkit-slash-command-inventory-and-proposal
  created: 2026-04-15 18:30:00+00:00
spec:
  name: CommandCompass — processkit slash-command inventory and v0.17.0 proposal
  kind: document
  location: context/artifacts/ART-20260415_1830-CommandCompass-processkit-slash-command-inventory-and-proposal.md
  format: markdown
  version: 1.0.0
  tags:
  - research
  - slash-commands
  - provider-neutral
  - v0.17.0
  - proposal
  produced_by: ACTOR-sr-researcher
  owner: ACTOR-sr-researcher
  links:
    inputs:
    - ART-20260415_1600-QuietLedger-rail5-auto-decision-capture-research
    - ART-20260414_1545-SharpGrid-follow-up-harness-capability-matrix
    related_decisions: []
---

# CommandCompass — processkit slash-command inventory and v0.17.0 proposal

**Author:** Senior Researcher (Opus) — ACTOR-sr-researcher
**Date:** 2026-04-15
**Audience:** Owner review, gates the v0.17.0 command-set FEAT(s).

---

## 1. Methodology

Sources used:

- **Codebase enumeration** — `Glob` over
  `context/skills/{processkit,devops}/*/commands/*.md` plus inspection
  of representative command files (`release-semver-prepare.md`,
  `workitem-management-create.md`, `team-review.md`,
  `morning-briefing-generate.md`).
- **Skill catalog** — `context/skills/processkit/skill-finder/SKILL.md`
  for trigger-phrase mapping and category buckets.
- **Per-harness slash surface** — already mapped in
  `ART-20260415_1600-QuietLedger` §4.1; that matrix is the ground truth
  for *which harnesses support custom slash commands*. Not repeated
  here. Updates since QuietLedger, where surfaced by web research,
  are flagged inline.
- **Web research (2026-04-15)** — Claude Code built-in commands,
  Codex CLI `~/.codex/prompts/`, Cursor `.cursor/commands/`, OpenCode
  `.opencode/command/`, plus `awesome-claude-code` and the Claude
  Command Suite for community lifecycle commands.
- **Owner constraint memory** — `feedback_no_skill_inflation.md`. The
  same logic ("extend before invent") applies to commands: prefer
  another command in an existing skill over a new skill-less command.

Confidence convention (unchanged from house style):
**Confirmed** (primary doc) / **Likely** (multiple secondary or strong
inference) / **Weak** (single secondary) / **Speculation** (no source).

All web claims dated 2026-04-15; re-verify at implementation.

---

## 2. Inventory — every existing processkit / devops command

Twenty-five command files exist today, spread across thirteen skills.
Provider reach is uniform: every command is a markdown file with YAML
frontmatter that aibox's installer translates into the per-harness
location (`.claude/commands/`, `~/.codex/prompts/`,
`.cursor/commands/`, `.opencode/command/`). Aider is excluded — no
slash surface (Confirmed via QuietLedger §4.1).

Reach legend: **CC** Claude Code · **CX** Codex CLI · **CR** Cursor ·
**OC** OpenCode · **AI** Aider.

| # | Skill | Command | Purpose | Reach |
|---|---|---|---|---|
| 1 | release-semver (devops) | `release-semver-prepare` | Bump version, draft changelog, create tag | CC CX CR OC |
| 2 | release-semver (devops) | `release-semver-publish` | Execute publish phase of the prepared release | CC CX CR OC |
| 3 | session-handover | `session-handover-write` | Generate end-of-session handover document | CC CX CR OC |
| 4 | owner-profiling | `owner-profiling-bootstrap` | Run initial profiling interview | CC CX CR OC |
| 5 | owner-profiling | `owner-profiling-refine` | Refine an existing owner profile | CC CX CR OC |
| 6 | owner-profiling | `owner-profiling-observe` | Record a behavioural observation | CC CX CR OC |
| 7 | skill-reviewer | `skill-reviewer-bulk-gotchas` | Bulk Gotchas-generation pass across catalog | CC CX CR OC |
| 8 | skill-reviewer | `skill-reviewer-audit` | 11-category audit of one skill | CC CX CR OC |
| 9 | note-management | `note-management-promote` | Promote a fleeting note to permanent artifact | CC CX CR OC |
| 10 | note-management | `note-management-review` | Review fleeting notes; promote/discard | CC CX CR OC |
| 11 | note-management | `note-management-capture` | Capture a new fleeting note | CC CX CR OC |
| 12 | morning-briefing | `morning-briefing-generate` | Session-start orientation summary | CC CX CR OC |
| 13 | skill-builder | `skill-builder-create` | Start interactive skill-creation workflow | CC CX CR OC |
| 14 | workitem-management | `workitem-management-create` | Create a new WorkItem | CC CX CR OC |
| 15 | standup-context | `standup-context-write` | Generate a standup update for today | CC CX CR OC |
| 16 | decision-record | `decision-record-query` | Query existing decisions matching args | CC CX CR OC |
| 17 | decision-record | `decision-record-write` | Record a new decision | CC CX CR OC |
| 18 | context-grooming | `context-grooming-run` | Prune and compact project context | CC CX CR OC |
| 19 | model-recommender | `model-recommender-profile` | Show capability profile for a model | CC CX CR OC |
| 20 | model-recommender | `model-recommender-setup` | Configure model access (questionnaire) | CC CX CR OC |
| 21 | model-recommender | `model-recommender-refresh` | Research/update model roster (Workflow C) | CC CX CR OC |
| 22 | model-recommender | `model-recommender-route` | Route a task to optimal model (Workflow B) | CC CX CR OC |
| 23 | team-creator | `team-create` | Compose a provider-neutral AI team | CC CX CR OC |
| 24 | team-creator | `team-rebalance` | Rebalance one or more team roles | CC CX CR OC |
| 25 | team-creator | `team-review` | Read-only team health-check / drift report | CC CX CR OC |

**Observations on the inventory:**

- **Naming convention is rigorously `<skill>-<verb>`.** Two exceptions
  (`team-create`, `team-rebalance`, `team-review`) because the skill
  is `team-creator` but the operations are short verbs without the
  full skill prefix. This is mild inconsistency, not breakage.
- **No top-level short aliases.** Nothing like `/standup`, `/decide`,
  `/onboard`, `/release`, `/groom`. Every invocation requires the full
  skill prefix. This is the gap the owner's question is probing.
- **No `/init`, `/help`, `/clear`, `/compact`-style session commands.**
  All harnesses ship those built-in; processkit does not need to
  duplicate (Confirmed from web search; see refs 1, 11, 12).
- **Several skills have zero commands.** `artifact-management`,
  `event-log`, `task-router`, `skill-gate`, `skill-finder`,
  `status-update-writer`, `agent-management`, `binding-management`,
  many `*-management` primitives. These rely on natural-language
  invocation through MCP tools or the trigger-phrase table — by
  design, not by oversight.

---

## 3. External landscape — typical lifecycle commands in the wild

Bucketed by lifecycle phase. Commands prefixed `/` are the typical
in-the-wild names; *italic* commands are processkit's nearest
equivalent today (if any).

### 3.1 Session

Universally built-in; downstream projects almost never re-implement.

- `/init` — bootstrap a CLAUDE.md / AGENTS.md (Claude Code built-in,
  Confirmed, ref 11).
- `/clear`, `/compact`, `/cost`, `/status`, `/help`, `/statusline`,
  `/insights` — Claude Code built-ins (Confirmed, ref 11).
- `/team-onboarding` — Claude Code built-in (v2.1.101, 2026-04-11)
  that scans CLAUDE.md, skills, hooks, recent workflows and writes a
  ramp-up guide (Confirmed, ref 2).
- Codex CLI offers `/exit`, `/help`, plus `/prompts:<name>` invocation
  for custom prompts in `~/.codex/prompts/` (Confirmed, ref 5).
- *processkit equivalents:* `/morning-briefing-generate`,
  `/session-handover-write`, `/context-grooming-run` cover the
  start-of-session and end-of-session arc that the harness built-ins
  do not.

### 3.2 Planning

- `/standup`, `/standup-report`, `/team:standup-report` —
  community-popular; summarise yesterday/today/blockers from git
  history (Likely, ref 2, ref 7).
- `/retro`, `/team:retrospective-analyzer` — weekly retrospective
  pulling commit history, shipping streaks, test-health (Likely,
  ref 2, ref 7).
- `/plan`, `/spec`, `/prd` — generate planning artifacts
  (Likely, ref 7, ref 9).
- `/decide`, `/adr` — record an architectural decision (Likely;
  community pattern, also processkit's QuietLedger Lever 3).
- *processkit equivalents:* `/standup-context-write`,
  `/decision-record-write`, `/workitem-management-create`. No retro
  command yet (gap).

### 3.3 Build / test

- `/build`, `/test`, `/lint`, `/fmt`, `/typecheck` — community
  staples; almost always shell out to project-specific Make/npm/cargo
  targets (Likely, ref 7, ref 6, ref 13).
- These are a thin wrapper around the project's existing build tool;
  they are not portable across projects. Each project re-defines them
  in its own `.claude/commands/`.
- *processkit equivalents:* none. processkit ships skills like
  `tdd-workflow`, `testing-strategy`, `ci-cd-setup` but no slash
  commands that wrap the project's actual build tool.

### 3.4 Review

- `/review` — Claude Code built-in (Confirmed, ref 1, ref 11).
- `/security-review` — Claude Code built-in (Confirmed via
  awesome-claude-code, ref 4; also surfaced in slash-finder above).
- `/code-review`, `/architectural-review` — community variants
  in Claude-Command-Suite (Likely, ref 7).
- *processkit equivalents:* `/team-review` (model-tier drift only;
  not code review). The `code-review` and `code-architecture-review`
  capability lives in skills, not commands.

### 3.5 Release

- `/release`, `/changelog`, `/version-bump`, `/publish`,
  `/docs:create-release-notes` — community standard
  (Likely, ref 7, ref 13).
- *processkit equivalents:* `/release-semver-prepare`,
  `/release-semver-publish`. **Strong match — already covered.**
  The only gap is the *short* alias: nothing called `/release`.

### 3.6 Ops

- `/deploy`, `/rollback`, `/incident`, `/oncall`, `/postmortem` —
  community; almost always project-specific (Likely, ref 6, ref 7).
- `gh`, `glab`, `linear`, `jira` — out-of-band CLIs; not exposed via
  slash commands but referenced from them.
- *processkit equivalents:* none. Skills exist
  (`incident-response`, `postmortem-writing`, `alerting-oncall`) but
  no commands. Mostly project-specific anyway.

### 3.7 Research

- Outside the AI-harness world, no consensus CLI for research
  workflows. eLabFTW + JupyterLab are notebook-based, not
  command-based (Confirmed, ref 14).
- AI-harness community: `/research`, `/literature-review`,
  `/hypothesis` exist as bespoke commands in individual repos, no
  standard (Weak, ref 4).
- *processkit equivalents:* no slash command. The
  `research-with-confidence` skill handles the workflow but is
  invoked by trigger phrase only.

### 3.8 Administrative / meta

- `/onboard`, `/team-onboarding` — Claude Code built-in plus
  community variants (Confirmed for built-in, ref 2).
- `/docs:create-onboarding-guide`, `/docs:create-architecture-doc` —
  Claude-Command-Suite (Likely, ref 7).
- `/groom`, `/cleanup`, `/audit` — community (Likely, ref 4).
- *processkit equivalents:* `/owner-profiling-bootstrap`,
  `/context-grooming-run`, `/skill-reviewer-audit`.

**Biggest takeaway from the external scan:** the community
converges on **short top-level verbs** (`/standup`, `/release`,
`/decide`, `/onboard`, `/test`, `/deploy`) rather than the
`<skill>-<verb>` style processkit uses. processkit has the
*capability* in nearly every case; what it lacks is the **short
alias surface** that makes commands discoverable from `/` autocomplete
without first knowing the skill name.

---

## 4. Gap analysis — owner-mentioned commands + adjacent surfacing

For each command, four columns: **already?** / **cross-project?** /
**owner?** / **best path**.

### 4.1 `/onboard`

- **Already?** Partial. Claude Code ships `/team-onboarding` as a
  built-in (Confirmed, ref 2) — duplicates the *teammate ramp* angle.
  processkit ships `/owner-profiling-bootstrap` for the
  *owner ramp* angle, which is different (one-time, per-owner, feeds
  the actor-profile system).
- **Cross-project?** Yes for the teammate-ramp angle, but the
  built-in already covers it. The processkit-specific angle is the
  **project-onboarding** one: "you just installed processkit on a
  fresh project — what do I do next?" That is *not* covered by the
  built-in or by `owner-profiling-bootstrap`.
- **Owner?** processkit (the project-onboarding angle is intrinsic to
  processkit; aibox handles installer concerns but not orientation).
- **Best path:** add `/onboard` as an alias-style command that
  delegates to a new short flow in `morning-briefing` or, better,
  hosted on `skill-finder` itself (the natural home for "where do I
  start"). No new skill. **Recommended host: `skill-finder`** —
  paired with the `core: true` flag already on that skill.

### 4.2 `/team-review`

- **Already?** Yes. `team-review` exists as a fully-fledged command
  on `team-creator` (#25 in the inventory) — already a short verb,
  already host-skill correct.
- **Cross-project?** Yes — every processkit consumer with an AI team
  benefits from drift detection.
- **Owner?** processkit.
- **Best path:** keep as-is. This is a *false gap* — already
  matches the proposed style. Optionally add `/team` as an even
  shorter alias that prints `team-review` output by default; low
  priority.

### 4.3 `/build`

- **Already?** No.
- **Cross-project?** **No.** processkit itself uses `npm`, but
  downstream projects are Python / Rust / Go / mixed. The body of
  any `/build` command is project-specific shell.
- **Owner?** Not processkit. The right pattern is for processkit's
  installer (aibox) to scaffold a per-project `.claude/commands/build.md`
  containing whatever the project's actual build command is — or for
  the project owner to add it themselves.
- **Best path:** **do not ship.** Document the pattern in AGENTS.md
  ("typical project commands you may want to add: `/build`, `/test`,
  `/lint`, `/fmt`, `/deploy` — these are project-specific; add them
  to your own `.claude/commands/`"). aibox follow-up: scaffold an
  optional template set on `aibox init`.

### 4.4 `/test`

- Same analysis as `/build`. Project-specific. Do not ship.

### 4.5 `/release`

- **Already?** Yes — `/release-semver-prepare` and
  `/release-semver-publish`. The functional capability is fully
  present. What is missing is the **short alias** `/release` that the
  community expects.
- **Cross-project?** Yes — semver is the processkit convention,
  enforced by the `release-semver` skill.
- **Owner?** processkit.
- **Best path:** add `/release` as a thin alias on the
  `release-semver` skill that defaults to "prepare" and accepts an
  optional `publish` argument. Two-line markdown file. Same skill,
  no inflation. (Aibox installer already places this skill in
  `devops/release-semver/` — alias lives alongside.)

### 4.6 `/research`

- **Already?** Capability yes (the `research-with-confidence` skill),
  command no — the only entry point is the trigger phrase.
- **Cross-project?** Yes — every processkit consumer benefits from
  the "investigate with confidence labels" workflow that produced
  this very artifact and QuietLedger.
- **Owner?** processkit.
- **Best path:** add `/research` (or
  `/research-with-confidence-investigate`) on the
  `research-with-confidence` skill. Argument-hint = the topic to
  investigate. Body: "Use the research-with-confidence skill to
  investigate `$ARGUMENTS` with explicit confidence labels and
  produce an artifact."

### 4.7 Adjacent commands surfaced (not in owner's list)

These appeared repeatedly in the external scan and have a clean
processkit host with no skill inflation:

- **`/decide`** — already in scope as QuietLedger Lever 3 follow-up;
  alias on `decision-record`. Listed as "should" below.
- **`/standup`** — alias on `standup-context` (existing skill).
  Community names match; processkit's name is wordier.
- **`/retro`** — *new* command on the existing `retrospective` skill
  (per skill-finder, the `retrospective` skill exists at
  category-level — verify file). A retro command would close the
  weekly-cadence gap visible in the external scan.
- **`/groom`** — alias on `context-grooming` (existing).
- **`/handover`** — alias on `session-handover` (existing).
- **`/note`** — alias on `note-management` (existing
  `note-management-capture`).
- **`/changelog`** — capability lives in the `changelog` skill; the
  release flow already touches it. Probably *don't* ship a separate
  command — `/release` covers it transitively.
- **`/audit`** — too generic (security audit? skill audit? dependency
  audit?). Skip.

---

## 5. Proposal — canonical v0.17.0 command set

Hard cap: ten new commands across all priority tiers. The proposal
uses seven new commands plus zero new skills. All are aliases to
existing skill capabilities; bodies are 1–3 lines of markdown.

| Proposed | Host skill | One-line purpose | Priority | Rationale | Open question |
|---|---|---|---|---|---|
| `/onboard` | `skill-finder` | Orient a new owner / fresh project — where to start, what to read first | **must** | Closes the project-onboarding gap that built-in `/team-onboarding` does not cover; lives on the always-installed `core: true` skill | Should it interview the owner (delegate to `owner-profiling-bootstrap`) or just print the orientation? |
| `/release` | `release-semver` | Prepare a semver release (alias for `release-semver-prepare`) | **must** | Community-standard short verb; capability already present | Should `/release publish` execute the publish phase, or only `/release-semver-publish`? |
| `/decide` | `decision-record` | Record a decision (alias for `decision-record-write`) | **must** | QuietLedger Lever 3 already specced this; aligns with Rail 5 enforcement work | None — design already in QuietLedger §4.3 |
| `/research` | `research-with-confidence` | Investigate a topic with explicit confidence labels and produce an artifact | **should** | Community pattern; canonicalises the workflow that produced this artifact | Should the alias enforce an artifact ID prefix convention or leave free-form? |
| `/standup` | `standup-context` | Generate today's standup (alias for `standup-context-write`) | **should** | High-frequency use; matches community naming | None |
| `/groom` | `context-grooming` | Prune and compact project context (alias for `context-grooming-run`) | **could** | Saves keystrokes; low marginal value | Risk of accidental destructive grooming if owner mis-types? Probably acceptable |
| `/retro` | `retrospective` (verify exists as a skill, not just a trigger) | Generate a weekly retrospective from git history + WorkItem state | **could** | Closes an external-scan gap; the only proposed command that would *create* meaningful new functionality (not just rename) | Does the `retrospective` skill exist as a `SKILL.md` or only as a trigger phrase pointing nowhere? Resolve before scoping. |

**Summary of proposal (3 must, 2 should, 2 could, 0 won't-as-new):**

- 3 **must** ship in v0.17.0: `/onboard`, `/release`, `/decide`.
- 2 **should** ship in v0.17.0 if effort permits: `/research`,
  `/standup`.
- 2 **could** ship in v0.17.0 or slip to v0.18.0: `/groom`, `/retro`.

**Effort estimate.** All five must/should commands are ≤5 lines of
markdown each. Total wall time across all seven: ~2 hours including
PROVENANCE refresh. The `/retro` command is the only one with
non-trivial body content (it must generate a retro from project
state) — call it ~0.5 day if the host skill exists, +1 day if the
skill needs authoring (which would itself violate
no-skill-inflation; see §6).

---

## 6. Anti-pattern flags — tempting but rejected

These were considered and explicitly rejected. Each is recorded so
that future owners do not re-propose them without revisiting these
reasons.

- **`/build`, `/test`, `/lint`, `/fmt`, `/typecheck`, `/deploy`,
  `/rollback`** — project-specific bodies; processkit cannot supply
  a meaningful default. Belongs in either (a) a per-project
  `.claude/commands/` written by the project owner or (b) an
  aibox-installer scaffold that copies a template set on `aibox init`.
  Shipping these from processkit would either be empty stubs (bad UX)
  or guess wrong about the project's tooling (worse UX).
- **`/changelog`** — would duplicate `/release`. The release flow
  already updates the changelog; a standalone command splits the
  surface without adding capability.
- **`/team`** — too generic. `team-create`, `team-rebalance`,
  `team-review` are already short verbs and disambiguate; adding a
  shorter `/team` would either overlap one of them (which?) or be a
  no-op help screen (low value).
- **`/audit`** — ambiguous. Maps to one of `dependency-audit`,
  `secure-coding`, `skill-reviewer-audit` depending on context. A
  generic command that asks "audit what?" is friction, not ergonomics.
- **`/init`** — already a Claude Code built-in (Confirmed, ref 11).
  Overriding the built-in would surprise users.
- **`/insights`, `/clear`, `/compact`, `/status`, `/help`,
  `/cost`** — Claude Code built-ins (Confirmed, ref 11). Same logic.
- **`/security-review`** — Claude Code built-in (Confirmed, ref 4).
  Don't shadow.
- **A new `commands` skill** to host orphan aliases — explicit
  no-skill-inflation violation. Aliases live with the skill they
  delegate to.

### Won't ship v0.17.0 (and why)

- **`/build`, `/test`, `/lint`, `/fmt`, `/deploy`** — project-specific;
  not processkit's responsibility. **Action: AGENTS.md gets a
  paragraph documenting the pattern; aibox follow-up issue tracks
  optional scaffold templates.**
- **`/postmortem`, `/incident`, `/oncall`** — capability lives in
  devops skills already; demand is project-specific (most processkit
  consumers are not on-call). **Action: defer; revisit when a
  consumer asks for it.**
- **`/changelog`, `/version-bump`** — covered transitively by
  `/release`. **Action: defer indefinitely.**
- **`/literature-review`, `/hypothesis`, `/experiment`** — research
  niche; the existing `research-with-confidence` skill plus the
  proposed `/research` alias is sufficient for a v0.17.0 baseline.
  **Action: revisit if a research-heavy consumer requests it.**

---

## 7. Open questions for the owner review

1. **Project-onboarding scope.** Should `/onboard` be an
   *interactive interview* (calls into `owner-profiling-bootstrap`)
   or a *one-shot orientation* (prints "read AGENTS.md, run
   `/morning-briefing-generate`, then look at the WorkItem queue")?
   The interactive flavour is higher-value but heavier; the one-shot
   is shippable in an hour.
2. **`/release` argument semantics.** Three options: (a) `/release`
   = prepare only, `/release-semver-publish` keeps its full name;
   (b) `/release [prepare|publish]` with prepare as the default;
   (c) `/release` = prepare, `/publish` = publish (two short
   verbs). The community pattern (ref 7) is closest to (a) or (b).
   Owner pick required to land the alias.
3. **Does the `retrospective` skill have a `SKILL.md`?** The
   `skill-finder` trigger table maps "retrospective", "retro",
   "lessons learned" → `retrospective`, but my codebase enumeration
   did not surface any commands under it. Need to confirm whether
   the skill exists as a real directory or only as a planned trigger.
   If it does not exist, `/retro` either drops to "won't ship v0.17.0"
   or forces a no-skill-inflation override (which is itself an open
   question).
4. **Naming style — long vs short?** Adopting short aliases is a
   one-way door for community familiarity but creates a dual surface
   (`/decide` *and* `/decision-record-write`). Owner: do we keep
   both forever, deprecate the long forms over two minor releases,
   or only ship the short form for a hand-picked subset?
5. **Per-harness publication scope.** All seven proposed commands
   work on Claude Code, Codex CLI, Cursor, OpenCode (Confirmed via
   QuietLedger §4.1 and refs 5, 6, 8). Aider has no slash surface —
   the natural-language fallback already exists. Confirm this is
   the agreed-on portability bar (no Aider-specific wrapper).
6. **AGENTS.md vs slash command for `/onboard`.** The orientation
   text would also fit naturally as an AGENTS.md "Getting started"
   section. If we add the section, do we still need the command?
   (My recommendation: yes — discoverable from `/` autocomplete is
   how new users find things. AGENTS.md is read once, not browsed.)
7. **aibox installer scaffold for project-specific commands.** If we
   accept that `/build`, `/test`, `/deploy` are project-specific, is
   the right next step an aibox FEAT to scaffold an opt-in template
   set, or do we leave it entirely to project owners? Out of scope
   for v0.17.0 itself but a downstream open question.

---

## 8. Provenance / sources

| Ref | URL | Used for | Confidence |
|---|---|---|---|
| 1 | https://code.claude.com/docs/en/slash-commands | Custom slash commands in `.claude/commands/`; built-ins | Confirmed |
| 2 | Claude Code v2.1.101 release notes (via web search 2026-04-15) — `/team-onboarding` built-in | Built-in onboarding command | Likely |
| 3 | https://github.com/hesreallyhim/awesome-claude-code | Community catalog of slash commands | Confirmed |
| 4 | https://github.com/qdhenry/Claude-Command-Suite | Production-ready community commands incl. `/docs:*`, `/team:*` | Likely |
| 5 | https://developers.openai.com/codex/cli/slash-commands | Codex CLI slash commands and `~/.codex/prompts/` | Confirmed |
| 6 | https://developers.openai.com/codex/custom-prompts | Codex custom-prompt frontmatter (`description:`, `argument-hint:`) | Confirmed |
| 7 | https://github.com/wshobson/commands | Production-ready commands collection (57 commands) | Likely |
| 8 | https://opencode.ai/docs/commands/ | OpenCode `.opencode/command/<name>.md` + frontmatter (`description`, `agent`, `model`, `subtask`) | Confirmed |
| 9 | https://cursor.com/docs/cli/reference/slash-commands | Cursor `.cursor/commands/` (v1.6, 2025-09-12) | Confirmed |
| 10 | https://www.scriptbyai.com/claude-code-commands-cheat-sheet/ | Claude Code commands cheat sheet 2026 | Likely |
| 11 | https://learn-prompting.fr/blog/claude-code-slash-commands-reference | Claude Code slash commands reference 2026 | Likely |
| 12 | https://clskills.in/blog/claude-code-slash-commands-2026 | Complete list of Claude Code slash commands 2026 | Likely |
| 13 | https://dev.to/subprime2010/claude-code-custom-slash-commands-build-your-own-deploy-review-test-1ifc | Community DIY `/deploy`, `/review`, `/test` patterns | Likely |
| 14 | https://subjectguides.york.ac.uk/openresearch/lifecycle | Open research lifecycle reference (eLabFTW, JupyterLab) | Confirmed |
| 15 | ART-20260415_1600-QuietLedger-rail5-auto-decision-capture-research | Per-harness slash-surface matrix (§4.1) | — |
| 16 | ART-20260414_1545-SharpGrid-follow-up-harness-capability-matrix | Cross-harness capability ground truth | — |

All web sources verified 2026-04-15; re-verify at implementation.
