---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-ml-pipeline
  name: ml-pipeline
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "ML pipeline design — data versioning, experiment tracking, deployment patterns, drift monitoring."
  category: ai
  layer: null
  when_to_use: "Use when building an ML pipeline from data to deployment, setting up MLOps tooling (DVC, MLflow, model registry), choosing deployment patterns (shadow, canary, A/B), or designing monitoring for drift and degradation."
---

# ML Pipeline Design

## Level 1 — Intro

A production ML pipeline runs from raw data to a monitored model in
production. The non-negotiable property is reproducibility: given
the same data version, feature config, and hyperparameters, you get
the same model. Without that, debugging is impossible six months
later.

## Level 2 — Overview

### Pipeline stages

```
Data collection -> Data versioning -> Feature engineering -> Training
    -> Evaluation -> Model registry -> Deployment -> Monitoring
```

Every stage has to be reproducible and every artifact has to be
traceable back to its inputs. See `references/pipeline-stages.md`
for stage-by-stage tools, best practices, and pitfalls.

### Data versioning

Track datasets like code. Every training run must reference an
exact data version.

- **DVC** — Git-like versioning for large files; metadata in Git,
  data in S3/GCS. `dvc push/pull` mirrors `git push/pull`.
- **Delta Lake / lakehouse** — versioned tables with time travel,
  good for structured data at scale.
- **Simple approach** — immutable datasets in object storage with a
  naming convention (`s3://data/training/v42/`). Never overwrite,
  always create new versions.

Minimum bar: every training run logs the exact dataset version,
data transformations are versioned code (not manual notebook
steps), and raw data is immutable.

### Feature engineering and feature stores

Compute features once, reuse across training and serving.

- **Feature store** (Feast, Tecton, Hopsworks) — centralized
  repository with consistent online (low-latency) and offline
  (batch) access.
- **Use one when** multiple models share features, training-serving
  skew is a problem, or features need complex transformations.
- **Skip it when** you have one model, simple inline features, and
  a small team.

Always: version feature definitions with model code, unit-test
feature pipelines (input X -> expected features Y), monitor feature
distributions in production.

### Experiment tracking

Record every run with config, metrics, and artifacts.

- **MLflow** — open source, self-host or managed, model registry
  built in.
- **Weights & Biases** — best UX, rich visualization, individual
  practitioners.
- **Neptune** — strong collaboration features for teams.

Per-run minimum log: git commit, dataset version, all
hyperparameters, train and validation metrics per epoch, final
test-set metrics, model artifact, environment (Python and package
versions).

### Model registry

A central catalog of trained models with metadata, versioning, and
lifecycle. Tag stages: `development`, `staging`, `production`,
`archived`. Store a model card per model: description, training
data, metrics, limitations, bias assessment. One model in
`production` per model name; promotion requires an automated quality
gate or human approval.

Tools: MLflow Model Registry, Vertex AI Model Registry, SageMaker
Model Registry, or a database + S3 references for small projects.

### Deployment patterns

| Pattern | Description | Use when |
|---|---|---|
| Shadow | New model runs alongside old, results compared but not served | Validating with real traffic, no user impact |
| Canary | New model serves 5–10% of traffic, ramping up | Limiting blast radius |
| A/B test | Two models serve different segments, measure business metrics | Comparing on real outcomes |
| Blue-green | Two identical environments, switch traffic at once | Need instant rollback |
| Feature flag | Model version gated by flag system | Gradual rollout, easy kill switch |

Default: shadow first to validate, canary rollout with automated
rollback on metric degradation.

Serving infrastructure:

- **Batch inference** — scheduled job (Airflow, cron); simplest;
  use when latency tolerance is hours.
- **Online inference (API)** — REST/gRPC endpoint; use for
  real-time. Frameworks: TorchServe, TF Serving, Triton, BentoML, or
  a FastAPI wrapper.
- **Embedded** — model shipped with the application (edge, mobile);
  use ONNX or TFLite for portability.

### Monitoring and drift

Production models degrade. Monitor proactively across three axes:

- **Data drift** — input feature distributions shift. KS test, PSI
  (Population Stability Index), Jensen-Shannon divergence. Alert
  past threshold.
