#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp[cli]>=1.0", "pyyaml>=6.0", "jsonschema>=4.0"]
# ///
"""End-to-end smoke test for processkit MCP servers.

Creates a fresh project directory, imports each server module directly
(bypassing the MCP transport — we are testing the tool functions, not
the protocol), and exercises a realistic workflow:

  1. workitem-management.create_workitem
  2. workitem-management.transition_workitem
  3. event-log.log_event (manual, to verify it round-trips)
  4. decision-record.record_decision
  5. binding-management.create_binding
  6. index-management.reindex + queries
"""
from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import shutil
from datetime import date, datetime, timezone
from pathlib import Path

PROCESSKIT = Path(__file__).resolve().parent.parent
LIB = PROCESSKIT / "src" / "context" / "skills" / "_lib"
sys.path.insert(0, str(LIB))


def import_server(name: str):
    """Import a server.py module by skill name without running its main()."""
    # Skills are now organized into category subdirectories. Search all of them.
    skills_root = PROCESSKIT / "src" / "context" / "skills"
    path = None
    for cat_dir in skills_root.iterdir():
        if not cat_dir.is_dir():
            continue
        candidate = cat_dir / name / "mcp" / "server.py"
        if candidate.is_file():
            path = candidate
            break
    if path is None:
        # Fallback: flat layout (pre-SteadyLeaf)
        path = skills_root / name / "mcp" / "server.py"
    spec = importlib.util.spec_from_file_location(f"server_{name}", path)
    module = importlib.util.module_from_spec(spec)
    # Server modules call _find_lib() at import — they need cwd to be inside processkit
    # OR PROCESSKIT_LIB_PATH set. We set the env var.
    os.environ["PROCESSKIT_LIB_PATH"] = str(LIB)
    spec.loader.exec_module(module)
    return module


def get_tool(server_module, name: str):
    """Extract a registered tool's underlying function from FastMCP.

    FastMCP stores tools in server._tool_manager._tools as Tool objects;
    each has a .fn attribute pointing to the original function.
    """
    sm = server_module.server
    tm = sm._tool_manager
    tool = tm._tools[name]
    return tool.fn


