---
name: note-management
description: |
  Captures, reviews, and promotes Note entities — the lightweight knowledge capture primitive in processkit. Notes are quick-capture units (thoughts, insights, questions, references) that are reviewed periodically and promoted to WorkItems, DecisionRecords, or other primitives when they ripen. Use when the user says "remember this", "note that", "I had an idea", or when running a periodic note review session.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-note-management
    version: "1.0.0"
    created: 2026-04-08T00:00:00Z
    category: process
    layer: 2
    commands:
      - name: note-management-capture
        args: "title"
        description: "Capture a new fleeting note with the given title"
      - name: note-management-review
        args: ""
        description: "Review all fleeting notes and decide what to promote or discard"
      - name: note-management-promote
        args: "note-id"
        description: "Promote a fleeting note to a more permanent artifact"
---

# Note Management

## Intro

Notes are processkit's capture layer — the place where ideas land
before they are ready to become backlog items, decisions, or
artifacts. Inspired by the Zettelkasten model: capture fast (fleeting),
refine deliberately (permanent), link explicitly, and promote when
something becomes actionable. The review cycle is what gives notes
their value — unreviewed notes are just noise.

## Overview

### Note types

| Type | When to use | Review horizon |
|---|---|---|
| **fleeting** | Quick thought, idea, or observation — not yet refined | Within 1 week |
| **insight** | A conclusion or realization from experience or reflection | Within 1 month |
| **reference** | Pointer to an external source, with your own summary | Evergreen |
| **question** | An open question you want to revisit | Until answered |

Start with `fleeting` when in doubt. If a note survives a review
session unchanged and seems worth keeping, promote to `insight` or
`reference`.

### Note file location and format

Notes live in `context/notes/` as individual Markdown files with YAML
frontmatter:

```
context/notes/
  NOTE-001-better-error-messages.md
  NOTE-002-rag-chunking-question.md
  ...
  INDEX.md         ← summary of all active notes
```

File naming: `NOTE-{id}-{kebab-title}.md` where `{id}` is the
sequential NOTE ID from the index.

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Note
metadata:
  id: NOTE-003
  created: 2026-04-08
spec:
  title: "Error messages should cite the field that caused the error, not just the error code"
  type: insight
  state: captured
  tags: [ux, error-handling, api-design]
  review_due: 2026-04-15
---

When a validation error returns `code: 400`, the user has no way to
know which field failed. Every error response should include `field`,
`message`, and a `docs_url` for context. I've seen this pattern
in Stripe's and GitHub's APIs — it's the right model.
```

### Capturing a note

When the user says something note-worthy ("remember this", "I had
an idea", "note that"):

1. **Assign the next NOTE ID** from `context/notes/INDEX.md`
2. **Pick the type**: fleeting (quick thought) or one of the specific
   types if already clear
3. **Write the title as a self-contained claim or question** — not
   a topic label. "Error messages should include the field name" is
   a note title; "Error messages" is a topic, not a note.
4. **Set `review_due`**: today + 7 days for fleeting, today + 30 days
   for insight/question, none for reference
5. **Update INDEX.md** with the new entry

```markdown
# Notes Index

Next ID: NOTE-004

## Active

| ID | Title | Type | State | Review Due |
|---|---|---|---|---|
| NOTE-003 | Error messages should cite the field that caused the error | insight | captured | 2026-04-15 |
| NOTE-002 | How does RAG chunking affect retrieval precision? | question | captured | 2026-04-14 |

## Promoted

| ID | Title | Promoted To |
|---|---|---|
| NOTE-001 | Add dark mode toggle | BACK-042 |

## Archived

