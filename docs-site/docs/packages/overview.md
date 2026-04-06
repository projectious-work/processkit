---
sidebar_position: 1
title: "Overview"
---

# Packages — Overview

Packages are opinionated bundles of skills that consumers select in their
`aibox.toml`. Pick one tier as your starting point; fine-tune with
`[skills] include/exclude` if needed.

## The five tiers

| Package    | Extends      | Intended for                                             |
|------------|--------------|----------------------------------------------------------|
| `minimal`  | —            | Solo developers and small side projects                  |
| `managed`  | `minimal`    | Small teams with a shared backlog and process cadences  |
| `software` | `managed`    | Software engineering teams building production systems  |
| `research` | `managed`    | Research, data science, and ML engineering projects     |
| `product`  | `software`   | Full product development (engineering + design + ops)  |

`managed` is the recommended default. Start there.

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
processkit_version = "v0.2.0"

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
[`src/packages/`](https://github.com/projectious-work/processkit/tree/main/src/packages):
`minimal.yaml`, `managed.yaml`, `software.yaml`, `research.yaml`,
`product.yaml`. The YAML is the source of truth; these docs pages
summarize the intent.
