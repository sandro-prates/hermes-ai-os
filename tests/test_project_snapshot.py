from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

from tools.project_snapshot import (
    SNAPSHOT_SCHEMA_VERSION,
    CommandResult,
    GitState,
    SnapshotError,
    apply_output,
    collect_paths,
    collect_projection,
    current_limitations,
    ensure_generation_allowed,
    find_git_root,
    inspect_git,
    parse_ls_tree,
    parse_porcelain,
    parse_simple_yaml_mapping,
    render_snapshot,
    required_state,
    settings_contract_lines,
)


def result(
    args: tuple[str, ...],
    *,
    returncode: int | None = 0,
    stdout: str = "",
    stderr: str = "",
    unavailable: bool = False,
) -> CommandResult:
    return CommandResult(args, returncode, stdout, stderr, unavailable)


def test_find_git_root_uses_git_result(tmp_path: Path) -> None:
    root = tmp_path / "repository"
    root.mkdir()

    def runner(args: tuple[str, ...], cwd: Path, env: dict[str, str] | None) -> CommandResult:
        assert args == ("git", "rev-parse", "--show-toplevel")
        assert cwd == tmp_path.resolve()
        assert env is None
        return result(args, stdout=f"{root}\n")

    assert find_git_root(tmp_path, runner) == root.resolve()


def test_find_git_root_reports_subprocess_failure(tmp_path: Path) -> None:
    def runner(args: tuple[str, ...], cwd: Path, env: dict[str, str] | None) -> CommandResult:
        return result(args, returncode=128, stderr="not a git repository")

    with pytest.raises(SnapshotError, match="not a git repository"):
        find_git_root(tmp_path, runner)


def test_parse_clean_status() -> None:
    staged, unstaged, untracked = parse_porcelain("")

    assert staged == ()
    assert unstaged == ()
    assert untracked == ()


def test_parse_staged_unstaged_and_untracked() -> None:
    data = "A  staged.py\0 M changed.py\0?? new.py\0MM both.py\0"

    staged, unstaged, untracked = parse_porcelain(data)

    assert staged == ("both.py", "staged.py")
    assert unstaged == ("both.py", "changed.py")
    assert untracked == ("new.py",)


def test_git_status_failure_is_unknown_not_clean(tmp_path: Path) -> None:
    def runner(args: tuple[str, ...], cwd: Path, env: dict[str, str] | None) -> CommandResult:
        if args[:2] == ("git", "status"):
            return result(args, returncode=128, stderr="status failed")
        return result(args, returncode=128, stderr="unavailable")

    state = inspect_git(tmp_path, tmp_path / "snapshot.md", runner)

    assert state.clean is None
    assert state.staged is None
    assert state.unstaged is None
    assert state.untracked is None


def test_git_state_reports_own_output_explicitly(tmp_path: Path) -> None:
    output = tmp_path / "docs" / "PROJECT_SNAPSHOT.md"

    def runner(args: tuple[str, ...], cwd: Path, env: dict[str, str] | None) -> CommandResult:
        if args[:2] == ("git", "status"):
            data = "?? docs/PROJECT_SNAPSHOT.md\0?? tools/project_snapshot.py\0"
            return result(args, stdout=data)
        return result(args, stdout="value\n")

    state = inspect_git(tmp_path, output, runner)

    assert state.untracked == ("docs/PROJECT_SNAPSHOT.md", "tools/project_snapshot.py")
    assert state.clean is False
    assert state.observed_before_output_write is True


def test_generation_allows_only_own_output() -> None:
    state = GitState(
        "main",
        "origin/main",
        "abc commit",
        "2026-01-01T00:00:00+00:00",
        (),
        (),
        ("docs/PROJECT_SNAPSHOT.md",),
        False,
    )

    ensure_generation_allowed(
        state,
        "docs/PROJECT_SNAPSHOT.md",
        audit_working_tree=False,
    )


def test_generation_refuses_relevant_changes() -> None:
    state = GitState(
        "main",
        "origin/main",
        "abc commit",
        "2026-01-01T00:00:00+00:00",
        (),
        ("README.md",),
        ("docs/PROJECT_SNAPSHOT.md",),
        False,
    )

    with pytest.raises(SnapshotError, match="README.md"):
        ensure_generation_allowed(
            state,
            "docs/PROJECT_SNAPSHOT.md",
            audit_working_tree=False,
        )


def test_audit_option_allows_relevant_changes() -> None:
    state = GitState(None, None, None, None, (), ("README.md",), (), False)

    ensure_generation_allowed(state, None, audit_working_tree=True)


