---
name: pk-repo-reconcile
description: Use the repo-management skill to reconcile repository issues, change requests, local commits, and pushes
---

Use the repo-management skill to plan and apply guarded repository
reconciliation. Detect the provider first, inspect local git state, list
open issues and change requests when supported, build a dry-run plan,
then apply only safe actions.

Do not force-push, bypass provider checks, merge drafts, or close issues
without evidence. Ask before destructive or ambiguous actions. For
provider actions that are not implemented or not authenticated, report
structured blockers instead of treating them as resolved.