(empty)
```

### Running a review session

A periodic review session works through all notes whose
`review_due` has passed or is within 2 days:

For each overdue note, make one of four decisions:

**Promote** — the idea is ready to become a real primitive:
1. Create the downstream entity (WorkItem, DecisionRecord, etc.)
2. Add `promotes_to: { kind: WorkItem, id: BACK-042 }` to the note frontmatter
3. Transition the note to `promoted`
4. Update INDEX.md

**Keep as permanent** — the note is worth keeping but not yet actionable:
1. Refine the body if the capture was rough
2. Set type to `insight` or `reference`
3. Transition state to `permanent`
4. Set a new `review_due` (30-90 days out)
5. Add links to related notes or entities

**Archive** — the note is no longer useful:
1. Transition state to `archived`
2. Move to the Archived section of INDEX.md

**Defer** — not ready to decide yet:
1. Keep state at `captured`
2. Extend `review_due` by 7 days
3. Add a one-line note on why it was deferred

### Linking notes

Notes should not stand alone — the value of a knowledge base comes
from connections. Link explicitly:

- Reference the note in the primitive it informed:
  `<!-- originated from NOTE-003 -->`
- Add related notes in the note body:
  `Related: NOTE-007 (similar concern about validation in the CLI)`
- When promoting, add a backlink in the created WorkItem's description

### Promotion patterns

| Note type | Common promotion target | Trigger |
|---|---|---|
| question | WorkItem (spike), Discussion | The question needs research or a team answer |
| insight | DecisionRecord | The insight captures a choice that was made |
| fleeting | WorkItem (task/chore) | The quick idea turns out to be actionable |
| reference | Artifact | The source becomes a formal reference material |

This skill also provides the `/note-management-capture` slash command for direct invocation — see `commands/note-management-capture.md`. This skill also provides the `/note-management-review` slash command for direct invocation — see `commands/note-management-review.md`. This skill also provides the `/note-management-promote` slash command for direct invocation — see `commands/note-management-promote.md`.

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Capturing topic labels instead of claims or questions.** "Error messages" is not a note — it's a tag. A note's title must be a self-contained claim ("Error messages should include the field name, not just the error code") or a specific question ("Does the auth middleware re-validate tokens on every request?"). Vague labels create a pile of notes with no re-discoverable content.
- **Reviewing notes without making a decision.** Reading through notes and doing nothing is not a review — it resets the review clock without advancing the note. Every note in a review session must exit with one of four decisions: promote, keep as permanent, archive, or defer with a reason and new date.
- **Never archiving notes.** A notes index that only grows and never shrinks stops being useful. Not every idea deserves to become permanent — many are superseded, wrong in retrospect, or simply no longer interesting. Archive aggressively; promoted and permanent notes are the signal.
- **Promoting a fleeting note without refining it first.** A rough, first-draft thought promoted directly to a DecisionRecord or WorkItem brings the roughness with it. Before promoting, read the note and refine: does the title accurately capture the claim? Is the body complete enough for a newcomer to understand without the original context?
- **Writing notes that require the original context to make sense.** "The thing we discussed about the API" is meaningless six weeks later. A note must be self-contained: include enough context that the note makes sense to the author (or an agent) who has no memory of the conversation or session where the idea was captured.
- **Not updating INDEX.md after a review session.** The index is the primary way to discover notes and track the review cadence. If notes are transitioned to `promoted` or `archived` without updating the index, the index becomes a stale liability rather than a useful tool.
- **Using notes as a dumping ground for everything instead of a capture layer for non-backlog ideas.** Notes are for ideas not yet ready to be backlog items. Things that are clearly tasks should go directly into a WorkItem. Things that are clearly decisions should go into a DecisionRecord. Notes are the intermediate capture for things that haven't crystallized yet — not a general-purpose inbox for all project work.

## Full reference

### Note ID assignment

IDs are sequential and permanent: `NOTE-001`, `NOTE-002`, etc. The
`Next ID` counter in INDEX.md determines the next number. IDs are
never reused, even when notes are archived.

### State transitions

```
captured → reviewing → permanent
                     → promoted  (terminal)
                     → archived  (terminal)
captured → archived
permanent → reviewing
permanent → promoted
permanent → archived
```

### Review cadence

Suggested cadence for a solo developer:

| Frequency | Action |
|---|---|
| Daily | Capture freely — do not review |
| Weekly | Review all fleeting notes past their review_due |
| Monthly | Review all permanent notes; check if any should be promoted |
| Quarterly | Archive anything in permanent that hasn't been revisited in >90 days |

For teams, assign a note review owner per sprint or rotate the
responsibility on a weekly basis.

### Note template

```markdown
---
apiVersion: processkit.projectious.work/v1
kind: Note
metadata:
  id: NOTE-{{id}}
  created: {{date}}
spec:
  title: "{{self-contained claim or question}}"
  type: {{fleeting|insight|reference|question}}
  state: captured
  tags: []
  review_due: {{date + 7 days for fleeting, + 30 for others}}
---

{{Note body — enough context to understand without memory of the session}}
```

### Relationship to other primitives

| Primitive | How notes relate |
|---|---|
| **WorkItem** | Notes often promote to WorkItems when an idea becomes a task |
| **DecisionRecord** | Insight notes about choices promote to DecisionRecords |
| **BACKLOG.md** | High-priority, well-understood items go here directly — not in notes |
| **STANDUPS.md** | Standups reference the work done; notes capture the ideas generated |