def test_tree_uses_only_tracked_head_files(tmp_path: Path) -> None:
    ignored = tmp_path / ".env.example"
    ignored.write_text("SECRET=local", encoding="utf-8")
    (tmp_path / "untracked.txt").write_text("local", encoding="utf-8")

    def runner(args: tuple[str, ...], cwd: Path, env: dict[str, str] | None) -> CommandResult:
        assert args == ("git", "ls-tree", "-r", "-z", "--full-tree", "HEAD")
        tree = (
            f"100644 blob {'a' * 40}\tREADME.md\0"
            f"100644 blob {'b' * 40}\tapps/backend/app/main.py\0"
        )
        return result(args, stdout=tree)

    paths = collect_paths(tmp_path, runner)

    assert paths == ["README.md", "apps/backend/app/main.py"]
    assert ".env.example" not in paths
    assert "untracked.txt" not in paths


def test_projection_fingerprint_is_normalized_and_excludes_snapshot() -> None:
    data = (
        f"100755 blob {'b' * 40}\tz espaço/ação.py\0"
        f"100644 blob {'c' * 40}\tdocs/PROJECT_SNAPSHOT.md\0"
        f"100644 blob {'a' * 40}\tREADME.md\0"
    )
    expected = (
        f"100644 blob {'a' * 40}\tREADME.md\n"
        f"100755 blob {'b' * 40}\tz espaço/ação.py\n"
    ).encode()

    projection = parse_ls_tree(data)

    assert projection.paths == ["README.md", "z espaço/ação.py"]
    assert len(projection.entries) == 2
    assert projection.fingerprint == hashlib.sha256(expected).hexdigest()


def test_projection_reports_git_ls_tree_failure(tmp_path: Path) -> None:
    def runner(args: tuple[str, ...], cwd: Path, env: dict[str, str] | None) -> CommandResult:
        return result(args, returncode=128, stderr="tree unavailable")

    with pytest.raises(SnapshotError, match="tree unavailable"):
        collect_projection(tmp_path, runner)


def test_completed_readme_task_is_parsed_by_exact_path(tmp_path: Path) -> None:
    state_text = """project:
  name: Hermes AI OS
last_completed_work:
  epic:
    id: EPIC-003
    name: Logging System
    status: completed
  sprint:
    id: SPRINT-02
    title: Logging System
    status: completed
  manual_runtime_validation:
    result: passed
current_task:
  id: TASK-README
  title: README e onboarding reproduzível do Hermes AI OS
  sprint: SPRINT-02
  status: completed
next_task: null
quality:
  pytest:
    result: passed
    passed_tests: 22
    warnings: 1
  ruff:
    result: passed
"""

    def runner(args: tuple[str, ...], cwd: Path, env: dict[str, str] | None) -> CommandResult:
        if args == ("git", "show", "HEAD:docs/01_PROJECT_STATE.yaml"):
            return result(args, stdout=state_text)
        return result(args, returncode=128)

    state = required_state(tmp_path, runner)

    assert (
        state["task"]
        == "TASK-README — README e onboarding reproduzível do Hermes AI OS"
    )
    assert state["epic_status"] == "completed"
    assert state["sprint_status"] == "completed"
    assert state["task_status"] == "completed"
    assert state["next_task"] == "Não identificado"


def planned_state_text(
    *,
    sprint_status: str = "planned",
    task_status: str = "planned",
    first_task_id: str = "DT-008",
    next_task_id: str = "DT-008",
    implementation: str = "false",
) -> str:
    return f"""project:
  name: Hermes AI OS
  phase:
    status: in_progress
last_completed_work:
  epic:
    id: EPIC-003
    name: Logging System
    status: completed
  sprint:
    id: SPRINT-02
    title: Logging System
    status: completed
  manual_runtime_validation:
    result: passed
current_task:
  id: TASK-README
  title: README
  sprint: SPRINT-02
  status: completed
next_sprint:
  id: SPRINT-03
  title: Reproducible Onboarding Baseline
  status: {sprint_status}
  epic:
    id: EPIC-004
    title: Foundation Reproducibility
  objective: Tornar o onboarding reproduzível
  implementation_started: {implementation}
  first_task:
    id: {first_task_id}
    title: Versionar e validar um .env.example sanitizado
next_task:
  id: {next_task_id}
  title: Versionar e validar um .env.example sanitizado
  sprint: SPRINT-03
  status: {task_status}
quality:
  pytest:
    result: passed
    passed_tests: 32
    warnings: 1
  ruff:
    result: passed
"""


def state_runner(text: str):
    def runner(
        args: tuple[str, ...], cwd: Path, env: dict[str, str] | None
    ) -> CommandResult:
        if args == ("git", "show", "HEAD:docs/01_PROJECT_STATE.yaml"):
            return result(args, stdout=text)
        return result(args, returncode=128)

    return runner


