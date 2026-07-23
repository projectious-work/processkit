---
name: proposition-management
description: >
  Record and maintain claims and risks through the Proposition interface.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v2
    id: SKILL-proposition-management
    version: "1.0.0-alpha.1"
    created: 2026-07-23T00:00:00Z
    category: processkit
    layer: 1
    uses:
      - skill: event-log
        purpose: Record proposition creation and updates.
      - skill: index-management
        purpose: Query Proposition interfaces and discriminators.
    provides:
      primitives: [Proposition]
      mcp_tools:
        - create_proposition
        - get_proposition
        - update_proposition
        - query_propositions
---

# Proposition Management

## Intro

Proposition management records claims and risks without splitting each
epistemic variant into a false top-level entity kind.

## Overview

Use `create_proposition(kind="claim", ...)` for an ordinary claim and
`kind="risk"` with likelihood and impact for a Risk discriminator. Read and
query through the shared Proposition interface. Updates revalidate the
selected discriminator overlay and preserve one `PROP-` identity.

## Gotchas

- **Do not create a top-level Risk entity.** Risk is a Proposition
  discriminator and must retain `kind: Proposition` in frontmatter.
- **Do not omit likelihood or impact for risks.** The generated Risk overlay
  requires both.
- **Do not silently change a proposition's discriminator.** `kind` is fixed
  after creation; supersede when semantics fundamentally change.
- **Do not treat confidence as a percentage.** The contract accepts a value
  from zero to one.
- **Do not query filenames to find risks.** Use the Proposition interface and
  `risk` discriminator stored in the index.

## Full reference

Claims accept status, confidence, ownership, evidence, scope, source, validity,
and supersession metadata. Risks add likelihood, probability, impact,
risk-status, response, mitigation, contingency, affected entities, and review
or realization timestamps.

Anti-patterns:

- Recording a task or defect as a Proposition instead of a WorkItem.
- Conflating risk acceptance with evidence that the risk is false.
- Rewriting a historical statement instead of recording supersession.
