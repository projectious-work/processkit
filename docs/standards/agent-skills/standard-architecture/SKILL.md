---
name: standard-architecture
description: Company software architecture, code design, and refactoring standards. Use when designing module boundaries, ports and adapters, use cases, writing architecture docs (arc42, C4, ADR), splitting large files, extracting libraries, or doing any refactoring larger than a rename.
---

# standard-architecture

Binding company standard. The rules below are the summary; the linked file is authoritative. Read only the section the task needs.

## Software architecture and code design standard

Keep the core free of infrastructure: ports in the core, adapters at the
edge, dependencies inward (*Hexagonal Architecture*); business rules in
entities and use cases (*Clean Architecture*); feature modules own their
data and talk only through module APIs. The repository's formatter and
linter decide style. Document with *arc42*, *C4-Diagrams*, and *ADR
according to Nygard*.

Full standard: `docs/standards/software-architecture-and-code-design.md`. Sections:

- Purpose and scope
- Principles
- Boundaries: Hexagonal Architecture
- Inside the core: Clean Architecture
- Modules
- Code conventions
- Testing consequences
- Architecture documentation

## Refactoring standard

Name the smells, secure behavior with characterization tests, refactor in
small catalog steps with green tests at every commit, use the *Mikado
Method* for large changes, and keep behavior changes out of `refactor:`
commits.

Full standard: `docs/standards/refactoring.md`. Sections:

- Purpose and scope
- Principles
- Procedure
- Commits and review