def final_state_runner(text: str):
    committed = {
        "docs/01_PROJECT_STATE.yaml": text,
        "docs/00_PROJECT_MASTER.md": "> **Sprint atual:** nenhuma\n",
        "docs/02_BACKLOG.md": (
            "Os itens abaixo vêm do `PROJECT_MASTER` e ainda não representam Sprints "
            "planejadas ou aprovadas.\n"
        ),
        "README.md": (
            "Banco de dados, runtime de agentes, memória, dashboard e\n"
            "integrações externas ainda não estão implementados.\n"
        ),
    }

    def runner(
        args: tuple[str, ...], cwd: Path, env: dict[str, str] | None
    ) -> CommandResult:
        if len(args) == 3 and args[:2] == ("git", "show") and args[2].startswith("HEAD:"):
            path = args[2][len("HEAD:") :]
            if path in committed:
                return result(args, stdout=committed[path])
        return result(args, returncode=128)

    return runner


def completed_state_text() -> str:
    return """project:
  name: Hermes AI OS
last_completed_work:
  epic:
    id: EPIC-004
    name: Foundation Reproducibility
    status: completed
  sprint:
    id: SPRINT-03
    title: Reproducible Onboarding Baseline
    status: completed
  manual_runtime_validation:
    result: passed
current_task:
  id: DT-008
  title: Versionar e validar um .env.example sanitizado
  sprint: SPRINT-03
  status: completed
  implementation:
    env_example_sanitized: true
quality:
  pytest:
    result: passed
    passed_tests: 44
    warnings: 1
  ruff:
    result: passed
"""


def sprint04_completed_state_text() -> str:
    return """project:
  name: Hermes AI OS
last_completed_work:
  epic:
    id: EPIC-004
    name: Foundation Reproducibility
    status: completed
  sprint:
    id: SPRINT-03
    title: Reproducible Onboarding Baseline
    status: completed
  manual_runtime_validation:
    result: passed
current_task:
  id: DT-008
  title: Versionar e validar um .env.example sanitizado
  sprint: SPRINT-03
  status: completed
  implementation:
    env_example_sanitized: true
active_work:
  sprint: none
last_completed_sprint:
  sprint:
    id: SPRINT-04
    title: Foundation Integrity Baseline
    status: completed
  epic: none
  functional_item: Criar testes automatizados da API base
  functional_item_status: completed
  application_import: passed
quality:
  pytest:
    result: passed
    passed_tests: 51
    warnings: 1
  ruff:
    result: passed
"""


def test_last_completed_sprint_precedes_historical_work(tmp_path: Path) -> None:
    state = required_state(
        tmp_path,
        final_state_runner(sprint04_completed_state_text()),
    )

    assert state["sprint"] == "SPRINT-04 — Foundation Integrity Baseline"
    assert state["sprint_status"] == "completed"
    assert state["epic"] == "nenhuma EPIC associada"
    assert state["epic_status"] == "não aplicável"
    assert state["task"] == "nenhuma Task ou DT formal"
    assert state["task_status"] == "não aplicável"
    assert state["functional_item"] == "Criar testes automatizados da API base"
    assert state["functional_item_status"] == "completed"
    assert state["active_sprint"] == "nenhuma"
    assert state["planned_sprint"] == "nenhuma"
    assert "EPIC-004" not in state["epic"]
    assert "DT-008" not in state["task"]


def test_active_sprint_precedes_last_completed_sprint(tmp_path: Path) -> None:
    text = sprint04_completed_state_text().replace(
        "active_work:\n  sprint: none\n",
        """active_work:
  sprint:
    id: SPRINT-ACTIVE
    title: Active Contract Fixture
    status: in_progress
  epic: none
  task:
    id: TASK-ACTIVE
    title: Active Task Fixture
    status: in_progress
""",
    )

    state = required_state(tmp_path, final_state_runner(text))

    assert state["sprint"] == "SPRINT-ACTIVE — Active Contract Fixture"
    assert state["sprint_status"] == "in_progress"
    assert state["active_sprint"] == "SPRINT-ACTIVE — Active Contract Fixture"
    assert state["epic"] == "nenhuma EPIC associada"
    assert state["task"] == "TASK-ACTIVE — Active Task Fixture"
    assert state["task_status"] == "in_progress"


def test_legacy_state_falls_back_to_last_completed_work(tmp_path: Path) -> None:
    state = required_state(tmp_path, final_state_runner(completed_state_text()))

    assert state["sprint"] == "SPRINT-03 — Reproducible Onboarding Baseline"
    assert state["epic"] == "EPIC-004 — Foundation Reproducibility"
    assert state["task"] == "DT-008 — Versionar e validar um .env.example sanitizado"


