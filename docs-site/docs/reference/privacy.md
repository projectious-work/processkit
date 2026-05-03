---
sidebar_position: 4
title: "Privacy Tiers"
---

# Privacy Tiers

processkit recognizes three privacy tiers for entities under `context/`.
The tier is declared via an optional `privacy:` field in `metadata` and
enforced by directory layout + a `.gitignore` rule.

## The three tiers

| Tier | Default? | Git status | Typical use |
|---|---|---|---|
| `public` | no | tracked | identity.md, README, public roadmap |
| `project-private` | **yes** (default if omitted) | tracked | workitems, decisions, logs, working-style.md |
| `user-private` | no | NOT tracked | team-and-relationships.md, personal scratch notes |

Most entities omit the field entirely and inherit `project-private`.

## Filesystem rule for `user-private`

Entities with `privacy: user-private` MUST live under a directory named
`private/` somewhere within `context/`. Projects should carry a
`.gitignore` rule like:

```
context/**/private/
```

This pattern matches `private/` directories at **any depth** under
`context/`, including directly under `context/` itself. So all of these
are excluded from git:

- `context/private/`
- `context/owner/private/`
- `context/foo/bar/private/`

But NOT directories named `private/` outside `context/` (e.g.
`cli/src/private/` would NOT be ignored by this rule).

Installers and validation tools should verify that any entity with
`privacy: user-private` lives under a `private/` directory under
`context/`. A user-private entity outside such a directory is invalid.

## Where the convention is used

- **`owner-profiling` skill**: `context/owner/private/team-and-relationships.md`
  is the canonical example. Notes about coworkers' communication styles,
  sensitivities, and interpersonal dynamics should never be checked into a
  shared repository.
- **Personal scratch notes**: any project can have a `context/private/` for
  personal drafts, half-formed ideas, or session notes that the agent
  should see but the team should not.
- **API keys / secrets** are NOT what this is for — those should be in
  environment variables or a secret manager. Privacy tiers are for
  human-readable content that's sensitive but not credentialed.

## Frontmatter example

```yaml
---
apiVersion: processkit.projectious.work/v1
kind: Context
metadata:
  id: OWNER-team-and-relationships
  privacy: user-private
  created: 2026-04-07T00:00:00Z
spec:
  description: "Per-person notes about collaborators."
---

# Team and Relationships

> ⚠️ PRIVACY: user-private. This file lives under context/owner/private/
> which is gitignored.

...
```

## Why directory enforcement, not just frontmatter

A frontmatter declaration alone wouldn't prevent the file from being
checked into git — `git add` doesn't read frontmatter. The directory rule
gives a hard guarantee via `.gitignore`. The frontmatter declaration is
documentation + lint validation; the directory placement is the actual
safety mechanism.

If you want a `user-private` file outside any `private/` directory, you
have two options:

1. Move it under a `private/` directory (correct)
2. Override the validation rule in local tooling (discouraged because it
   defeats the safety mechanism)

## Public files

`privacy: public` is documentation, not security — anything in a public
git repo is already world-readable. The distinction between `public` and
`project-private` only matters when the project is in a private repo: in
that case `public` files are fine to syndicate to a public mirror or
include in a generated README, while `project-private` files are not.
For projects in public repos, `public` and `project-private` are
functionally identical.

## Docs-site filtering

Projects that build a Docusaurus docs site from their context content
must exclude private subtrees from the build. Add this to the `docs`
preset in `docusaurus.config.js`:

```js
docs: {
  exclude: ['**/private/**'],
}
```

This is the same rule processkit's own docs-site carries. The rule
matches `private/` directories at any depth, so `context/private/`,
`context/owner/private/`, and any deeper nesting are all excluded.

## Multi-user projects

For projects where multiple people work from the same repository, the
current convention is **flat `context/private/`**: a single gitignored
directory that is personal to whoever is running the agent locally.

A per-user subdirectory convention (`context/private/<username>/`) is
**not yet standardized**. The actor primitive (`actor-profile`) captures
identity but the privacy directory layout does not yet key on it.
Defer the multi-user convention until a real project asks for it —
at that point, `context/private/<username>/` is the natural extension
and requires no schema changes, only a new gitignore pattern.

*This decision was recorded in response to aibox DEC-030 /
[processkit#1](https://github.com/projectious-work/processkit/issues/1).*
