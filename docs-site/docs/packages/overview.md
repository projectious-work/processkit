---
sidebar_position: 1
title: "Overview"
---

# Packages — Overview

Packages are opinionated bundles of skills. Pick one tier as your
starting point, then add or remove skills through your installer or local
package metadata when you need a narrower context.

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

When installing manually, select a package by copying the shipped
context and then enabling the tier through your own harness or installer
configuration. Managed installers can expose this directly. For example,
aibox uses:

```toml
# aibox.toml
[processkit]
source = "https://github.com/projectious-work/processkit.git"
version = "v0.25.0"

[context]
packages = ["software"]
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

then reference it from your installer or package selection config:

```toml
[context]
packages = ["my-team"]
```

## Source files

Each tier is defined in a YAML file in
[`src/.processkit/packages/`](https://github.com/projectious-work/processkit/tree/main/src/.processkit/packages):
`minimal.yaml`, `managed.yaml`, `software.yaml`, `research.yaml`,
`product.yaml`. The YAML is the source of truth; these docs pages
summarize the intent.

## Why packages are standalone

processkit packages are content, not environment machinery:

- **Reusable content.** The skills, schemas, and MCP servers in processkit
  work with any compatible agent harness or MCP client. They are not
  tied to a specific devcontainer implementation.
- **Forkable catalog.** Organisations can maintain a private fork of
  processkit with custom skills, schemas, and MCP servers. That fork is
  consumable by any installer that can copy the release files and launch
  the MCP commands.
- **Independent release cadence.** Content (skills, primitives) changes
  more frequently than infrastructure. Keeping packages in processkit
  lets users update process content without changing their harness.