def test_final_state_is_explicit_and_has_no_active_or_planned_sprint(
    tmp_path: Path,
) -> None:
    runner = final_state_runner(completed_state_text())

    state = required_state(tmp_path, runner)

    assert state["epic"] == "EPIC-004 — Foundation Reproducibility"
    assert state["epic_status"] == "completed"
    assert state["sprint"] == "SPRINT-03 — Reproducible Onboarding Baseline"
    assert state["sprint_status"] == "completed"
    assert state["task"] == "DT-008 — Versionar e validar um .env.example sanitizado"
    assert state["task_status"] == "completed"
    assert state["active_sprint"] == "nenhuma"
    assert state["planned_sprint"] == "nenhuma"


def test_limitations_require_exact_committed_evidence(tmp_path: Path) -> None:
    limitations = current_limitations(tmp_path, final_state_runner(completed_state_text()))

    assert limitations == [
        "Banco de dados ainda não implementado.",
        "Runtime de agentes ainda não implementado.",
        "Memória ainda não implementada.",
        "Dashboard ainda não implementado.",
        "Integrações externas ainda não implementadas.",
    ]


def test_missing_sprint_absence_evidence_is_not_invented(tmp_path: Path) -> None:
    state = required_state(tmp_path, state_runner(completed_state_text()))

    assert state["active_sprint"] == "Não identificado"
    assert state["planned_sprint"] == "Não identificado"


def test_planned_epic_and_sprint_are_parsed_from_exact_paths(tmp_path: Path) -> None:
    state = required_state(tmp_path, state_runner(planned_state_text()))

    assert state["next_epic"] == "EPIC-004 — Foundation Reproducibility"
    assert state["next_sprint"] == "SPRINT-03 — Reproducible Onboarding Baseline"
    assert state["next_sprint_status"] == "planned"
    assert state["next_sprint_objective"] == "Tornar o onboarding reproduzível"
    assert (
        state["next_sprint_first_task"]
        == "DT-008 — Versionar e validar um .env.example sanitizado"
    )
    assert state["next_task_status"] == "planned"
    assert state["next_sprint_implementation"] == "não"


def test_milestone_in_progress_does_not_activate_planned_sprint(tmp_path: Path) -> None:
    state = required_state(tmp_path, state_runner(planned_state_text()))

    assert state["next_sprint_status"] == "planned"
    assert "in_progress" not in state["next_sprint_status"]


def test_partial_planned_sprint_fails_instead_of_inventing_data(tmp_path: Path) -> None:
    text = """project:
  name: Hermes AI OS
next_sprint:
  id: SPRINT-03
  status: planned
"""

    with pytest.raises(SnapshotError, match="next_sprint incompleto"):
        required_state(tmp_path, state_runner(text))


def test_invalid_planned_status_fails_clearly(tmp_path: Path) -> None:
    with pytest.raises(SnapshotError, match="status inválido"):
        required_state(
            tmp_path,
            state_runner(planned_state_text(sprint_status="in_progress")),
        )


def test_invalid_planned_task_status_fails_clearly(tmp_path: Path) -> None:
    with pytest.raises(SnapshotError, match="próxima Task"):
        required_state(
            tmp_path,
            state_runner(planned_state_text(task_status="in_progress")),
        )


def test_started_implementation_fails_instead_of_reporting_planned(tmp_path: Path) -> None:
    with pytest.raises(SnapshotError, match="sem implementação iniciada"):
        required_state(
            tmp_path,
            state_runner(planned_state_text(implementation="true")),
        )


@pytest.mark.parametrize("missing", ["first", "next"])
def test_missing_structured_task_id_fails_clearly(tmp_path: Path, missing: str) -> None:
    text = planned_state_text()
    marker = "    id: DT-008\n" if missing == "first" else "  id: DT-008\n"
    text = text.replace(marker, "", 1)

    with pytest.raises(SnapshotError, match="incompleto"):
        required_state(tmp_path, state_runner(text))


def test_divergent_structured_task_ids_fail_clearly(tmp_path: Path) -> None:
    with pytest.raises(SnapshotError, match="informação ambígua.*id"):
        required_state(
            tmp_path,
            state_runner(planned_state_text(next_task_id="DT-999")),
        )


def test_ambiguous_next_task_fails_clearly(tmp_path: Path) -> None:
    text = planned_state_text().replace(
        "  title: Versionar e validar um .env.example sanitizado\n  sprint:",
        "  title: Outra Task\n  sprint:",
    )

    with pytest.raises(SnapshotError, match="informação ambígua"):
        required_state(tmp_path, state_runner(text))


