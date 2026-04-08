---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-documentation
  name: documentation
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Writing effective project documentation — READMEs, API doc comments, and inline comments that explain why."
  category: process
  layer: 3
  when_to_use: "Use when writing or improving documentation — READMEs, doc comments, inline comments, or when code lacks explanation for non-obvious behavior."
---

# Documentation

## Level 1 — Intro

Good documentation answers the questions a reader actually has:
what is this, how do I use it, why does it work this way. Identify
the audience first, then write the smallest doc that serves them.
Doc comments live with the code; READMEs live with the project.

## Level 2 — Overview

### Identify the audience

Decide before writing whether the reader is a developer integrating
the API, an end-user running the tool, or a future maintainer
reading the source. Each gets a different doc.

### README structure

For a project README:

1. **What it is** — one sentence
2. **Quick start** — install command and the first useful command
3. **Usage examples** — the 2-3 most common cases
4. **Configuration reference** — flags, env vars, config files
5. **Contributing guide** — only if open source

### API documentation

Every public function gets a doc comment. Include:

- What it does (one sentence)
- Parameters
- Return value
- Errors or panics
- A short usage example for non-obvious APIs

### Inline comments

Use inline comments sparingly:

- Comment **why**, not **what** — the code shows the what.
- Document non-obvious business rules.
- Explain workarounds with links to issues or specs.
- Never comment out code — delete it. Git remembers.

### Locality

Keep docs close to code. Doc comments beat wiki pages beat
external sites. The further docs travel from the code, the faster
they go stale.

## Level 3 — Full reference

### Example doc comment

```rust
/// Calculates the shipping cost based on weight and destination zone.
///
/// Returns `None` if the destination zone is not serviceable.
/// Weights over 30kg use freight pricing instead.
```

The example is short, names the inputs and outputs, and surfaces
the two non-obvious rules (unservicable zones return `None`,
heavy items switch to freight).

### Anti-patterns

- **Restating the code** — `// increments i` next to `i += 1`.
- **Stale comments** — comments that contradict the code are
  worse than no comments. Delete or update them on every change.
- **Tutorial-as-README** — a README is a map, not a textbook.
  Link to the tutorial; don't inline it.
- **Undocumented public API** — every exported symbol is a
  promise. If it's worth exporting, it's worth a doc comment.
- **TODO comments without owners or dates** — they rot. Either
  fix it or file a ticket and link the ticket id.

### When to write less

A function with a self-evident name and a short body usually
needs no doc comment. Save the words for the parts where the
reader might be surprised.