- **Concept drift** — relationship between features and target
  changes. Watch prediction distribution; track business metrics
  alongside model metrics; compare predictions against delayed
  ground-truth labels when possible.
- **Operational** — latency p50/p99, error rate, input-validation
  failures, GPU/memory utilization.

Retraining triggers: scheduled (weekly/monthly), drift-based
(threshold breached), or performance-based (metric degraded).

### CI/CD for ML

ML CI/CD extends software CI/CD with data and model validation.

**On every code change (CI):** unit tests for feature engineering
and transformations, smoke training on a small data subset, lint
and code quality.

**On model promotion (CD):** full evaluation on the held-out test
set, comparison against current production, bias and fairness
checks, shadow deployment for N hours, automated canary rollout
with rollback triggers.

Tools: GitHub Actions + DVC + MLflow, or managed platforms like
Vertex AI Pipelines, SageMaker Pipelines, Kubeflow.

## Level 3 — Full reference

### Pipeline orchestration tools

| Tool | Type | Best for |
|---|---|---|
| Apache Airflow | General DAG orchestration | Complex workflows, many integrations |
| Kubeflow Pipelines | K8s-native ML pipelines | Teams already on Kubernetes |
| Vertex AI Pipelines | Managed (GCP) | GCP-native teams, minimal ops |
| SageMaker Pipelines | Managed (AWS) | AWS-native teams, minimal ops |
| Prefect / Dagster | Modern Python orchestration | Python-first teams, better DX than Airflow |
| ZenML | ML-specific orchestration | Teams wanting an ML pipeline abstraction |

### Stage-by-stage gotchas

- **Ingestion** — silently dropping malformed records is a bug;
  always count and log rejects. Upstream schemas change without
  notice; pin and validate.
- **Versioning** — overwriting datasets in place ("just re-run the
  ETL") destroys lineage. Versioning only the final dataset and not
  intermediates makes debugging impossible.
- **Feature engineering** — training-serving skew is the canonical
  failure: features computed differently offline and online. Use
  shared transformation code or a feature store.
- **Training** — tuning hyperparameters on the test set is data
  leakage. Use train/val/test or nested cross-validation.
- **Evaluation** — a single aggregate metric hides subgroup
  failures. Always compare against current production, not just a
  random baseline.
- **Registry** — no model card means no one remembers what data or
  metrics applied. Make the model card a required field.
- **Deployment** — going to 100% traffic without shadow or canary
  is the most common production incident.
- **Monitoring** — monitoring only operational metrics (latency,
  errors) without model quality metrics is a silent failure.

For full per-stage tool lists and best practices, see
`references/pipeline-stages.md`.

### Anti-patterns

- **Notebook in production.** Convert to a parameterized script
  with config files.
- **Hardcoded paths and credentials.** Use config + secret managers.
- **Models stored on someone's laptop.** Use a registry from day
  one — even a database row pointing at S3 is fine.
- **No rollback plan.** If the new model is bad, how do you revert?
  Answer this before the first deploy.
- **Retraining too often.** Expensive and unstable.
- **Retraining too rarely.** Stale model quietly degrades.

### Worked scenarios

**Greenfield ML project.** Scaffold `data/`, `features/`,
`models/`, `notebooks/`, `tests/`. Initialize DVC. Set up MLflow
locally. Write a training script that logs all params and metrics.
CI: lint, unit tests, train on a sample. Makefile with `train`,
`evaluate`, `serve`.

**Recommendation CTR dropped 15% this week.** Check the data drift
dashboard first — did input features shift? Check upstream pipeline
health. Compare recent feature distributions to training data via
PSI. If drift is found, trace to root cause (new user segment, data
bug, seasonality). If no drift, check concept drift on recent
labeled data. Recommend retraining if confirmed.

**Designing a safe deployment for a new model.** Set up the
registry with staging and production stages. Shadow deploy first:
route real traffic to both old and new for 48 hours, compare
outputs. If acceptable, canary 5% with automated rollback if error
rate increases by >2%. Ramp to 100% over a week. Drift monitoring
on day one.
