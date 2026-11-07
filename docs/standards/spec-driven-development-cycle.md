# Spec-driven development-cycle standard

## Purpose and scope

This standard defines how projectious.work implements a phase or material
change against an accepted specification. It applies when a repository has a
normative product or engineering specification.

This standard does not prescribe where specifications are stored or how
specification changes are represented. Those questions are deferred pending
the company discussion on specifications, OpenSpec, and processkit. It does
require the selected baseline and every change to it to be explicit.

A repository adopting this standard, or a later revision of it, names the
first phase it applies to. Phases completed before that point are not reopened
or re-gated; their evidence stands as recorded.

Terms in *italics* are
[Semantic Anchors](https://github.com/llm-coding/Semantic-Anchors/tree/ccb05b6bd41a663eaf2595e707d98f35d743e61f)
(commit `ccb05b6b`, 2026-10-26; adopting a later revision is a standards
change).

## Small-change path

A direct, narrowly scoped change request from the owner (for example "move
this hint into the sidebar, collapsible, also on mobile") does not restart the
cycle. The agent:

1. implements the change immediately;
2. updates the accepted baseline and the affected tests in the same change,
   with a one-line note in the baseline's change record;
3. decides open details with sensible defaults and lists them afterwards.

No new alternatives, approval round, or phase is required. During an active
phase with a frozen contract (§5), the updated contract becomes a new frozen
reference that the integration owner hands to both tracks (§6). A change that
alters scope, public interfaces, security, compatibility, or persistence is not
a small change and follows the full cycle.

## Principles

- Establish the contract before distributing implementation work.
- Trace normative requirements, not every explanatory sentence as if it were
  an independent requirement.
- Use parallel agents only where work and ownership are genuinely separable.
- Review the plan and implementation independently against the complete
  applicable specification.
- Never change the specification silently to legitimize implementation drift.
- A phase is complete only when product truth and evidence agree.

## 0. Establish the baseline

Before planning, record:

- accepted specification version or source commit;
- roadmap phase or change scope;
- applicable specification files, normative requirements, schemas, examples,
  and acceptance journeys;
- governing decisions and company standards;
- unresolved ambiguities and blockers; and
- evidence required for completion.

Essential ambiguity is a stop condition. Explanatory prose is reviewed for
contradiction; normative requirements and executable contracts receive strict
traceability.

### User-facing behavior

When the change introduces user-facing behavior, the baseline also defines how
it looks and feels, not only what exists:

- where the feature lives, how users reach it, how they notice pending work,
  and how it moves;
- at least three alternatives for a new mental model, each a distinct stance
  (different place, navigation, or attention guidance), with a mockup, what it
  makes easy, what it costs, when it wins, and a reasoned recommendation;
  extending an existing feature needs one alternative with a mockup;
- the chosen alternative phrased as testable *EARS* requirements ("When
  <trigger>, the product shall <response>").

The owner approves the chosen alternative with the baseline; from then on it is
as normative as the functional requirements.

### Phase contract

A roadmap item names a phase's outcome; it is not a contract. Before planning,
the phase produces a contract: the specification changes, schemas, fixtures,
examples, and an interface catalog for everything the phase makes observable,
such as operations, artifacts, options and defaults, result fields, error
codes, supported targets, and the observable check for each effect, including
absence when something is disabled. Where the catalog is data, it is
machine-readable and validated with the specification. Owner decisions the
contract depends on are made here, not during implementation.

The contract is *test-ready* when an author who reads only the contract can
derive every acceptance test without reading code and without inventing an
identifier, option, default, result field, error code, or supported target. A
contract that is not test-ready blocks approval.

## 1. Build requirement, dependency, and risk inventories

Classify applicable requirements by component, public interface, security,
compatibility, persistence, migration, concurrency, failure behavior,
documentation, test level, external dependency, and implementation order.

Produce a traceability matrix that maps every normative requirement to planned
work, expected evidence, and verification method (end-to-end journey, unit or
component test, or visual check). End-to-end journeys cover main paths and
security-critical cases; everything else uses lower test layers. Identify cross-cutting invariants before tasks are
distributed.

## 2. Draft the implementation plan

The plan defines:

- a task dependency graph;
- affected and expected files or components;
- interfaces created or changed;
- tests, fixtures, and validation commands;
- documentation, roadmap, and development-note work;
- security, compatibility, migration, and recovery consequences;
- integration checkpoints and rollback strategy;
- owner and reviewer for every task; and
- requirement IDs addressed by every task.

The plan covers specification conformance work as well as feature code.

## 3. Assign agents and models

Use the parallelism justified by the task graph, ownership boundaries, and
integration cost, within the limits of the
[agent execution budget standard](agent-execution-budget.md). The plan
records:

- independent work packages;
- tasks that must remain sequential;
- exclusive or coordinated file ownership;
- frozen shared interfaces;
- expected deliverables and evidence;
- integration owner; and
- model class chosen for cost, complexity, and risk.

Use cost-efficient models for bounded inventory, mechanical edits, fixtures,
and routine checks. Use deeper reasoning for architecture, security,
migrations, ambiguous failures, synthesis, and conformance review. A single
agent is preferred when tasks depend on one evolving shared mental model.

## 4. Review the plan against the complete baseline

A reviewer other than the primary plan author checks the draft against every
applicable specification file, normative requirement, schema, maintained
example, acceptance journey, decision, and company standard.

The reviewer is a different agent, model, or person than the author and does
not receive the author's reasoning. If the designated reviewer is unavailable,
the gate is blocked and reported. It is never skipped, and the reviewer, model,
or provider is never switched silently; a substitute requires explicit
authorization and is recorded in the cycle record. The designated reviewer
(person or agent identity, and for an agent its model and provider) is
recorded before the review starts; a reviewer proposed by automated model
routing is recorded the same way.

The reviewer also confirms that the phase contract is test-ready.

Each normative requirement is classified:

```text
covered
not applicable, with rationale
blocked by an unresolved decision
requires a specification change
deferred with explicit authority
```

Missing coverage, inconsistent sequencing, overlapping ownership, inadequate
tests, and unjustified exclusions amend the plan before implementation.

## 5. Approve and baseline the revised plan

Record the specification baseline, plan revision, ownership, expected
evidence, accepted exclusions, risks, and integration order. The owner approves
the reviewed phase contract, which is then frozen: its commit or version is
recorded in the cycle record as the contract reference that both tracks in §6
start from. Baselining makes changes visible; it does not prohibit learning.

## 6. Implement in controlled waves

Implementation proceeds in dependency order:

1. shared contracts and foundations;
2. independent components;
3. planned integration checkpoints;
4. affected verification after each wave; and
5. resolution of interface drift before dependent work continues.

For user-facing behavior, acceptance tests and implementation are separated by
an information barrier that lasts until the integration loop below has passed.
The primary session is the integration owner: it starts both tracks, writes
the acceptance-test track's brief from the contract only, and is the only
participant that sees both. It does not implement; the implementation track
is a separate session or sub-agent.

- **Acceptance-test track.** A fresh agent session, with no conversation
  history, works in its own worktree created from the frozen contract and
  commits to a tests-only branch. Its input is the contract, the applicable
  acceptance journeys, and the test harness at the contract commit. It does
  not read implementation branches and receives no implementation reasoning.
  Its tests exercise only public interfaces and name the requirement or
  acceptance ID each test verifies.
- **Implementation track.** Works from the frozen contract and the codebase on
  its own branch, writes its unit and component tests test-first, and does not
  see the acceptance tests, test plan, or test identifiers while the barrier
  lasts.

Both tracks start after the freeze and run in parallel. An implementer who
cannot see the tests optimizes for the contract, not for test structure. The
integration owner then runs the integration loop:

1. Merge both branches onto the phase integration branch (see the
   [Git branching standard](git-branching-and-release-promotion.md#phase-integration-branches))
   and run the acceptance tests. Both tracks keep working on their own
   branches; neither reads the integration branch while the barrier lasts.
2. Classify every failure and record the classification in the cycle record:
   - *implementation defect:* returned to the implementation track as expected
     versus observed behavior in contract terms, never as test source;
   - *test defect:* the test contradicts the contract; returned to the
     acceptance-test track with the test ID, the contract reference, and the
     rationale, never with implementation details;
   - *contract defect:* the contract is ambiguous or wrong; affected work
     stops and §7 applies;
   - *infrastructure failure:* handled under the
     [agent execution budget](agent-execution-budget.md) rerun rule.
3. Repeat until every acceptance test passes without skips. A test changes
   only through the test-defect route and is never weakened to make it pass.

A track that disputes a classification gets at most 2 review rounds; then the
integration owner decides against the contract and records the decision. The
acceptance tests and the implementation merge into the integration branch
together. The barrier covers black-box acceptance tests only.

Every work package reports requirements addressed, files changed, tests run,
deviations, remaining risks, documentation impact, and proposed specification
changes. Implementers do not expand scope without revising the plan.

## 7. Control discoveries and baseline changes

When implementation reveals a specification defect or necessary change, stop
affected work and record a proposed baseline change with rationale and impact
on requirements, plans, tests, security, compatibility, documentation, and
roadmap. Continue only after the change is accepted or rejected through the
project's governing process. An accepted change produces a new frozen contract
reference for both tracks.

An accepted change updates the baseline and plan. Already completed work is
rechecked against affected requirements. Implementation convenience never
silently redefines the contract.

## 8. Verify implementation independently

After integration, an independent reviewer, under the same reviewer rules as
§4, checks the implementation and evidence against the same complete baseline
used for plan review. Summaries are
inputs, not proof. Inspect source, tests, schemas, examples, generated output,
documentation, roadmap, development notes, and applicable standards.

Each normative requirement is classified:

```text
satisfied
partially satisfied
not satisfied
not applicable
unverifiable
specification inconsistency
```

Verification includes negative and failure behavior, not only successful
acceptance paths.

## 9. Close gaps and repeat verification

Every result other than satisfied or accepted non-applicability causes one of:

- implementation correction;
- added or corrected tests and evidence;
- documentation correction;
- controlled specification change;
- authorized roadmap deferral; or
- blocked phase completion.

Repeat affected conformance checks after correction. A gap report without
closure is not completion.

## 10. Complete phase evidence

A phase becomes complete only when:

- implementation is integrated;
- required verification passes without unexplained skips;
- the conformance matrix is accepted;
- specification and executable contracts reflect implemented behavior;
- user documentation describes observed behavior;
- the development note captures decisions, deviations, and validation;
- roadmap status and evidence links are updated;
- changelog and release material are updated where applicable; and
- follow-up work has explicit ownership and location.

## 11. Retrospect and improve

For significant phases, compare planned and actual decomposition, agent/model
cost and effectiveness, integration friction, specification gaps, late defect
detection, and validation value. Feed reusable improvements into company
standards, processkit, project guidance, or model routing.

## Required cycle record

The cycle leaves a reviewable record containing baseline, phase contract and
its frozen reference, plan, task graph, ownership, traceability matrix,
designated reviewers, plan-conformance result, integration-loop failure
classifications, implementation
evidence, implementation-conformance result, accepted baseline changes, gap
closures, and completion approval.

## Agent briefing

> Baseline the specification, turn the roadmap item into a test-ready contract,
> map every normative requirement, plan ownership and evidence, review contract
> and plan independently, and freeze the contract. Then write user-facing
> acceptance tests in a fresh session from the frozen contract only, implement
> in parallel without seeing those tests, and loop until every test passes,
> classifying each failure as implementation, test, contract, or
> infrastructure defect. Verify independently against the same complete
> baseline. No requirement disappears and no specification change is silent.
> Small direct changes update baseline and tests in place.
