#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.10"
# dependencies = ["mcp[cli]>=1.0", "pyyaml>=6.0", "jsonschema>=4.0"]
# ///
"""End-to-end smoke test for all 5 processkit MCP servers.

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
from pathlib import Path

PROCESSKIT = Path(__file__).resolve().parent.parent
LIB = PROCESSKIT / "src" / "lib"
sys.path.insert(0, str(LIB))


def import_server(name: str):
    """Import a server.py module by skill name without running its main()."""
    path = PROCESSKIT / "src" / "skills" / name / "mcp" / "server.py"
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
            PROCESSKIT / "src" / "primitives" / "schemas",
            context_root / "schemas",
        )
        shutil.copytree(
            PROCESSKIT / "src" / "primitives" / "state-machines",
            context_root / "state-machines",
        )

        os.chdir(workdir)

        # Clear caches in lib modules so they pick up the new project
        from processkit import paths, schema, state_machine, config, index
        schema.load_schema.cache_clear()
        state_machine.load.cache_clear()
        config.load_config.cache_clear()

        # Import servers
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
        result = create_wi(
            title="Add aibox lint command",
            type="story",
            priority="high",
            description="Walk context/ and validate frontmatter.",
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

        list_roles = get_tool(role, "list_roles")
        lr = list_roles()
        print("list_roles:", len(lr))
        assert any(x["id"] == role_id for x in lr)

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

        # 6. index management
        reindex = get_tool(idx, "reindex")
        stats = reindex()
        print("reindex stats:", stats)
        # workitem + 2 logs + decision + actor + role + role-binding +
        # scope + gate + work-binding
        assert stats["entities"] >= 10
        assert stats["events"] >= 1

        query_e = get_tool(idx, "query_entities")
        wi_rows = query_e(kind="WorkItem")
        print("query_entities WorkItem:", len(wi_rows))
        assert len(wi_rows) == 1

        search = get_tool(idx, "search_entities")
        s = search(text="lint", limit=10)
        print("search lint:", len(s))
        assert any(r["id"] == wi_id for r in s)

        events = get_tool(idx, "query_events")
        ev = events(subject=wi_id)
        print("events for wi:", ev)
        assert len(ev) >= 1

        print("\n=== ALL SERVER SMOKE TESTS PASSED ===")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


if __name__ == "__main__":
    run()
