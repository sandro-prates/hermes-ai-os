from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCKERFILE = ROOT / "Dockerfile"
DOCKERIGNORE = ROOT / ".dockerignore"

PYTHON_IMAGE = (
    "python:3.14.6-slim-trixie@sha256:"
    "d4fea6e20c09820028eea3f5c17f5b8ebd2ecb9c2bf28e561681a74a96090e4f"
)
UV_IMAGE = (
    "ghcr.io/astral-sh/uv:0.11.28@sha256:"
    "5c3ab83183a73c5d319a77009eb425b60d5bb937f339fb7876788ebf567baf48"
)


def dockerfile() -> str:
    return DOCKERFILE.read_text(encoding="utf-8")


def dockerignore() -> set[str]:
    return {
        line.strip()
        for line in DOCKERIGNORE.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def test_container_files_exist() -> None:
    assert DOCKERFILE.is_file()
    assert DOCKERIGNORE.is_file()


def test_multi_stage_pinned_inputs() -> None:
    text = dockerfile()
    assert text.count("FROM ") == 2
    assert text.count(PYTHON_IMAGE) == 2
    assert UV_IMAGE in text
    assert re.search(r"@sha256:[0-9a-f]{64}", text)
    assert "latest" not in text.lower()


def test_locked_production_dependency_install() -> None:
    text = dockerfile()
    assert "COPY pyproject.toml uv.lock" in text
    assert "uv sync --locked --no-dev --no-editable" in text
    assert "pip install" not in text.lower()
    assert "uv lock" not in text.lower()
    assert "--all-extras" not in text
    assert not re.search(r"(?<!no)--dev\b", text)


def test_runtime_is_explicitly_non_root() -> None:
    text = dockerfile()
    assert re.search(r"groupadd\s+--gid\s+10001", text)
    assert re.search(r"useradd\s+--uid\s+10001\s+--gid\s+10001", text)
    assert "USER 10001:10001" in text


def test_runtime_contract() -> None:
    text = dockerfile()
    assert "HEALTHCHECK" in text
    assert "urllib.request" in text
    assert "EXPOSE 8000" in text
    assert 'CMD ["python", "-m", "uvicorn"' in text
    assert '"--host", "0.0.0.0"' in text
    assert "ADD " not in text
    assert "sudo" not in text.lower()
    assert "secret" not in text.lower()


def test_runtime_copies_only_application_and_environment() -> None:
    text = dockerfile()
    assert "COPY --from=builder --chown=10001:10001 /opt/venv /opt/venv" in text
    assert "COPY --chown=10001:10001 apps/backend /app/apps/backend" in text
    assert "COPY --from=uv" not in text
    assert "COPY tests" not in text
    assert "COPY docs" not in text


def test_dockerignore_protects_sensitive_and_non_runtime_inputs() -> None:
    ignored = dockerignore()
    for required in {
        ".git", ".venv", ".env", ".env.*", "__pycache__", "*.pyc",
        ".pytest_cache", ".ruff_cache", ".coverage", "htmlcov", "logs", "data",
        "temp", "workspace", "docs", "tests", "Hermes-Experiments", "*.zip",
        "*.tar", "*.log",
    }:
        assert required in ignored
    assert {"pyproject.toml", "uv.lock", "apps/backend"}.isdisjoint(ignored)
