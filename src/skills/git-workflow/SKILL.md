---
name: git-workflow
description: |
  Git workflow conventions — branch naming, conventional commits, PR descriptions, and merge strategy. Use when deciding on a branch name, writing a commit message or PR description, or choosing a merge strategy.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-git-workflow
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 3
---

# Git Workflow

## Intro

Use typed branch names, Conventional Commits, and PR descriptions
that explain the why. Squash-merge feature branches for a clean
history. Keep commits atomic and never force-push to shared
branches.

## Overview

### Branch naming

Format: `<type>/<issue>-<short-description>`

Types: `feat/`, `fix/`, `refactor/`, `docs/`, `chore/`

Examples:

- `feat/42-add-user-auth`
- `fix/17-null-pointer-crash`
- `refactor/89-extract-payment-service`

### Commit messages

Follow Conventional Commits:

- **Format:** `<type>: <description>` — lowercase, imperative
  mood, no trailing period
- **Types:** `feat`, `fix`, `refactor`, `docs`, `test`, `chore`,
  `ci`
- **Body:** explain WHY, not WHAT (the diff shows what)
- **Footer:** `fixes #N` or `refs #N` for issue links

### PR descriptions

- **Title:** same format as commit messages, under 70 characters
- **Body:** Summary (what and why), test plan, breaking changes
- Link related issues

### Merge strategy

- **Squash merge** for feature branches — keeps mainline history
  clean
- **Merge commit** for long-lived branches — preserves context
  across the merge
- **Rebase** to keep a feature branch up to date before opening
  the PR

## Full reference

### General rules

- Commit early and often on feature branches; squash at merge time.
- Never force-push to shared branches (`main`, `develop`, release
  branches).
- Keep commits atomic — one logical change per commit. A commit
  that touches three unrelated concerns is three commits.
- A commit message body wraps at 72 columns; the subject line at
  50 if you can.

### Worked example

User: "What should I name this branch for adding search?"

Suggest `feat/30-add-search-functionality` if there's an issue
#30; otherwise `feat/add-search-functionality`. Match the
existing repo's convention if it differs.

### Anti-patterns

- **Mega-commits** — "various fixes" with 40 files changed.
  Impossible to review or revert.
- **Force-push to main** — destroys other contributors' work.
- **Commit messages like "wip", "fix", "stuff"** — every commit
  should be reviewable on its own.
- **PRs with no description** — the PR description is for the
  reviewer, not the author. "See commits" is not a description.
- **Branches that live for months** — long-lived branches
  diverge from main and become merge nightmares. Rebase weekly
  or split the work.

### When to break the rules

Solo-on-a-private-branch force-pushes are fine. Trivial typo
fixes don't need a long body. Use judgment, but the defaults
above are right for almost every team setting.
