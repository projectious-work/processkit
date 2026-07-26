---
title: OKF Compatibility Analysis
description: Analysis of OKF as an import, export, and publication profile.
---

# OKF Compatibility Analysis

Source:

- Google Cloud announcement, "Introducing the Open Knowledge Format",
  published 2026-06-12
- `GoogleCloudPlatform/knowledge-catalog` `okf/SPEC.md`, v0.1 draft,
  inspected at `d44368c15e38e7c92481c5992e4f9b5b421a801d`

Analyzed: 2026-07-04

## Recommendation

processkit v1.0 should support OKF as an import/export and publication
profile, but should not make OKF the canonical internal format.

In practical terms:

- Yes: emit conformant OKF bundles from selected processkit knowledge.
- Yes: ingest OKF bundles into processkit as external knowledge sources.
- Yes: preserve OKF-compatible affordances in v1.0 schema design where
  they do not weaken processkit semantics.
- No: do not require the whole repository or canonical `context/` tree
  to be an OKF bundle.
- No: do not replace processkit entity IDs, typed relations, lifecycle
  states, validation modes, event logs, or interface-aware queries with
  OKF's permissive markdown conventions.

This gives us interoperability without losing the benefits that make
processkit more than an LLM wiki.

## What OKF Is

OKF v0.1 is a deliberately small knowledge-bundle format:

- a directory tree of UTF-8 markdown files
- YAML frontmatter at the top of every concept document
- `type` as the only required frontmatter key
- optional `title`, `description`, `resource`, `tags`, and `timestamp`
- file path, minus `.md`, as the concept ID
- normal markdown links as graph edges
- optional `index.md` files for progressive disclosure
- optional `log.md` files for chronological history
- permissive consumers that tolerate missing optional fields, unknown
  types, unknown keys, broken links, and missing indexes

The announcement frames OKF as a vendor-neutral, agent- and
human-friendly standard for exchanging metadata, context, and curated
knowledge. It explicitly says OKF is a format, not a platform or service.

## Fit With processkit Goals

OKF strongly aligns with several processkit goals:

- plain files over service lock-in
- git-native review, diffs, history, and distribution
- human-readable and agent-readable knowledge
- provider-neutral consumption
- markdown plus YAML frontmatter
- progressive disclosure through indexes
- graph navigation through links

This means OKF is strategically relevant. It is close enough to
processkit's existing shape that ignoring it would create unnecessary
interoperability debt.

## Limits And Mismatches

OKF is intentionally less strict than processkit needs to be.

Key mismatches:

- OKF has no fixed taxonomy; processkit v1.0 is explicitly building a
  typed ontology with T/P/D/C classes.
- OKF treats `type` values as unregistered strings; processkit needs
  schema-backed kinds, discriminators, and interfaces.
- OKF concepts are identified by bundle-relative paths; processkit uses
  stable entity IDs and may move storage paths as an implementation
  detail.
- OKF links are untyped and their relationship meaning lives in prose;
  processkit needs typed Bindings, explicit relations, lifecycle
  transitions, and queryable graph semantics.
- OKF requires permissive consumption of broken links and unknown fields;
  processkit needs strict validation for migrated kinds and controlled
  tolerant validation during migration.
- OKF `log.md` is prose history; processkit LogEntry entities are
  structured, append-only process evidence.
- OKF reserves lowercase `index.md` and `log.md`; processkit has richer
  index, schema, migration, and event-log machinery that should not be
  collapsed into those two files.

There is also a reference-implementation/spec mismatch: the v0.1 spec
says only `type` is required for conformance, while the checked-in
reference agent's `OKFDocument.validate()` currently requires `type`,
`title`, `description`, and `timestamp`. For processkit, the spec should
be treated as normative and the reference implementation as an example
producer profile, not as the compatibility contract.

## Compatibility Model

The right compatibility model is a projection layer:

```text
processkit canonical entities
  -> OKF exporter
  -> conformant OKF bundle

OKF bundle
  -> OKF importer
  -> external-source Artifacts / Notes / indexed knowledge
```

The canonical v1.0 system should keep:

- generated schemas and validation modes
- entity IDs
- lifecycle state machines
- typed relations and Bindings
- interface-aware queries
- event logs
- MCP tools as the write path

The OKF layer should provide:

- read-only exports for external consumers
- lossy-but-useful imports of external OKF knowledge
- optional round-trip preservation of unknown OKF frontmatter
- generated `index.md` files for exported bundles
- generated `log.md` files only as human-facing summaries, not as the
  source of truth for process events

## Proposed v1.0 Requirements

Add an "OKF compatibility" acceptance slice to the v1.0 plan:

1. Define a processkit OKF exporter profile.
2. Map each exported processkit kind to an OKF `type`.
3. Include `title`, `description`, `timestamp`, and `tags` wherever
   available, even though only `type` is required by OKF.
4. Preserve processkit IDs in an extension key such as
   `processkit_id`.
5. Preserve processkit kind/interface metadata in extension keys such as
   `processkit_kind` and `processkit_interfaces`.
6. Encode typed relations in extension frontmatter, while also emitting
   normal markdown links for generic OKF consumers.
7. Generate conformant `index.md` files for progressive disclosure.
8. Treat `log.md` as an optional generated changelog summary.
9. Provide an OKF validator mode that checks v0.1 conformance.
10. Provide an OKF importer that marks imported knowledge as external
    and does not pretend it has full processkit lifecycle semantics.

## Decision Guidance

Adopt OKF compatibility if it remains a boundary format.

Do not adopt OKF as the internal canonical model unless the OKF
specification evolves to cover typed relations, lifecycle semantics,
stable non-path IDs, validation profiles, and structured event history.
That would be a different standard from OKF v0.1.

The safest wording for the v1.0 roadmap is:

> processkit v1.0 SHOULD be able to produce and consume OKF v0.1
> bundles, while retaining processkit's stricter canonical schema,
> lifecycle, relation, and MCP semantics internally.
