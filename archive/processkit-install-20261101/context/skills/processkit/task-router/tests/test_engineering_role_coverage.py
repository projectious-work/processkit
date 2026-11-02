"""Tests for BACK-20260510_0344-MerryFox — WildPanda P2 follow-up.

Verifies that every domain group now returns a non-null
`recommended_team_member_slug` in route_task output, and that the 9
newly-added engineering groups resolve to a TeamMember with
`default_role: ROLE-software-engineer` when one is active.

Run with:

    uv run --with pyyaml --with pytest --with mcp \
        pytest context/skills/processkit/task-router/tests/test_engineering_role_coverage.py -v
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import pytest

_REPO_ROOT = Path(__file__).resolve().parents[5]
_SERVER_DIR = _REPO_ROOT / "context" / "skills" / "processkit" / "task-router" / "mcp"
sys.path.insert(0, str(_SERVER_DIR))


def _load_server():
    spec = importlib.util.spec_from_file_location(
        "task_router_server",
        _SERVER_DIR / "server.py",
    )
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------
# GROUP_PREFERRED_ROLE completeness
# ---------------------------------------------------------------------------

def test_all_domain_groups_have_preferred_role_entry():
    """Every domain group in DOMAIN_GROUPS must appear in GROUP_PREFERRED_ROLE.

    This is the structural completeness gate: a missing entry means
    recommended_team_member_slug will always be None for that group.
    """
    server = _load_server()
    uncovered = set(server.DOMAIN_GROUPS.keys()) - set(server.GROUP_PREFERRED_ROLE.keys())
    assert not uncovered, (
        f"Domain groups without a GROUP_PREFERRED_ROLE entry: {uncovered!r}. "
        "Add a mapping in GROUP_PREFERRED_ROLE so sub-agent dispatch always has "
        "a recommended TeamMember."
    )


# ---------------------------------------------------------------------------
# Engineering groups → ROLE-software-engineer
# ---------------------------------------------------------------------------

ENGINEERING_GROUPS = ["event", "actor", "index", "skill", "gate", "model", "id", "role", "binding"]

@pytest.mark.parametrize("group", ENGINEERING_GROUPS)
def test_engineering_group_maps_to_software_engineer_role(group):
    """Each newly-covered engineering group must map to ROLE-software-engineer."""
    server = _load_server()
    role = server.GROUP_PREFERRED_ROLE.get(group)
    assert role == "ROLE-software-engineer", (
        f"Group '{group}' maps to {role!r}; expected 'ROLE-software-engineer'"
    )


# ---------------------------------------------------------------------------
# _recommend_team_member returns non-null for all groups (when roster has members)
# ---------------------------------------------------------------------------

ALL_GROUPS = [
    "workitem", "decision", "discussion", "scope", "retro",  # PM groups
    "event", "actor", "index", "skill", "gate", "model", "id", "role", "binding",  # Engineering
]

@pytest.mark.parametrize("group", ALL_GROUPS)
def test_recommend_team_member_non_null_for_all_groups(group):
    """_recommend_team_member must return a non-null slug for every domain group
    because there is at least one active TeamMember matching each required role.

    PM groups → Cora (ROLE-product-manager).
    Engineering groups → Finn (ROLE-software-engineer).
    """
    server = _load_server()
    slug = server._recommend_team_member(group)
    assert slug is not None, (
        f"_recommend_team_member('{group}') returned None. "
        "Check that an active TeamMember with the matching default_role exists."
    )
    assert isinstance(slug, str) and slug


# ---------------------------------------------------------------------------
# route_task: recommended_team_member_slug is non-null for representative tasks
# ---------------------------------------------------------------------------

REPRESENTATIVE_TASKS = [
    # (task_description, expected_group_hint)
    ("log an audit event for the deployment", "event"),
    ("search the entity index for active scopes", "index"),
    ("find which skill applies to this task", "skill"),
    ("create a quality gate for the release", "gate"),
    ("list models in the registry", "model"),
    ("generate a new processkit ID for the artifact", "id"),
    ("list all roles in the project", "role"),
    ("create a binding between the actor and the scope role", "binding"),
]

@pytest.mark.parametrize("task_desc,expected_group", REPRESENTATIVE_TASKS)
def test_route_task_returns_non_null_slug_for_engineering_tasks(task_desc, expected_group):
    """route_task must return a non-null recommended_team_member_slug for
    tasks that route to engineering domain groups.
    """
    server = _load_server()
    out = server.route_task(task_desc, scoring_mode="token")
    assert "error" not in out, f"Routing failed for task {task_desc!r}: {out}"
    assert "recommended_team_member_slug" in out
    slug = out["recommended_team_member_slug"]
    assert slug is not None, (
        f"recommended_team_member_slug is None for task {task_desc!r} "
        f"(routed to domain_group={out.get('domain_group')!r}). "
        f"Expected group: {expected_group!r}."
    )


# ---------------------------------------------------------------------------
# _recommend_team_member: engineering groups resolve to finn when finn is active
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("group", ENGINEERING_GROUPS)
def test_engineering_group_resolves_to_finn_slug(group):
    """When Finn (ROLE-software-engineer/senior/ai-agent) is active in the roster,
    each engineering group must resolve to 'finn'.
    """
    server = _load_server()
    active_members = server._list_active_team_members()
    finn_present = any(tm["slug"] == "finn" and tm.get("default_role") == "ROLE-software-engineer"
                       for tm in active_members)
    if not finn_present:
        pytest.skip("finn TeamMember not active in this roster; skipping slug-resolution assertion")
    slug = server._recommend_team_member(group)
    assert slug == "finn", (
        f"Expected 'finn' for engineering group '{group}', got {slug!r}"
    )


# ---------------------------------------------------------------------------
# _recommend_team_member: PM groups still resolve to cora
# ---------------------------------------------------------------------------

PM_GROUPS = ["workitem", "decision", "discussion", "scope", "retro"]

@pytest.mark.parametrize("group", PM_GROUPS)
def test_pm_group_still_resolves_to_cora_slug(group):
    """PM groups must still resolve to 'cora' after the engineering extension."""
    server = _load_server()
    active_members = server._list_active_team_members()
    cora_present = any(tm["slug"] == "cora" and tm.get("default_role") == "ROLE-product-manager"
                       for tm in active_members)
    if not cora_present:
        pytest.skip("cora TeamMember not active in this roster; skipping slug-resolution assertion")
    slug = server._recommend_team_member(group)
    assert slug == "cora", (
        f"Expected 'cora' for PM group '{group}', got {slug!r}"
    )
