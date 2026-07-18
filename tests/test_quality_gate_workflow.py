from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

WORKFLOW_PATH = Path(".github/workflows/quality-gate.yml")

EXPECTED_ACTIONS = {
    "actions/checkout": (
        "9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
        "v7.0.0",
    ),
    "actions/setup-python": (
        "ece7cb06caefa5fff74198d8649806c4678c61a1",
        "v6.3.0",
    ),
    "astral-sh/setup-uv": (
        "11f9893b081a58869d3b5fccaea48c9e9e46f990",
        "v8.3.2",
    ),
}

EXPECTED_MATRIX = {
    ("ubuntu-latest", "3.12"),
    ("ubuntu-latest", "3.13"),
    ("ubuntu-latest", "3.14"),
    ("windows-latest", "3.14"),
}


def raw() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def workflow() -> dict[str, Any]:
    loaded = yaml.load(raw(), Loader=yaml.BaseLoader)
    assert isinstance(loaded, dict)
    return loaded


def job() -> dict[str, Any]:
    jobs = workflow()["jobs"]
    assert set(jobs) == {"quality-gate"}
    return jobs["quality-gate"]


def steps() -> list[dict[str, Any]]:
    result = job()["steps"]
    assert isinstance(result, list)
    assert all(isinstance(step, dict) for step in result)
    return result


def action_steps() -> dict[str, dict[str, Any]]:
    found: dict[str, dict[str, Any]] = {}
    for step in steps():
        uses = step.get("uses")
        if isinstance(uses, str):
            action, separator, _ = uses.partition("@")
            assert separator == "@"
            found[action] = step
    return found


def commands() -> str:
    return "\n".join(
        str(step["run"])
        for step in steps()
        if isinstance(step.get("run"), str)
    )


def step_index(fragment: str) -> int:
    for index, step in enumerate(steps()):
        searchable = " ".join(
            str(step.get(key, ""))
            for key in ("name", "uses", "run")
        )
        if fragment in searchable:
            return index
    raise AssertionError(f"Step not found: {fragment}")


def test_workflow_exists_and_parses() -> None:
    assert WORKFLOW_PATH.is_file()
    assert workflow()["name"] == "Quality Gate"


def test_triggers_are_exact() -> None:
    triggers = workflow()["on"]
    assert set(triggers) == {"push", "pull_request", "workflow_dispatch"}
    assert triggers["push"] == {"branches": ["main"]}
    assert triggers["pull_request"] == {"branches": ["main"]}
    assert triggers["workflow_dispatch"] == ""


def test_permissions_are_exactly_read_only() -> None:
    assert workflow()["permissions"] == {"contents": "read"}
    assert not re.search(r"(?m)^\s*[\w-]+\s*:\s*write\s*$", raw().lower())


def test_matrix_and_strategy_are_exact() -> None:
    include = job()["strategy"]["matrix"]["include"]
    combinations = {(item["os"], item["python-version"]) for item in include}
    assert combinations == EXPECTED_MATRIX
    assert len(include) == 4
    assert job()["strategy"]["fail-fast"] == "false"
    assert 15 <= int(job()["timeout-minutes"]) <= 20


@pytest.mark.parametrize(
    ("action", "sha", "version"),
    [
        (name, values[0], values[1])
        for name, values in EXPECTED_ACTIONS.items()
    ],
)
def test_external_action_is_pinned_and_commented(
    action: str,
    sha: str,
    version: str,
) -> None:
    step = action_steps()[action]
    assert step["uses"] == f"{action}@{sha}"
    assert re.fullmatch(r"[0-9a-f]{40}", sha)
    pattern = (
        rf"(?m)^\s*uses:\s*{re.escape(action)}@{sha}"
        rf"\s+#\s+{re.escape(version)}\s*$"
    )
    assert re.search(pattern, raw())


def test_checkout_disables_credentials() -> None:
    checkout = action_steps()["actions/checkout"]
    assert checkout["with"]["persist-credentials"] == "false"


def test_setup_python_uses_matrix_version() -> None:
    setup_python = action_steps()["actions/setup-python"]
    assert setup_python["with"]["python-version"] == "${{ matrix.python-version }}"


def test_setup_uv_is_exact_and_cacheless() -> None:
    setup_uv = action_steps()["astral-sh/setup-uv"]
    assert setup_uv["with"] == {
        "version": "0.11.28",
        "enable-cache": "false",
    }


def test_environment_is_exact() -> None:
    assert job()["env"] == {
        "PYTHONPATH": "apps/backend",
        "UV_EXCLUDE_NEWER": "2026-07-14T11:53:48.187Z",
    }


@pytest.mark.parametrize(
    "required",
    [
        "uv lock --check",
        "uv sync --locked --all-extras",
        "uv run --locked python tools/project_snapshot.py --check",
        "uv run --locked ruff check . --no-cache",
        "uv run --locked python -m pytest -p no:cacheprovider",
        "from app.main import app",
        "git diff --exit-code -- .",
    ],
)
def test_required_command_exists(required: str) -> None:
    assert required in commands()


@pytest.mark.parametrize(
    "forbidden",
    [
        "pull_request_target",
        "write-all",
        "read-all",
        "actions/cache@",
        "upload-artifact",
        "download-artifact",
        "secrets.",
        "deployment",
        "schedule:",
        "workflow_run:",
        "repository_dispatch:",
    ],
)
def test_forbidden_workflow_fragment_is_absent(forbidden: str) -> None:
    assert forbidden not in raw().lower()


@pytest.mark.parametrize(
    "forbidden",
    [
        "twine ",
        "uv publish",
        "pip publish",
        "npm publish",
        "docker push",
        "gh release",
        "ruff format",
        "sed -i",
        "perl -pi",
        "git apply",
    ],
)
def test_forbidden_command_fragment_is_absent(forbidden: str) -> None:
    assert forbidden not in commands().lower()


def test_no_git_write_command_exists() -> None:
    pattern = re.compile(
        r"(?m)\bgit\s+"
        r"(add|commit|push|reset|clean|checkout|restore|"
        r"rebase|pull|merge|tag)\b"
    )
    assert not pattern.search(commands().lower())


def test_uv_lock_is_check_only() -> None:
    lock_lines = [
        line.strip()
        for line in commands().splitlines()
        if line.strip().startswith("uv lock")
    ]
    assert lock_lines == ["uv lock --check"]


def test_ruff_has_no_autofix() -> None:
    text = commands().lower()
    assert "--fix" not in text
    assert "ruff format" not in text


def test_essential_steps_are_ordered() -> None:
    fragments = (
        "actions/checkout@",
        "actions/setup-python@",
        "astral-sh/setup-uv@",
        "uv lock --check",
        "uv sync --locked --all-extras",
        "tools/project_snapshot.py --check",
        "ruff check . --no-cache",
        "python -m pytest -p no:cacheprovider",
        "from app.main import app",
        "git diff --exit-code -- .",
    )
    indices = [step_index(fragment) for fragment in fragments]
    assert indices == sorted(indices)