def test_snapshot_uses_committed_head_and_is_deterministic(tmp_path: Path) -> None:
    committed_state = planned_state_text()
    committed_files = {
        "docs/01_PROJECT_STATE.yaml": committed_state,
        "pyproject.toml": """[project]
name = "hermes-ai-os"
version = "0.0.1"
requires-python = ">=3.12,<3.15"
dependencies = ["fastapi>=0.139,<1.0"]
""",
        "apps/backend/app/main.py": '@app.get("/")\ndef root(): ...\n',
        "docs/02_BACKLOG.md": """# Backlog

## DT-008 — `.env.example` ignorado e ausente do Git

**Status:** ⚠️ Aberta
""",
        "docs/00_PROJECT_MASTER.md": "# Master\n",
        "docs/03_CHANGELOG.md": "# Changelog\n",
        "README.md": (
            "Banco de dados, runtime de agentes, memória, dashboard e\n"
            "integrações externas ainda não estão implementados.\n"
        ),
    }
    tracked = "".join(
        f"100644 blob {index:040x}\t{path}\0"
        for index, path in enumerate(sorted(committed_files), 1)
    )
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs/01_PROJECT_STATE.yaml").write_text(
        "project:\n  name: WRONG WORKTREE VALUE\n",
        encoding="utf-8",
    )
    (tmp_path / ".env.example").write_text("SECRET=ignored", encoding="utf-8")

    def runner(args: tuple[str, ...], cwd: Path, env: dict[str, str] | None) -> CommandResult:
        if args == ("git", "ls-tree", "-r", "-z", "--full-tree", "HEAD"):
            return result(args, stdout=tracked)
        if len(args) == 3 and args[:2] == ("git", "show") and args[2].startswith("HEAD:"):
            relative = args[2][len("HEAD:") :]
            if relative in committed_files:
                return result(args, stdout=committed_files[relative])
            return result(args, returncode=128, stderr="not tracked")
        return result(args, returncode=128, stderr="unexpected command")

    output = tmp_path / "docs/PROJECT_SNAPSHOT.md"
    first = render_snapshot(tmp_path, output, runner)
    second = render_snapshot(tmp_path, output, runner)

    assert first == second
    assert SNAPSHOT_SCHEMA_VERSION == 3
    assert "schema do snapshot: 3" in first
    assert "fingerprint SHA-256" in first
    assert "- Status da EPIC: completed" in first
    assert "- Status da Sprint: completed" in first
    assert "- Status da Task: completed" in first
    assert "\n- status:" not in first
    assert "## 3. Continuidade de Sprint" in first
    assert "- Próxima Sprint planejada: SPRINT-03 — Reproducible Onboarding Baseline" in first
    assert "## 15. Limitações Atuais" in first
    assert "- Banco de dados ainda não implementado." in first
    assert "- Runtime de agentes ainda não implementado." in first
    assert "- Memória ainda não implementada." in first
    assert "- Dashboard ainda não implementado." in first
    assert "- Integrações externas ainda não implementadas." in first
    assert "DT-008 — `.env.example` ignorado e ausente do Git — ⚠️ Aberta" in first
    assert "WRONG WORKTREE VALUE" not in first
    assert "\n├── .env.example" not in first
    assert str(tmp_path) not in first
    assert "working tree: limpa" not in first
    assert "último commit" not in first
    assert "data do commit" not in first


