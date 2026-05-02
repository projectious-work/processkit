---
sidebar_position: 1
title: "apiVersion Policy"
---

# apiVersion Policy

processkit uses a Kubernetes-style `apiVersion` field on every entity:

```yaml
apiVersion: processkit.projectious.work/v1
```

## The group

The group `processkit.projectious.work` is a reverse-DNS name anchored on
the owning organization (`projectious.work`) with `processkit` as a
subcomponent. This prevents name collisions if other organizations fork
or publish compatible primitives under their own domains.

The form `<reverse-dns-group>/<version>` is the Kubernetes-idiomatic
shape — exactly one slash. Tools that split on `/` expect exactly two
parts.

## Evolution rules

| apiVersion                              | Status            | Meaning                                              |
|-----------------------------------------|-------------------|------------------------------------------------------|
| `processkit.projectious.work/v1`        | current (v0.1.0+) | Initial stable version                               |
| `processkit.projectious.work/v1beta1`   | not used          | Reserved                                             |
| `processkit.projectious.work/v2`        | planned           | Breaking contract with explicit migration required   |

### Non-breaking changes (stay at v1)

- Adding new optional fields to schemas
- Adding new primitive kinds
- Adding new states to a state machine
- Adding new skills
- Adding new packages

### Breaking changes (require v2)

- Removing or renaming existing fields
- Changing the type or meaning of existing fields
- Removing states from a state machine (stranding existing entities)
- Removing primitive kinds
- Changing the semantics of `metadata.id`, `metadata.created`, or other cross-cutting fields

## Migration between versions

The SmoothTiger/SmoothRiver v2 direction is a **no-shim** contract:
v2 schemas and index semantics become authoritative, and processkit does
not add hidden dual-read or permissive validation paths for v1 data.
Existing v1 contexts remain a migration source, not a long-term
compatibility target.

For a v1 context moving to v2:

1. `aibox sync` generates a diff between the old upstream reference
   templates (stored verbatim in
   `context/templates/processkit/<old-version>/`) and the new ones.
2. A `Migration` entity records the affected files, source and target
   `apiVersion`, source and target processkit versions, and the proposed
   plan.
3. The agent runs the migration through `migration-management`, using
   dry-run diagnostics before applying changes.
4. The user approves the project-specific plan before the migration
   reaches `applied`.
5. After migration, v2 validation rejects unknown kinds, stale primitive
   assumptions, and ad hoc event/type vocabulary that v1 tolerated.

No automatic in-place patching — migrations always go through the agent.

Provenance: the v2 direction follows
`DEC-20260430_1416-SmoothTiger-adopt-breaking-v2-implementation-plan-for`
and the SmoothRiver work plan at
https://github.com/projectious-work/internal/blob/main/context/artifacts/ART-20260430_1242-SmoothRiver-processkit-project-work-plan.md.
