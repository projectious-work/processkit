---
apiVersion: processkit.projectious.work/v1
kind: Skill
metadata:
  id: SKILL-python-best-practices
  name: python-best-practices
  version: "1.1.0"
  created: 2026-04-06T00:00:00Z
spec:
  description: "Python conventions and patterns — typing, testing, project layout, tooling."
  category: language
  layer: null
  when_to_use: "Use when writing or reviewing Python code, setting up a new Python project, or deciding on tooling, typing, or testing conventions."
---

# Python Best Practices

## Level 1 — Intro

Modern Python is opinionated: `src/` layout, `pyproject.toml`, type
hints on public APIs, `pytest` for tests, `ruff` for lint and format.
Apply these conventions when writing or reviewing Python code.

## Level 2 — Overview

### Project layout

Use the `src/` layout. The package lives at `src/<package>/` with an
`__init__.py`; tests live in a sibling `tests/` tree mirroring the
package structure. Configuration goes in `pyproject.toml` — never
`setup.py` or `setup.cfg`. Prefer `uv` for dependency management when
the project supports it; fall back to `pip-tools` or `poetry`
otherwise.

```
my-project/
├── pyproject.toml
├── src/
│   └── my_package/
│       ├── __init__.py
│       └── core.py
└── tests/
    └── test_core.py
```

### Type hints

Add type hints to all public function signatures and dataclass fields.
Use `from __future__ import annotations` at the top of every module to
enable modern syntax (PEP 563-style postponed evaluation) without
runtime cost. Prefer `TypeAlias`, `Protocol`, and `dataclass` over raw
dicts and tuples for non-trivial data shapes.

### Testing with pytest

Test files mirror the `src/` tree: `src/my_package/foo.py` is tested
by `tests/test_foo.py`. Use fixtures for shared setup and `parametrize`
for variant testing. Name tests `test_<function>_<scenario>_<expected>`
so failures self-document.

### Code style

Format with `ruff format`, lint with `ruff check`. Both replace older
combinations of black + isort + flake8 + pyupgrade. Prefer dataclasses
or Pydantic models over plain dicts. Use `pathlib.Path` over
`os.path`. Use f-strings over `.format()` or `%` formatting.

### Error handling

Raise specific exception classes, not generic `Exception`. Define
custom exception classes per domain (e.g.
`UserNotFoundError(LookupError)`). Never write a bare `except:` —
always catch the specific exception type you expect.

## Level 3 — Full reference

### `pyproject.toml` skeleton

```toml
[project]
name = "my-package"
version = "0.1.0"
description = "Short description."
requires-python = ">=3.10"
dependencies = [
    "httpx>=0.27",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=4.0",
    "ruff>=0.5",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 80
target-version = "py310"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

### Type-hint patterns

| Use case | Pattern |
|---|---|
| Function returning nothing | `def foo() -> None:` (not `-> ()` or omitted) |
| Optional value | `x: int \| None` (PEP 604, modern) over `Optional[int]` |
| Iterable input | `Iterable[T]` for read-only consumption; `list[T]` only when mutation is needed |
| Callback / interface | `Protocol` over abstract base class |
| Frozen value | `dataclass(frozen=True)` or `tuple` |
| Factory return type | The interface (`Protocol` or ABC), not the concrete class |

### Testing conventions

- **Fixtures over setup methods.** pytest fixtures are composable and
  scoped; `unittest`-style `setUp/tearDown` is not.
- **One assertion per test, ideally.** When more is genuinely needed,
  use `pytest.subtests` or split.
- **No mocking the unit under test.** Mock the boundary
  (HTTP client, database driver, clock). Mocking the function you're
  testing means you're testing the mock.
- **Coverage is a smoke alarm, not a goal.** Aim for meaningful
  coverage of branching logic, not 100% line coverage.

### Async vs sync

Use `async`/`await` when the workload is genuinely I/O bound and the
ecosystem supports it (HTTP servers, network clients, databases with
async drivers). Do **not** make a library async by default — sync
callers cannot easily wrap async code, but async callers can wrap
sync code via `asyncio.to_thread`. Default to sync; opt into async
when concurrency is the point.

### Anti-patterns to avoid

- **Bare `except:`** — catch specific types
- **`from module import *`** — explicit imports only
- **Mutable default arguments** (`def foo(x=[]):`) — use `None` and
  initialize inside
- **Generic exception handling that swallows errors** — at minimum
  log + re-raise; never silently `pass`
- **Mixing tabs and spaces** — ruff catches this; never bypass
- **`os.path.join` over `Path / Path`** — pathlib is the modern API
- **Shell-style string concatenation for SQL** — parametrized queries
  always

### When to break the rules

Every rule above has exceptions. Pin yourself to the rule until you
understand why it exists; only then are you qualified to break it.
Common legitimate exceptions: type-stub files (`.pyi`) intentionally
omit type hints in body, scientific code uses `numpy` arrays which
have their own typing patterns, scripts under ~50 lines may skip the
`src/` layout.
