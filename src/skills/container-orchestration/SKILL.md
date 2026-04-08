---
name: container-orchestration
description: |
  Docker Compose patterns for multi-service apps — health checks, networking, volumes, dependencies. Use when writing or editing docker-compose files, designing multi-service architectures, debugging container networking, or managing volumes and service dependencies.
metadata:
  processkit:
    apiVersion: processkit.projectious.work/v1
    id: SKILL-container-orchestration
    version: "1.1.0"
    created: 2026-04-06T00:00:00Z
    category: infrastructure
---

# Container Orchestration

## Intro

Docker Compose stitches multiple containers into a single declarative
stack: services, networks, and volumes described in one YAML file. Get
health checks, dependency conditions, and named volumes right and
everything else follows.

## Overview

### Compose file structure

Define services, networks, and volumes at the top level. Prefer named
volumes for persistent data and explicit networks for inter-service
communication:

```yaml
services:
  app:
    build: .
    networks:
      - backend
    volumes:
      - app-data:/data

networks:
  backend:

volumes:
  app-data:
```

### Build vs image

Use `build` for services you develop and `image` for third-party
services. Combine both to tag locally built images:

```yaml
services:
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
      args:
        PYTHON_VERSION: "3.12"
    image: myproject/api:dev
  redis:
    image: redis:7-alpine
```

### Health checks and dependencies

Always define health checks on services that other services depend on.
Without them, `depends_on` only waits for the container to start — not
for the service inside to be ready:

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 5s
      timeout: 3s
      retries: 5
      start_period: 10s
  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
```

### Networking

Compose creates a default network per project. Use custom networks to
isolate traffic:

```yaml
services:
  web:
    networks: [frontend, backend]
  api:
    networks: [backend]
  db:
    networks: [backend]

networks:
  frontend:
  backend:
```

Services resolve each other by service name. Only expose ports to the
host when necessary — inter-service traffic uses the container port
directly. Use `expose` for documentation, `ports` for host binding.

### Volume strategies

- **Named volumes** — persistent data managed by Docker; survives
  `docker compose down`
- **Bind mounts** — map host paths for development (live reload)
- **tmpfs** — in-memory; for sensitive data or caches

```yaml
volumes:
  - pg-data:/var/lib/postgresql/data    # named volume
  - ./src:/app/src                       # bind mount
  - type: tmpfs
    target: /tmp
```

`docker compose down -v` removes named volumes (destructive). Back up
volume data with a one-off `docker run` using a bind mount.

### Environment management

Use `.env` files for defaults and override per environment:

```yaml
services:
  app:
    env_file:
      - .env
      - .env.local    # overrides, git-ignored
    environment:
      - NODE_ENV=production   # explicit override
```

Never put secrets directly in `docker-compose.yml`. Use `env_file` with
git-ignored files or Docker secrets in swarm mode.

### Profiles

Use profiles to make services optional:

```yaml
services:
  app:
    build: .
  mailhog:
    image: mailhog/mailhog
    profiles: [debug]
```

Start with `docker compose --profile debug up` to include debug
services. Services without a profile always start.

## Full reference

### Common commands

```bash
docker compose up -d              # start all services detached
docker compose up -d --build      # rebuild images before starting
docker compose ps                 # list running services
docker compose logs -f app        # follow logs for a service
docker compose exec app sh        # shell into running container
docker compose down               # stop and remove containers/networks
docker compose down -v            # also remove volumes (destructive)
docker compose config             # validate and display resolved config
```

### Debugging workflow: service cannot reach the database

```bash
# 1. Check both services are on the same network
docker compose ps
docker network inspect $(docker compose config --format json | jq -r '.networks | keys[0]')
# 2. Verify the db is healthy
docker compose exec db pg_isready -U postgres
# 3. Test connectivity from the app container
docker compose exec app ping db
docker compose exec app nc -zv db 5432
# 4. Check environment variables
docker compose exec app env | grep DB
```

### Adding a service with zero-downtime restart

```bash
# 1. Add the service to docker-compose.yml
# 2. Validate the config
docker compose config --quiet
# 3. Start only the new service
docker compose up -d new-service
# 4. Verify health
docker compose ps new-service
docker compose logs new-service
```

### One-off commands in a service context

```bash
# Database migration
docker compose run --rm app python manage.py migrate
# Interactive database shell
docker compose exec db psql -U postgres
# Run tests with the full service stack
docker compose run --rm app pytest
```

### Reference architectures

The complete YAML examples live in `references/compose-patterns.md`.
The key patterns, in increasing complexity:

- **Web + database** — the baseline production stack: app service with
  health-checked postgres, named volume for data, `restart:
  unless-stopped` on both. Always wire `depends_on` with
  `condition: service_healthy`.
- **Web + database + cache** — add redis with `--appendonly yes` and
  an `allkeys-lru` memory cap. The web service waits on both
  dependencies.
- **Worker queue** — web enqueues jobs, celery workers process them via
  RabbitMQ. Scale workers with `deploy.replicas`. Both web and worker
  depend on the broker AND the database being healthy.
- **Reverse proxy** — nginx or Traefik in front of application services
  for TLS termination, load balancing, and static assets. Proxy lives
  on the `frontend` network; app straddles `frontend` and `backend`;
  db is `backend`-only.

### Anti-patterns

- **`depends_on` without health checks** — the dependent service will
  race its dependency
- **Hardcoded secrets in `docker-compose.yml`** — use `env_file` with a
  git-ignored local file
- **`latest` tags for third-party images** — pin to a specific version
  so builds are reproducible
- **Bind-mounting `.` into the container in production** — bind mounts
  are for development; production should use the built image
- **Missing `restart:` policy** — default is `no`, which means a crashed
  service stays down until you notice
