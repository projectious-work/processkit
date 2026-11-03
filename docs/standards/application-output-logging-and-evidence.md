# Application output, logging, and evidence standard

## Purpose and scope

This standard separates requested results, operational diagnostics, and
durable domain evidence. It applies to command-line applications, services,
workers, and user-facing applications according to their application profile.

## Three information channels

1. **Application output** communicates the result requested by a person or
   program.
2. **Operational logs** explain runtime decisions, dependencies, and failures.
3. **Domain or run evidence** records durable facts required for recovery,
   audit, reconciliation, or product behavior.

These channels MAY share an internal event model but MUST have distinct
contracts and retention. Rotating operational logs MUST NOT erase authoritative
domain evidence. Logs MUST NOT be presented as authoritative evidence unless a
product contract explicitly promotes them into an evidence store.

## Semantic events and rendering

Applications construct typed or structured semantic events before rendering.
Terminal escape sequences, localized prose, and sink formatting do not belong
in domain event objects.

Structured events SHOULD include where applicable:

- schema or event version;
- timestamp and severity;
- stable event name;
- component and operation;
- correlation, request, run, or trace identifier;
- outcome and error category;
- attributed child or external dependency; and
- redacted structured fields.

The actor identifies the human, service, or agent that performed or attested
the action. It MUST NOT be replaced by the affected subject, task, gate, or
artifact identifier. Delegated actions record both the initiating and
executing identities when that distinction matters to authority or audit.

Human renderers MAY use color, tables, progress, and other decoration. Plain
and machine renderers remain stable and deterministic.

Long-running trusted gates use evidence-first events where practical: task
start, heartbeat, output, pass, warning, skip, failure, and cleanup. An event
is emitted only after its underlying evidence is flushed. Presentation failure
must not rerun candidate work; a deterministic plain renderer remains
available. TUI state, widget state, and clipboard contents are never evidence.

Progress has a stable denominator and explicit pending, running, passed,
warning, skipped, and failed states. Security-relevant layouts are tested for
one visible frame per panel, absent empty containers, correct heading
association, and equivalent narrow/wide semantic structure.

## Streams and formats

CLI applications write requested results to stdout and diagnostics to stderr.
Machine-readable output MUST contain only the declared envelope on stdout.
Non-interactive execution selects plain output unless explicitly overridden.
Color control respects `NO_COLOR` and project-specific settings.

Applications document supported log sinks, formats, levels, rotation,
retention, and failure behavior. Enabling a sink that can disclose data or
perform network egress requires an authorized configuration source.

## Redaction and data handling

Redaction occurs before events reach any renderer, buffer, file, telemetry
exporter, or test artifact. It covers credentials, secret-shaped values,
personal data, sensitive paths, and product-specific protected fields.
Chunked and concurrent output MUST not bypass redaction at boundaries.

Raw modes are exceptional. They require explicit invocation, document their
risk, and MUST NOT imply that known secrets are safe to print.

## Failure and correlation

Logs and evidence distinguish refusal, dependency failure, timeout,
cancellation, partial success, and complete success. Child-process or remote
events retain source attribution. Concurrent events carry correlation data and
must not be reordered into a false lifecycle narrative.

Immutable validation evidence and mutable publication journals have separate
contracts. Manifest-covered files stop changing before their digests are
finalized; later publication commands and results cannot mutate that manifest.

## Evidence integrity

A gate or milestone pass records enough structured evidence to reproduce or
independently assess the claim. Where applicable this includes the exact
subject or candidate, validator and version, invocation or evaluation profile,
actor, occurrence time, outcome, warnings or exceptions, and a stable evidence
locator or digest. A bare success sentence, HTTP status, or release URL is
useful context but is not sufficient proof when stronger machine-verifiable
evidence exists.

Evidence references remain resolvable outside the producer's workspace.
Producer-local absolute paths MAY appear as diagnostic metadata but MUST NOT be
the sole locator for an audit record, release artifact, or gate result.

## Testing

Tests separately assert output, diagnostics, structured logs, evidence,
redaction, exit or outcome status, rotation, concurrency, and sink failure.
Golden output is reviewed as a product contract; volatile values are
normalized deliberately rather than ignored broadly.

## Agent briefing

> Output answers the request, logs explain operation, and evidence records
> durable truth. Do not collapse these channels. Structure and redact events
> before rendering or export.
