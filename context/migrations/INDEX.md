# Migrations Index

## Pending (0)

None.

## In Progress (0)

None.

## Applied (1)

| Date       | Migration                                | Notes |
|------------|------------------------------------------|-------|
| 2026-05-13 | MIG-RUNTIME-DRIFT-20260512T113641 — aibox-runtime-drift  → 0.25.10 | 8 drifted managed runtime file(s) found at 0.25.10 |

## Rejected (4)

| Date       | Migration                                | Reason |
|------------|------------------------------------------|--------|
| 2026-05-13 | MIG-20260513T152530 — processkit v0.26.2 → v0.26.5 | Rejected per pk-doctor migration_integrity finding: affected_groups/body rows exist but affected_files is empty, so thi… |
| 2026-05-13 | MIG-DISABLED-HARNESS-STATE — aibox  → | Resolved without purging disabled harness host state. The user asked to clear pending migrations, but this migration wo… |
| 2026-05-13 | MIG-RUNTIME-20260513T152530 — aibox-runtime-home 0.25.13 → 0.25.13 | Rejected per pk-doctor migration_integrity findings: same-version runtime migration has affected_groups/body rows but a… |
| 2026-05-13 | MIG-RUNTIME-20260513T180157 — aibox-runtime-home 0.25.13 → 0.25.14 | Rejected per pk-doctor migration_integrity finding: affected_groups/body rows exist but affected_files is empty, so the… |

## CLI Migrations

| File | Range | Status |
|------|-------|--------|
| 20260410_1353_0.17.5-to-0.17.6.md | v0.17.5 → v0.17.6 | completed |
| 20260410_1523_0.17.6-to-0.17.9.md | v0.17.6 → v0.17.9 | completed |
| 20260410_1554_0.17.9-to-0.17.10.md | v0.17.9 → v0.17.10 | completed |
| 20260410_1616_0.17.10-to-0.17.11.md | v0.17.10 → v0.17.11 | completed |
| 20260410_2351_0.17.11-to-0.17.12.md | v0.17.11 → v0.17.12 | completed |
| 20260411_2249_0.17.12-to-0.17.15.md | v0.17.12 → v0.17.15 | completed |
| 20260413_1336_0.18.1-to-0.18.2.md | v0.18.1 → v0.18.2 | completed |
| 20260417_1626_0.18.2-to-0.18.3.md | v0.18.2 → v0.18.3 | completed (doc stale — actual host jumped 0.18.2 → 0.18.4; aibox upstream investigating the skipped 0.18.3 sync artefacts) |