def run():
    workdir = Path(tempfile.mkdtemp(prefix="processkit-smoke-"))
    print(f"workdir: {workdir}")
    try:
        # 1. Set up a minimal project
        (workdir / "aibox.toml").write_text(
            '[aibox]\nversion = "0.14.1"\n[context]\npackages = ["managed"]\n'
        )
        (workdir / "context").mkdir()
        # Seed schemas + state machines at the consumer install paths so
        # paths.primitive_schemas_dir / state_machines_dir find them.
        # paths.find_project_root walks up looking for aibox.toml — that
        # finds workdir. The lib then looks for:
        #   workdir/context/schemas/        (consumer install)
        #   workdir/context/state-machines/ (consumer install)
        # falling back to processkit's src/primitives/{schemas,state-machines}
        # if not present. We seed at the consumer location to exercise that
        # code path.
        context_root = workdir / "context"
        shutil.copytree(
            PROCESSKIT / "src" / "context" / "schemas",
            context_root / "schemas",
        )
        shutil.copytree(
            PROCESSKIT / "src" / "context" / "state-machines",
            context_root / "state-machines",
        )

        os.chdir(workdir)

        # Seed a minimal skill catalog so skill-finder and task-router
        # can parse triggers and read skill descriptions.
        _skf_src = (
            PROCESSKIT
            / "src" / "context" / "skills"
            / "processkit" / "skill-finder" / "SKILL.md"
        )
        _skf_dst = (
            workdir / "context" / "skills"
            / "processkit" / "skill-finder"
        )
        _skf_dst.mkdir(parents=True, exist_ok=True)
        shutil.copy(_skf_src, _skf_dst / "SKILL.md")

        # Seed workitem-management SKILL.md so task-router can read its
        # description excerpt.
        _wi_src = (
            PROCESSKIT
            / "src" / "context" / "skills"
            / "processkit" / "workitem-management" / "SKILL.md"
        )
        _wi_dst = (
            workdir / "context" / "skills"
            / "processkit" / "workitem-management"
        )
        _wi_dst.mkdir(parents=True, exist_ok=True)
        shutil.copy(_wi_src, _wi_dst / "SKILL.md")
        _wi_assets = _wi_dst / "assets"
        _wi_assets.mkdir(parents=True, exist_ok=True)
        (_wi_assets / "workitem-template.md").write_text(
            "---\n"
            "apiVersion: processkit.projectious.work/v2\n"
            "kind: WorkItem\n"
            "metadata:\n"
            "  id: BACK-template-asset\n"
            "  created: 2026-04-30T00:00:00Z\n"
            "spec:\n"
            "  title: Skill asset template must not enter project index\n"
            "  state: backlog\n"
            "  type: task\n"
            "  priority: medium\n"
            "---\n",
            encoding="utf-8",
        )

        # Seed a minimal processes/ directory with a release.md override
        # so task-router's process_override lookup can be exercised.
        _proc_dir = workdir / "context" / "processes"
        _proc_dir.mkdir(parents=True, exist_ok=True)
        (_proc_dir / "release.md").write_text(
            "---\nkind: Process\nmetadata:\n  id: PROC-release\n---\n"
            "# Release process override\n"
        )

        # Seed a YAML entity so the v2 migration helper covers schemas /
        # state machines, not only Markdown entities.
        _smoke_sm = context_root / "state-machines" / "smoke.yaml"
        _smoke_sm.write_text(
            "---\n"
            "apiVersion: processkit.projectious.work/v1\n"
            "kind: StateMachine\n"
            "metadata:\n"
            "  id: SM-smoke\n"
            "  name: smoke\n"
            "spec:\n"
            "  initial: start\n"
            "  terminal: [done]\n"
            "  states:\n"
            "    start:\n"
            "      transitions:\n"
            "        - to: done\n"
            "    done:\n"
            "      transitions: []\n",
            encoding="utf-8",
        )

        # Clear caches in lib modules so they pick up the new project
        # (config.load_config is no longer cached — reads disk on every call)
        from processkit import paths, schema, state_machine, config, index
        schema.load_schema.cache_clear()
        state_machine.load.cache_clear()

        # YAML loaders return native date/datetime objects for unquoted
        # timestamps; validation must treat those as their serialized JSON
        # representation so historical context remains valid under v2.
        _date_errs = schema.validate_spec(
            "Note",
            {
                "title": "Smoke dated note",
                "body": "Validate YAML-native date compatibility.",
                "type": "question",
                "state": "captured",
                "review_due": date(2026, 4, 30),
            },
        )
        assert _date_errs == [], _date_errs
        _datetime_errs = schema.validate_spec(
            "Migration",
            {
                "source": "processkit",
                "from_version": "v1",
                "to_version": "v2",
                "state": "pending",
                "generated_by": "smoke-test",
                "generated_at": datetime(2026, 4, 30, tzinfo=timezone.utc),
                "summary": "Validate YAML-native datetime compatibility.",
            },
        )
        assert _datetime_errs == [], _datetime_errs

        # Import servers
        tr = import_server("task-router")
        sg = import_server("skill-gate")
        wi = import_server("workitem-management")
        dec = import_server("decision-record")
        bind = import_server("binding-management")
        elog = import_server("event-log")
        idx = import_server("index-management")
        idm = import_server("id-management")
        actor = import_server("actor-profile")
        role = import_server("role-management")
        scope = import_server("scope-management")
        gate = import_server("gate-management")
        disc = import_server("discussion-management")
        art = import_server("artifact-management")
        mig = import_server("migration-management")
        note = import_server("note-management")
        agent_card = import_server("agent-card")
        eval_gate = import_server("eval-gate-authoring")
        security = import_server("security-projections")
        skf = import_server("skill-finder")
        agg = import_server("aggregate-mcp")

        aggregate_tools = get_tool(agg, "list_aggregate_tools")()
        print("aggregate-mcp tool count:", aggregate_tools["count"])
        assert aggregate_tools["count"] >= 90
        assert "create_workitem" in agg.server._tool_manager._tools

        # 0. id-management sanity
        gen_id = get_tool(idm, "generate_id")
        prev = gen_id(kind="WorkItem")
        print("id-management.generate_id:", prev)
        assert prev["id"].startswith("BACK-")

        validate = get_tool(idm, "validate_id")
        v_ok = validate(id="BACK-calm-fox")
        print("id-management.validate_id ok:", v_ok)
        assert v_ok["valid"] and v_ok["kind"] == "WorkItem"

        v_bad = validate(id="UNKNOWN-foo")
        print("id-management.validate_id bad:", v_bad)
        assert not v_bad["valid"]

        finfo = get_tool(idm, "format_info")
        f = finfo()
        print("id-management.format_info:", f["format"], f["slug"])
        assert "BACK" in f["prefixes"].values()

        # 2. workitem flow
        create_wi = get_tool(wi, "create_workitem")
        bad_summary = create_wi(
            title="Bad summary shape",
            slug_summary="too short",
        )
        print("create_workitem bad slug_summary:", bad_summary)
        assert bad_summary.get("error") == "invalid slug_summary"

        result = create_wi(
            title="Add aibox lint command",
            type="story",
            priority="high",
            description="Walk context/ and validate frontmatter.",
            slug_summary="validate context frontmatter automatically",
        )
        print("create_workitem:", result)
        assert "id" in result and result["state"] == "backlog"
        wi_id = result["id"]

        transition_wi = get_tool(wi, "transition_workitem")
        t = transition_wi(id=wi_id, to_state="in-progress")
        print("transition workitem:", t)
        assert t.get("ok")

        # Bad transition
        bad = transition_wi(id=wi_id, to_state="done")
        print("bad transition (expected error):", bad)
        assert "error" in bad

        get_wi = get_tool(wi, "get_workitem")
        full = get_wi(id=wi_id)
        print("get workitem:", full)
        assert full["state"] == "in-progress"
        assert full["type"] == "story"

        # 3. log event manually
        log = get_tool(elog, "log_event")
        log_result = log(
            event_type="workitem.transitioned",
            summary=f"Moved {wi_id} to in-progress",
            actor="ACTOR-claude",
            subject=wi_id,
            subject_kind="WorkItem",
            details={"from_state": "backlog", "to_state": "in-progress"},
        )
        print("log_event:", log_result)
        assert "id" in log_result

        # 4. decision record
        record = get_tool(dec, "record_decision")
        d = record(
            title="Use the SQLite indexer in processkit (not aibox)",
            decision="The SQLite index lives in a processkit MCP server.",
            rationale="Schema knowledge stays in processkit; decoupled from aibox CLI.",
            state="accepted",
            related_workitems=[wi_id],
        )
        print("record_decision:", d)
        assert "id" in d and d["state"] == "accepted"
        dec_id = d["id"]

        # Link workitem ↔ decision
        link = get_tool(wi, "link_workitems")
        l = link(from_id=wi_id, to_id=dec_id, relation="related_decisions")
        print("link workitems:", l)
        assert l.get("ok")

        # 4b. actor-profile
        create_actor = get_tool(actor, "create_actor")
        a = create_actor(
            name="Alice Chen",
            type="human",
            email="alice@example.com",
            expertise=["backend", "rust"],
        )
        print("create_actor:", a)
        assert "id" in a and a["id"].startswith("ACTOR-")
        actor_id = a["id"]

        get_actor_t = get_tool(actor, "get_actor")
        ga = get_actor_t(id=actor_id)
        print("get_actor:", ga["name"], ga["expertise"])
        assert ga["name"] == "Alice Chen"

        update_actor_t = get_tool(actor, "update_actor")
        ua = update_actor_t(id=actor_id, expertise=["backend", "rust", "databases"])
        print("update_actor:", ua)
        assert ua["ok"] and "expertise" in ua["updated"]

        list_actors_t = get_tool(actor, "list_actors")
        la = list_actors_t(type="human")
        print("list_actors human:", len(la))
        assert any(x["id"] == actor_id for x in la)

        # bad type rejected
        bad = create_actor(name="Test", type="robot")
        print("bad actor type (expected error):", bad)
        assert "error" in bad

        # Regression guard for BACK-20260421_0156: create_actor must emit an
        # `actor.created` LogEntry whose spec.actor equals the new actor id
        # (self-attribution), and the emitted spec must pass LogEntry schema
        # validation (actor is a required field).
        from processkit import entity as _entity, index as _index_mod, schema as _schema_mod
        _db_ac = _index_mod.open_db()
        try:
            _ev_actor_created = _index_mod.query_events(
                _db_ac, event_type="actor.created", subject=actor_id
            )
        finally:
            _db_ac.close()
        print("log side effects — actor.created:", len(_ev_actor_created))
        assert len(_ev_actor_created) >= 1, "actor.created LogEntry missing"
        _log_row = _ev_actor_created[0]
        _log_id = _log_row["id"]
        # Resolve the LogEntry entity so we can inspect its full spec and run
        # schema validation (not just the indexed event row).
        _db_ac = _index_mod.open_db()
        try:
            _log_full = _index_mod.get_entity(_db_ac, _log_id)
        finally:
            _db_ac.close()
        assert _log_full and _log_full.get("path"), (
            f"LogEntry {_log_id!r} missing path in index: {_log_full}"
        )
        _log_ent = _entity.load(_log_full["path"])
        assert _log_ent.spec.get("actor") == actor_id, (
            f"actor.created LogEntry spec.actor={_log_ent.spec.get('actor')!r} "
            f"expected {actor_id!r} (self-attribution)"
        )
        _log_errs = _schema_mod.validate_spec("LogEntry", _log_ent.spec)
        assert _log_errs == [], (
            f"actor.created LogEntry fails schema validation: {_log_errs}"
        )
        print(
            "actor.created LogEntry self-attribution + schema validation: OK"
        )

        # 4c. role-management
        create_role = get_tool(role, "create_role")
        r = create_role(
            name="reviewer",
            description="Reviews code and documentation changes before merge.",
            responsibilities=[
                "Read PRs within 48 hours",
                "Approve or request changes with actionable feedback",
            ],
            default_scope="project",
        )
        print("create_role:", r)
        assert "id" in r and r["id"].startswith("ROLE-")
        role_id = r["id"]

        create_role_template = get_tool(role, "create_role_template")
        triage_role = create_role_template(template="inbox-triage")
        print("create_role_template inbox-triage:", triage_role)
        assert "id" in triage_role and triage_role["id"].startswith("ROLE-")

        list_roles = get_tool(role, "list_roles")
        lr = list_roles()
        print("list_roles:", len(lr))
        assert any(x["id"] == role_id for x in lr)
        assert any(x["id"] == triage_role["id"] for x in lr)

        link_rta = get_tool(role, "link_role_to_actor")
        lk = link_rta(
            role_id=role_id,
            actor_id=actor_id,
            scope="SCOPE-project-x",
            valid_from="2026-04-01",
        )
        print("link_role_to_actor:", lk)
        assert lk["ok"]
        role_binding_id = lk["binding_id"]

        # 4d. scope-management
        create_scope = get_tool(scope, "create_scope")
        sc = create_scope(
            name="Sprint 42",
            kind="sprint",
            starts_at="2026-04-01",
            ends_at="2026-04-14",
            goals=["Ship lint", "Publish docs-site"],
        )
        print("create_scope:", sc)
        assert "id" in sc and sc["state"] == "planned"
        scope_id = sc["id"]

        transition_scope = get_tool(scope, "transition_scope")
        ts = transition_scope(id=scope_id, to_state="active")
        print("transition_scope active:", ts)
        assert ts["ok"]

        bad_scope_t = transition_scope(id=scope_id, to_state="planned")
        print("bad scope transition (expected error):", bad_scope_t)
        assert "error" in bad_scope_t

        list_scopes = get_tool(scope, "list_scopes")
        ls = list_scopes(kind="sprint")
        print("list_scopes sprint:", len(ls))
        assert any(x["id"] == scope_id for x in ls)

        # 4e. gate-management
        create_gate = get_tool(gate, "create_gate")
        g = create_gate(
            name="code-review",
            description="At least one reviewer has approved the change.",
            kind="manual",
            validator="A second actor reviews and approves.",
            required_roles=[role_id],
            blocking=True,
            evidence_required=True,
        )
        print("create_gate:", g)
        assert "id" in g
        gate_id = g["id"]

        evaluate_gate = get_tool(gate, "evaluate_gate")
        # missing evidence on a gate that requires it
        bad_eval = evaluate_gate(id=gate_id, outcome="passed")
        print("bad evaluate (expected error):", bad_eval)
        assert "error" in bad_eval

        good_eval = evaluate_gate(
            id=gate_id,
            outcome="passed",
            actor=actor_id,
            evidence="https://example.com/pr/42",
        )
        print("good evaluate_gate:", good_eval)
        assert good_eval["ok"] and good_eval["log_id"].startswith("LOG-")

        list_gates = get_tool(gate, "list_gates")
        lg = list_gates(blocking=True)
        print("list_gates blocking:", len(lg))
        assert any(x["id"] == gate_id for x in lg)

        # 4f. discussion-management
        open_disc = get_tool(disc, "open_discussion")
        d = open_disc(
            question="What ID format should processkit-the-repo itself use?",
            participants=[actor_id],
            body="# Discussion body\n\nInitial notes go here.\n",
        )
        print("open_discussion:", d)
        assert "id" in d and d["state"] == "active"
        disc_id = d["id"]

        transition_disc = get_tool(disc, "transition_discussion")
        td = transition_disc(id=disc_id, to_state="resolved")
        print("transition_discussion resolved:", td)
        assert td["ok"]

        add_outcome = get_tool(disc, "add_outcome")
        ao = add_outcome(id=disc_id, decision_id=dec_id)
        print("add_outcome:", ao)
        assert ao["ok"] and dec_id in ao["outcomes"]

        # idempotent
        ao2 = add_outcome(id=disc_id, decision_id=dec_id)
        assert ao2["outcomes"] == ao["outcomes"]

        list_disc = get_tool(disc, "list_discussions")
        ld = list_disc()
        print("list_discussions:", len(ld))
        assert any(x["id"] == disc_id for x in ld)

        # reopening allowed
        td2 = transition_disc(id=disc_id, to_state="active")
        print("reopen discussion:", td2)
        assert td2["ok"]

        # 4g. artifact-management
        create_art = get_tool(art, "create_artifact")
        a_doc = create_art(
            name="Sprint 42 retrospective report",
            kind="document",
            produced_by=wi_id,
            tags=["retro", "sprint-42"],
            description="# Sprint 42 Retro\n\nWhat went well...",
        )
        print("create_artifact (document):", a_doc)
        assert "id" in a_doc and a_doc["id"].startswith("ART-")
        art_id = a_doc["id"]

        a_url = create_art(
            name="Grafana latency dashboard",
            kind="url",
            location="https://grafana.internal/d/api-latency",
            tags=["monitoring"],
        )
        print("create_artifact (url):", a_url)
        assert "id" in a_url

        bad_kind = create_art(name="x", kind="invalid-kind")
        print("bad artifact kind (expected error):", bad_kind)
        assert "error" in bad_kind

        get_art_t = get_tool(art, "get_artifact")
        g_art = get_art_t(id=art_id)
        print("get_artifact:", g_art["name"], g_art["kind"])
        assert g_art["kind"] == "document"
        assert "retro" in g_art["tags"]

        query_art = get_tool(art, "query_artifacts")
        q_docs = query_art(kind="document")
        print("query_artifacts document:", len(q_docs))
        assert any(x["id"] == art_id for x in q_docs)

        q_tagged = query_art(tags=["retro"])
        print("query_artifacts tagged retro:", len(q_tagged))
        assert any(x["id"] == art_id for x in q_tagged)

        update_art = get_tool(art, "update_artifact")
        u = update_art(id=art_id, version="1.0", tags=["retro", "sprint-42", "final"])
        print("update_artifact:", u)
        assert u["ok"]

        g_updated = get_art_t(id=art_id)
        assert g_updated["version"] == "1.0"
        assert "final" in g_updated["tags"]

        def _updated_line(text: str) -> str | None:
            for line in text.splitlines():
                if line.strip().startswith("updated:"):
                    return line.strip()
            return None

        a_url_path = Path(a_url["path"])
        before_touchless = _updated_line(a_url_path.read_text(encoding="utf-8"))
        u_touchless = update_art(
            id=a_url["id"],
            version="1.0",
            touch_updated_at=False,
        )
        print("update_artifact touchless:", u_touchless)
        assert u_touchless["ok"]
        after_touchless = _updated_line(a_url_path.read_text(encoding="utf-8"))
        assert after_touchless == before_touchless

        # 4g.1. v2 workflow/projection helpers
        create_gate_template = get_tool(gate, "create_gate_template")
        gt = create_gate_template(template="interrupt-fire")
        print("create_gate_template interrupt-fire:", gt)
        assert "id" in gt and gt["name"] == "interrupt-fire"

        create_note = get_tool(note, "create_note")
        note_created = create_note(
            title="Investigate provider route budget signal",
            body="Check whether budget bindings feed provider routing.",
            type="question",
            tags=["v2", "budget"],
            slug_summary="investigate provider route budget",
        )
        print("create_note:", note_created)
        assert "id" in note_created

        prepare_inbox_dirs = get_tool(note, "prepare_hook_inbox_dirs")
        inbox_dirs = prepare_inbox_dirs()
        print("prepare_hook_inbox_dirs:", sorted(inbox_dirs["dirs"]))
        assert inbox_dirs["ok"]
        for state in ("inbox", "claimed", "done", "failed"):
            assert (Path(inbox_dirs["dirs"][state])).is_dir()
        bad_inbox_dirs = prepare_inbox_dirs(base_dir="../bad")
        print("prepare_hook_inbox_dirs bad (expected error):", bad_inbox_dirs)
        assert "error" in bad_inbox_dirs

        capture_inbox = get_tool(note, "capture_inbox_item")
        inbox = capture_inbox(
            title="Interrupt current work for budget breach",
            body="Provider route exceeded the configured budget threshold.",
            injection_mode="interrupt",
            channel="smoke-test",
            target_workitem=wi_id,
        )
        print("capture_inbox_item:", inbox)
        assert inbox["inbox"]["status"] == "captured"
        assert inbox["inbox"]["injection_mode"] == "interrupt"

        claim_inbox = get_tool(note, "claim_inbox_item")
        claimed = claim_inbox(id=inbox["id"], actor=actor_id)
        print("claim_inbox_item:", claimed)
        assert claimed["ok"] and claimed["inbox"]["status"] == "claimed"

        complete_inbox = get_tool(note, "complete_inbox_item")
        completed = complete_inbox(
            id=inbox["id"],
            actor=actor_id,
            result={"workitem": wi_id},
        )
        print("complete_inbox_item:", completed)
        assert completed["ok"] and completed["inbox"]["status"] == "completed"

        proc_def = create_art(
            name="Smoke process definition",
            kind="process-definition",
            description="# Smoke process\n\n1. Plan\n2. Execute\n",
        )
        schedule_rule = create_art(
            name="Weekday maintenance window",
            kind="schedule-rule",
            description="RRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR",
        )
        cost_policy = create_art(
            name="Smoke provider budget",
            kind="cost-policy",
            description='{"monthly_cap_usd": 25}',
        )
        assert all("id" in x for x in [proc_def, schedule_rule, cost_policy])

        create_process = get_tool(wi, "create_process_instance")
        proc = create_process(
            title="Run smoke process instance",
            process_definition_artifact=proc_def["id"],
            steps=["Plan smoke run carefully", "Execute smoke run carefully"],
            priority="medium",
        )
        print("create_process_instance:", proc)
        assert "id" in proc and len(proc["children"]) == 2

        create_sep = get_tool(wi, "create_sep_handoff")
        sep = create_sep(
            title="Escalate smoke exception review",
            source_actor=actor_id,
            target="human-review",
            payload={"reason": "smoke-test"},
        )
        print("create_sep_handoff:", sep)
        assert "id" in sep

        create_time_window = get_tool(bind, "create_time_window")
        tw = create_time_window(
            subject=proc["id"],
            target=actor_id,
            recurrence_rule_artifact=schedule_rule["id"],
            description="Smoke process weekday window",
        )
        print("create_time_window:", tw)
        assert "id" in tw

        create_budget = get_tool(bind, "create_budget_application")
        budget = create_budget(
            cost_policy_artifact=cost_policy["id"],
            target="provider-router",
            enforcement_point="provider-router.dispatch",
            cap_usd=25.0,
        )
        print("create_budget_application:", budget)
        assert "id" in budget

        agent_card_art = create_art(
            name="Smoke agent card",
            kind="agent-card",
            description=(
                '{"description":"Smoke agent","capabilities":["tools"],'
                '"endpoints":{"mcp":"stdio"}}'
            ),
        )
        project_card = get_tool(agent_card, "project_agent_card")
        card = project_card(
            artifact_id=agent_card_art["id"],
            output_path=".well-known/smoke-agent-card.json",
        )
        print("project_agent_card:", card["checksum"])
        assert card["written"]
        assert Path(card["output_path"]).is_file()

        (workdir / "context" / "runs").mkdir(parents=True, exist_ok=True)
        (workdir / "context" / "runs" / "run-001.json").write_text(
            '{"id":"run-001","output":"ok"}\n',
            encoding="utf-8",
        )
        collect_runs = get_tool(eval_gate, "collect_run_outputs")
        runs = collect_runs()
        print("collect_run_outputs:", runs)
        assert any(r["path"] == "context/runs/run-001.json" for r in runs)

        codify_eval = get_tool(eval_gate, "codify_eval")
        evspec = codify_eval(
            category_id="smoke",
            name="Smoke output quality",
            eval_kind="llm-as-judge",
            description="Judge whether the smoke output is acceptable.",
            judge="MODEL-smoke-judge",
        )
        print("codify_eval:", evspec)
        assert "artifact_id" in evspec and "gate_id" in evspec

        calibrate = get_tool(eval_gate, "calibrate_judge")
        cal = calibrate(
            judge_id="MODEL-smoke-judge",
            eval_artifact_id=evspec["artifact_id"],
            agreement=0.95,
            sample_n=20,
        )
        print("calibrate_judge:", cal)
        assert cal["ok"]

        bind_eval = get_tool(eval_gate, "bind_eval_to_runs")
        evbind = bind_eval(
            eval_artifact_id=evspec["artifact_id"],
            target="run-output",
            description="Smoke eval binding",
        )
        print("bind_eval_to_runs:", evbind)
        assert "id" in evbind

        ids_rule_art = create_art(
            name="Smoke IDS rule",
            kind="agent-ids-rule",
            description=(
                '{"match":{"tool":"shell"},"action":"alert",'
                '"kprobes":[{"call":"sys_execve","syscall":true}]}'
            ),
        )
        project_ids = get_tool(security, "project_agent_ids_rule")
        ids_proj = project_ids(artifact_id=ids_rule_art["id"])
        print("project_agent_ids_rule:", ids_proj["checksum"])
        assert ids_proj["written"] and Path(ids_proj["output_path"]).is_file()

        project_tetragon = get_tool(security, "project_tetragon_tracing_policy")
        tet_proj = project_tetragon(artifact_id=ids_rule_art["id"])
        print("project_tetragon_tracing_policy:", tet_proj["checksum"])
        assert tet_proj["written"] and Path(tet_proj["output_path"]).is_file()

        # 4h. migration-management
        #     Seed two pending Migration fixtures directly on disk (aibox
        #     sync generates these in real life), then exercise start /
        #     apply / reject through the MCP server to assert:
        #       - state transitions are validated and stamped
        #       - files move between pending/, in-progress/, applied/
        #       - INDEX.md is regenerated with Pending/In Progress/
        #         Applied/Rejected sections
        #       - migration.transitioned / migration.applied /
        #         migration.rejected events land in the log.
        _mig_dir = workdir / "context" / "migrations"
        (_mig_dir / "pending").mkdir(parents=True, exist_ok=True)
        (_mig_dir / "in-progress").mkdir(parents=True, exist_ok=True)
        (_mig_dir / "applied").mkdir(parents=True, exist_ok=True)

        _mig1_id = "MIG-20260420T120000"
        _mig2_id = "MIG-20260420T120001"
        _mig1_path = _mig_dir / "pending" / f"{_mig1_id}.md"
        _mig2_path = _mig_dir / "pending" / f"{_mig2_id}.md"

        _mig1_path.write_text(
            "---\n"
            "apiVersion: processkit.projectious.work/v1\n"
            "kind: Migration\n"
            "metadata:\n"
            f"  id: {_mig1_id}\n"
            "  created: 2026-04-20T12:00:00Z\n"
            "spec:\n"
            "  source: processkit\n"
            "  from_version: v0.18.2\n"
            "  to_version: v0.19.0\n"
            "  state: pending\n"
            "  generated_by: smoke-test\n"
            "  generated_at: 2026-04-20T12:00:00Z\n"
            "  summary: \"smoke: apply happy path\"\n"
            "---\n\n"
            "# Migration apply-happy-path\n\nBody.\n"
        )
        _mig2_path.write_text(
            "---\n"
            "apiVersion: processkit.projectious.work/v1\n"
            "kind: Migration\n"
            "metadata:\n"
            f"  id: {_mig2_id}\n"
            "  created: 2026-04-20T12:00:01Z\n"
            "spec:\n"
            "  source: processkit\n"
            "  from_version: v0.18.2\n"
            "  to_version: v0.19.0\n"
            "  state: pending\n"
            "  generated_by: smoke-test\n"
            "  generated_at: 2026-04-20T12:00:01Z\n"
            "  summary: \"smoke: reject path\"\n"
            "---\n\n"
            "# Migration reject-path\n\nBody.\n"
        )

        list_mig = get_tool(mig, "list_migrations")
        lm = list_mig()
        print("list_migrations (pre):", len(lm))
        assert len(lm) >= 2, f"expected at least 2 migrations, got {lm}"
        assert all(m.get("state") == "pending" for m in lm)

        get_mig = get_tool(mig, "get_migration")
        gm = get_mig(id=_mig1_id)
        print("get_migration:", gm["id"], gm["state"])
        assert gm["id"] == _mig1_id and gm["state"] == "pending"
        assert gm["body"].startswith("\n# Migration apply-happy-path") or (
            "apply-happy-path" in gm["body"]
        )

        # Partial-ID lookup via index fallback — the raw "20260420T120001"
        # word-pair alone should not resolve, but a MIG-prefixed full ID
        # must.  Skip the partial-ID assertion here: the index has not
        # been reindexed in this test yet.

        # Happy path: start then apply
        start_mig = get_tool(mig, "start_migration")
        sm_res = start_mig(id=_mig1_id)
        print("start_migration:", sm_res)
        assert sm_res["ok"] and sm_res["to_state"] == "in-progress"
        assert not _mig1_path.is_file(), "pending file must be removed"
        assert (_mig_dir / "in-progress" / f"{_mig1_id}.md").is_file()

        # Double-start must fail (already moved out of pending)
        sm_bad = start_mig(id=_mig1_id)
        print("start_migration (already started, expect error):", sm_bad)
        assert "error" in sm_bad

        apply_mig = get_tool(mig, "apply_migration")
        am = apply_mig(id=_mig1_id, notes="Smoke test applied this migration.")
        print("apply_migration:", am)
        assert am["ok"] and am["to_state"] == "applied"
        assert not (_mig_dir / "in-progress" / f"{_mig1_id}.md").is_file()
        assert (_mig_dir / "applied" / f"{_mig1_id}.md").is_file()

        # Verify spec now has applied_at + progress_notes
        gm_applied = get_mig(id=_mig1_id)
        assert gm_applied["state"] == "applied"
        assert gm_applied["applied_at"], "applied_at must be stamped"
        assert gm_applied["started_at"], "started_at must be stamped"
        assert any(
            n.get("note", "").startswith("Smoke test applied")
            for n in (gm_applied["progress_notes"] or [])
        ), f"progress_notes missing: {gm_applied['progress_notes']}"

        # Reject path from pending (skips in-progress entirely)
        reject_mig = get_tool(mig, "reject_migration")
        rm = reject_mig(id=_mig2_id, reason="Smoke test rejected this one.")
        print("reject_migration:", rm)
        assert rm["ok"] and rm["to_state"] == "rejected"
        assert not _mig2_path.is_file()
        # Rejected files park under applied/
        assert (_mig_dir / "applied" / f"{_mig2_id}.md").is_file()

        gm_rej = get_mig(id=_mig2_id)
        assert gm_rej["state"] == "rejected"
        assert gm_rej["rejected_reason"] == "Smoke test rejected this one."

        # Reject without a reason must fail
        rm_bad = reject_mig(id=_mig2_id, reason="")
        print("reject_migration empty reason (expected error):", rm_bad)
        assert "error" in rm_bad

        # INDEX.md was regenerated and contains the four sections.
        _mig_index = (_mig_dir / "INDEX.md").read_text()
        print("INDEX.md sections:", [
            ln for ln in _mig_index.splitlines() if ln.startswith("## ")
        ])
        assert "## Pending" in _mig_index
        assert "## In Progress" in _mig_index
        assert "## Applied" in _mig_index
        assert "## Rejected" in _mig_index
        assert _mig1_id in _mig_index
        assert _mig2_id in _mig_index

        # Implicit-start via apply_migration(pending)
        _mig3_id = "MIG-20260420T120002"
        _mig3_path = _mig_dir / "pending" / f"{_mig3_id}.md"
        _mig3_path.write_text(
            "---\n"
            "apiVersion: processkit.projectious.work/v1\n"
            "kind: Migration\n"
            "metadata:\n"
            f"  id: {_mig3_id}\n"
            "  created: 2026-04-20T12:00:02Z\n"
            "spec:\n"
            "  source: processkit\n"
            "  from_version: v0.18.2\n"
            "  to_version: v0.19.0\n"
            "  state: pending\n"
            "  generated_by: smoke-test\n"
            "  generated_at: 2026-04-20T12:00:02Z\n"
            "  summary: \"smoke: implicit-start\"\n"
            "---\n\n"
            "# Migration implicit-start\n\nBody.\n"
        )
        am_implicit = apply_mig(id=_mig3_id)
        print("apply_migration (implicit start):", am_implicit)
        assert am_implicit["ok"]
        assert am_implicit["from_state"] == "pending"
        assert am_implicit["to_state"] == "applied"
        assert (_mig_dir / "applied" / f"{_mig3_id}.md").is_file()

        # Filtered list
        lm_applied = list_mig(state="applied")
        print("list_migrations applied:", [m["id"] for m in lm_applied])
        assert any(m["id"] == _mig1_id for m in lm_applied)
        assert any(m["id"] == _mig3_id for m in lm_applied)
        assert not any(m["id"] == _mig2_id for m in lm_applied)  # rejected

        lm_rejected = list_mig(state="rejected")
        assert any(m["id"] == _mig2_id for m in lm_rejected)

        migrate_v2 = get_tool(mig, "migrate_context_to_v2")
        v2_plan = migrate_v2(dry_run=True)
        print("migrate_context_to_v2 dry run:", v2_plan["changed_count"])
        assert v2_plan["dry_run"] is True
        assert v2_plan["ok"] is True
        assert v2_plan["changed_count"] >= 1
        assert (
            "context/state-machines/smoke.yaml" in v2_plan["changed_paths"]
        ), v2_plan["changed_paths"][:20]

        # Assert migration events landed in the log
        from processkit import index as _index
        _db = _index.open_db()
        try:
            _ev_mig_trans = _index.query_events(
                _db, event_type="migration.transitioned"
            )
            _ev_mig_applied = _index.query_events(
                _db, event_type="migration.applied"
            )
            _ev_mig_rejected = _index.query_events(
                _db, event_type="migration.rejected"
            )
        finally:
            _db.close()
        print("migration.transitioned:", len(_ev_mig_trans))
        print("migration.applied:", len(_ev_mig_applied))
        print("migration.rejected:", len(_ev_mig_rejected))
        # start_migration on _mig1 + implicit start in apply(_mig3) = 2
        assert len(_ev_mig_trans) >= 2, _ev_mig_trans
        # apply on _mig1 + apply on _mig3 = 2
        assert len(_ev_mig_applied) >= 2, _ev_mig_applied
        # reject on _mig2 = 1
        assert len(_ev_mig_rejected) >= 1, _ev_mig_rejected

        print("migration-management smoke test: PASSED")

        # 5. binding
        create_bind = get_tool(bind, "create_binding")
        b = create_bind(
            type="work-assignment",
            subject=wi_id,
            target=actor_id,
            scope="SCOPE-sprint-42",
            valid_from="2026-04-01",
            valid_until="2026-04-14",
            description="Alice owns this for sprint 42",
        )
        print("create_binding:", b)
        assert "id" in b
        bind_id = b["id"]

        resolve = get_tool(bind, "resolve_bindings_for")
        bindings_for_wi = resolve(entity_id=wi_id, at_time="2026-04-06")
        print("bindings for workitem:", bindings_for_wi)
        assert any(x["id"] == bind_id for x in bindings_for_wi)

        # 5b. assert log entries were written as side effects
        # log_side_effect indexes immediately, so we can query without reindex.
        from processkit import index as _index
        _db = _index.open_db()
        try:
            _ev_created = _index.query_events(
                _db,
                event_type="workitem.created",
                subject=wi_id,
            )
            _ev_transitioned = _index.query_events(
                _db,
                event_type="workitem.transitioned",
                subject=wi_id,
            )
            _ev_dec = _index.query_events(_db, event_type="decision.created")
            _ev_scope = _index.query_events(_db, event_type="scope.created")
            _ev_gate = _index.query_events(_db, event_type="gate.created")
            _ev_gate_eval = _index.query_events(
                _db,
                event_type="gate.passed",
                subject=gate_id,
            )
            _ev_disc = _index.query_events(_db, event_type="discussion.opened")
            _ev_art = _index.query_events(_db, event_type="artifact.created")
        finally:
            _db.close()
        print("log side effects — workitem.created:", len(_ev_created))
        print("log side effects — workitem.transitioned:", len(_ev_transitioned))
        print("log side effects — decision.created:", len(_ev_dec))
        print("log side effects — scope.created:", len(_ev_scope))
        print("log side effects — gate.created:", len(_ev_gate))
        print("log side effects — gate.passed:", len(_ev_gate_eval))
        print("log side effects — discussion.opened:", len(_ev_disc))
        print("log side effects — artifact.created:", len(_ev_art))
        assert len(_ev_created) >= 1, "workitem.created log entry missing"
        assert len(_ev_transitioned) >= 1, "workitem.transitioned log entry missing"
        assert len(_ev_dec) >= 1, "decision.created log entry missing"
        assert len(_ev_scope) >= 1, "scope.created log entry missing"
        assert len(_ev_gate) >= 1, "gate.created log entry missing"
        assert len(_ev_gate_eval) >= 1, "gate.passed log entry missing"
        assert len(_ev_disc) >= 1, "discussion.opened log entry missing"
        assert len(_ev_art) >= 1, "artifact.created log entry missing"

        # Systemic self-attribution guard (BACK-20260421_0209-*).
        # Every entity-mutating MCP tool must pass actor=<subject-id> to its
        # log helper so the emitted LogEntry passes schema validation (actor
        # is a required field on LogEntry). Spot-check the four canonical
        # tools: workitem-management create + transition, decision-record
        # record_decision, and discussion-management open_discussion.
        from processkit import entity as _entity_sa, schema as _schema_sa
        _sa_cases = [
            ("workitem.created",      wi_id,   "create_workitem"),
            ("workitem.transitioned", wi_id,   "transition_workitem"),
            ("decision.created",      dec_id,  "record_decision"),
            ("discussion.opened",     disc_id, "open_discussion"),
        ]
        _db_sa = _index.open_db()
        try:
            for _evt, _subj, _label in _sa_cases:
                _rows = _index.query_events(
                    _db_sa,
                    event_type=_evt,
                    subject=_subj,
                )
                assert _rows, (
                    f"{_label}: no {_evt!r} LogEntry found for {_subj!r}"
                )
                _full = _index.get_entity(_db_sa, _rows[0]["id"])
                assert _full and _full.get("path"), (
                    f"{_label}: LogEntry row has no path: {_full}"
                )
                _ent = _entity_sa.load(_full["path"])
                assert _ent.spec.get("actor") == _subj, (
                    f"{_label}: spec.actor={_ent.spec.get('actor')!r} "
                    f"expected {_subj!r} (self-attribution)"
                )
                _errs = _schema_sa.validate_spec("LogEntry", _ent.spec)
                assert _errs == [], (
                    f"{_label}: LogEntry fails schema validation: {_errs}"
                )
        finally:
            _db_sa.close()
        print("systemic self-attribution guard: 4 tools OK")
        # End systemic self-attribution guard.

        # 6. index management
        reindex = get_tool(idx, "reindex")
        stats = reindex()
        print("reindex stats:", stats)
        # workitem + decision + actor + role + role-binding + scope + gate +
        # gate-eval-log + discussion + work-binding + artifacts + migrations
        # + side-effect logs
        assert stats["entities"] >= 13
        assert stats["events"] >= 7, (
            "expected at least 7 events (log side effects), "
            f"got {stats['events']}"
        )

        query_e = get_tool(idx, "query_entities")
        wi_rows = query_e(kind="WorkItem")
        print("query_entities WorkItem:", len(wi_rows))
        wi_row_ids = {row["id"] for row in wi_rows}
        assert wi_id in wi_row_ids
        assert proc["id"] in wi_row_ids
        assert sep["id"] in wi_row_ids
        assert "BACK-template-asset" not in wi_row_ids
        assert len(wi_rows) >= 5

        search = get_tool(idx, "search_entities")
        s = search(text="lint", limit=10)
        print("search lint:", len(s))
        assert any(r["id"] == wi_id for r in s)

        s_phrase = search(text='"Sprint 42"', limit=10)
        print("search Sprint 42 phrase:", len(s_phrase))
        assert any(r["id"] == art_id for r in s_phrase)

        # Hyphen-heavy strings are invalid or surprising in raw FTS5 MATCH
        # syntax; search_entities must preserve the old forgiving LIKE
        # fallback for those agent queries.
        s_fallback = search(text="api-latency", limit=10)
        print("search api-latency fallback:", len(s_fallback))
        assert any(r["id"] == a_url["id"] for r in s_fallback)

        semantic_status = get_tool(idx, "semantic_status")
        sem_status = semantic_status()
        print("semantic status:", sem_status)
        assert sem_status["chunks"] >= stats["entities"]
        assert sem_status["dimensions"] == 128

        semantic = get_tool(idx, "semantic_search_entities")
        sem = semantic(text="sprint retrospective lessons", limit=10)
        print("semantic search:", len(sem), "sqlite_vec:", sem_status["sqlite_vec_available"])
        assert isinstance(sem, list)

        hybrid = get_tool(idx, "hybrid_search_entities")
        h = hybrid(text='"Sprint 42"', limit=10)
        print("hybrid search:", len(h))
        assert any(r["id"] == art_id for r in h)

        events = get_tool(idx, "query_events")
        ev = events(subject=wi_id)
        print("events for wi:", ev)
        assert len(ev) >= 1

        # 7. skill-finder
        find_skill = get_tool(skf, "find_skill")
        list_skills = get_tool(skf, "list_skills")

        fs = find_skill(task_description="create a work item for this bug")
        print("find_skill workitem:", fs)
        assert fs.get("skill") == "workitem-management", (
            f"expected workitem-management, got {fs}"
        )
        assert fs.get("match_confidence", 0) > 0

        fs2 = find_skill(task_description="session start")
        print("find_skill skill-gate:", fs2)
        assert fs2.get("skill") == "skill-gate", (
            f"expected skill-gate, got {fs2}"
        )
        assert fs2.get("match_confidence") == 1.0

        ls = list_skills()
        print("list_skills count:", len(ls))
        # Only skill-finder itself is seeded in this temp workdir
        assert any(s["skill"] == "skill-finder" for s in ls)
        assert all("skill" in s and "has_mcp" in s for s in ls)

        ls_pk = list_skills(category="processkit")
        print("list_skills processkit:", len(ls_pk))
        assert all(s["category"] == "processkit" for s in ls_pk)

        # 8. task-router
        route_task_fn = get_tool(tr, "route_task")

        # 8a. High-confidence workitem route
        rt_wi = route_task_fn(
            task_description="create a work item for the login bug"
        )
        print("route_task workitem:", rt_wi)
        assert rt_wi.get("domain_group") == "workitem", (
            f"expected workitem group, got {rt_wi}"
        )
        assert rt_wi.get("tool") == "create_workitem", (
            f"expected create_workitem, got {rt_wi.get('tool')}"
        )
        assert rt_wi.get("confidence", 0) >= 0.5, (
            f"expected confidence >= 0.5, got {rt_wi.get('confidence')}"
        )
        assert rt_wi.get("routing_basis") == "keyword_match"
        assert rt_wi.get("tool_qualified") == (
            "processkit-workitem-management__create_workitem"
        )
        assert len(rt_wi.get("candidate_tools", [])) >= 1
        # skill_description_excerpt should be populated from seeded SKILL.md
        assert isinstance(rt_wi.get("skill_description_excerpt"), str)

        # 8b. Decision route
        rt_dec = route_task_fn(
            task_description="record a decision about the database schema"
        )
        print("route_task decision:", rt_dec)
        assert rt_dec.get("domain_group") == "decision", (
            f"expected decision group, got {rt_dec}"
        )
        assert rt_dec.get("confidence", 0) > 0

        # 8c. Release task — "plan the release" is a meta-task that maps via
        #     the skill-finder trigger table to release-semver (no single MCP
        #     tool owns it). Expect skill=release-semver and process_override
        #     pointing to the seeded context/processes/release.md.
        #     If the skill-finder table is not seeded in the temp workdir
        #     (only skill-finder SKILL.md is seeded), the router may fall
        #     back to a low-confidence domain match — accept any result that
        #     does not assert a wrong high-confidence match.
        rt_rel = route_task_fn(
            task_description="plan the release and bump the version"
        )
        print("route_task release:", rt_rel)
        # Must not error
        assert "error" not in rt_rel, f"unexpected error: {rt_rel}"
        # If release-semver was matched, process_override must be present
        if rt_rel.get("skill") == "release-semver":
            assert "process_override" in rt_rel, (
                f"expected process_override for release-semver, got {rt_rel}"
            )

        # 8d. Empty input → error
        rt_empty = route_task_fn(task_description="")
        print("route_task empty (expected error):", rt_empty)
        assert "error" in rt_empty

        # 9. skill-gate: acknowledge_contract + check_contract_acknowledged
        # Seed the compliance contract asset so the server can find it.
        _sg_assets_src = (
            PROCESSKIT
            / "src" / "context" / "skills"
            / "processkit" / "skill-gate" / "assets"
        )
        _sg_assets_dst = (
            workdir / "context" / "skills"
            / "processkit" / "skill-gate" / "assets"
        )
        if _sg_assets_src.is_dir():
            shutil.copytree(_sg_assets_src, _sg_assets_dst, dirs_exist_ok=True)

        os.environ["PROCESSKIT_SESSION_ID"] = "smoke-test-session"

        ack_fn = get_tool(sg, "acknowledge_contract")
        check_fn = get_tool(sg, "check_contract_acknowledged")

        # Version mismatch → ok=False, no marker written
        bad_ack = ack_fn(version="v999")
        print("acknowledge_contract bad version (expected ok=false):", bad_ack)
        assert not bad_ack["ok"], f"expected ok=false, got {bad_ack}"
        assert "version mismatch" in bad_ack.get("error", ""), (
            f"expected 'version mismatch' in error, got {bad_ack}"
        )

        # Not yet acknowledged → acknowledged=False
        not_acked = check_fn()
        print("check_contract_acknowledged before ack:", not_acked)
        assert not not_acked["acknowledged"], (
            f"expected acknowledged=false before ack, got {not_acked}"
        )

        # Valid acknowledgement — read current version from the contract asset
        _contract_text = (
            _sg_assets_src / "compliance-contract.md"
        ).read_text() if _sg_assets_src.is_dir() else ""
        import re as _re
        _m = _re.search(r"<!--\s*pk-compliance\s+(v\d+)\s*-->", _contract_text)
        _current_version = _m.group(1) if _m else "v1"
        good_ack = ack_fn(version=_current_version)
        print(f"acknowledge_contract {_current_version}:", good_ack)
        assert good_ack["ok"], f"expected ok=true, got {good_ack}"
        assert "contract_hash" in good_ack
        assert "expires_at" in good_ack
        assert "contract" in good_ack
        # Verify marker file was written
        _marker = (
            workdir / "context" / ".state" / "skill-gate"
            / "session-smoke-test-session.ack"
        )
        assert _marker.is_file(), f"marker file not written: {_marker}"
        import json as _json
        _mdata = _json.loads(_marker.read_text())
        assert "contract_hash" in _mdata and "acknowledged_at" in _mdata, (
            f"marker missing expected fields: {_mdata}"
        )
        print("skill-gate marker file:", _marker.name, "— fields:", list(_mdata))

        # Now acknowledged → acknowledged=True
        acked = check_fn()
        print("check_contract_acknowledged after ack:", acked)
        assert acked["acknowledged"], (
            f"expected acknowledged=true after ack, got {acked}"
        )
        assert acked["contract_hash"] == good_ack["contract_hash"]
        assert acked["session_id"] == "smoke-test-session"
        assert isinstance(acked["age_seconds"], int)

        print("skill-gate smoke test: PASSED")

        # ── 1% rule guard (DEC-20260414_1430-SteelLatch / FEAT-InkStamp) ──────
        # Assert that every locked MCP tool description contains "1% rule".
        # If any description is missing the string, fail loudly so CI catches it.
        _1pct_checks = [
            (tr,   "route_task"),
            (skf,  "find_skill"),
            (wi,   "create_workitem"),
            (wi,   "transition_workitem"),
            (dec,  "record_decision"),
            (elog, "log_event"),
            (disc, "open_discussion"),
            (art,  "create_artifact"),
            (sg,   "acknowledge_contract"),
            (sg,   "check_contract_acknowledged"),
        ]
        _1pct_failures = []
        for _srv_mod, _tool_name in _1pct_checks:
            _tm = _srv_mod.server._tool_manager
            _tool_obj = _tm._tools.get(_tool_name)
            if _tool_obj is None:
                _1pct_failures.append(
                    f"  MISSING TOOL: {_tool_name!r} not found in server"
                )
                continue
            _desc = _tool_obj.description or ""
            if "1% rule" not in _desc:
                _1pct_failures.append(
                    f"  MISSING '1% rule' in description of {_tool_name!r}"
                )
        if _1pct_failures:
            raise AssertionError(
                "1% rule CI guard failed — the following tool descriptions "
                "are missing the literal string '1% rule':\n"
                + "\n".join(_1pct_failures)
                + "\n\nFix: append the canonical 1%-rule sentence to each "
                "tool's docstring in its server.py."
            )
        print(
            "1% rule guard: all 10 locked tools carry the '1% rule' string."
        )
        # End 1% rule guard.

        # BraveBird: reload_schemas live-reload regression guard.
        # Each of the 4 schema-active servers (event-log, workitem,
        # decision-record, artifact-management) must expose a
        # reload_schemas tool that clears the _lib schema + state_machine
        # caches so a disk-level schema edit is visible without a server
        # restart. See DEC-QuickPine + BACK-BraveBird.
        for _srv_obj, _srv_name in [
            (elog, "event-log"),
            (wi, "workitem-management"),
            (dec, "decision-record"),
            (art, "artifact-management"),
        ]:
            _reload = get_tool(_srv_obj, "reload_schemas")
            _result = _reload()
            assert _result.get("ok") is True, (
                f"reload_schemas on {_srv_name}: ok=false, got {_result}"
            )
            assert "cleared" in _result, (
                f"reload_schemas on {_srv_name}: missing 'cleared' field"
            )
            assert set(_result["cleared"].keys()) >= {
                "schemas",
                "state_machines",
            }, (
                f"reload_schemas on {_srv_name}: cleared missing keys, "
                f"got {_result['cleared'].keys()}"
            )
        print(
            "reload_schemas guard: all 4 schema-active servers expose a "
            "callable reload_schemas with correct shape."
        )
        # End BraveBird guard.

        print("\n=== ALL SERVER SMOKE TESTS PASSED ===")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    run()
