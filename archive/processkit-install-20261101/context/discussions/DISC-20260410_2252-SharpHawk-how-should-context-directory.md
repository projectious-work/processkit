---
apiVersion: processkit.projectious.work/v2
kind: Discussion
metadata:
  id: DISC-20260410_2252-SharpHawk-how-should-context-directory
  created: '2026-04-10T22:52:14+00:00'
  updated: '2026-04-11T05:03:40+00:00'
spec:
  question: How should context/ directory structure, primitive taxonomy (Artifact
    vs Note), Zettelkasten linking, and AGENTS.md scope be clarified and improved
    in processkit?
  state: archived
  opened_at: '2026-04-10T22:52:14+00:00'
  participants:
  - ACTOR-claude
  - ACTOR-owner
  closed_at: '2026-04-10T22:53:34+00:00'
---

## Driving questions

1. Why do agents create free-form files instead of using skills/MCP
   tools?
2. Where do team descriptions, work instructions, PRDs, and research
   results belong?
3. What is the difference between an Artifact, a Work Instruction,
   and a Note?
4. What directory structure should `context/` have, and why does
   `discussions/` exist as a top-level directory?
5. Should Note be a separate primitive or a subtype of Artifact?
6. Are Artifact entities pointers or self-hosted documents?
7. Is the Zettelkasten linking mechanism (qualified note-to-note
   links) missing from the Note schema?

## Resolutions

### R1 — AGENTS.md bloat is an antipattern
Keep AGENTS.md as complete as necessary but as lean as possible.
It should contain only what an agent needs at session start that
cannot be derived from the project structure or entities.

### R2 — Team configuration belongs in Actor entity files
Model, role (PM vs developer), and parallelism pattern for AI actors
belong in their Actor entity files — not in AGENTS.md. Actor
profiles have their own update cycle; duplicating this in AGENTS.md
causes immediate drift.

### R3 — Work instructions are Artifacts
A project-specific operational document (asciinema recording guide,
release procedure variant) is a `kind: document` Artifact. No new
primitive needed. For formal repeatable processes, use a Process
entity in `context/processes/`.

### R4 — Artifact schema must acknowledge self-hosted content
The description "processkit does not store artifact content itself;
just the pointer" is inconsistent with actual usage (the PRD stores
its full content inline). Two valid patterns must be documented:
- **Self-hosted**: Markdown body after frontmatter; `location` may
  self-reference or be omitted.
- **Pointer**: deliverable lives elsewhere; `location` is the URL,
  path, or storage ID.

### R5 — Note stays a separate primitive (lifecycle justifies it)
Notes have lifecycle mechanics (state machine, `review_due`,
`promotes_to`) that Artifacts lack. These are the mechanics that
make the Zettelkasten capture-and-promote workflow function. Note
and Artifact schemas should cross-reference the distinction
explicitly.

### R6 — Note type taxonomy should align with Luhmann/Ahrens
In the Luhmann/Ahrens model, permanent notes are never discarded.
The current `type` enum (fleeting, insight, reference, question)
approximates but does not map cleanly to (fleeting, literature,
permanent). The mapping and intent should be explicit in the schema
description. Notes are not inherently ephemeral.

### R7 — Qualified links are missing from the Note schema (critical)
The Zettelkasten insight-generation mechanism depends on qualified
note-to-note links — not just tags. Tags are for categorical
discovery; links with explicit relation and context are for
reasoning. The Note schema needs a `links` field:

    links:
      - target: NOTE-xxx-yyy
        relation: elaborates  # elaborates | contradicts | supports
                              # | is-example-of | see-also | refines
                              # | sourced-from
        context: "One sentence explaining why this connection matters."

The `context` sub-field is non-optional in Luhmann practice.

### R8 — context/ uses one directory per primitive kind (correct)
The current scheme is correct: one top-level directory per `kind:`,
flat instance files within. The indexer eliminates the need for
subtype subdirectories.

### R9 — Discussion is a legitimate separate primitive
Discussion models structured deliberation (question → exploration →
DecisionRecord). The epistemic arc: Note → Discussion →
DecisionRecord → WorkItem.

### R10 — Missing directories need documenting in AGENTS.md
context/owner/, context/actors/, context/roles/ are defined in
schemas but absent from the AGENTS.md layout table.

### R11 — MCP config paths are stale after skills reorganization
The .mcp.json still references pre-reorganization paths. Correct
paths are under context/skills/processkit/<name>/mcp/server.py.
Config must be regenerated.
