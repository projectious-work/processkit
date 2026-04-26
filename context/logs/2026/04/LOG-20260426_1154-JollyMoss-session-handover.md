---
apiVersion: processkit.projectious.work/v1
kind: LogEntry
metadata:
  id: LOG-20260426_1154-JollyMoss-session-handover
  created: '2026-04-26T11:54:32+00:00'
spec:
  event_type: session.handover
  timestamp: '2026-04-26T11:54:32+00:00'
  summary: Session handover — v0.22.0 shipped; RoyalFern Model schema landed (jurisdiction
    + data_privacy + 3 more) backfilled across all 34 models
  actor: ACTOR-claude
  details:
    session_date: '2026-04-26'
    current_state: 'Clean working tree on main @ 8e914d7. v0.22.0 was tagged + GitHub-released
      yesterday (https://github.com/projectious-work/processkit/releases/tag/v0.22.0).
      On top of that, RoyalFern shipped today: five additive optional fields on Model.spec_schema.versions[]
      (jurisdiction, data_privacy, knowledge_cutoff, vendor_model_id, latency_p50_ms),
      backfilled across all 34 model entities by two parallel subagents, plus model-recommender
      SKILL.md updated under the Governance dimension with structured-fields block
      + 4 query_models filter examples. pk-doctor: 0 ERROR / 2 WARN / 10 INFO — the
      two WARNs remain the aibox#55-gated preauth_applied items.'
    open_threads:
    - 'WildGrove (BACK-20260425_1316, in-progress, high-priority bug) — Phase A processkit-side
      shipped in v0.22.0 (preauth.json + preauth_applied check). Phase B is aibox#55:
      aibox sync needs to read the spec and merge into .claude/settings.json. WI stays
      in-progress until aibox#55 ships and the 2 preauth_applied WARNs flip to 1 INFO.'
    - WildButter (BACK-20260409_1652, in-progress, high epic) — Docusaurus docs-site.
      Untouched in this session and the last several; status unknown without revisit.
      May need to be re-scoped or paused.
    - CleverRiver (BACK-20260425_1711, backlog, high-priority bug) — processkit-side
      defensive migration_integrity check shipped in v0.22.0. WI stays in backlog
      as cross-project tracker for the upstream aibox-sync diff-generator fix. No
      processkit work pending.
    - VastLark (BACK-20260425_1235, backlog, low) — skill-gate PreToolUse matcher
      gap (auto-renew misses on create_binding). Identified as a v0.22.0 candidate
      during release triage but deferred (has aibox-side dependency similar to WildGrove).
      Cheap candidate for v0.23.0.
    - 'RapidDaisy (BACK-20260425_1755, backlog, medium bug) — log_event MCP skips
      actor required-field validation. Filed today. Workaround in use: callers pass
      actor explicitly (this very handover does so).'
    - 'CalmArch (BACK-20260425_1755, backlog, medium bug) — workitem-management MCP
      serializes long descriptions with fragile double-quoted scalars. Filed today.
      Workaround: rewrite as YAML literal block scalar after the fact.'
    - model-recommender query_models() filter implementation — SKILL.md docs the 4
      new filter examples (phi_hipaa_eligible, jurisdiction_country_in, training_on_customer_data,
      etc.) but the MCP server doesn't yet implement filtering on the new fields.
      No WI filed yet — waiting on owner decision whether to bundle into v0.23.0 or
      batch.
    - v0.22.1 release decision pending — RoyalFern (schema + 34-file backfill + SKILL.md
      docs) is shippable but not yet tagged. Owner asked at end of session; awaiting
      decision. If shipped, also a chance to bundle VastLark and the model-recommender
      filter implementation.
    next_recommended_action: Decide whether to cut v0.22.1 today (RoyalFern alone
      is a clean, shippable schema enhancement) or batch RoyalFern + VastLark + model-recommender
      filter implementation into a focused v0.23.0. Owner has the deciding vote —
      surface the trade-off (one-feature point release vs. coherent batch) and proceed.
    branch: main
    commit: 8e914d7
    behavioral_retrospective:
    - Undercounted model files (34 actual vs 18 claimed) in the RoyalFern WI description
      before delegating. Both shard subagents discovered the discrepancy and flagged
      it in their reports. One-off arithmetic miss; encoded inline by correcting the
      WI scope at backfill time. Not worth a feedback memory.
    - 'Told both backfill subagents that context/models/ has no src/context/ mirror
      — false; the mirror exists for all of context/. Both agents called out the bad
      assumption in their reports and proceeded correctly anyway, but the post-edit
      drift required a manual sync pass that would have been avoidable. Filed as durable
      lesson: when delegating writes, verify mirror status of target dirs before stating
      it in the prompt.'
---
