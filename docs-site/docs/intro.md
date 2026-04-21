---
sidebar_position: 1
title: "Introduction"
slug: /
---

# processkit

**processkit gives AI agents domain-specific intelligence.**
It is the content layer for [aibox](https://github.com/projectious-work/aibox) —
structured skills, process primitives, and MCP servers that make agents reliably
good at specific tasks rather than generically capable at all of them.

## The design

Anthropic's agent-skill framework identifies five patterns for how skills add
value. processkit is built around **Pattern 5 — domain-specific intelligence**:
every skill packages the conventions, gotchas, and decision rules that a domain
expert would carry in their head, so the agent doesn't have to reconstruct them
from first principles on every task.

> Pattern 5 skills add specialized knowledge *beyond* raw tool access.
> The agent using a skill reasons like a domain expert, not like a generalist
> who happens to have the right tools available.

This is what separates a processkit skill from a plain system prompt: the skill
is the domain expert. The agent is the executor.

## What processkit ships

- **20 process primitives** — WorkItem, LogEntry, DecisionRecord, Note,
  Migration, Actor, Role, Binding, Scope, Category, Constraint, Gate, Schedule, Process,
  StateMachine, Metric, Discussion, Artifact, Context, CrossReference.
  Framework-agnostic building blocks shipped as YAML schemas + state machines.
- **128+ skills** — engineering, language, framework, infrastructure, design, data,
  security, AI/ML, process-primitive, document/asset creation, meta-cognitive,
  and role-specific skills (PRD writing, user research, legal review, data storytelling).
  Each skill follows the Anthropic Agent Skills spec: YAML frontmatter, three-section
  body (Intro / Overview / Full reference), 7 agent-specific gotchas, and an
  optional Python MCP server.
- **5 package tiers** — `minimal`, `managed`, `software`, `research`, `product` — curated
  bundles of skills for common use cases.
- **Python MCP servers** (from v0.3.0) — mechanical-correctness tools for foundation skills,
  delivered via the official MCP SDK with PEP 723 inline dependencies.
- **Configurable upstream + diff script** *(from v0.4.0)* — `[processkit] source` in
  `aibox.toml` accepts any git URL (GitHub, GitLab, Gitea, self-hosted), so companies
  can fork processkit, customize it, and have their projects consume the fork.

## How it's used

A consumer selects a processkit source and version in their `aibox.toml`:

```toml
[processkit]
source  = "https://github.com/projectious-work/processkit.git"
version = "v0.18.2"

[context]
packages = ["managed"]
```

`aibox init` fetches that tag and installs the selected package's
skills, primitives, and process templates into the project's `context/`
directory (provider-neutral — nothing lands under `.claude/`). The
project gets `aibox.lock` at the repository root (Cargo-style, pinning
the resolved source URL + version + commit) and a verbatim reference
copy of every shipped file at
`context/templates/processkit/<version>/`. A future `aibox sync` reads
SHAs from those reference templates on the fly to classify what's been
changed locally vs upstream — no separate manifest file is needed.

Users can add more skills from any GitHub repo using the same pattern.

## The two repos

| Concern                | aibox                                       | processkit                                |
|------------------------|---------------------------------------------|-------------------------------------------|
| Containers & toolchain | Yes — CLI, images, devcontainer scaffolding | No                                        |
| Skills & process       | No (consumes from processkit)               | Yes — skills, primitives, MCP servers     |
| CLI surface            | `aibox init`, `aibox start`, ...            | None (consumed, not run)                  |
| Release mechanism      | GHCR images + CLI binary                    | Git tags                                  |

Splitting content from infrastructure lets both sides evolve at their natural pace.

## Where to go next

- [Getting Started](./getting-started/overview) — install aibox, consume processkit, create your first entity
- [Primitives](./primitives/overview) — the 20 building blocks and the entity file format
- [Skills](./skills/overview) — the skill package format and the catalog
- [Packages](./packages/overview) — the five tiers and how to pick one
- [Reference → Privacy Tiers](./reference/privacy) — public, project-private, user-private
- [Reference → Migration](./reference/migration) — the migration model

## Status

- **v0.1.0** — foundation (entity format, three primitives, two state machines)
- **v0.2.0** — skill migration (85 + 16 skills, packages, this docs site)
- **v0.3.0** — MCP servers (six servers, shared lib, smoke tests)
- **v0.4.0** — Migration primitive, owner-profiling, context-grooming,
  PROVENANCE.toml + diff script, configurable upstream source URL, privacy tiers
- **v0.5.0** — Anthropic Agent Skills spec alignment, Gotchas discipline (7 per skill),
  Intro/Overview/Full reference structure, FORMAT.md, skill-builder + skill-reviewer,
  scripts/ subdirectory, assets/, session-handover, standup-context
- **v0.5.1** — 30 new skills (document creation, meta-cognitive, role-specific),
  Note primitive + note-management skill, status-briefing
- **v0.7.0–v0.9.0** — `src/context/` mirror restructure; all primitives gain JSON
  schemas; auto-log side-effects in all entity-mutating MCP servers
- **v0.10.0** — skills directory reorganised into 7 category subdirectories
  (`processkit/`, `engineering/`, `devops/`, `data-ai/`, `product/`, `documents/`,
  `design/`); `resolve_entity()` 3-stage ID lookup (exact → prefix → word-pair);
  structured error responses from all MCP read tools
- **v0.11.0** — Note `links` field (Zettelkasten relations with typed edges);
  Artifact self-hosted and pointer patterns documented; MCP server path fixes
  after v0.10.0 reorganisation
- **v0.11.1** — `pascal` and `camel` word styles correctly distinct;
  `context/` dogfood mirror synced with `resolve_entity()`
- **v0.12.0** — `artifact-management` skill and MCP server (Layer 2);
  `create_artifact`, `get_artifact`, `query_artifacts`, `update_artifact`;
  Artifact is a catalogue record with no state machine
- **v0.13.0** — `task-router` and `skill-finder` MCP servers;
  `route_task()` returns skill + process override + tool in one call;
  `skill-gate` meta-skill (1% rule); MCP tool prerequisite prompts on all
  20 entity-mutating tools; one-sentence imperative description convention
- **v0.14.0** — enforcement Rails 1–4: canonical compliance
  contract + AGENTS.md primacy header (Rail 1); provider-neutral hook
  scripts for SessionStart / UserPromptSubmit / PreToolUse (Rail 2);
  `acknowledge_contract()` MCP tool on `skill-gate` (Rail 3); 1%-rule
  sentence in 8 entity-mutating MCP tool descriptions (Rail 4)
- **v0.15.0** — `team-creator` skill (provider-neutral team composition
  by cost/outcome tier, 3 commands, no new MCP server); session-
  orientation wiring (AGENTS.md "Session start" block + extended
  SessionStart hook); `status-briefing` v1.1.0 (pending-migrations
  source + token-budget snapshot); 6 new artifacts; 3 follow-up
  WorkItems including OpenWeave (4-layer overrides) and Rail 5 (L1+L2)
- **v0.16.0** — canonical team-composition schema fields
  (closes aibox issue #6): `Role.primary_contact` / `clone_cap` /
  `cap_escalation`, `Actor.is_template` / `templated_from`; `team-creator`
  v1.1.0 emits them on every run; two applied migrations back-fill
  existing entities; `role-management` + `actor-profile` bumped to v1.0.1
- **v0.17.0** — 13 `/pk-*` ergonomic slash commands
  (provider-neutral `/pk-<verb>` namespace); OpenWeave 4-layer override
  for `team-creator` v1.2.0; Rail 5 decision-capture gate + sweeper
  (shadow-mode); compliance contract v2; `pk-commands` YAML block in
  AGENTS.md for build/test/lint; ShadowCount calibration (NO-GO on block)
- **v0.18.0** — CapabilityProfileRouting three-layer model
  selection (catalog / preferences / role standard sets);
  `Role.model_profiles` ranked array + optional `Actor.model_profile_override`;
  13 additional `/pk-*` promotions (26 total, 0 legacy commands);
  skill-gate PreToolUse hook decoupled from `session_id`;
  `emit_compliance_contract.py` echoes `hookEventName` for Claude Code 2.1+
- **v0.18.1** — hotfix release: sync `src/context/` with content
  that had been landing only in the dogfooded `context/` tree since v0.15.0
  (team-creator skill, 26 `/pk-*` commands, Rail 5 scripts + fixtures, schema
  updates). Fixes [#7](https://github.com/projectious-work/processkit/issues/7):
  `emit_compliance_contract.py` now emits `hookEventName` so Claude Code 2.1+
  accepts the hook envelope.
- **v0.18.2** *(current)* — fixes [#8](https://github.com/projectious-work/processkit/issues/8):
  stale `mcp-config.json` paths in 12 of 16 per-skill configs blocked MCP
  server startup in derived projects. Adds `skip_decision_record` MCP tool +
  compliance contract v2 bump, `scripts/check-src-context-drift.sh` release-time
  drift guard, session-start skill-check checklist (SnappyTrout), and
  `/pk-standup` vs `/pk-status` differentiation.
- **v1.0.0** — first stable release (not yet scheduled)
