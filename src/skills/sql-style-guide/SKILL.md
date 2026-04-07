---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-sql-style-guide
  name: sql-style-guide
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "SQL style — snake_case, singular tables, named constraints, one-clause-per-line formatting."
  category: language
  layer: null
  when_to_use: "Use when writing or reviewing SQL, designing schemas, or naming tables, columns, constraints, and migrations."
---

# SQL Style Guide

## Level 1 — Intro

Use `snake_case` everywhere, keep table names singular, name every
constraint explicitly, and format queries with one clause per line
and leading commas. Consistency is the point — the exact choices
matter less than picking them and holding the line.

## Level 2 — Overview

### Table and column naming

- `snake_case` for all identifiers: `user_account`, `created_at`.
- Tables are singular: `user`, `order`, `product` — not `users`.
- Join tables combine both names: `user_role`, `order_product`.
- Boolean columns use `is_` or `has_`: `is_active`,
  `has_subscription`.
- Timestamp columns use `_at`: `created_at`, `updated_at`,
  `deleted_at`.
- Primary keys are `id`; foreign keys are `<referenced_table>_id`.
- Avoid reserved words as identifiers; rename instead of quoting.

### Keyword capitalization

- SQL keywords in UPPERCASE: `SELECT`, `FROM`, `WHERE`, `JOIN`.
- Function names in UPPERCASE: `COUNT()`, `COALESCE()`, `NOW()`.
- Identifiers in lowercase.

Pick one style per project and enforce it with a linter.

### Query formatting

One clause per line. Leading commas in select lists make diffs
trivial:

```sql
SELECT
    u.id
  , u.name
  , u.email
  , u.created_at
FROM user u
JOIN order o ON o.user_id = u.id
WHERE u.is_active = true
ORDER BY u.created_at DESC
```

Use explicit `JOIN` syntax — never comma joins in `FROM`. Align
`ON` with its `JOIN`. Use short, meaningful table aliases
(`u` for user, `o` for order).

### Constraint naming

| Kind       | Pattern                        | Example                  |
|------------|--------------------------------|--------------------------|
| Primary key| `pk_<table>`                   | `pk_user`                |
| Foreign key| `fk_<table>_<referenced>`      | `fk_order_user`          |
| Unique     | `uq_<table>_<columns>`         | `uq_user_email`          |
| Check      | `ck_<table>_<description>`     | `ck_order_positive_total`|
| Index      | `ix_<table>_<columns>`         | `ix_user_created_at`     |

Always name constraints explicitly — never rely on auto-generated
names. Auto names make it impossible to reference a constraint in
a later migration without hunting for it.

### Migration files

- Sequential timestamped names:
  `20260322_001_create_user_table.sql`.
- One structural change per migration; never mix schema and data
  changes.
- Always write both `up` and `down` migrations.
- The file name describes the action: `add_email_to_user`,
  `create_order_table`, `drop_legacy_column`.

### Query best practices

- Avoid `SELECT *` — list columns explicitly so adding a column
  doesn't silently change query output.
- Use CTEs (`WITH`) to decompose complex queries into readable
  steps instead of nested subqueries.
- Prefer `WHERE EXISTS (SELECT 1 FROM ...)` over
  `WHERE col IN (SELECT ...)` for correlated subqueries — the
  planner usually produces a better plan.
- Use `COALESCE` for default values rather than handling nulls in
  the application layer.
- Always specify `ORDER BY` when results must be deterministic —
  SQL gives no ordering guarantee otherwise.

## Level 3 — Full reference

### Comment conventions

Use `--` for single-line comments and explain *why*, not *what*:

```sql
-- Exclude soft-deleted rows even though the partial index
-- already filters them; a future index change might not.
SELECT id FROM user WHERE deleted_at IS NULL;
```

Comment non-obvious filter values:

```sql
WHERE status = 3  -- 3 = 'completed'
```

Add a header comment to any complex query explaining the business
question it answers.

### Anti-patterns

- Plural table names (`users`) — fine if the team has already
  standardized on it, but the join-table convention falls apart:
  `users_roles` vs `user_role`.
- Unnamed constraints — database engines invent long, unstable
  names that are impossible to reference in migrations.
- `SELECT *` in production code.
- Quoting reserved words as identifiers instead of renaming.
- Comma joins in the `FROM` clause.
- Concatenating SQL with string formatting — always use
  parameterized queries.
- Mixing schema changes and data backfills in one migration —
  they have different failure modes and rollback strategies.
- Trailing commas in select lists (breaks when the last column is
  commented out) — leading commas avoid this.

### Example schema slice

```sql
CREATE TABLE "user" (
    id         BIGSERIAL PRIMARY KEY,
    email      TEXT NOT NULL,
    is_active  BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT pk_user PRIMARY KEY (id),
    CONSTRAINT uq_user_email UNIQUE (email)
);

CREATE INDEX ix_user_created_at ON "user" (created_at);
```

### Review checklist

- [ ] Tables singular, columns `snake_case`, booleans `is_`,
      timestamps `_at`
- [ ] All constraints explicitly named
- [ ] One structural change per migration, with down migration
- [ ] No `SELECT *`
- [ ] Explicit `JOIN ... ON`, no comma joins
- [ ] `ORDER BY` present when determinism is required
- [ ] Complex queries decomposed with CTEs
- [ ] Header comment on queries with non-obvious business intent
