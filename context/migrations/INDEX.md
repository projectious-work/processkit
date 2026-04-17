# Migrations Index

## Pending (0)

None.

## In Progress (0)

None.

## Applied (11)

| Date       | Migration                                | Notes |
|------------|------------------------------------------|-------|
| 2026-04-10 | MIG-20260410T123638 — processkit v0.7.0 → v0.7.0 | AGENTS.md conflict: kept local (fully customised). 153 changed-locally-only: no action. |
| 2026-04-10 | MIG-20260410T123848 — processkit v0.8.0 → v0.8.0 | AGENTS.md conflict: kept local. All v0.8.0 additions already present. |
| 2026-04-10 | MIG-20260410T215118 — processkit v0.10.0 → v0.10.0 | AGENTS.md conflict: local customised file retained. |
| 2026-04-11 | MIG-20260411T042618 — processkit v0.11.1 → v0.11.1 | AGENTS.md conflict: local customised file retained. |
| 2026-04-13 | MIG-20260411T204940 — processkit v0.13.0 → v0.13.0 | AGENTS.md conflict resolved by restoring the filled local file on top of the new scaffold. |
| 2026-04-13 | MIG-RUNTIME-20260413T112909 — runtime-home 0.18.1 → 0.18.1 | New runtime-home files accepted; snapshots present under context/templates/aibox-home/0.18.1. |
| 2026-04-13 | MIG-RUNTIME-20260413T113638 — runtime-home 0.18.1 → 0.18.2 | Runtime-home updates accepted; snapshots present under context/templates/aibox-home/0.18.2. |
| 2026-04-14 | MIG-20260414T085054 — processkit v0.13.0 → v0.13.0 | Same-version re-scan. AGENTS.md conflict: kept local. Four changed-locally-only files: no action. |
| 2026-04-15 | MIG-20260415T085311 — processkit v0.15.0 → v0.16.0 | Role schema: add primary_contact, clone_cap, cap_escalation. 8 role entities updated. |
| 2026-04-15 | MIG-20260415T095000 — processkit v0.15.0 → v0.16.0 | Actor schema: add is_template, templated_from. 8 actor entities (templates) updated. |
| 2026-04-17 | MIG-20260417T142628 — processkit v0.13.0 → v0.17.0 | Documentary only — live tree already at v0.17.0 (three 0.15→0.17 releases shipped in the 2026-04-15→17 session). All 9 server.py conflicts identical to v0.17.0 template; AGENTS.md + INDEX.md kept as intentional local customizations; all 11 new-upstream skill-gate files present. |
| 2026-04-17 | MIG-RUNTIME-20260417T142628 — runtime-home 0.18.2 → 0.18.3 | yazi/keymap.toml accepted; toggle-pane.yazi plugin installed; .claude/keybindings.json kept local. |

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
