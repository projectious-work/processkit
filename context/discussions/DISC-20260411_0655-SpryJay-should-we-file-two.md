---
apiVersion: processkit.projectious.work/v2
kind: Discussion
metadata:
  id: DISC-20260411_0655-SpryJay-should-we-file-two
  created: '2026-04-11T06:55:04+00:00'
  updated: '2026-04-11T06:56:42+00:00'
spec:
  question: 'Should we file two aibox bugs: (1) docs-docusaurus addon installs create-docusaurus
    instead of docusaurus CLI, and (2) Docusaurus 3.9.2 build fails with ProgressPlugin
    schema mismatch?'
  state: resolved
  opened_at: '2026-04-11T06:55:04+00:00'
  closed_at: '2026-04-11T06:56:42+00:00'
---

## Context

Discovered during WildButter docs-site work (2026-04-11). Attempted to
build docs-site and hit two distinct failures.

## Bug 1 — Wrong package in docs-docusaurus addon

The generated Dockerfile contains:
```
RUN npm install -g create-docusaurus@latest
```

`create-docusaurus` is the *scaffolding* tool for creating new Docusaurus
projects. It does not install the `docusaurus` CLI. As a result, `docusaurus`
is not on PATH and `npm run build` fails with `sh: 1: docusaurus: not found`
unless the user manually runs `npm install` in the `docs-site/` directory
first.

Fix: the addon should either install `@docusaurus/core` globally, or run
`npm install` in the docs-site directory as part of the container build
(e.g. via `post_create_command` or a Dockerfile step).

## Bug 2 — Docusaurus 3.9.2 build fails with Webpack ProgressPlugin error

Even after running `npm install` locally, the build fails:

```
ValidationError: Invalid options object. Progress Plugin has been
initialized using an options object that does not match the API schema.
options has an unknown property 'name' ... 'color' ... 'reporters'
```

This is a compatibility issue between `progress-webpack-plugin` and the
Webpack version bundled with Docusaurus 3.9.2. Likely an upstream
Docusaurus regression.

Fix: downgrade Docusaurus to 3.8.x or wait for an upstream patch.
The `docs-docusaurus` addon pins `docusaurus = { version = "3" }` which
resolves to `3.latest` — explicit minor pinning (e.g. `"3.8"`) would
avoid this.

## Decision needed

Do we file both as aibox issues? Bug 1 is clearly an aibox bug.
Bug 2 is upstream Docusaurus but the addon's unpinned `version = "3"`
exposes consumers to it — aibox could protect against this by pinning
to a tested minor.
