---
sidebar_position: 19
title: "Discussion"
---

# Discussion

A structured, multi-turn conversation exploring an open question.
Discussions capture the back-and-forth of deliberation and produce
(or fail to produce) DecisionRecords as outcomes.

| | |
|---|---|
| **ID prefix** | `DISC` |
| **State machine** | `discussion` |
| **MCP server** | `discussion-management` |
| **Skill** | `discussion-management` (Layer 4) |

## State machine

```
active → resolved
       ↘ closed (no outcome)
```

`resolved` and `closed` are terminal.

## Fields

### Required

| Field | Type | Description |
|---|---|---|
| `question` | string | The driving question — one crisp sentence |
| `state` | string | Current state |

### Optional

| Field | Type | Description |
|---|---|---|
| `participants` | `ACTOR-*[]` | Actors participating |
| `related` | `DISC-*[]` | Related discussion IDs |
| `outcomes` | `DEC-*[]` | DecisionRecord IDs produced by this discussion |
| `opened_at` | datetime | When the discussion started |
| `closed_at` | datetime | When it was marked resolved or closed |

## Example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Discussion
metadata:
  id: DISC-20260411_0910-ClearWave-primitive-page-format
  created: '2026-04-11T09:10:00Z'
spec:
  question: What format should per-primitive reference pages follow?
  state: resolved
  participants: [ACTOR-claude, ACTOR-20260411_0906-owner]
  outcomes: [DEC-20260411_0911-SwiftMeadow-primitive-page-format]
  opened_at: '2026-04-11T09:10:00Z'
  closed_at: '2026-04-11T09:30:00Z'
---
```

## Notes

- Use `add_outcome` to attach a DecisionRecord after it has been created
  with `record_decision`. Both tools auto-log.
- Discussions are the audit trail behind decisions — if a decision was
  reached after deliberation, the Discussion captures the reasoning path.
- Transition to `resolved` when a Decision was reached; to `closed` when
  the question was abandoned or became moot.
- The Markdown body (below the YAML frontmatter) is the space for the
  discussion thread — arguments, evidence, proposals, objections.
