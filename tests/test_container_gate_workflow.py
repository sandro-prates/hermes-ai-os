from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml

WORKFLOW_PATH = Path(__file__).resolve().parents[1] / ".github/workflows/container-gate.yml"
CHECKOUT_SHA = "9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0"


def raw() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


def workflow() -> dict[str, Any]:
    loaded = yaml.load(raw(), Loader=yaml.BaseLoader)
    assert isinstance(loaded, dict)
    return loaded


def steps() -> list[dict[str, Any]]:
    return workflow()["jobs"]["container-gate"]["steps"]


def commands() -> str:
    return "\n".join(str(step.get("run", "")) for step in steps())


def test_workflow_exists_and_parses() -> None:
    assert WORKFLOW_PATH.is_file()
    assert workflow()["name"] == "Container Gate"


def test_triggers_and_permissions_are_restricted() -> None:
    triggers = workflow()["on"]
    assert set(triggers) == {"push", "pull_request", "workflow_dispatch"}
    assert triggers["push"] == {"branches": ["main"]}
    assert triggers["pull_request"] == {"branches": ["main"]}
    assert workflow()["permissions"] == {"contents": "read"}
    assert "pull_request_target" not in raw()
    assert not re.search(r"(?m)^\s*[\w-]+:\s*write\s*$", raw().lower())


def test_single_linux_job_with_timeout() -> None:
    jobs = workflow()["jobs"]
    assert set(jobs) == {"container-gate"}
    job = jobs["container-gate"]
    assert job["runs-on"] == "ubuntu-latest"
    assert 15 <= int(job["timeout-minutes"]) <= 20


def test_checkout_is_accepted_pin_without_credentials() -> None:
    checkout = next(step for step in steps() if "actions/checkout@" in step.get("uses", ""))
    assert checkout["uses"] == f"actions/checkout@{CHECKOUT_SHA}"
    assert checkout["with"]["persist-credentials"] == "false"
    assert "# v7.0.0" in raw()


def test_required_container_and_application_checks_exist() -> None:
    text = commands().lower()
    for fragment in (
        "docker build --no-cache", "docker inspect", "docker run", "health",
        "curl --fail", "/api/v1/health", "x-request-id", "read-only", "id -u",
        "pytest", "ruff", "httpx", "uv", "log_format=console", "log_format=json",
        "git diff --exit-code -- .",
    ):
        assert fragment in text


def test_request_id_modes_and_runtime_guards_are_explicit() -> None:
    text = commands().lower()
    assert "generated_request_id" in text
    assert "preserved_request_id" in text
    assert "--user" in text or "user" in text
    assert "read-only" in text or "readonly" in text
    assert "pytest" in text and "ruff" in text and "httpx" in text


def test_cleanup_and_diagnostics_exist() -> None:
    text = commands().lower()
    assert "trap" in text
    assert "docker rm" in text
    assert "docker logs" in text
    assert "docker login" not in text
    assert "docker push" not in text
    for forbidden in (
        "secrets.", "upload-artifact", "download-artifact", "actions/cache", "deploy"
    ):
        assert forbidden not in text
