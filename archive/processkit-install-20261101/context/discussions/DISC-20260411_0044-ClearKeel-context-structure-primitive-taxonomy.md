---
apiVersion: processkit.projectious.work/v2
kind: Discussion
metadata:
  id: DISC-20260411_0044-ClearKeel-context-structure-primitive-taxonomy
  created: '2026-04-11T00:44:00+00:00'
  updated: '2026-04-11T05:03:41+00:00'
spec:
  question: How should the context/ directory, primitive taxonomy, and Zettelkasten
    linking be structured and clarified in processkit?
  state: archived
  opened_at: '2026-04-11T00:44:00+00:00'
  closed_at: '2026-04-11T00:44:00+00:00'
  participants:
  - ACTOR-claude
  - ACTOR-owner
  outcomes: []
---

## Driving questions

1. Why do agents create free-form files instead of using skills/MCP tools?
2. Where do team descriptions, work instructions, PRDs, and research
   results belong?
3. What is the difference between an Artifact, a Work Instruction, and
   a Note?
4. What directory structure should `context/` have, and why does
   `discussions/` exist as a top-level directory?
5. Should Note be a separate primitive or a subtype of Artifact?
6. Are Artifact entities pointers or self-hosted documents?
7. Is the Zettelkasten linking mechanism (qualified note-to-note links)
   missing from the Note schema?

## Resolutions

### R1 — AGENTS.md bloat is an antipattern
Keep AGENTS.md as complete as necessary but as lean as possible.
It should contain only what an agent needs at session start that
cannot be derived from the project structure or entities. Anything
with its own lifecycle, owner, or update cadence belongs in an
entity.

### R2 — Team configuration belongs in Actor entity files
Model, role (PM vs developer), and parallelism pattern for AI actors
belong in their Actor entity files — not in AGENTS.md. Actor profiles
have their own update cycle; duplicating this in AGENTS.md causes
immediate drift.

### R3 — Work instructions are Artifacts
A project-specific operational document (asciinema recording guide,
release procedure variant) is a `kind: document` Artifact. No new
primitive is needed. For formal repeatable processes, use a Process
entity in `context/processes/`.

### R4 — Artifact schema should acknowledge self-hosted content
The schema description ("processkit does not store artifact content
itself; just the pointer") is inconsistent with actual usage (the
PRD artifact stores its full content inline). The schema should
acknowledge two valid patterns:
- **Self-hosted**: Markdown body after frontmatter; `location` may
  self-reference or be omitted.
- **Pointer**: deliverable lives elsewhere; `location` is the URL,
  path, or storage ID.

### R5 — Note state machine justifies keeping it separate from Artifact
Notes have lifecycle mechanics (state machine, `review_due`,
`promotes_to`) that Artifacts lack. These mechanics are what make
the Zettelkasten capture-and-promote workflow function. Merging Note
into Artifact would require adding optional lifecycle fields to
Artifact, changing its character for non-note uses. Note stays a
separate primitive, but the schemas should cross-reference the
distinction explicitly.

### R6 — Notes are not ephemeral; the type taxonomy needs alignment
In Luhmann/Ahrens, permanent notes are never discarded — they are
the knowledge base. The current `type` enum (fleeting, insight,
reference, question) approximates but does not cleanly map to the
three canonical types (fleeting, literature, permanent). The mapping
should be made explicit in the schema description.

### R7 — Qualified links are missing from the Note schema
The Zettelkasten insight-generation mechanism depends on qualified
note-to-note links, not just tags. Tags are for categorical
discovery; links with context are for reasoning. The Note schema
needs a `links` field:

```yaml
links:
  - target: NOTE-xxx-yyy
    relation: elaborates  # elaborates | contradicts | supports |
                          # is-example-of | see-also | refines |
                          # sourced-from
    context: "One sentence explaining why this connection matters."
```

The `context` sub-field is non-optional in Luhmann practice.

### R8 — context/ directory structure: one dir per primitive kind
The current scheme (`context/workitems/`, `context/discussions/`,
`context/notes/`, etc.) is correct. Each top-level directory maps
1:1 to a primitive `kind:`, making it machine-readable without
convention lookup. The indexer eliminates the need for
subtype-based subdirectories within a kind. This is the "class /
object" pattern: top level = kind, files within = instances.

### R9 — Discussion is a legitimate separate primitive
Discussion models structured deliberation (question → exploration →
DecisionRecord). It is not a WorkItem (not a unit of work), not a
Note (multi-party, structured, produces outcomes), not an Artifact
(no deliverable). The epistemic arc is: Note → Discussion →
DecisionRecord → WorkItem.

### R10 — context/owner/, context/actors/, context/roles/ need
documenting
These directories are defined in schemas but absent from the
AGENTS.md layout table. They should be added.

### R11 — MCP config paths are stale after skills reorganization
The `.mcp.json` at project root still references
`context/skills/<name>/mcp/server.py` (pre-reorganization paths).
After the `e86ad06` reorganization commit, the correct paths are
`context/skills/processkit/<name>/mcp/server.py` (and category
subdirs for non-processkit skills). The config must be regenerated.
