---
name: agent-card
description: |
  Project processkit agent-card Artifacts into canonical public
  agent-card JSON files. Use when publishing an agent identity,
  endpoint, capability, or interoperability card from repository
  context into a runtime-visible file.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-agent-card
    version: "2.0.0-alpha.1"
    created: 2026-04-30T00:00:00Z
    category: processkit
    layer: 3
    provides:
      primitives: [Artifact, Actor]
      mcp_tools: [project_agent_card]
---

# Agent Card

## Intro

Agent cards describe a runnable or externally visible agent in a
provider-neutral JSON shape. Store the canonical source as an Artifact
with `spec.kind=agent-card`; use `project_agent_card` to render the
public JSON file and return a checksum.

The source Artifact may put the card under `spec.card`, or it may store
YAML/JSON card content in the Markdown body. Optional Actor data can
augment the projected card with runtime interfaces.