def test_final_markdown_keeps_dt007_as_debt_and_reports_limitations(
    tmp_path: Path,
) -> None:
    committed_files = {
        "docs/01_PROJECT_STATE.yaml": sprint04_completed_state_text(),
        "docs/00_PROJECT_MASTER.md": "> **Sprint atual:** nenhuma\n",
        "docs/02_BACKLOG.md": """# Backlog

## DT-007 — Pesquisa tecnológica vazia

**Status:** ⚠️ Aberta

DT-007 não integra formalmente a EPIC-004 e não foi ativada automaticamente.

# Roadmap de Alto Nível

Os itens abaixo vêm do `PROJECT_MASTER` e ainda não representam Sprints planejadas ou aprovadas.
""",
        "docs/03_CHANGELOG.md": "# Changelog\n",
        "README.md": (
            "Banco de dados, runtime de agentes, memória, dashboard e\n"
            "integrações externas ainda não estão implementados.\n"
        ),
        ".env.example": """APP_NAME=Hermes AI OS
APP_VERSION=0.0.1
ENVIRONMENT=development
DEBUG=true
HOST=127.0.0.1
PORT=8000
log_level=INFO
LOG_FORMAT=console
REQUEST_ID_HEADER=X-Request-ID
""",
        "tests/test_env_example.py": """
assert set(values) == expected_names
loaded = Settings(_env_file=ENV_EXAMPLE, _env_file_encoding="utf-8")
""",
        "apps/backend/app/core/settings.py": """class Settings(BaseSettings):
    APP_NAME: str = "Hermes AI OS"
    APP_VERSION: str = "0.0.1"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "console"
    REQUEST_ID_HEADER: str = "X-Request-ID"
    model_config = SettingsConfigDict(case_sensitive=False, extra="ignore")
""",
        "apps/backend/app/core/observability/middleware.py": """
request_id = headers.get(settings.REQUEST_ID_HEADER) or str(uuid.uuid4())
token = set_request_id(request_id)
response_headers[settings.REQUEST_ID_HEADER] = request_id
""",
        "apps/backend/app/core/observability/request_context.py": (
            "_request_id: ContextVar[str] = ContextVar(\"request_id\")\n"
        ),
        "apps/backend/app/core/observability/filters.py": (
            "record.request_id = get_request_id()\n"
        ),
        "pyproject.toml": """[project]
name = "hermes-ai-os"
version = "0.0.1"
requires-python = ">=3.12,<3.15"
dependencies = []
""",
    }
    tracked = "".join(
        f"100644 blob {index:040x}\t{path}\0"
        for index, path in enumerate(sorted(committed_files), 1)
    )

    def runner(
        args: tuple[str, ...], cwd: Path, env: dict[str, str] | None
    ) -> CommandResult:
        if args == ("git", "ls-tree", "-r", "-z", "--full-tree", "HEAD"):
            return result(args, stdout=tracked)
        if len(args) == 3 and args[:2] == ("git", "show") and args[2].startswith("HEAD:"):
            path = args[2][len("HEAD:") :]
            if path in committed_files:
                return result(args, stdout=committed_files[path])
        return result(args, returncode=128, stderr="not tracked")

    rendered = render_snapshot(tmp_path, tmp_path / "snapshot.md", runner)
    continuity = rendered[
        rendered.index("## 3. Continuidade de Sprint") :
        rendered.index("## 4. Estrutura Relevante")
    ]

    assert "- EPIC: nenhuma EPIC associada" in rendered
    assert "- Status da EPIC: não aplicável" in rendered
    assert "- Sprint: SPRINT-04 — Foundation Integrity Baseline" in rendered
    assert "- Status da Sprint: completed" in rendered
    assert "- Task: nenhuma Task ou DT formal" in rendered
    assert "- Status da Task: não aplicável" in rendered
    assert "- Item funcional: Criar testes automatizados da API base" in rendered
    assert "- Status do item funcional: completed" in rendered
    assert "\n- status:" not in rendered
    assert "- Sprint ativa: nenhuma" in continuity
    assert "- Próxima Sprint planejada: nenhuma" in continuity
    assert "DT-007" not in continuity
    assert (
        "DT-007 — Pesquisa tecnológica vazia — ⚠️ Aberta — separada do escopo "
        "encerrado e não ativada"
    ) in rendered
    assert "- Banco de dados ainda não implementado." in rendered
    assert "- Runtime de agentes ainda não implementado." in rendered
    assert "- Memória ainda não implementada." in rendered
    assert "- Dashboard ainda não implementado." in rendered
    assert "- Integrações externas ainda não implementadas." in rendered
    assert "- Formatos identificados no código: `console` e `json`." in rendered
    assert "Header de correlação configurável por `Settings.REQUEST_ID_HEADER`" in rendered
    assert "- Request ID gerado automaticamente quando ausente." in rendered
    assert "- Request ID enviado pelo cliente preservado." in rendered
    assert "- Request ID incluído no header da resposta." in rendered
    assert "correlação baseado em `ContextVar`" in rendered
    assert "Request ID do contexto injetado nos registros de log." in rendered
    assert "`.env.example` presente, sanitizado e rastreado na projeção." in rendered
    assert "correspondem exatamente aos campos externos suportados por `Settings`" in rendered
    expected_variables = (
        "`APP_NAME`, `APP_VERSION`, `ENVIRONMENT`, `DEBUG`, `HOST`, `PORT`, "
        "`LOG_LEVEL`, `LOG_FORMAT`, `REQUEST_ID_HEADER`"
    )
    assert expected_variables in rendered
    variables_line = next(
        line for line in rendered.splitlines() if line.startswith("- Variáveis suportadas")
    )
    assert variables_line.count("`") == 20
    assert "case_sensitive=false" in rendered
    assert "considera `env_prefix` e aliases simples" in rendered
    assert "nomes canônicos são preservados" in rendered
    assert "Aliases complexos e configurações ambíguas" in rendered
    assert "fail-closed" in rendered
    assert "Colisões no template ou nos nomes externos" in rendered
    assert "chaves ausentes, adicionais ou duplicadas" in rendered
    assert "carregado e validado com sucesso por `pydantic-settings`" in rendered
    assert "Contrato protegido por `tests/test_env_example.py`." in rendered
    assert "Arquivo `.env` real ausente da projeção rastreada." in rendered
    assert "git ls-tree HEAD" in rendered
    assert "entradas rastreadas em HEAD" in rendered
    assert "ordenação da projeção: determinística" in rendered
    assert "branch, upstream, hash, data e mensagem de commit" in rendered
    assert "`docs/PROJECT_SNAPSHOT.md` é excluído da projeção" in rendered
    assert "## 12. Alterações Locais" not in rendered
    canonical_lower = rendered.casefold()
    assert "staged" not in canonical_lower
    assert "unstaged" not in canonical_lower
    assert "untracked" not in canonical_lower

    def settings_contract(settings_source: str, template_source: str) -> list[str]:
        sources = {
            "apps/backend/app/core/settings.py": settings_source,
            ".env.example": template_source,
            "tests/test_env_example.py": """
assert set(values) == expected_names
loaded = Settings(_env_file=ENV_EXAMPLE, _env_file_encoding="utf-8")
""",
            "docs/01_PROJECT_STATE.yaml": completed_state_text(),
        }

        def contract_runner(
            args: tuple[str, ...], cwd: Path, env: dict[str, str] | None
        ) -> CommandResult:
            if (
                len(args) == 3
                and args[:2] == ("git", "show")
                and args[2].startswith("HEAD:")
            ):
                path = args[2][len("HEAD:") :]
                if path in sources:
                    return result(args, stdout=sources[path])
            return result(args, returncode=128)

        return settings_contract_lines(tmp_path, sorted(sources), contract_runner)

    false_settings = """class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    model_config = SettingsConfigDict(case_sensitive=False)
"""
    assert "`LOG_LEVEL`" in "\n".join(
        settings_contract(false_settings, "log_level=INFO\n")
    )

    true_settings = false_settings.replace("False", "True")
    with pytest.raises(SnapshotError, match="divergente"):
        settings_contract(true_settings, "log_level=INFO\n")

    with pytest.raises(SnapshotError, match="Colisões.*env.example"):
        settings_contract(false_settings, "LOG_LEVEL=INFO\nlog_level=DEBUG\n")

    colliding_settings = """class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    log_level: str = "DEBUG"
    model_config = SettingsConfigDict(case_sensitive=False)
"""
    with pytest.raises(SnapshotError, match="Colisões.*Settings"):
        settings_contract(colliding_settings, "LOG_LEVEL=INFO\n")

    prefixed_settings = """class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    model_config = SettingsConfigDict(env_prefix="HERMES_", case_sensitive=False)
"""
    assert "`HERMES_LOG_LEVEL`" in "\n".join(
        settings_contract(prefixed_settings, "hermes_log_level=INFO\n")
    )

    aliased_settings = """class Settings(BaseSettings):
    LOG_LEVEL: str = Field("INFO", validation_alias="LEVEL")
    model_config = SettingsConfigDict(case_sensitive=False)
"""
    assert "`LEVEL`" in "\n".join(
        settings_contract(aliased_settings, "level=INFO\n")
    )

    complex_alias = aliased_settings.replace(
        'validation_alias="LEVEL"',
        'validation_alias=AliasChoices("LEVEL", "LOG_LEVEL")',
    )
    with pytest.raises(SnapshotError, match="Alias complexo"):
        settings_contract(complex_alias, "LEVEL=INFO\n")

    with pytest.raises(SnapshotError, match="ausentes"):
        settings_contract(true_settings, "OTHER=INFO\n")
    with pytest.raises(SnapshotError, match="Colisões"):
        settings_contract(true_settings, "LOG_LEVEL=INFO\nLOG_LEVEL=DEBUG\n")
    with pytest.raises(SnapshotError, match="case_sensitive ausente"):
        settings_contract(
            true_settings.replace("case_sensitive=True", "extra=\"ignore\""),
            "LOG_LEVEL=INFO\n",
        )


