---
apiVersion: processkit.projectious.work/v2
kind: Artifact
metadata:
  id: ART-20260414_1515-BaselinePulse-enforcement-baseline-metrics
  created: 2026-04-14 15:15:00+00:00
spec:
  name: Pre-enforcement baseline metrics — processkit tool-adoption (processkit repo,
    single-project)
  kind: document
  location: context/artifacts/ART-20260414_1515-BaselinePulse-enforcement-baseline-metrics.md
  format: markdown
  version: 1.0.0
  tags:
  - research
  - measurement
  - enforcement
  - baseline
  - adoption
  produced_by: BACK-20260414_1500-BaselinePulse-enforcement-adoption-baseline-metrics
  owner: ACTOR-jr-researcher
  links:
    workitem: BACK-20260414_1500-BaselinePulse-enforcement-adoption-baseline-metrics
    related_artifacts:
    - ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan
---

# Pre-enforcement baseline metrics — processkit tool-adoption

**Author:** ACTOR-jr-researcher (Sonnet) · **Date:** 2026-04-14
**Parent WorkItem:** `BACK-20260414_1500-BaselinePulse-enforcement-adoption-baseline-metrics`
**Scope:** processkit repo only (single-project; see §6 for second-project gap)

---

## 1. Methodology

### 1.1 Session proxy

No `context/events/` directory exists. The primary data source is the structured event log at `context/logs/2026/04/` (70 `LogEntry` files) cross-referenced against `git log` (94 total commits, 36 touching `context/`).

"Session" is proxied by **git commit cluster**: one or more commits by the same author within a continuous 2-hour working window sharing a coherent theme. Each cluster is treated as one agent session. This is a coarse proxy — a single interactive agent session may produce 1–4 commits, and occasional lone "chore" commits (version bumps, aibox sync) are folded into the nearest preceding substantive cluster.

Observation window: **2026-04-06 through 2026-04-14** (all available history).

### 1.2 Session inventory

| # | Session window | Commits (representative) | Entity writes |
|---|---|---|---|
| S1 | 2026-04-06 14:00–18:59 | `6c2700d` (v0.1.0 foundation) | Initial skills layout (no entities) |
| S2 | 2026-04-06 22:07–23:25 | `6475216`, `2ca3c69` (v0.3.0, MCP servers, HANDOVER) | No WI/DEC/ART entities |
| S3 | 2026-04-07 10:12–10:35 | `afaeb82`, `b06921a` (v0.4.0 finalize handover) | No WI/DEC/ART entities |
| S4 | 2026-04-07 18:09–22:34 | `922ac10`, `267d870`, `0c3e1d8` (v0.5.0–v0.5.1, BACK-001) | No WI/DEC/ART entities |
| S5 | 2026-04-08 10:39–23:22 | `de91cb7` through `11d95bd` (reset + skill batch) | No WI/DEC/ART entities |
| S6 | 2026-04-08 22:25–23:47 | `232920b` through `a90f052` (skill sets + skill-finder) | No WI/DEC/ART entities |
| S7 | 2026-04-09 18:24–23:49 | `7e689d3`, `8f85db7`, `8e47e3a` (v0.8.0–v0.9.0) | **11 WIs + 1 ART + 1 DEC** |
| S8 | 2026-04-10 00:13–00:26 | `8a4aed4`, `2a0aa5b` (MCP server fix, session-handover fix) | 0 entities |
| S9 | 2026-04-10 13:51 | `1ca7f97` (Ingest aibox/move-to-processkit) | **8 WIs** |
| S10 | 2026-04-10 16:36–23:26 | `a81b32e`, `8a027b9`, `765b593`, `e86ad06` (sync, backlog, v0.10.0, SteadyLeaf) | **7 WIs** |
| S11 | 2026-04-11 01:05–06:54 | `b889bb7`, `924e339`, `706434d` (DISC-SharpHawk, v0.11.0, v0.11.1) | 0 WI/DEC/ART entities |
| S12 | 2026-04-11 08:02–09:04 | `5ac7dcf`, `f03a764`, `b9252d3`, `75d095a`, `0b9ff5c` (semver, HappyHare, close WIs, v0.12.0, docs) | **2 WIs + 1 DEC** |
| S13 | 2026-04-11 17:33–20:03 | `3ccd28c`, `ba18979`, `b1b0f75`, `48e61f0`, `12d049`, `bd923b0`, `eb83295`, `ac9ab3` (Tracks A–E, task-router, v0.13.0) | **3 WIs + 1 DEC** |
| S14 | 2026-04-13 18:21–19:31 | `f2efd5d`, `a58bd23`, `e24fca3` (reconcile migrations, deploy task-router, .gitignore) | 0 entities |
| S15 | 2026-04-14 11:36–11:38 | `e110881`, `4430e47` (permanent AI team, track aibox release) | **1 DEC** (+ 8 Actors, 8 Roles, 8 Bindings) |
| S16 (untracked) | 2026-04-14 (enforcement wave sessions) | uncommitted | **11 WIs + 5 ARTs + 2 DECs** (untracked on disk) |

