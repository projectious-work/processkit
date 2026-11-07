# Git branching and release promotion standard

## Purpose and scope

This is the default branching standard for projectious.work software
repositories. It defines how humans and AI agents develop, stage, release, and
maintain versioned software.

This document governs Git topology and promotion. The linked
[software verification and release-engineering standard](software-verification-and-release-engineering.md)
governs the evidence, tests, artifacts, and post-publication checks required
before those branch and tag transitions.

Use the version-line workflow when a major rewrite or a parallel major version
is underway. A repository that has no parallel major line MAY use short-lived
branches directly against `main`, provided `main` remains releasable and the
repository documents that simpler mode. Opening a version line activates every
rule below.

In branch names, `X` denotes the numeric major version. For example, the v1
line uses `v1.x-dev`, not a branch literally named `vX.x-dev`.

Terms in *italics* are
[Semantic Anchors](https://github.com/llm-coding/Semantic-Anchors/tree/ccb05b6bd41a663eaf2595e707d98f35d743e61f)
(commit `ccb05b6b`, 2026-10-26; adopting a later revision is a standards
change).

## Branch roles

```text
stable baseline on main
        │
        ├── vX.x-dev ── feat/* and fix/* integration
        │       │
        │       └── fast-forward promotion ──> vX.x-pre-release
        │                                            │
        │                                            └── alpha / beta tags
        │                                                    │
        │                            fast-forward promotion ──> vX.x-release
        │                                                            │
        │                                                            └── rc / final tags
        │                                                                    │
        └──────────────────── fast-forward final commit into main <─────────┘
```

| Branch | Role | Permitted changes |
|---|---|---|
| `main` | Published stable history and the latest supported major release. | Stable release promotions and production incident fixes only. |
| `vX.x-dev` | Normal integration branch for major line X. | Reviewed short-lived feature, fix, documentation, and release-preparation branches. |
| `vX.x-pre-release` | Exact staging pointer for alpha and beta validation. | Fast-forward promotions from `vX.x-dev` only. |
| `vX.x-release` | Exact stabilization pointer for release candidates and the final release. | Fast-forward promotions from `vX.x-pre-release` only. |
| `vX.x-maintenance` | Optional integration branch for a still-supported older major after a newer major becomes stable. | Reviewed fixes and patch-release preparation for that older major. |

The three version-line branches start at the same stable `main` commit.
`vX.x-pre-release` and `vX.x-release` are promotion pointers, not independent
development branches. Do not commit on them and do not merge topic branches
into them.

## Normal development

1. Create `feat/<topic>` or `fix/<topic>` from the current `vX.x-dev` tip.
2. Keep the branch focused and short-lived.
3. Merge it into `vX.x-dev` through the repository's required review and
   checks. Squash merge is the default for topic branches unless the repository
   has an explicit reason to preserve their commits.
4. Never merge a feature branch directly into `vX.x-pre-release`,
   `vX.x-release`, or `main`.
5. Delete the topic branch after integration when repository policy permits.

Documentation, tests, schemas, migrations, and release metadata follow the
same review path as code. AI agents MUST inspect the repository's current
version line and target branch before creating a branch or pull request.

### Commit messages

Commit messages and squash-merge titles follow *Conventional Commits*: a type
(`feat`, `fix`, `docs`, `refactor`, `test`, `build`, `chore`, …), an optional
scope, and an imperative subject; `!` or a `BREAKING CHANGE:` footer marks a
breaking change. Types map to *Keep a Changelog* sections and to the
*Semantic Versioning (SemVer)* bump. Required attribution trailers follow the
repository's policy.

### Keeping the integration branch green

After every merge, the author checks the verification of the merge commit on
the target branch. A red integration branch is fixed forward immediately,
before new work builds on it. Acceptance tests written ahead of their
implementation stay on their change branch and merge together with the
implementation that makes them pass; the integration branch never carries an
intentionally failing test.

### Phase integration branches

A spec-driven phase with separate acceptance-test and implementation tracks
uses a phase integration branch `phase/<phase-id>`, created from the
development-line tip at the frozen contract. The tests-only and implementation
branches merge into it during the integration loop. When every acceptance test
passes without skips, the phase integration branch merges into the development
line as one unit through the normal review path and is then deleted. It never
receives unrelated work and never merges partially.

## Approval and merge authority

Changes that require owner approval MAY receive that approval either:

- as a recorded GitHub pull-request review; or
- as an explicit instruction from the owner to the acting AI agent in the
  current, auditable working conversation.

Approval is a human decision, not a particular GitHub review object. An AI
agent that has verified the proposed source and target, reported the relevant
checks and risks, and received explicit owner approval MAY perform the merge on
the owner's behalf. The agent records the approval channel in the merge or
release evidence. General standing permission, silence, an ambiguous "looks
good", or approval for a different revision does not authorize a merge.

Repositories MAY configure GitHub branch protection or rulesets to require a
recorded approving review. This is an optional, project-level enforcement
choice, appropriate when multiple maintainers, external contributors,
regulatory controls, or project risk justify it. It is not the company
default. A repository using conversational owner approval MUST NOT configure a
required GitHub review count that prevents the approved AI-agent merge, unless
the owner intentionally chooses to complete a GitHub review as an additional
gate.

An agent MUST NOT bypass a configured protection rule merely because approval
exists elsewhere. If repository settings are stricter than the documented
project policy, stop and reconcile the setting or obtain the required GitHub
approval; do not use an administrator bypass as the routine path.

## Promotion and freeze

A promotion moves the destination branch to an already reviewed and tested
source commit. It MUST preserve commit identity:

```sh
git merge --ff-only <source-branch>
```

The equivalent protected-branch operation is acceptable when it demonstrably
makes the destination point at the exact source SHA. Squash, rebase, and merge
commits are prohibited for promotions. Approval, checks, and release evidence
are attached to the source SHA before the pointer moves.

At the first promotion to `vX.x-pre-release`, the release train enters feature
freeze. Until the final release reaches `main`, `vX.x-dev` accepts only changes
within the approved release scope: defect fixes, security fixes, tests,
documentation, version-independent release preparation, and explicitly
approved removals. Unrelated features wait until the train completes or use a
separate version line.

If a stabilization defect is found, create `fix/<topic>` from `vX.x-dev`, merge
it back into `vX.x-dev`, repeat the required checks, and promote the new tip
through every stage again. This rule keeps promotion branches free of unique
commits.

If `--ff-only` cannot promote a branch, stop. Do not force-push, rebase, or
manufacture an ancestry rewrite. Reconcile the divergence on `vX.x-dev`, rerun
the applicable validation, and retry the promotion. A public tag makes its
referenced history immutable.

## Release sequence and tags

1. Promote an approved `vX.x-dev` tip to `vX.x-pre-release`.
2. Create alpha and beta tags on validated `vX.x-pre-release` commits as
   needed, for example `v1.0.0-alpha.1` and `v1.0.0-beta.1`.
3. Promote the accepted beta commit, or a later revalidated commit, to
   `vX.x-release`.
4. Create release-candidate tags on validated `vX.x-release` commits, for
   example `v1.0.0-rc.1`.
5. If any tracked content changes after an RC, rerun the required checks and
   create a higher RC tag. The final release MUST NOT silently differ from its
   last accepted candidate.
6. After final validation, create the stable tag, for example `v1.0.0`, on the
   accepted `vX.x-release` commit.
7. Fast-forward `main` to that exact commit. Verify that `main`,
   `vX.x-release`, and the stable tag resolve to the same commit.

Alpha and beta stages are used according to product risk; every release does
not have to use both. RC validation is required unless the repository's
documented release policy explicitly permits a lower-risk patch release to
skip it.

Release tags MUST be annotated and SHOULD be cryptographically signed. A
published tag MUST never be moved or reused. Build metadata and release
artifacts MUST identify the tagged commit.

Version ordering follows Semantic Versioning 2.0.0. For an otherwise equal
version core, the intended progression is:

```text
alpha.N < beta.N < rc.N < final
```

Use numeric counters beginning at 1 and increase them monotonically within
each stage. SemVer defines prerelease versions as lower precedence than the
matching stable version.

## Production incidents and patch releases

For an incident in the current stable major:

1. Create `fix/<topic>` from the affected stable release tag, not from a
   development branch.
2. Apply the smallest safe fix and its regression test.
3. Validate and release the next patch version through the protected stable
   path. While `main` still represents that major, integrate the reviewed fix
   into `main` and tag the resulting accepted release commit.
4. Merge the updated `main` into the active development line for that same
   major before its next promotion. This preserves the ancestry required to
   fast-forward the eventual release back into `main`. Resolve any compatibility
   work through a reviewed synchronization branch.
5. Forward-port the fix into affected newer-major development lines through a
   separate reviewed change. Merge or cherry-pick according to codebase
   compatibility and preserve traceability to the incident and original
   commit.
6. Re-promote any active prerelease train whose candidate must contain the
   fix.

Never merge an active development line backward into a stable incident branch.
Never claim that a production action rolled back automatically merely because
the Git history was restored.

## Older-major maintenance

Create `vX.x-maintenance` only when all of the following are true:

- a newer major version has become the stable line on `main`;
- major X remains within its documented support window; and
- the project intends to publish further X-series patch releases.

Branch it from the latest stable vX tag. Fixes for that major use short-lived
`fix/<topic>` branches targeting `vX.x-maintenance`. Tag patch releases from
validated maintenance commits, using an RC when the project risk policy
requires one. Do not merge an older maintenance branch wholesale into `main`;
forward-port relevant fixes individually into active newer lines.

Archive or delete the maintenance branch when support ends, while retaining
immutable tags and release artifacts.

## Protection and audit requirements

- Repositories SHOULD protect `main` and long-lived version or maintenance
  branches with GitHub rulesets when the collaboration or risk profile warrants
  platform enforcement. Technical branch protection is optional for
  owner-operated repositories.
- Whether enforced by GitHub or by the documented agent workflow, prohibit
  force-pushes and branch deletion except through an explicitly approved
  recovery procedure.
- Require the repository's applicable tests, security checks, release gates,
  and explicit owner approval before integration or promotion. A recorded
  GitHub review is required only when the repository explicitly selects that
  enforcement profile.
- Restrict promotion and tagging rights to the release role or its explicitly
  authorized automation.
- Record source SHA, destination SHA, checks, approvals, toolchain versions,
  and produced artifacts for every release promotion.
- Run releases from clean worktrees and fetch remote state immediately before
  ancestry and tag checks.
- Do not create or modify a published release tag to repair a mistake; publish
  a new version.

## Agent briefing

> When a version line is active, develop only through short-lived branches
> into `vX.x-dev`. Promote exact commits by fast-forward through
> `vX.x-pre-release`, then `vX.x-release`, then `main`. Never put unique commits
> on a promotion branch. Start stable incident fixes from the affected release
> tag and forward-port them into every affected active development line.

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

## Authoritative references

- [Git merge documentation](https://git-scm.com/docs/git-merge), including the
  fail-closed behavior of `--ff-only`.
- [Git tag documentation](https://git-scm.com/docs/git-tag), including
  annotated and signed release tags.
- [Semantic Versioning 2.0.0](https://semver.org/).
