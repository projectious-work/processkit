---
name: standard-application-engineering
description: Company application engineering standards: application profiles, layered configuration, output/logging/evidence channels, and compatibility of machine interfaces. Use when building or changing a CLI, service, worker, or MCP server's configuration, output, logs, JSON results, schemas, or public contracts, or when deciding which standards apply to a product.
---

# standard-application-engineering

Binding company standard. The rules below are the summary; the linked file is authoritative. Read only the section the task needs.

## Application profiles for engineering standards

Select standards by product behavior, not implementation language. Declare
every applicable profile, combine their requirements, and make exceptions
explicit and reviewable.

Full standard: `docs/standards/application-profiles.md`. Sections:

- Purpose
- Profiles
- Conditional overlays
- Composite products
- Applicability record

## Application configuration standard

Configuration precedence answers which source wins; authority answers
whether that source may set the key at all. Preserve both, expose redacted
provenance, and never use committed project configuration as an implicit
privilege escalation path.

Full standard: `docs/standards/application-configuration.md`. Sections:

- Purpose and scope
- Precedence
- Authority is separate from precedence
- File and value behavior
- Effective configuration and provenance
- Testing

## Application output, logging, and evidence standard

Output answers the request, logs explain operation, and evidence records
durable truth. Do not collapse these channels. Structure and redact events
before rendering or export.

Full standard: `docs/standards/application-output-logging-and-evidence.md`. Sections:

- Purpose and scope
- Three information channels
- Semantic events and rendering
- Streams and formats
- Redaction and data handling
- Failure and correlation
- Evidence integrity
- Testing

## Compatibility and machine-interface standard

Treat public and persisted machine interfaces as products. Version their
meaning, keep human rendering separate, prove rejection behavior, and never
call a change compatible based only on syntactic schema compatibility.

Full standard: `docs/standards/compatibility-and-machine-interfaces.md`. Sections:

- Purpose and scope
- Versioning
- Machine-readable results
- CLI profile
- Change classification
- Contract verification