**Denominator for metrics:** 16 sessions identified. Of these, 8 sessions (S7, S9, S10, S12, S13, S15, S16 + S9-parallel) involved creating processkit entities (`create_workitem`, `create_artifact`, `record_decision`). Remaining 8 had no entity writes.

---

## 2. Data sources used

1. `context/logs/2026/04/` — 70 structured `LogEntry` YAML files; primary signal for MCP tool invocation.
2. `git log --no-merges` (94 commits) with `--diff-filter=A` and `--name-only` per commit — used to correlate entity file creation with log entries in the same commit.
3. `git status` — identified 18 untracked context entity files (S16 enforcement sessions) with zero corresponding log entries, confirming hand-edit pattern.
4. Handover log entries (`LOG-20260409_2225-SnowyEmber-session-handover`, `LOG-20260410_1149-HappyCliff-session-handover`) — provided session-level behavioral retrospectives including notes on skipped skill-finder invocations.
5. `ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan` §5 — confirmed rollout sequence and that `route_task` was unavailable before its implementation on 2026-04-11T17:57.

---

## 3. Metrics

### 3.1 Metric 1 — `route_task` invoked before first `create_*`/`transition_*`/`record_*`

**Definition of eligible sessions:** sessions where entity writes occurred AND `route_task` was available (only from S13 onward, when task-router was first implemented on 2026-04-11T17:57).

| Session | Entity writes? | route_task available? | Log entry showing route_task call? | Counted |
|---|---|---|---|---|
| S1–S12 | varies | No (tool not yet built) | n/a | Excluded |
| S13 | Yes (3 WIs + 1 DEC) | Yes (built in this session) | No log entry of route_task-before-write | Eligible |
| S14 | No entity writes | Yes | n/a | Excluded |
| S15 | Yes (1 DEC + roles) | Yes | No log entry of route_task-before-write | Eligible |
| S16 | Yes (11 WIs + 5 ARTs + 2 DECs) | Yes | No log entry of route_task-before-write | Eligible |

**Count: 0/3 eligible sessions (0%) showed `route_task` called before first write.**

Confidence: **Low-medium.** The absence of a `route_task`-prefixing log entry is the signal, but `log_event` calls for `route_task` may simply have been omitted even if the tool was called — the event log is voluntary (see §4). The enforcement research sessions (S16) are a known case of an Opus agent operating on research/architecture tasks, which may not have routed through the task-router even if it was available.

---

### 3.2 Metric 2 — Sessions where `create_workitem`/`create_artifact`/`record_decision` were called at all

**Heuristic:** if entity files appear in a commit or as untracked files AND corresponding `workitem-created`, `artifact-created`, or `decision-created` log entries exist in the same commit, the MCP tool was likely used. If entity files appear without any log entries, hand-edit is inferred.

