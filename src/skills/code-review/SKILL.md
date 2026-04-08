---
name: code-review
description: |
  Structured code review with a checklist covering correctness, clarity, tests, security, performance, and style. Use when reviewing a PR, diff, or set of code changes before merging — including phrases like "review this", "check my changes", or "is this ready to merge".
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-code-review
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: process
    layer: 3
---

# Code Review

## Intro

Code review is a structured pass over a diff against a fixed
checklist, then a categorized response: must-fix, should-fix, nit.
The goal is to surface real defects with specific line references,
not to rewrite the author's code.

## Overview

### The review checklist

Read the diff or changed files, then evaluate each change against:

- **Correctness** — Does the code do what it claims? Are edge
  cases handled?
- **Clarity** — Are names descriptive? Is the logic easy to
  follow on a single read?
- **Tests** — Are new behaviors tested? Do existing tests still
  hold?
- **Security** — Hardcoded secrets, SQL injection, unsafe input
  handling, missing authz?
- **Performance** — Unnecessary allocations, N+1 queries,
  accidental O(n^2) loops?
- **Style** — Consistent with the project's existing conventions
  (not your personal preferences)?

### Categorize findings

Sort each finding into one bucket and label it explicitly:

- **Must fix** — bugs, security issues, broken tests, contract
  violations
- **Should fix** — unclear naming, missing tests for non-trivial
  paths, code smells
- **Nit** — style preferences, minor suggestions, taste calls

Always include specific line references and concrete suggestions.
Acknowledge what was done well — review is not adversarial.

## Full reference

### Example output shape

> **Must fix:** `parse_input()` on line 42 doesn't handle empty
> strings — this will panic.
>
> **Should fix:** The variable `x` on line 15 could be renamed to
> `retry_count` for clarity.
>
> **Nit:** Consider extracting lines 30-45 into a helper function.
>
> Overall: Good separation of concerns. The error handling pattern
> is clean.

### Anti-patterns

- **Rewriting in review** — propose, don't dictate. The author
  owns the code.
- **Bikeshedding** — if it's a nit, label it a nit and move on.
- **Stamp-of-approval review** — skimming and approving without
  reading the changed lines defeats the purpose.
- **Vague comments** — "this looks weird" is not actionable. Say
  what's weird and what would fix it.
- **Reviewing in one pass when the diff is huge** — split the
  review across sessions or push back on PR scope.

### When to escalate

If the diff has fundamental design issues, stop the line-by-line
review and discuss the design first. Line comments on a diff that
should never have been written waste both sides' time.
