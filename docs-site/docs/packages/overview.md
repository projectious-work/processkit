---
sidebar_position: 1
title: "Overview"
---

# Packages — Overview

Packages are opinionated bundles of skills that consumers select in their
`aibox.toml`. Pick one tier as your starting point; fine-tune with
`[skills] include/exclude` if needed.

## The five tiers

| Package    | Extends      | Best for                                                  |
|------------|--------------|-----------------------------------------------------------|
| `minimal`  | —            | Solo developers, side projects, early-stage experiments   |
| `managed`  | `minimal`    | Small teams who want a shared backlog and cadence rituals |
| `software` | `managed`    | Engineering teams building production software systems    |
| `research` | `managed`    | Data science, ML, and research-heavy projects             |
| `product`  | `software`   | Full product teams: engineering + design + product ops    |

`managed` is the recommended default. Start there and add skills as
needed rather than starting with `software` or `product`.

## What each tier adds

Each tier is cumulative — higher tiers include everything below them.

| Tier | Key additions over the tier below |
|---|---|
| `minimal` | Backlog (WorkItem), event-log, actor-profile, git-workflow, debugging, testing-strategy, error-handling |
| `managed` | Roles, decisions (DecisionRecord), scopes, standup, session-handover, retrospective, release-semver, code-review, refactoring, TDD, documentation, dependency-management |
| `software` | Architecture, API design, databases, infrastructure (Docker, k8s, Terraform), security (OWASP, auth), observability, performance |
| `research` | Data science, data pipeline, data quality, feature engineering, pandas/polars, RAG, ML pipeline, prompt engineering, LaTeX, infographics |
| `product` | Frontend design, mobile design, logo design, FastAPI, TypeScript, Flutter, Tailwind, Reflex, SEO, PRD writing, user research |

## How composition works

Packages compose via `spec.extends`. The effective skill set of a package
is the union of its parent(s)' effective skill sets plus its own
`includes.skills`. Cycles are not allowed.

```
minimal ── managed ── software ── product
                   └─ research
```

## Using a package

```toml
# aibox.toml
[context]
packages = ["software"]
processkit_version = "v0.15.0"

[skills]
include = ["logo-design"]       # add to software
exclude = ["terraform-basics"]  # remove from software
```

## Creating a project package

For deeper customization, create your own package file under
`context/packages/`:

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Package
metadata:
  id: PKG-my-team
  name: my-team
  version: "1.0.0"
spec:
  description: "Custom bundle for my team."
  extends: [managed]
  includes:
    skills:
      - rust-conventions
      - auth-patterns
      - logging-strategy
---
```

then reference it in `aibox.toml`:

```toml
[context]
packages = ["my-team"]
```

## Source files

Each tier is defined in a YAML file in
[`src/context/packages/`](https://github.com/projectious-work/processkit/tree/main/src/context/packages):
`minimal.yaml`, `managed.yaml`, `software.yaml`, `research.yaml`,
`product.yaml`. The YAML is the source of truth; these docs pages
summarize the intent.

## Why processkit and aibox are separate projects

processkit and [aibox](https://github.com/projectious-work/aibox) split
content from infrastructure deliberately:

- **Reusable content.** The skills, schemas, and MCP servers in processkit
  work with any AI agent harness — Claude Code, Cursor, Codex CLI, or a
  custom agent. They are not tied to aibox's devcontainer machinery.
- **Forkable catalog.** Organisations can maintain a private fork of
  processkit with custom skills, schemas, and MCP servers. That fork is
  consumable by aibox (or any other tool) without changes to the consumer.
  A team's specialized domain knowledge lives in their fork, not in their
  infrastructure.
- **Independent release cadence.** Content (skills, primitives) changes
  more frequently than infrastructure (container images, CLI). Splitting
  the repos lets each side version independently — processkit can ship
  new skills without an aibox release, and aibox can update its CLI
  without invalidating pinned processkit content.
- **Smaller aibox.** aibox is a thin installer and environment manager.
  It does not need to carry 128+ skills, 13 MCP servers, and 20 primitive
  schemas in its own repo. processkit handles all of that.
