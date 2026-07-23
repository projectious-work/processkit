---
name: skill-management
description: >
  Manage Skill package manifests as v1 ontology entities.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-skill-management
    version: "1.0.0-alpha.1"
    created: 2026-07-23T00:00:00Z
    category: processkit
    layer: 1
    provides:
      primitives: [Skill]
      mcp_tools:
        - create_skill
        - get_skill
        - update_skill
        - transition_skill
        - list_skills
---

# Skill Management

## Intro

Skill management projects Agent Skills packages into the v1 Skill ontology
without inventing a second canonical file. The package `SKILL.md` remains the
source of truth and is validated, indexed, and governed through MCP.

## Overview

Use `create_skill` for a small conformant package, `update_skill` for manifest
metadata, and `transition_skill` for lifecycle state changes. Use
skill-builder for richer authoring and skill-reviewer for quality review.

All writes validate the projected manifest against the generated Skill schema,
refresh the read index, and emit an event.

## Gotchas

- **Do not create a parallel `context/skills/*.md` entity.** The package
  manifest is the canonical Skill representation.
- **Do not use metadata updates for lifecycle changes.** State changes belong
  to `transition_skill`.
- **Do not replace skill-builder.** This server provides ontology lifecycle
  parity; skill-builder still owns full package design.
- **Do not use unsafe names or categories.** Names are kebab-case and paths
  remain beneath `context/skills/`.

## Full reference

The server indexes each package as `Skill` with its declared `SKILL-*` ID.
Projected fields include name, description, version, state, category, layer,
uses, provides, commands, triggers, owners, and capabilities.
