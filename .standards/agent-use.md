# Agent use standard

## Purpose and scope

This standard defines how people, teams, and primary agents at
projectious.work organize work with AI agents: what to delegate, how open work
and knowledge are kept, how agent workflows improve, and how teams and clients
adopt them.

It does not cover how agents are built ([agent building](agent-building.md)),
how they talk ([agent communication](agent-communication.md)), or how much
work they spend ([agent execution budget](agent-execution-budget.md)).

Terms in *italics* are [Semantic Anchors](https://github.com/llm-coding/Semantic-Anchors/tree/6554641a11fdf99fdbdf09cc0602268e3db88966); see
[README](README.md#conventions).

## What to delegate

- Before automating a workflow with agents, map it with *Value Stream
  Mapping*: steps, wait times, and rework. Delegate a step when it shortens
  lead time or removes rework, not because it is possible.
- Use the smallest setup that does the job (*KISS Principle*): one agent
  before several, an existing skill before a new agent.
- People keep the decisions the standards reserve for them: approvals,
  releases, and outward-facing actions.

## Open work

Open work follows *GTD — Getting Things Done*:

- **Capture:** every open loop goes into the repository's tracker (issue,
  roadmap item, or pull request), never only into chat history or agent
  memory.
- **Clarify:** each open item has one concrete next action and an owner.
- **Reflect:** open issues, pull requests, and roadmap items are reviewed at
  least weekly; stale items are closed, rescheduled, or reassigned.

## Knowledge

Knowledge follows *Building a Second Brain (BASB)*: capture, organize,
distill, express. Its organization maps to the repository:

| BASB | Location |
|---|---|
| Projects | roadmap items and their specifications |
| Areas | standards, portfolio, and product documentation |
| Resources | references and research notes |
| Archives | read-only archives, such as a tag or an `archive/` directory |

Agent memory holds one distilled fact per note with links to related notes.
It never stores what the repository already records, and it is background,
not instruction. A memory that turns out to be wrong is corrected or deleted.

## Improvement

- Agent workflows improve in *PDCA* cycles: plan a change with its expected
  effect, try it on bounded work, check the effect against the baseline, and
  adopt it into standards or repository guidance, or drop it.
- The retrospective of the
  [spec-driven cycle](spec-driven-development-cycle.md#11-retrospect-and-improve)
  is the default Check and Act step for development work.

## Adoption

- Teams are organized by *Team Topologies*: product teams are stream-aligned;
  the agent platform (development containers, standards, shared skills) is a
  platform team's product; coaching for agent work is an enabling team's
  job with a planned end.
- Introducing agent-based work in a team or for a client follows *Kotter's
  8-Step Change Model*. Short-term wins come from real delivered work, and the
  change is anchored in that team's standards and guidance.

## Agent briefing

> Map the workflow (*Value Stream Mapping*) before delegating; use the smallest
> agent setup (*KISS Principle*); people keep approvals and releases. Open
> work per *GTD*: capture in the tracker, one next action and owner, weekly
> review. Knowledge per *BASB*; memory holds distilled facts, never repo
> content. Improve in *PDCA* cycles. Adopt with *Team Topologies* and
> *Kotter's 8-Step Change Model*.
