---
name: standard-git-branching
description: Company Git branching and release promotion standard. Use when creating branches, choosing a merge target, merging PRs, promoting through vX.x-dev/pre-release/release/main, tagging releases, or fixing a production incident on a stable line.
---

# standard-git-branching

Binding company standard. The rules below are the summary; the linked file is authoritative. Read only the section the task needs.

## Git branching and release promotion standard

When a version line is active, develop only through short-lived branches
into `vX.x-dev`. Promote exact commits by fast-forward through
`vX.x-pre-release`, then `vX.x-release`, then `main`. Never put unique commits
on a promotion branch. Start stable incident fixes from the affected release
tag and forward-port them into every affected active development line.

Before acting, an agent reports the selected mode, source branch, target
branch, intended version, and whether the operation is topic integration,
promotion, stable incident repair, or older-major maintenance. Ambiguity is a
stop condition, not permission to infer a target.

Before merging, the agent asks for explicit owner approval unless a valid
approval for the exact revision is already recorded. After approval, the agent
may merge and continue the authorized release or deployment sequence. A GitHub
`REVIEW_REQUIRED` result means the configured repository settings still demand
a GitHub review; the agent reports the policy mismatch instead of treating the
platform status as a company-wide requirement or bypassing it.

Full standard: `docs/standards/git-branching-and-release-promotion.md`. Sections:

- Purpose and scope
- Branch roles
- Normal development
- Approval and merge authority
- Promotion and freeze
- Release sequence and tags
- Production incidents and patch releases
- Older-major maintenance
- Protection and audit requirements
- Authoritative references