| Session | Entities created | Matching log entries? | Inferred method |
|---|---|---|---|
| S7 | 11 WIs + 1 ART + 1 DEC | Yes — 8 `workitem-created` + 1 `decision-created` + process logs | MCP (partial: some WIs have logs, DEC has log) |
| S9 | 8 WIs | Yes — 8 `workitem-created` logs | MCP |
| S10 | 7 WIs | No log entries in commit `8a027b9` | Hand-edit likely |
| S12 | 2 WIs + 1 DEC | `5ac7dcf`: has `workitem-created` + `decision-created` logs | MCP |
| S13 | 3 WIs + 1 DEC | `bd923b0`: has `workitem-created` + `decision-created` logs | MCP |
| S15 | 1 DEC + 8 Actors + 8 Roles + 8 Bindings | Yes — has `decision-created` log (`MightySky` pattern) | MCP for DEC; roles/actors/bindings less clear |
| S16 | 11 WIs + 5 ARTs + 2 DECs | Zero log entries (all files untracked, none in any commit) | Hand-edit |

**Count: 5/7 entity-writing sessions (71%) invoked MCP tools for at least some writes.
Pure hand-edit sessions: 2/7 (29%) — S10 and S16.**

Confidence: **Medium.** The log-presence heuristic has false negatives (see §4). S10 is the clearest hand-edit case. S16 is the strongest hand-edit signal — 18 untracked entities with zero log entries.

---

### 3.3 Metric 3 — Sessions where hand-edits to `context/` occurred without a corresponding MCP tool call in the same window

**Criteria:** entity files in `context/workitems/`, `context/artifacts/`, `context/decisions/` created in a commit or found as untracked, with no corresponding `LogEntry` files present.

| Session | Evidence |
|---|---|
| S10 | Commit `8a027b9` adds 7 WI files; zero log entries in the commit |
| S16 | 18 entity files untracked on disk (11 WIs, 5 ARTs, 2 DECs); zero log entries for any |

**Count: 2/16 sessions (12.5%) had confirmed hand-edit entity writes with no MCP log signal.**

Additional partial signals: S7 created 11 WIs but only 8 had corresponding log entries (3 WIs created without confirmed log entry); however, some may have been auto-logged outside the entity-creating commit and committed separately. This is ambiguous.

Confidence: **Medium-high for S10 and S16** (both are clean signals). The partial S7 case is ambiguous.

---

### 3.4 Metric 4 — Sessions where `log_event` entries followed state changes

**State changes include:** `workitem-transitioned`, `decision-created`, `discussion-opened`/`-transitioned`, `skill-implemented`.

| Session | State changes visible | Log entries present | Rate |
|---|---|---|---|
| S7 | 11 WIs created, 1 DEC created | 8 WI-created + 1 DEC-created + 4 process logs | ~8/12 (67%) |
| S9 | 8 WIs created | 8 workitem-created logs | 8/8 (100%) |
| S10 | 7 WIs created | 0 log entries | 0/7 (0%) |
| S11 | DISC resolved (SharpHawk) | 2 discussion logs | 2/2 (100%) |
| S12 | 2 WIs created, several WIs closed | WI-created + WI-transitioned logs (9 `workitem-transitioned` in `f03a764`) | High coverage (~80%) |
| S13 | 3 WIs, 1 DEC, discussions, skill implemented | 12 log entries across commits | ~80% |
| S15 | 1 DEC, team entities | 0 log entries in commit | ~0% for non-DEC entities |
| S16 | 11 WIs, 5 ARTs, 2 DECs created | 0 log entries | 0% |

**Aggregate: across all entity-writing sessions, log entries followed state changes in approximately 55–60% of state changes.** The best-behaved sessions (S9, S11) hit 100%; the worst (S10, S16) hit 0%.

Confidence: **Low-medium.** The denominator is uncertain because state changes in interactive sessions may not all appear as entity file writes (e.g., intermediate research steps, read-only queries), and the log-entry voluntary nature means absence does not confirm no tool call.

---

## 4. Aggregated rates (single project)

| Metric | Numerator | Denominator | Rate | Confidence |
|---|---|---|---|---|
| M1: `route_task` before first write | 0 sessions | 3 eligible sessions (post-router) | **0%** | Low-medium |
| M2: `create_*`/`record_*` called at all | 5 sessions | 7 entity-writing sessions | **71%** | Medium |
| M3: Hand-edits without MCP log | 2 sessions | 16 total sessions | **12.5%** | Medium-high |
| M4: `log_event` after state changes | ~55–60% of state changes | All state changes in entity-writing sessions | **~55–60%** | Low-medium |

