from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from tools.project_snapshot import (
    SnapshotError,
    parse_simple_yaml_mapping,
    required_state_v2,
)

PROJECT_STATE = Path(__file__).resolve().parents[1] / "docs/01_PROJECT_STATE.yaml"
LEGACY_OPERATIONAL_ROOTS = {
    "current_task",
    "previous_completed_work",
    "last_completed_work",
    "active_work",
    "last_completed_sprint",
    "dt_007_activated",
}


def load_state() -> dict[str, object]:
    data = yaml.safe_load(PROJECT_STATE.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


def activation_state() -> str:
    return """schema_version: 2
project:
  name: Hermes AI OS
work:
  active:
    sprint:
      id: SPRINT-06
      title: Continuity State Integrity
      status: in_progress
    task:
      id: DT-009
      title: Integridade do estado de continuidade
      status: in_progress
      sprint: SPRINT-06
  last_completed:
    sprint:
      id: SPRINT-05
      title: Technology Decision Baseline
      status: completed
    task:
      id: DT-007
      title: Pesquisa tecnológica
      status: completed
      activated_in_sprint: SPRINT-05
  planned:
    sprint: null
    task: null
quality:
  application_import: passed
  pytest:
    result: passed
    passed_tests: 54
    warnings: 1
  ruff:
    result: passed
"""


def test_real_project_state_uses_only_schema_2_work_contract() -> None:
    state = load_state()

    assert state["schema_version"] == 2
    assert "work" in state
    work = state["work"]
    assert isinstance(work, dict)
    assert set(work) == {"active", "last_completed", "planned"}
    assert LEGACY_OPERATIONAL_ROOTS.isdisjoint(state)
    continuity = state.get("continuity")
    assert isinstance(continuity, dict)
    assert "active_sprint" not in continuity
    assert "next_sprint" not in continuity


def test_real_project_state_has_explicit_active_completed_and_planned_values() -> None:
    state = load_state()

    project = state["project"]
    assert isinstance(project, dict)
    assert project["phase"] == {
        "id": "M1",
        "name": "Infraestrutura",
        "status": "in_progress",
    }

    work = state["work"]
    assert isinstance(work, dict)
    assert set(work) == {"active", "last_completed", "planned"}

    active = work["active"]
    completed = work["last_completed"]
    planned = work["planned"]

    assert isinstance(active, dict)
    assert isinstance(completed, dict)
    assert isinstance(planned, dict)
    assert set(active) == {"sprint", "task"}
    assert set(completed) == {"sprint", "task"}
    assert set(planned) == {"sprint", "task"}

    assert active["sprint"] is None
    assert active["task"] is None
    assert completed["sprint"] == {
        "id": "SPRINT-10",
        "title": "Snapshot Quality Gate Integrity",
        "status": "completed",
    }
    assert completed["task"] is None
    assert planned["sprint"] is None
    assert planned["task"] is None

    quality = state["quality"]
    assert isinstance(quality, dict)
    assert quality["pytest"] == {
        "command": "python -m pytest",
        "result": "passed",
        "collected_tests": 161,
        "passed_tests": 161,
        "warnings": 1,
    }

    documentation = state["documentation"]
    assert isinstance(documentation, dict)
    handoff = documentation["handoff"]
    assert isinstance(handoff, dict)
    assert handoff["path"] == "docs/HANDOFF_2026-07-20-SPRINT-10.md"

    closure = state["sprint_10_closure"]
    assert isinstance(closure, dict)
    assert closure["status"] == "completed"
    assert closure["implementation_commit"] == (
        "513afbaf64b11156d1859ed2bec8c85fff3cac7f"
    )
    assert closure["implementation_snapshot_commit"] == (
        "cb2171f315430c977ca929ffb468363a0d5f079e"
    )
    assert closure["remote_acceptance"] == {
        "quality_gate": {
            "run_id": 29723471112,
            "status": "completed",
            "conclusion": "success",
            "jobs_total": 4,
        },
        "container_gate": {
            "run_id": 29723471158,
            "status": "completed",
            "conclusion": "success",
            "jobs_total": 1,
        },
    }
    assert closure["sprint_11_authorized"] is False


def test_activation_contract_preserves_sprint_05_and_dt_007_as_last_completed() -> None:
    values = parse_simple_yaml_mapping(activation_state())

    rendered = required_state_v2(values)

    assert rendered["sprint"] == "SPRINT-06 — Continuity State Integrity"
    assert rendered["task"] == "DT-009 — Integridade do estado de continuidade"
    assert values[("work", "last_completed", "sprint", "id")] == "SPRINT-05"
    assert values[("work", "last_completed", "task", "id")] == "DT-007"
    assert (
        values[("work", "last_completed", "task", "activated_in_sprint")]
        == "SPRINT-05"
    )


@pytest.mark.parametrize(
    "addition",
    [
        "current_task:\n  id: DT-008\n",
        "dt_007_activated: false\n",
        "active_work:\n  sprint: none\n",
        "last_completed_work:\n  sprint:\n    id: SPRINT-03\n",
        "last_completed_sprint:\n  sprint:\n    id: SPRINT-05\n",
        "continuity:\n  active_sprint: none\n",
        "continuity:\n  next_sprint: none\n",
    ],
)
def test_schema_2_rejects_parallel_legacy_operational_sources(addition: str) -> None:
    values = parse_simple_yaml_mapping(activation_state() + addition)

    with pytest.raises(SnapshotError, match="fontes operacionais legadas"):
        required_state_v2(values)


def test_schema_2_rejects_unknown_work_fields() -> None:
    text = activation_state().replace(
        "  planned:\n", "  unexpected: value\n  planned:\n"
    )

    with pytest.raises(SnapshotError, match="campos desconhecidos em work"):
        required_state_v2(parse_simple_yaml_mapping(text))


def test_schema_2_rejects_sprint_repeated_between_states() -> None:
    text = activation_state().replace("id: SPRINT-05", "id: SPRINT-06").replace(
        "activated_in_sprint: SPRINT-05", "activated_in_sprint: SPRINT-06"
    )

    with pytest.raises(SnapshotError, match="repete uma Sprint"):
        required_state_v2(parse_simple_yaml_mapping(text))


def test_schema_2_rejects_task_associated_with_wrong_sprint() -> None:
    text = activation_state().replace(
        "activated_in_sprint: SPRINT-05", "activated_in_sprint: SPRINT-04"
    )

    with pytest.raises(SnapshotError, match="Sprint errada"):
        required_state_v2(parse_simple_yaml_mapping(text))


def test_schema_2_rejects_incompatible_status() -> None:
    text = activation_state().replace("status: in_progress", "status: completed", 1)

    with pytest.raises(SnapshotError, match="status incompatível"):
        required_state_v2(parse_simple_yaml_mapping(text))
