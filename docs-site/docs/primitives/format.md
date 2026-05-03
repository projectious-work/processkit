---
sidebar_position: 2
title: "Entity File Format"
---

# Entity File Format

Every processkit primitive entity is stored as a Markdown file with a
YAML frontmatter block. The format is inspired by Kubernetes objects —
stable, versioned, and easy to parse.

## Canonical shape

```yaml
---
apiVersion: processkit.projectious.work/v1   # required — schema version
kind: WorkItem                                # required — primitive type
metadata:                                     # required
  id: BACK-calm-fox
  created: 2026-04-06T10:30:00Z
  updated: 2026-04-06T11:15:00Z
  labels:
    priority: high
spec:                                         # required — entity-specific
  title: "Add a release audit check"
  state: in-progress
  assignee: ACTOR-alice
---

# Body — freeform Markdown

Human-readable description, acceptance criteria, notes, history.
```

## The four top-level keys

| Key          | Required | Purpose                                                           |
|--------------|----------|-------------------------------------------------------------------|
| `apiVersion` | yes      | Schema version. Always `processkit.projectious.work/v1` at v0.x. |
| `kind`       | yes      | Primitive type. Determines which schema validates `spec`.         |
| `metadata`   | yes      | Identity, timestamps, labels. Cross-cutting fields.               |
| `spec`       | yes      | Entity-specific fields. Validated by primitive schema.            |

## metadata fields

| Field     | Required | Type              | Notes                                                  |
|-----------|----------|-------------------|--------------------------------------------------------|
| `id`      | yes      | string            | Unique identifier. Format configurable (see below).    |
| `created` | yes      | ISO 8601 datetime | UTC. Never edited after creation.                      |
| `updated` | no       | ISO 8601 datetime | Set on modification.                                   |
| `labels`  | no       | map[string]string | Arbitrary key-value tags. Used by queries and filters. |

## ID formats

Configurable per project through installer or processkit settings:

| `id_format` | `id_slug` | Example                     |
|-------------|-----------|-----------------------------|
| `word`      | `false`   | `BACK-calm-fox`             |
| `word`      | `true`    | `BACK-calm-fox-add-lint`    |
| `uuid`      | `false`   | `BACK-550e8400-e29b-41d4`   |
| `uuid`      | `true`    | `BACK-550e8400-add-lint`    |

The prefix (`BACK-`, `LOG-`, `DEC-`, ...) is determined by the primitive
kind and is not configurable. See
[Reference → ID Formats](../reference/id-formats) for details.

## apiVersion policy

`apiVersion` follows the Kubernetes convention: `<group>/<version>`, where
the group is a reverse-DNS name anchored on the owning organization. For
processkit the group is `processkit.projectious.work`, making `processkit`
a subcomponent of the `projectious.work` organization. This prevents
name collisions if other organizations fork or publish compatible
primitives under their own domains.

See [Reference → apiVersion Policy](../reference/apiversion-policy) for
the evolution rules.

## Authoritative source

The authoritative specification is
[`src/context/schemas/`](https://github.com/projectious-work/processkit/tree/main/src/context/schemas)
in the processkit repo. This page is a condensed overview; the shipped
schema files define the authoritative `spec` contracts for each kind.