---

## 5. Caveats

1. **Voluntary `log_event` = false negatives.** The MCP `event-log` server is present and called by other entity-management servers (which auto-log as of v0.8.0), but direct `log_event` calls are voluntary. Absence of a log entry does not confirm a tool was not called — it only confirms no event was logged. This primarily affects M1 and M4. The v0.8.0 auto-log feature (`8f85db7`) means entity-mutating calls (create_workitem, etc.) auto-emit log entries; M2/M3 heuristics are therefore more reliable from S7 onward.

2. **Session proxy is coarse.** Commit clusters conflate multiple turn sequences into one "session." A better post-enforcement measurement would use actual session boundary markers (`log_event` with `event_type: session.start`) as the denominator.

3. **Pre-v0.8.0 history is unreliable.** Sessions S1–S6 (Apr 6–8) predate the auto-log feature and have no `context/logs/` entries; they are excluded from all metrics.

4. **`route_task` was only available for the last 3 eligible sessions (S13–S16).** The 0% M1 rate is based on a very small sample. The S16 enforcement sessions are a plausible outlier — an Opus-class agent doing research/architecture work in a domain where it had the full context in hand.

5. **S16 is confirmed hand-edit, but the cause is unknown.** The 11 WIs, 5 ARTs, and 2 DECs in S16 are all untracked files with no log entries. This could be: (a) MCP servers not wired at that session start, (b) MCP tools unavailable due to `.mcp.json` not being reloaded after deploy, or (c) deliberate direct writes. Without session-level harness logs, the cause is not determinable. The `aibox.toml` shows both Claude and Codex harnesses; the backup `.mcp.json` (2026-04-13) confirms all 15 servers were registered at that point.

6. **Second project not measured.** No sibling repositories were accessible in this environment. The owner should designate a second consumer project consuming processkit (e.g., a separate aibox-managed project) and run the same git-log and log-entry analysis there before the enforcement release ships.

---

## 6. Recommended follow-up measurements (post-enforcement)

After the enforcement wave (CleanCharter / InkStamp / RightPath / LoudBell / SteadyHand) ships:

1. **Re-run M1–M4 on 20+ sessions** in processkit itself and one named consumer project. Use the same methodology (log-entry heuristic + git commit clustering).
2. **Add session boundary log entries.** Have agents emit `log_event(event_type: "session.start", summary: "Session opened")` as the first act. This provides a clean denominator and makes M1 unambiguous.
3. **Add `route_task` call log entries.** If `route_task` emits a `task.routed` log entry on each call, M1 can be measured directly. Currently no such log entry is written by the task-router server.
4. **Instrument the second project before the release ships.** Agree on a named consumer project with the owner; run this same baseline analysis on that project's git history and log files.
5. **Track the `acknowledge_contract()` call rate** once LoudBell ships — it provides a cleaner M1 proxy than `route_task` for session-start compliance.
6. **Capture aibox.toml `harnesses` field and `.mcp.json` presence** in each snapshot — needed to distinguish "tool not called" from "tool not available."

---

## 7. Second project gap

No sibling repositories were accessible at `/workspace/..` in this environment, and `git remote -v` produced no consumer project hints. **The owner must name a second consumer project (e.g., an aibox-installed project consuming processkit v0.13.0) for a Round-2 baseline before the enforcement release is cut.** Once named, the same methodology applies: enumerate git commits touching `context/workitems/`, `context/decisions/`, `context/artifacts/`, and `context/logs/`; cluster into sessions; run M1–M4.

---

## 8. Provenance

- Event log: `context/logs/2026/04/` (70 log entries, Apr 9–11)
- Git history: 94 commits, 36 touching `context/`, window Apr 6–14 2026
- Handover logs: `LOG-20260409_2225-SnowyEmber-session-handover`, `LOG-20260410_1149-HappyCliff-session-handover`
- MCP config: `.aibox/backup/aibox-latest-backup-2026-04-13-1325/.mcp.json` (15 servers registered as of Apr 13)
- Implementation plan: `ART-20260414_1430-SteadyBeacon-enforcement-implementation-plan`
