---
name: dockerfile-review
description: |
  Dockerfile best practices — layer optimization, caching, security, image size. Use when writing, reviewing, or optimizing Dockerfiles, investigating bloated images, or fixing cache-busting build orders.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-dockerfile-review
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: infrastructure
---

# Dockerfile Review

## Intro

A good Dockerfile is small, cache-friendly, reproducible, and does not
run as root. Most problems come from three mistakes: ordering layers
wrong (busting the cache), forgetting to clean up package manager
state, and using `ADD` when `COPY` is what you meant.

## Overview

### Layer optimization

Every instruction creates a layer; layers are cached in order. Order
instructions from least to most frequently changing so the cache stays
warm. Combine related `RUN` commands with `&&` to collapse layers.
Keep a `.dockerignore` file so build context does not balloon with
`node_modules`, `.git`, and local caches.

### Caching dependencies

Copy dependency manifests and install **before** copying source code.
If the manifests haven't changed, the install layer is reused:

```dockerfile
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
```

Pin dependency versions so builds are reproducible. Unpinned
dependencies produce "works in CI, fails in prod" surprises.

### Security

- Don't run as root. Create a non-root user and `USER` into it after
  setup.
- Never `COPY` secrets into an image. Use BuildKit build secrets or
  inject via runtime environment variables.
- Pin base images by digest for supply-chain integrity:
  `FROM python:3.12-slim@sha256:...`.
- Remove package manager caches after installing
  (`rm -rf /var/lib/apt/lists/*`).

### Size reduction

- Start from slim or alpine base images where the ecosystem supports
  it.
- Use multi-stage builds for compiled languages — the final stage
  should not contain the compiler.
- Remove build tools after compilation.
- Use `--no-install-recommends` with `apt-get`.

### Correctness

- Prefer `COPY` over `ADD` — `ADD` has magic behavior (URL fetch,
  auto-extraction) that usually surprises you.
- Set `WORKDIR` instead of `cd` in `RUN` commands.
- Use the exec form of `CMD` and `ENTRYPOINT`:
  `["executable", "arg"]`, not the shell form.

## Full reference

### Canonical Python Dockerfile

```dockerfile
# syntax=docker/dockerfile:1.7
FROM python:3.12-slim@sha256:... AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim@sha256:...
RUN useradd --create-home --uid 1000 app
WORKDIR /app
COPY --from=builder /install /usr/local
COPY --chown=app:app . .
USER app
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1
ENTRYPOINT ["python", "-m", "myapp"]
```

Notable choices: multi-stage build so pip's build deps are not in the
final image, explicit non-root user, `COPY --chown` so we don't need
a later `chown`, exec-form entrypoint, environment variables set via
`ENV` rather than inside the command.

### Canonical apt cleanup

```dockerfile
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
 && rm -rf /var/lib/apt/lists/*
```

Always combine `update`, `install`, and cleanup into one `RUN`. A
separate `RUN rm -rf /var/lib/apt/lists/*` does nothing for image size
because the previous layer already committed those files.

### Multi-stage build for Go

```dockerfile
FROM golang:1.22-alpine AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 go build -o /out/app ./cmd/app

FROM gcr.io/distroless/static-debian12
COPY --from=builder /out/app /app
USER nonroot:nonroot
ENTRYPOINT ["/app"]
```

### Anti-patterns

- **`COPY . .` before installing dependencies** — every source change
  busts the install cache
- **Running as root in production** — add a user and `USER` into it
- **`ADD` with a local path** — use `COPY`; reserve `ADD` for URL
  fetches and tar auto-extraction
- **`latest` base image tags** — pin to a specific version, ideally by
  digest
- **Shell-form `CMD` / `ENTRYPOINT`** — breaks signal handling; use
  the exec form
- **`apt-get install` without `--no-install-recommends`** — pulls in
  tons of suggested packages
- **Secrets via `ARG` or `ENV`** — they persist in image history; use
  BuildKit secrets (`--mount=type=secret`) instead
- **Missing `.dockerignore`** — sends `.git`, `node_modules`, and
  everything else to the daemon as build context

### Review checklist

- Is the base image pinned (ideally by digest)?
- Are dependencies installed before source is copied?
- Is `.dockerignore` present and sensible?
- Does the final stage run as non-root?
- Are package manager caches removed in the same `RUN`?
- Is `ENTRYPOINT` / `CMD` in exec form?
- Are compile-time deps excluded from the final stage?
- Is there any `latest`, any bare `ADD`, any secret in `ARG`/`ENV`?
