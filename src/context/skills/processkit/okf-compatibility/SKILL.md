---
name: okf-compatibility
description: >
  Export processkit entities as conformant Open Knowledge Format bundles.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-okf-compatibility
    version: "1.0.0-alpha.1"
    created: 2026-07-23T00:00:00Z
    category: processkit
    layer: 2
    provides:
      primitives: []
      mcp_tools:
        - export_okf_bundle
        - validate_okf_bundle
---

# OKF Compatibility

## Intro

OKF compatibility projects selected canonical processkit entities into the
Open Knowledge Format v0.1 boundary format. It does not replace processkit
schemas, stable IDs, typed relations, lifecycles, or event history.

## Overview

Use `export_okf_bundle` to create a new bundle beneath the project root. Each
concept document includes the required OKF `type`, human-facing metadata, and
processkit extension keys. Typed references are retained in extension
frontmatter and rendered as ordinary Markdown links for generic consumers.

Use `validate_okf_bundle` to check the v0.1 core contract and internal links.

## Gotchas

- **Do not treat export as round-trip canonical storage.** It is a boundary
  projection and may be intentionally lossy.
- **Do not overwrite a prior export.** Choose a new directory so bundles are
  reviewable and reproducible.
- **Do not hide processkit identity.** Extension keys preserve stable IDs,
  kinds, interfaces, and typed references.
- **Do not require aibox.** Export and validation run from processkit alone.

## Full reference

OKF v0.1 requires UTF-8 Markdown with YAML frontmatter containing `type`.
processkit's producer profile additionally emits title, description,
timestamp, tags, `processkit_id`, `processkit_kind`,
`processkit_interfaces`, and `processkit_relations` when available.
