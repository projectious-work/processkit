---
sidebar_position: 14
title: "Note"
---

# Note

A Zettelkasten capture layer for ideas, observations, and references.
Notes exist on a spectrum from raw capture (fleeting) to permanent
knowledge (insight).

| | |
|---|---|
| **ID prefix** | `NOTE` |
| **State machine** | `note` |
| **MCP server** | none (file-based) |
| **Skill** | `note-management` (Layer 4) |

## State machine

```
fleeting → insight
         ↘ promoted   (promoted to another entity kind)
         ↘ archived
```

`insight`, `promoted`, and `archived` are terminal.

## Note types (Luhmann/Ahrens taxonomy)

| Type | Description |
|---|---|
| `fleeting` | Quick capture, not yet refined — review within a week |
| `insight` | Permanent note — self-contained conclusion, part of knowledge base |
| `reference` | Literature note — pointer to an external source with summary |
| `question` | Open question — may promote to WorkItem (spike) or Discussion |

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `title` | string (1–120) | Self-contained claim or question — not a topic label |
| `body` | string | The note content |
| `type` | enum | `fleeting` · `insight` · `reference` · `question` |
| `state` | string | Current state |

### Optional

| Field | Type | Description |
|---|---|---|
| `tags` | string[] | Freeform tags for discoverability |
| `source` | string | For `reference` notes: URL, book title, or conversation |
| `promotes_to` | object | `{kind, id}` — target entity when promoted |
| `review_due` | date | When the note should be reviewed |
| `links` | object[] | Typed edges to other Notes (see below) |

## Links — typed Zettelkasten edges

Each entry in `links` has:

| Field | Type | Description |
|---|---|---|
| `target` | `NOTE-*` | The linked note |
| `relation` | enum | See table below |
| `context` | string (≥10 chars) | One sentence explaining *why* the connection matters |

| Relation | Meaning |
|---|---|
| `elaborates` | This note expands on the target |
| `contradicts` | This note disagrees with the target |
| `supports` | This note provides evidence for the target |
| `is-example-of` | This note is a concrete case of the target's claim |
| `see-also` | Related but not directly argumentative |
| `refines` | This note sharpens or corrects the target |
| `sourced-from` | This note draws its content from the target |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Note
metadata:
  id: NOTE-20260411_0905-ClearDawn-fts5-trigram
  created: '2026-04-11T09:05:00Z'
spec:
  title: FTS5 trigram tokeniser matches substrings without pre-tokenisation
  body: |
    SQLite's FTS5 with the trigram tokeniser splits text into overlapping
    3-character sequences. This lets you search for partial words
    (e.g. "Crow" matches "StoutCrow") without needing a dedicated
    tokenisation pass. Ideal for entity ID word-pair search.
  type: insight
  state: insight
  tags: [sqlite, fts5, search]
  links:
    - target: NOTE-20260411_0906-BrightWave-search-ux
      relation: supports
      context: >
        Trigram matching is what makes the search UX feel instant —
        users type partial word-pairs and get matches immediately.
---
```

## Notes

- **Title discipline matters**: a good Note title is a self-contained
  claim or question — `"FTS5 trigram tokeniser matches substrings"` not
  `"FTS5 notes"`. The title alone should convey the idea.
- Tags group notes by topic; links build arguments. Use both.
- A `question` note that remains unanswered after a week should become
  a Discussion or WorkItem spike.
