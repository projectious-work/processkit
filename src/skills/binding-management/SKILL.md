---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-binding-management
  name: binding-management
  version: "1.0.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Manage Binding entities — scoped, temporal, many-to-many relationships between any two primitives."
  category: process
  layer: 2
  uses: [event-log, actor-profile, index-management, id-management]
  provides:
    primitives: [Binding]
    mcp_tools: [create_binding, query_bindings, end_binding, resolve_bindings_for]
    templates: [binding]
  when_to_use: "Use when a relationship between two entities needs scope, time, or its own attributes — e.g. 'Alice is the tech lead for project X from Jan to June' or 'the security gate applies to the release process only on the main branch'."
---

# Binding Management

## Level 1 — Intro

A Binding is an entity that connects two other entities with optional scope,
temporality, and conditions. It is the junction-table pattern promoted to
a primitive, and it is the right choice whenever a relationship is more than
a simple "A references B" — for example "Alice is the tech lead on project X
for 2026," or "the security gate applies to the release process only on the
main branch."

## Level 2 — Overview

### When to use a Binding vs a cross-reference

**Rule:** if a relationship has **scope**, **time**, or **its own attributes**
→ Binding. If it is just "A relates to B" → cross-reference in frontmatter.

| Situation                                                 | Binding or cross-ref? |
|-----------------------------------------------------------|-----------------------|
| "BACK-foo blocks BACK-bar"                                | cross-ref             |
| "DEC-x is related to BACK-y"                              | cross-ref             |
| "Alice is a developer" (globally, permanently)            | cross-ref (in Actor)  |
| "Alice is tech lead on project X for 2026"                | **Binding**           |
| "The security gate applies to the release process"       | cross-ref (in Process)|
| "The security gate applies to release process *only on main branch*" | **Binding** |
| "Sprint 42 runs from Apr 1 to Apr 14 and scopes these items" | **Binding**        |

If in doubt, prefer the cross-reference. Promote to a Binding only when you
actually need the extra dimensions.

### Binding types

`spec.type` is freeform; conventions emerge per project. Common ones:

| type                  | subject kind | target kind |
|-----------------------|--------------|-------------|
| `role-assignment`     | Actor        | Role        |
| `work-assignment`     | WorkItem     | Actor       |
| `process-gate`        | Process      | Gate        |
| `process-scope`       | Process      | Scope       |
| `schedule-scope`      | Schedule     | Scope       |
| `constraint-scope`    | Constraint   | Scope       |
| `category-assignment` | any          | Category    |

### Shape

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Binding
metadata:
  id: BIND-bright-falcon
  created: 2026-04-06T00:00:00Z
spec:
  type: role-assignment
  subject: ACTOR-alice
  target: ROLE-tech-lead
  scope: SCOPE-project-x
  valid_from: 2026-01-01
  valid_until: 2026-12-31
  conditions:
    approval_required: false
  description: "Alice fills the tech-lead role on project X for 2026."
---

Optional body: context for why this binding exists, related discussion, etc.
```

### Workflow

1. Pick the `type` — match an existing convention if possible.
2. Set `subject` (the entity "receiving" the relationship) and `target`
   (the entity "being bound to").
3. Set `scope` if the binding only applies within a particular scope.
4. Set `valid_from` / `valid_until` if the binding is time-bounded.
5. Add `conditions` for arbitrary constraints.
6. Save to `context/bindings/`.
7. Log `binding.created`.

### Ending a binding

To end a binding:

- **Preferred:** set `valid_until` to the current date, log `binding.ended`.
- **Alternative:** delete the Binding file (only if it was created in error).

Do NOT edit `subject` or `target` of an existing binding — write a new one
and end the old one. The history is what makes Bindings useful.

### Resolving "who currently fills role X in scope Y?"

1. Find Bindings where `type: role-assignment` and `target: ROLE-x` and
   (`scope: SCOPE-y` or `scope: null`).
2. Filter to those active at the current time (`valid_from ≤ now ≤ valid_until`
   or either unset).
3. Return the `subject` IDs.

The Phase 3 MCP server provides `resolve_bindings_for(entity_id, type?, at_time?)`.

## Level 3 — Full reference

### Fields

| Field         | Type           | Notes                                                            |
|---------------|----------------|------------------------------------------------------------------|
| `type`        | string         | Freeform — the binding type. Conventions per project.            |
| `subject`     | string         | ID of the entity on the "from" side of the relationship.         |
| `target`      | string         | ID of the entity on the "to" side of the relationship.           |
| `scope`       | string         | Optional. Scope ID within which this binding applies.            |
| `valid_from`  | date/datetime  | Optional. When the binding starts being in effect.               |
| `valid_until` | date/datetime  | Optional. When the binding stops being in effect.                |
| `conditions`  | map            | Optional. Freeform constraints.                                  |
| `description` | string         | One-line human-readable summary.                                 |

### Why Binding is generalized from RoleBinding

DISC-001 introduced RoleBinding as the 18th primitive. DISC-002 §11 investigated
whether this should be generalized. The pattern of "put a third thing between
two things so either can change independently" is fundamental in software
design (GoF patterns, DI, junction tables) and appears in at least 7 relationship
types in processkit. Generalizing keeps the primitive count at 18 while covering
more cases. See DEC-023.

### No enforcement

Bindings are descriptive. processkit does not prevent actions based on
bindings — e.g., a WorkItem doesn't refuse to transition if the actor isn't
bound to the required role. Enforcement is a governance concern
(DEC-017).

### Indexing

In Phase 3, the index MCP server maintains a `bindings` table:

```
bindings(id, type, subject, subject_kind, target, target_kind,
         scope, valid_from, valid_until, active)
```

with `active` computed from `valid_from`/`valid_until` vs current time.
This makes "who currently holds role X" a single SQL query.

### Idempotency for "current state" bindings

When the same effective state is re-asserted (e.g. "Alice is still tech
lead"), prefer extending `valid_until` on the existing Binding rather than
creating a new one. This keeps history clean. If the underlying situation
*changed* and just happened to end up in the same place, that's a new
Binding.
