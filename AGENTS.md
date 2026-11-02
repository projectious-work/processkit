# AGENTS.md

Project instructions for any AI agent or human working in this repository.
Provider-specific files such as `CLAUDE.md` are thin pointers; edit this
file.

## About

processkit is a versioned, provider-neutral library of process primitives,
skills, and MCP servers.

This repository develops that product. It no longer runs on its own installed
copy: the development container uses `[context] mode = "harness-only"`, so no
processkit MCP gateway, hooks, skills, or entity tree are active here.

- `src/` is the product source that ships to consumers.
- `archive/processkit-install-20261101/` is the retired installation. Treat it
  as read-only history. See its `README.md`.

## Setup

```sh
./scripts/check-docs-local.sh
uv run scripts/smoke-test-servers.py
```

Some maintenance scripts still expect the retired root `context/` tree. The
archive `README.md` lists them.

## Code style and PRs

- Hard-wrap Markdown, Python, and YAML at 80 columns. Tables, URLs,
  frontmatter, and code fences are exempt.
- Use Conventional Commits. Never use `--no-verify`.
- Squash-merge PRs, with tests green before merge.

## Container

- Never edit `.devcontainer/Dockerfile`; use `Dockerfile.local`.
- `apiVersion` is locked through v1.x; `v2` requires a full migration.
- `_find_lib()` uses the current directory, so smoke tests call `os.chdir()`
  before invoking servers.
