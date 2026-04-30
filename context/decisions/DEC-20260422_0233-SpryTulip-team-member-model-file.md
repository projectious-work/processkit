---
apiVersion: processkit.projectious.work/v2
kind: DecisionRecord
metadata:
  id: DEC-20260422_0233-SpryTulip-team-member-model-file
  created: '2026-04-22T02:33:37+00:00'
spec:
  title: Team-member model, file-based tiered memory, A2A Agent Cards, and team-manager
    skill
  state: accepted
  decision: 'Replace the Actor abstraction with a Team-Member abstraction that supports
    two patterns: persistent core team (humans + named AI personas) and ephemeral
    consultants (role+seniority invocations resolved at dispatch — no persisted entity).
    Persistent team-members are file-based directory trees (persona.md + A2A-compatible
    card.json + tiered memory: working / episodic / semantic / procedural / relational
    / lessons) stored as Markdown with YAML frontmatter. Adopt topical (non-personal)
    filenames; add a `private/` subdirectory per team-member for developer-local content
    (gitignored by default). Adopt a default-exclude export policy: exports include
    persona, card, knowledge, skills, lessons; exclude journal/, relations/, project-scoped
    content. Introduce a new `team-manager` skill that owns lifecycle, a curated international
    name pool (~60 names), memory-tree scaffolding, export/import with A2A signature
    validation, and 10 consistency checks — wired into pk-doctor as a 5th check category
    `team_consistency`. Ship `.gitignore.example` at the processkit repo root bundling
    all project gitignores. Reflection cadence: per-task + daily journal + weekly
    promotion with Park-style importance scoring and Ebbinghaus decay.'
  context: 'Current design has 10 actor files: 8 role-class that duplicate roles 1:1
    (no information gain) and 2 identity-class. The role-class layer is dead ceremony.
    Ad-hoc agent-harness worker incarnations are already ephemeral — they don''t need
    persistence. The industry (2025-2026) has converged on file-based, tiered agent
    memory (DiffMem, GitAgent, AGENTS.md — 60k+ repos), cross-vendor memory import/export
    (Claude Mar 2026, Gemini Mar 2026), A2A signed Agent Cards (Linux Foundation Sept
    2025, v0.3), and dual-memory poisoning defenses (A-MemGuard against MemoryGraft/MINJA,
    achieving >95% attack reduction). The value proposition for persistent AI team-members
    accrues over time via six vectors: accumulated domain knowledge, observed working
    preferences, project history + rationale, relational intelligence, reflected lessons,
    and skill maturation — making the team-member an exportable asset that can travel
    to other projects.'
  rationale: '(1) Collapsing role-class actors eliminates duplication with zero information
    loss. (2) File-based Markdown+frontmatter matches processkit''s aesthetic: diffable,
    grep-able, git-tracked, portable by tarball, not vendor-locked. (3) The tiered
    memory architecture (working/episodic/semantic/procedural/relational/lessons)
    is the convergent 2025-2026 pattern across MemGPT/Letta, mem0, Zep/Graphiti, CrewAI,
    A-MEM. (4) Topical filenames + `private/` subdirectory + sensitivity frontmatter
    tags cover the shared-vs-local axis cleanly (mirrors .env / .env.local convention).
    (5) International name pool owned by team-manager prevents naming collisions and
    keeps AI team-member names human-friendly and non-brand-conflicting. (6) A2A Agent
    Cards are near-zero-cost to ship now (one JSON file per team-member) and high-value
    if A2A becomes standard. (7) The lessons/ tier implements A-MemGuard-style consensus
    defense against memory-poisoning attacks. (8) pk-doctor integration routes findings
    through the existing error/warning pipeline — no new UI surface needed.'
  alternatives:
  - option: Keep actor-role distinction and layer memory on top
    rejected_because: Preserves empty ceremony; 8 role-class actors add complexity
      without information gain over roles.
  - option: Vector/graph-backed memory (mem0, Zep/Graphiti)
    rejected_because: Vendor-locked, not diffable in git, breaks processkit's file-based
      aesthetic; can still be added later as an index layer over the canonical files.
  - option: Shared memory only, no private/ subdirectory
    rejected_because: Developers need a place for private observations and local-only
      context; .env/.env.local convention is established and understood.
  - option: Personal-name filenames like bernhard-work-style.md
    rejected_because: Leaks identity into every path; topical filenames + slug-keyed
      relations/ achieve the same intent without the leak.
  - option: Export-by-default including project-scoped journal
    rejected_because: Risk of privacy/confidentiality leaks on team-member export;
      default-exclude with opt-in is the safer policy.
  - option: Single mandatory reflection cadence (daily only)
    rejected_because: Research (Park et al., Meta-Policy Reflexion 2025) shows multi-tier
      cadence produces higher-quality semantic memory than a single consolidation
      point.
  consequences: Breaking change; no backward compatibility (per user directive). Deprecates
    `actor-profile` skill; renames schema `actor.yaml` → `team-member.yaml`; removes
    MCP tools create_actor/get_actor/… in favor of create_team_member/get_team_member/…
    Requires migration of `ACTOR-20260421_0144-ThriftyOtter-owner` to new structure
    and removal of `ACTOR-20260421_0144-AmberDawn-legacy-historical-backfill` (not
    meaningful). Removes 8 role-class actors. Adds `.gitignore.example` at repo root
    + installer hook to seed per-project. Adds memory consolidation cadence (per-task
    + daily + weekly). Adds export/import tooling with signature validation. pk-doctor
    gains 5th check category `team_consistency` with 10 sub-checks. Agent harnesses
    that previously read actor files must be updated — one-time breakage acknowledged.
  deciders:
  - ACTOR-20260421_0144-ThriftyOtter-owner
  related_workitems:
  - BACK-20260422_0231-WildSeal-v0-19-0-phase
  - BACK-20260422_0231-TallWillow-v0-19-0-phase
  - BACK-20260422_0232-CuriousOwl-v0-19-0-phase
  decided_at: '2026-04-22T02:33:36+00:00'
---
