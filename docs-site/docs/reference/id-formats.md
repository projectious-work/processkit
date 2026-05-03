---
sidebar_position: 2
title: "ID Formats"
---

# ID Formats

Entity IDs in processkit have the shape `<PREFIX>-<id-body>`. The prefix
is determined by the primitive kind and is not configurable. The id-body
has two independent configuration axes: **format** and **slug**.

## Configuration

In the consuming project's `aibox.toml`:

```toml
[context]
id_format = "word"   # word | uuid
id_slug = false      # true | false
```

## The four combinations

| `id_format` | `id_slug` | Example                     | Notes                                        |
|-------------|-----------|-----------------------------|----------------------------------------------|
| `word`      | `false`   | `BACK-calm-fox`             | Default. Short, memorable, solo-friendly    |
| `word`      | `true`    | `BACK-calm-fox-add-lint`    | Memorable + descriptive for prose contexts  |
| `uuid`      | `false`   | `BACK-550e8400-e29b-41d4`   | Uniqueness guarantees for large teams       |
| `uuid`      | `true`    | `BACK-550e8400-add-lint`    | UUID + readable context                     |

## Prefix registry

| Primitive       | Prefix   |
|-----------------|----------|
| WorkItem        | `BACK`   |
| LogEntry        | `LOG`    |
| DecisionRecord  | `DEC`    |
| Migration       | `MIG`    |
| Artifact        | `ART`    |
| Note            | `NOTE`   |
| Actor           | `ACTOR`  |
| Role            | `ROLE`   |
| Binding         | `BIND`   |
| Scope           | `SCOPE`  |
| Category        | `CAT`    |
| CrossReference  | —        |
| Gate            | `GATE`   |
| Schedule        | `SCHED` (legacy v1) |
| Constraint      | `CONST`  |
| Context         | `CTX`    |
| Discussion      | `DISC`   |
| Process         | `PROC` (legacy v1) |
| StateMachine    | `SM` (legacy v1) |

`Metric`, `Model`, `Process`, `Schedule`, and `StateMachine` do not
reserve first-class primitive prefixes in the v2 contract. The legacy
prefixes remain documented so existing v1 contexts can be migrated and
read correctly.

## Word generation

Word-based IDs come from the [`petname`](https://crates.io/crates/petname)
algorithm: one adjective + one noun (or two, depending on
`id_format_depth` — default 2). Collisions are detected at generation
time and a third component is appended if needed.

## Slugs

When `id_slug = true`, a content-derived slug is appended to the ID body.
For a WorkItem with title "Add release audit check", the slug would be
`add-release-audit-check` (first N tokens, kebab-case, truncated).

Slugs are for human readability and do not affect uniqueness — the word
or UUID portion still guarantees that.

## Choosing a format

- **Solo developer:** `word` + `slug: false` — shortest, most memorable
- **Small team with process:** `word` + `slug: true` — readable in prose
- **Large team or automation-heavy:** `uuid` + `slug: true` — uniqueness + readability
- **Automation-only:** `uuid` + `slug: false` — machines don't care about readability
