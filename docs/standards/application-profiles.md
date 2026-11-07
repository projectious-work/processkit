# Application profiles for engineering standards

## Purpose

Company standards describe outcomes that span several kinds of software. This
document defines applicability profiles so a CLI convention is not imposed on
a library, and a service requirement is not imposed on a documentation-only
repository.

A repository declares one primary profile and any secondary profiles in its
engineering documentation. It records justified exceptions rather than
silently ignoring an applicable requirement.

## Profiles

### CLI application

Applies configuration precedence, stdout/stderr separation, terminal and
machine rendering, exit codes, signal handling, cross-platform distribution,
and black-box command tests.

### Service or worker

Applies API/protocol compatibility, structured logs, correlation and tracing,
health and readiness, cancellation, graceful shutdown, deployment
configuration, data retention, and service-level integration tests.

### User-interface application

Applies accessible interaction, local and remote state boundaries, privacy,
error recovery, visual regression where valuable, API compatibility, and
user-journey tests. CLI-only stream and exit-code rules do not apply unless the
project also ships a CLI.

### Library or SDK

Applies API compatibility, dependency discipline, supported runtime versions,
examples as contracts, unit/property tests, and package publication. It
normally delegates logging and configuration policy to the host application.

### Schema, protocol, or process package

Applies independent contract versioning, metaschema validation, positive and
negative fixtures, compatibility and migration, generated-reference drift,
and consumer conformance tests.

### Infrastructure or template product

Applies declarative-contract validation, provider/tool compatibility,
credential isolation, plan/review/rollback or teardown evidence, disposable
end-to-end acceptance, and cost/cleanup controls.

### Documentation or website

Applies local reproducible builds, links, accessibility, generated-content
drift, public metadata, and content/release consistency. Runtime configuration
and application logging rules are normally not applicable.

## Conditional overlays

### Host-gated release

Applies when native-host, container-engine, signing, or publication authority
is intentionally unavailable in the development environment. It activates the
[human-controlled host-phase execution standard](human-controlled-host-phase-execution.md),
including the portable producer/verifier handover, lifecycle separation,
schema-versioned validation manifest, credential-free validation, bounded
publisher, capability adapters, and conformance cases.

The overlay is selected because of authority and trust boundaries, not because
of implementation language or a particular container product. Projects record
the host-only properties being proven and any reviewed non-applicable cases.

## Composite products

A product MAY declare several profiles. Requirements combine; one profile does
not weaken another. The repository documents component boundaries so reviewers
can identify which profile governs each artifact.

## Applicability record

The project records:

- selected profiles and components;
- supported platforms and distribution surfaces;
- applicable verification and release gates;
- stronger project-specific requirements; and
- non-applicable or deferred company requirements with rationale.

Profile selection is reviewed when the product boundary or distribution model
changes.

## Agent briefing

> Select standards by product behavior, not implementation language. Declare
> every applicable profile, combine their requirements, and make exceptions
> explicit and reviewable.
