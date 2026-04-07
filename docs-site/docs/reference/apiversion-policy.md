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
| `processkit.projectious.work/v2`        | future            | Bumped when a breaking change requires migration    |

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

When v2 is introduced:

1. processkit ships both v1 and v2 schemas for a transition period.
2. `aibox sync` generates a diff between the old upstream reference
   templates (stored verbatim in
   `context/templates/processkit/<old-version>/`) and the new ones.
3. The diff is presented to the agent as a migration prompt.
4. The agent applies the changes with human approval.
5. After a deprecation window, v1 schemas are removed.

No automatic in-place patching — migrations always go through the agent.
