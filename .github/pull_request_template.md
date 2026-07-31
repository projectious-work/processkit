## What this changes

<!-- One or two sentences. Link the issue or DecisionRecord if there is one. -->

## Why

<!-- What breaks or stays awkward without it. -->

## Contract impact

- [ ] No change to schemas, tool signatures, ID formats, or package contents
- [ ] Breaking change — described below and added to `CHANGELOG.md`

## Checks run locally

GitHub Actions runs the v1 Rust/generated-doc gates; maintainers also report
checks locally. Tick what you ran:

- [ ] `./scripts/check-docs-local.sh`
- [ ] `uv run scripts/smoke-test-servers.py`
- [ ] `uv run scripts/smoke-test-package.py`
- [ ] `./scripts/check-src-context-drift.sh --release-deliverable`
- [ ] Not applicable

<!-- Paste failures rather than omitting them. -->
