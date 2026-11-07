# Software architecture and code design standard

## Purpose and scope

This standard defines the default structure of projectious.work software:
how boundaries, modules, and code are shaped, and how architecture is
documented. It applies to applications with domain logic and external
integrations — CLIs, services, workers, and MCP servers. Libraries apply the
inner rules and leave composition to their host.

Terms in *italics* are
[Semantic Anchors](https://github.com/llm-coding/Semantic-Anchors/tree/ccb05b6bd41a663eaf2595e707d98f35d743e61f)
(commit `ccb05b6b`, 2026-10-26; adopting a later revision is a standards
change): their
established meaning applies; deviations are stated inline.

## Principles

- The core does not know its delivery mechanism or infrastructure.
- Each architectural frame has one job; frames are not mixed into vague
  hybrids.
- Module boundaries are as deliberate as service boundaries.
- Architecture documentation records what a reader cannot recover from the
  code, especially decisions and their reasons.

## Boundaries: Hexagonal Architecture

*Hexagonal Architecture* governs the system boundary:

- Domain and application form the core. Public functionality lives there.
- The core defines ports (interfaces) for everything external: CLI and MCP
  entry points, filesystems, processes, container engines, Git, network
  services, model providers, clocks, and randomness.
- Adapters implement ports. Dependencies point inward only; the core never
  imports an adapter.
- A composition root at the edge (the program's `main`, server bootstrap, or
  test harness) wires adapters to ports.

## Inside the core: Clean Architecture

*Clean Architecture* governs the inside of the core: business rules live in
entities and use cases; frameworks, databases, transport, and serialization
are details behind interfaces.

## Modules

- Cut the core along bounded contexts (*Domain-Driven Design (Evans)*,
  tactical patterns). Use one Ubiquitous Language: the same terms in
  specification, code, tests, CLI output, and documentation.
- Modules are feature-centric and own their data and state. They communicate
  only through explicit module APIs and never reach into another module's
  internal types, tables, or files.
- Module and package dependencies are acyclic.

## Code conventions

- The repository's formatter and linter configuration is authoritative. Code
  that does not pass them is not finished. A repository without a linter
  configuration enforces the language's standard formatter and static checks
  (for example `gofmt` and `go vet`) in its verification scripts; adopting a
  linter commits its configuration and names the tool in the project
  specification.
- Language idioms: *Effective Go* for Go, *Effective Python* for Python, the
  Rust API Guidelines for Rust. The repository's configuration wins over the
  idiom source where they differ.
- *SOLID* applies at type and module level. Functions keep a *Single Level of
  Abstraction Principle*: a use case reads as calls to ports and domain
  operations; details move into named functions.

## Testing consequences

The core is tested through its ports with in-memory fakes; adapters receive
their own integration tests against the real dependency. The test style
follows the
[software verification standard](software-verification-and-release-engineering.md)
(*TDD, Chicago School*).

## Architecture documentation

- Structure per *arc42*. Fill only sections that carry information; at
  minimum context and scope (§3), building blocks (§5), crosscutting concepts
  (§8), architecture decisions (§9), and risks and technical debt (§11).
- Diagrams per *C4-Diagrams*: context and container views for every product,
  component views where a container's structure is not obvious.
- Architecture decisions as *ADR according to Nygard* (context, decision,
  consequences), stored next to the code or in the project's decision store.
  Superseded decisions are marked, never deleted.
- Before removing a boundary, check, or rule whose purpose is unclear, find
  the reason it exists (*Chesterton's Fence*), usually in an ADR.

## Agent briefing

> Keep the core free of infrastructure: ports in the core, adapters at the
> edge, dependencies inward (*Hexagonal Architecture*); business rules in
> entities and use cases (*Clean Architecture*); feature modules own their
> data and talk only through module APIs. The repository's formatter and
> linter decide style. Document with *arc42*, *C4-Diagrams*, and *ADR
> according to Nygard*.