def test_simple_yaml_rejects_unsupported_content() -> None:
    with pytest.raises(SnapshotError, match="não suportad"):
        parse_simple_yaml_mapping("project: {name: unsafe-inline-map}\n")


def test_generation_is_deterministic_for_same_state(tmp_path: Path) -> None:
    output = tmp_path / "snapshot.md"
    expected = "# stable\n"

    assert apply_output(output, expected, check=False) == 0
    first = output.read_bytes()
    assert apply_output(output, expected, check=False) == 0

    assert output.read_bytes() == first


def test_generated_content_has_no_absolute_path(tmp_path: Path) -> None:
    output = tmp_path / "snapshot.md"
    expected = "# Snapshot\n- arquivo: `tools/project_snapshot.py`\n"

    apply_output(output, expected, check=False)

    assert str(tmp_path) not in output.read_text(encoding="utf-8")


def test_check_mode_accepts_current_snapshot_without_writing(tmp_path: Path) -> None:
    output = tmp_path / "snapshot.md"
    output.write_text("current\n", encoding="utf-8", newline="\n")
    before = output.stat().st_mtime_ns

    assert apply_output(output, "current\n", check=True) == 0
    assert output.stat().st_mtime_ns == before


def test_check_mode_rejects_stale_snapshot_without_writing(tmp_path: Path) -> None:
    output = tmp_path / "snapshot.md"
    output.write_text("stale\n", encoding="utf-8", newline="\n")

    assert apply_output(output, "current\n", check=True) == 1
    assert output.read_text(encoding="utf-8") == "stale\n"


