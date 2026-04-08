---
name: decisions-adr
description: |
  Records architectural and process decisions in context/DECISIONS.md with rationale and alternatives, in inverse-chronological ADR format. Use when the user makes a significant technical or process decision that should be captured for future readers.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-decisions-adr
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 2
---

# Decision Tracking (ADR format)

## Intro

Decisions are recorded in `context/DECISIONS.md`, one entry per
choice, numbered `DEC-NNN` in inverse chronological order. Each
entry captures what was decided, why, and what else was on the
table.

## Overview

### Where decisions live

All entries go in `context/DECISIONS.md`. New decisions are added
at the top (just below the file header). Older decisions are
pushed down. The file's "Next ID" counter (if present) determines
the next number.

### Entry format

Each entry contains:

- **Decision** — what was chosen, in one sentence
- **Rationale** — why this option was picked
- **Alternatives** — what else was considered

Add the date in parentheses after the title:

```
## DEC-042: Use Postgres over MySQL (2026-04-07)

**Decision:** Standardize on Postgres for all new services.

**Rationale:** Better JSON support, stronger constraint system,
existing team familiarity.

**Alternatives:** MySQL (less expressive types), SQLite (won't
scale to multi-instance deploys).
```

## Gotchas

Agent-specific failure modes — provider-neutral pause-and-self-check items:

- **Recording only the decision, not the alternatives considered.** A decision that says "we chose Postgres" without recording that MySQL and SQLite were also evaluated gives future maintainers no context for why the choice was made. The "Alternatives" field is not optional — it documents what was consciously rejected and prevents re-litigating the same options.
- **Recording only the positives of the chosen option.** A decision record that describes only why the chosen option is good is advocacy, not documentation. Future readers need to understand what was knowingly accepted. List the trade-offs and costs of the chosen option alongside its benefits.
- **Editing an accepted decision in place when circumstances change.** An accepted decision is a permanent historical record. Changing it in place erases the original rationale and leaves future readers uncertain whether the current content reflects the original decision or a revision. When a decision is revisited, write a new entry that references and supersedes the old one.
- **Recording implementation details as decisions.** Decisions are for choices that a future maintainer might reasonably ask "why did we do it this way?" — not for routine implementation choices, refactors, or bug fixes. "We added error handling to the payment module" is not a decision. "We chose to use retry-on-idempotent-methods only, not retry-all, for payment requests" is a decision.
- **Using a decision record for a rejected approach that was never seriously considered.** A decision record should reflect an actual deliberation, not a post-hoc rationalization. Recording "we considered a microservices approach but chose a monolith" when microservices were never seriously evaluated creates a misleading impression of the decision process.
- **Leaving decisions unreferenced — captured but never linked.** A decision that isn't referenced from the code comment, PR description, or context file that it explains is at risk of being forgotten. After writing a decision record, add a reference to it from the place in the code or documentation where the decision manifests.
- **Reusing or skipping decision IDs.** IDs are sequential and permanent. Reusing a deleted ID creates confusion about which entry is the real one. Skipping IDs (e.g., jumping from DEC-041 to DEC-043) creates gaps that are hard to explain. Assign the next sequential ID from the "Next ID" counter every time, with no exceptions.

## Full reference

### Numbering rules

- IDs are sequential and never reused.
- Inverse chronological in the file means newest at the top —
  but ID `DEC-042` is always `DEC-042`, regardless of where it
  sits relative to neighbors after later edits.
- If a decision is superseded, do not delete it. Add a new entry
  that references the superseded ID, and add a "Superseded by
  DEC-NNN" note to the original.

### What counts as a decision

Anything a future maintainer might reasonably ask "why did we do
it this way?" about. Examples:

- Choosing one library or framework over another
- Deciding on a coding convention that isn't enforced by tooling
- Setting a process rule (e.g. "all PRs require two reviewers")
- Rejecting a proposed approach (record the rejection so it
  doesn't get re-proposed)

What does *not* count: routine implementation choices, refactors,
bug fixes. These belong in commit messages, not decision records.

### Cross-referencing

Link decisions from code comments, PR descriptions, or other
context files when they explain the reasoning behind a choice.
A decision that isn't referenced from anywhere is at risk of
being forgotten.
