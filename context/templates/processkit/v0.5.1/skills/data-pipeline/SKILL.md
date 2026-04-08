---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-data-pipeline
  name: data-pipeline
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Data pipeline patterns — ETL/ELT, batch vs streaming, idempotency, orchestration."
  category: data
  layer: null
  when_to_use: "Use when designing a data pipeline, choosing between batch and streaming, implementing ingestion or transformation, setting up orchestration, or debugging pipeline failures."
---

# Data Pipeline

## Level 1 — Intro

A reliable data pipeline is idempotent, observable, and stage-validated.
Default to ELT into a modern warehouse, default to batch over streaming,
and design every step to be safely re-runnable from day one.

## Level 2 — Overview

### ETL vs ELT

ETL (Extract, Transform, Load) transforms before loading; use it when the
target has limited compute or PII must be filtered before storage. ELT
(Extract, Load, Transform) loads raw data first and transforms in the
warehouse; prefer it for analytics on BigQuery, Snowflake, or Redshift
because it preserves raw data and allows re-transformation. Never split
transformation logic between pipeline and warehouse without documenting
which side owns the source of truth.

### Batch vs streaming

Start with batch unless there is an explicit real-time requirement. Batch
is simpler to build, debug, and retry. Streaming is required for
real-time dashboards, alerting, and event-driven systems but adds
ordering, late-arrival, and exactly-once complexity. Micro-batch (Spark
Structured Streaming, 1–5 minute intervals) bridges the gap when full
streaming is overkill.

### Idempotency

Every step must be safely re-runnable without duplicating data. Use
upserts (`INSERT ON CONFLICT UPDATE`) or merge statements for loading.
Partition output by date or run id and overwrite entire partitions on
rerun. Include a deduplication step that hashes natural-key columns
before loading. Running a job twice should produce the same result as
running it once.

### Data quality at every stage

Validate after extraction, after transformation, and after loading.
Compare source and destination row counts within tolerance. Check for
nulls in required columns and duplicates in unique keys. Validate value
ranges (dates in expected window, amounts non-negative). Fail fast on
violations rather than propagating bad data downstream, and log row
counts, null rates, and duplicate rates for every run.

### Orchestration

Use a workflow orchestrator (Airflow, Prefect, Dagster) for scheduling
and dependency management. Define DAGs with explicit task dependencies,
configure retries with exponential backoff (3 retries at 1/5/15 minute
delays), and prefer sensors or triggers over polling. Tag tasks with
owners and SLA expectations. Keep task definitions thin — business
logic lives in importable modules so it can be unit-tested.

## Level 3 — Full reference

### Schema management

Use a schema registry (Avro, Protobuf, JSON Schema) for event-driven
pipelines. Enforce backward compatibility: new fields are optional,
existing fields are never removed or renamed. Version schemas
explicitly (`v1`, `v2`) with documented migration paths. Document each
field with name, type, description, example value, and nullability.
Test schema changes against consumers before deploying to production.

### Backfill strategies

Design pipelines to accept a date-range parameter from the start. Use
partition overwrite for backfills: reprocess and replace entire
partitions rather than mutating in place. Run backfills at lower
priority so they do not starve production workloads. Test on a small
date range before scaling up, and track which partitions have been
reprocessed.

### Monitoring and dead letter queues

Alert on pipeline failure, SLA breach, and unexpected row-count
changes (> 20% deviation). Log start time, end time, rows processed,
and rows rejected. Use dead letter queues for records that fail
processing — DLQ entries must include the original payload, error
message, timestamp, and source topic or table. Review and reprocess
DLQ records regularly; they represent data loss until resolved.

### Worked examples

- **Daily sales API to warehouse:** ELT in three stages — extract
  (paginated API call, raw JSON to cloud storage), load (bulk insert
  into a staging table), transform (SQL in the warehouse to clean,
  deduplicate, and join with dimensions). Date-range parameter for
  backfills, partition-overwrite loads, source/staging row-count
  checks, Airflow DAG with retries.
- **Duplicate records:** Diagnose the idempotency gap — insert-only
  load is the usual culprit. Add a natural-key hash column,
  switch to `INSERT ON CONFLICT`, add a pre-load dedupe step, and
  add a quality check comparing distinct key counts source vs target.
- **Streaming vs batch for events:** If events only feed daily
  reports, recommend batch with hourly micro-batches. If real-time
  alerting is needed, recommend Kafka-based streaming but warn about
  exactly-once complexity. Either way, design for idempotency and
  include a DLQ for malformed events.

### Anti-patterns

- Insert-only loads with no dedupe — guaranteed duplicates on retry
- Transformation logic split across pipeline and warehouse with no
  documented owner
- Streaming chosen for "future-proofing" without a real-time use case
- Quality checks only at the end of the pipeline (bad data has
  already propagated)
- DAGs that hide business logic inside task callables, making them
  untestable in isolation
