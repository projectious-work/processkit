---
sidebar_position: 3
title: "managed"
---

# managed

**Intended for:** small teams with a shared backlog and process cadences.
**Extends:** `minimal`

The recommended default. Adds roles, decisions, scopes, and all lightweight
process artifacts (standups, retros, session handovers) on top of minimal.

## What managed adds on top of minimal

**Process primitives (all 16 new skills):**
`role-management`, `decision-record`, `scope-management`,
`category-management`, `cross-reference-management`, `binding-management`,
`process-management`, `state-machine-management`, `gate-management`,
`schedule-management`, `constraint-management`, `discussion-management`,
`metrics-management`.

**Lightweight process artifacts:**
`backlog-context`, `decisions-adr`, `standup-context`, `session-handover`,
`context-archiving`, `retrospective`, `estimation-planning`, `code-review`,
`documentation`, `refactoring`, `tdd-workflow`, `incident-response`,
`postmortem-writing`, `release-semver`, `integration-testing`,
`dependency-management`.

## When to upgrade

- You need production-grade infrastructure, observability, and security skills → `software`
- You need data/ML skills → `research`
- You need design + frontend + everything → `product`

## Source

[`src/packages/managed.yaml`](https://github.com/projectious-work/processkit/blob/main/src/packages/managed.yaml)