def test_check_mode_rejects_missing_snapshot(tmp_path: Path) -> None:
    output = tmp_path / "missing.md"

    assert apply_output(output, "current\n", check=True) == 1
    assert not output.exists()


def test_writing_is_restricted_to_selected_output(tmp_path: Path) -> None:
    sentinel = tmp_path / "sentinel.txt"
    sentinel.write_text("unchanged", encoding="utf-8")
    output = tmp_path / "nested" / "snapshot.md"

    assert apply_output(output, "snapshot\n", check=False) == 0

    assert output.read_text(encoding="utf-8") == "snapshot\n"
    assert sentinel.read_text(encoding="utf-8") == "unchanged"
    assert sorted(path.name for path in tmp_path.iterdir()) == ["nested", "sentinel.txt"]


def test_output_is_utf8_without_bom_and_uses_lf(tmp_path: Path) -> None:
    output = tmp_path / "snapshot.md"

    apply_output(output, "ação\nsegunda linha\n", check=False)
    raw = output.read_bytes()

    assert not raw.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in raw
    assert raw.endswith(b"\n")
    assert raw.decode("utf-8") == "ação\nsegunda linha\n"


def test_snapshot_remains_valid_after_its_own_commit(tmp_path: Path) -> None:
    repository = tmp_path / "repositório com espaços"
    repository.mkdir()
    script = Path(__file__).resolve().parents[1] / "tools" / "project_snapshot.py"

    def command(*args: str, expected: int = 0) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            args,
            cwd=repository,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
        assert completed.returncode == expected, completed.stdout + completed.stderr
        return completed

    command("git", "init", "-b", "main")
    command("git", "config", "user.name", "Snapshot Test")
    command("git", "config", "user.email", "snapshot-test@local.invalid")
    (repository / "docs").mkdir()
    (repository / "pasta com espaço").mkdir()
    (repository / ".gitignore").write_text("ignored.tmp\n", encoding="utf-8")
    (repository / "pasta com espaço/ação.txt").write_text("inicial\n", encoding="utf-8")
    (repository / "pyproject.toml").write_text(
        """[project]
name = "snapshot-fixture"
version = "1.0.0"
requires-python = ">=3.12"
dependencies = []
""",
        encoding="utf-8",
    )
    (repository / "docs/01_PROJECT_STATE.yaml").write_text(
        """project:
  name: Snapshot Fixture
last_completed_work:
  epic:
    id: EPIC-TEST
    name: Snapshot
  sprint:
    id: SPRINT-TEST
  manual_runtime_validation:
    result: passed
current_task:
  title: Snapshot
  status: completed
next_task: null
quality:
  pytest:
    result: passed
    passed_tests: 1
    warnings: 0
  ruff:
    result: passed
""",
        encoding="utf-8",
    )
    for name, content in {
        "00_PROJECT_MASTER.md": "# Master\n",
        "02_BACKLOG.md": "# Backlog\n",
        "03_CHANGELOG.md": "# Changelog\n",
    }.items():
        (repository / "docs" / name).write_text(content, encoding="utf-8")
    (repository / "ignored.tmp").write_text("ignored\n", encoding="utf-8")
    command("git", "add", ".")
    command("git", "commit", "-m", "initial projection")

    command(sys.executable, str(script))
    snapshot = repository / "docs/PROJECT_SNAPSHOT.md"
    first_hash = hashlib.sha256(snapshot.read_bytes()).hexdigest()
    command(sys.executable, str(script), "--check")

    command("git", "add", "docs/PROJECT_SNAPSHOT.md")
    command("git", "commit", "-m", "add snapshot only")
    command(sys.executable, str(script), "--check")
    assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == first_hash

    command("git", "commit", "--allow-empty", "-m", "metadata only")
    command(sys.executable, str(script), "--check")

    tracked = repository / "pasta com espaço/ação.txt"
    tracked.write_text("alterado\n", encoding="utf-8")
    command("git", "add", "pasta com espaço/ação.txt")
    command("git", "commit", "-m", "change projected content")
    command(sys.executable, str(script), "--check", expected=1)
    command(sys.executable, str(script))
    command(sys.executable, str(script), "--check")

    snapshot.write_text(snapshot.read_text(encoding="utf-8") + "adulterado\n", encoding="utf-8")
    command(sys.executable, str(script), "--check", expected=1)


def test_git_state_type_documents_unknown_values() -> None:
    state = GitState(None, None, None, None, None, None, None, None)

    assert state.clean is None
