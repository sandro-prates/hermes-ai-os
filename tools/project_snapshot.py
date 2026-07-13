"""Generate a deterministic, factual technical snapshot for Hermes AI OS."""

from __future__ import annotations

import argparse
import ast
import hashlib
import os
import re
import subprocess
import sys
import tomllib
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from pathlib import Path

DEFAULT_OUTPUT = Path("docs/PROJECT_SNAPSHOT.md")
SNAPSHOT_SCHEMA_VERSION = 3
CANONICAL_SNAPSHOT_PATH = "docs/PROJECT_SNAPSHOT.md"
NOT_IDENTIFIED = "Não identificado"
NONE = "Nenhum"
EXCLUDED_PARTS = {
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".ruff_cache",
    "node_modules",
    "logs",
}
MAIN_DOCUMENTS = (
    "docs/00_PROJECT_MASTER.md",
    "docs/01_PROJECT_STATE.yaml",
    "docs/02_BACKLOG.md",
    "docs/03_CHANGELOG.md",
)


class SnapshotError(RuntimeError):
    """An internal error that prevents a trustworthy snapshot."""


@dataclass(frozen=True)
class CommandResult:
    """Result of a subprocess, including unavailable commands."""

    args: tuple[str, ...]
    returncode: int | None
    stdout: str = ""
    stderr: str = ""
    unavailable: bool = False

    @property
    def succeeded(self) -> bool:
        return not self.unavailable and self.returncode == 0

    @property
    def failed(self) -> bool:
        return not self.unavailable and self.returncode not in {None, 0}


Runner = Callable[[Sequence[str], Path, dict[str, str] | None], CommandResult]


@dataclass(frozen=True)
class GitState:
    """Observed Git state. None means that Git information was unavailable."""

    branch: str | None
    upstream: str | None
    commit: str | None
    commit_date: str | None
    staged: tuple[str, ...] | None
    unstaged: tuple[str, ...] | None
    untracked: tuple[str, ...] | None
    clean: bool | None
    observed_before_output_write: bool = True


@dataclass(frozen=True)
class QualityState:
    ruff: str
    pytest: str
    application_import: str


@dataclass(frozen=True, order=True)
class TreeEntry:
    path: str
    mode: str
    object_type: str
    object_id: str


@dataclass(frozen=True)
class ProjectedTree:
    entries: tuple[TreeEntry, ...]
    fingerprint: str

    @property
    def paths(self) -> list[str]:
        return [entry.path for entry in self.entries]


def run_command(
    args: Sequence[str],
    root: Path,
    env: dict[str, str] | None = None,
) -> CommandResult:
    """Run a subprocess and preserve success, failure, or unavailability."""
    command = tuple(str(arg) for arg in args)
    try:
        result = subprocess.run(
            command,
            cwd=root,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
        )
    except OSError as error:
        return CommandResult(
            args=command,
            returncode=None,
            stderr=str(error),
            unavailable=True,
        )
    return CommandResult(
        args=command,
        returncode=result.returncode,
        stdout=result.stdout,
        stderr=result.stderr,
    )


def find_git_root(start: Path | None = None, runner: Runner = run_command) -> Path:
    """Locate the Git root from any path inside the worktree."""
    location = (start or Path.cwd()).resolve()
    result = runner(("git", "rev-parse", "--show-toplevel"), location, None)
    if result.unavailable:
        raise SnapshotError(f"Git indisponível: {result.stderr.strip() or NOT_IDENTIFIED}")
    if result.failed or not result.stdout.strip():
        detail = result.stderr.strip() or f"código {result.returncode}"
        raise SnapshotError(f"Não foi possível localizar a raiz Git: {detail}")
    return Path(result.stdout.strip()).resolve()


def is_relevant(path: str) -> bool:
    """Return whether a repository-relative path may enter the snapshot."""
    normalized = path.replace("\\", "/")
    excluded = any(part in EXCLUDED_PARTS for part in Path(normalized).parts)
    return not excluded and not normalized.endswith((".pyc", ".pyo"))


def parse_porcelain(data: str) -> tuple[tuple[str, ...], ...]:
    """Parse Git porcelain v1 -z into staged, unstaged, and untracked paths."""
    staged: set[str] = set()
    unstaged: set[str] = set()
    untracked: set[str] = set()
    entries = data.split("\0")
    index = 0
    while index < len(entries):
        entry = entries[index]
        index += 1
        if not entry:
            continue
        if len(entry) < 4:
            raise SnapshotError("Saída inválida de git status --porcelain.")
        code = entry[:2]
        path = entry[3:].replace("\\", "/")
        if code[0] in {"R", "C"}:
            if index >= len(entries) or not entries[index]:
                raise SnapshotError("Rename/copy incompleto em git status --porcelain.")
            path = entries[index].replace("\\", "/")
            index += 1
        if not is_relevant(path):
            continue
        if code == "??":
            untracked.add(path)
            continue
        if code[0] not in {" ", "?"}:
            staged.add(path)
        if code[1] not in {" ", "?"}:
            unstaged.add(path)
    return tuple(sorted(staged)), tuple(sorted(unstaged)), tuple(sorted(untracked))


def git_value(root: Path, runner: Runner, *args: str) -> str | None:
    result = runner(("git", *args), root, None)
    return result.stdout.strip() if result.succeeded and result.stdout.strip() else None


def relative_output(root: Path, output: Path) -> str | None:
    try:
        return output.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def inspect_git(root: Path, output: Path, runner: Runner = run_command) -> GitState:
    """Inspect Git before writing output, without treating failures as clean."""
    branch = git_value(root, runner, "branch", "--show-current")
    upstream = git_value(root, runner, "rev-parse", "--abbrev-ref", "@{upstream}")
    commit = git_value(root, runner, "log", "-1", "--format=%h %s")
    commit_date = git_value(root, runner, "show", "-s", "--format=%cI", "HEAD")
    status = runner(
        ("git", "status", "--porcelain=v1", "-z", "--untracked-files=all"),
        root,
        None,
    )
    if not status.succeeded:
        return GitState(
            branch=branch,
            upstream=upstream,
            commit=commit,
            commit_date=commit_date,
            staged=None,
            unstaged=None,
            untracked=None,
            clean=None,
        )
    staged, unstaged, untracked = parse_porcelain(status.stdout)
    return GitState(
        branch=branch,
        upstream=upstream,
        commit=commit,
        commit_date=commit_date,
        staged=staged,
        unstaged=unstaged,
        untracked=untracked,
        clean=not (staged or unstaged or untracked),
    )


def parse_scalar(value: str) -> str | bool | int | float | tuple[()] | None:
    value = value.strip()
    if value == "[]":
        return ()
    if value.startswith(("{", "[")):
        raise SnapshotError("Estrutura YAML inline não suportada.")
    if not value or value in {"null", "Null", "NULL", "~"}:
        return None
    if value in {"true", "True", "TRUE"}:
        return True
    if value in {"false", "False", "FALSE"}:
        return False
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def parse_simple_yaml_mapping(text: str) -> dict[tuple[str, ...], object]:
    """Parse strict mapping scalars needed from PROJECT_STATE without PyYAML."""
    values: dict[tuple[str, ...], object] = {}
    stack: list[tuple[int, tuple[str, ...]]] = [(-1, ())]
    ignored_list_indent: int | None = None
    for number, raw_line in enumerate(text.splitlines(), 1):
        if "\t" in raw_line:
            raise SnapshotError(f"PROJECT_STATE contém tab na linha {number}.")
        stripped = raw_line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        if ignored_list_indent is not None:
            if indent > ignored_list_indent or (
                indent == ignored_list_indent and stripped.startswith("-")
            ):
                continue
            ignored_list_indent = None
        if stripped.startswith("-"):
            ignored_list_indent = indent
            continue
        match = re.fullmatch(r"([A-Za-z_][A-Za-z0-9_]*):(?:\s+(.*))?", stripped)
        if not match:
            raise SnapshotError(f"PROJECT_STATE não suportado na linha {number}.")
        key, raw_value = match.groups()
        while stack[-1][0] >= indent:
            stack.pop()
        path = (*stack[-1][1], key)
        if raw_value is None:
            stack.append((indent, path))
            continue
        if path in values:
            raise SnapshotError(f"Campo duplicado em PROJECT_STATE: {'.'.join(path)}")
        values[path] = parse_scalar(raw_value)
    return values


def head_text(root: Path, relative: str, runner: Runner) -> str | None:
    """Read a tracked UTF-8 file exactly as stored in HEAD."""
    result = runner(("git", "show", f"HEAD:{relative}"), root, None)
    return result.stdout if result.succeeded else None


def required_state(root: Path, runner: Runner) -> dict[str, str]:
    text = head_text(root, "docs/01_PROJECT_STATE.yaml", runner)
    if text is None:
        return {
            "project": NOT_IDENTIFIED,
            "epic": NOT_IDENTIFIED,
            "epic_status": NOT_IDENTIFIED,
            "sprint": NOT_IDENTIFIED,
            "sprint_status": NOT_IDENTIFIED,
            "task": NOT_IDENTIFIED,
            "task_status": NOT_IDENTIFIED,
            "active_sprint": NOT_IDENTIFIED,
            "planned_sprint": NOT_IDENTIFIED,
            "next_task": NOT_IDENTIFIED,
            "next_epic": NOT_IDENTIFIED,
            "next_sprint": NOT_IDENTIFIED,
            "next_sprint_status": NOT_IDENTIFIED,
            "next_sprint_objective": NOT_IDENTIFIED,
            "next_sprint_first_task": NOT_IDENTIFIED,
            "next_task_status": NOT_IDENTIFIED,
            "next_sprint_implementation": NOT_IDENTIFIED,
            "functional_item": NOT_IDENTIFIED,
            "functional_item_status": NOT_IDENTIFIED,
        }
    values = parse_simple_yaml_mapping(text)

    def get(path_key: tuple[str, ...]) -> str:
        value = values.get(path_key)
        return NOT_IDENTIFIED if value is None else str(value)

    def required_text(path: tuple[str, ...], label: str) -> str:
        value = values.get(path)
        if not isinstance(value, str) or not value:
            raise SnapshotError(f"PROJECT_STATE possui {label} inválido.")
        return value

    def optional_entity(
        prefix: tuple[str, ...],
        *,
        absent: str,
    ) -> tuple[str, str]:
        scalar = values.get(prefix)
        entity_id = values.get((*prefix, "id"))
        if isinstance(scalar, str) and scalar.casefold() in {"none", "nenhuma"}:
            return absent, "não aplicável"
        if scalar is not None:
            raise SnapshotError(
                f"PROJECT_STATE possui valor ambíguo em {'.'.join(prefix)}."
            )
        if entity_id is None:
            return absent, "não aplicável"
        if not isinstance(entity_id, str) or not entity_id:
            raise SnapshotError(
                f"PROJECT_STATE possui identificador inválido em {'.'.join(prefix)}."
            )
        title = values.get((*prefix, "title"), values.get((*prefix, "name")))
        if not isinstance(title, str) or not title:
            raise SnapshotError(
                f"PROJECT_STATE possui título inválido em {'.'.join(prefix)}."
            )
        status = values.get((*prefix, "status"))
        if not isinstance(status, str) or not status:
            raise SnapshotError(
                f"PROJECT_STATE possui status inválido em {'.'.join(prefix)}."
            )
        return f"{entity_id} — {title}", status

    active_id = values.get(("active_work", "sprint", "id"))
    active_scalar = values.get(("active_work", "sprint"))
    completed_id = values.get(("last_completed_sprint", "sprint", "id"))
    active_fields = any(path[:2] == ("active_work", "sprint") for path in values)
    completed_fields = any(
        path[:2] == ("last_completed_sprint", "sprint") for path in values
    )
    if active_id is None and active_scalar is None and active_fields:
        raise SnapshotError("PROJECT_STATE possui Sprint ativa incompleta.")
    if completed_id is None and completed_fields:
        raise SnapshotError("PROJECT_STATE possui última Sprint concluída incompleta.")
    if active_id is not None:
        sprint_id = required_text(("active_work", "sprint", "id"), "Sprint ativa")
        sprint_title = required_text(
            ("active_work", "sprint", "title"), "título da Sprint ativa"
        )
        sprint_status = required_text(
            ("active_work", "sprint", "status"), "status da Sprint ativa"
        )
        if sprint_status != "in_progress":
            raise SnapshotError(
                "PROJECT_STATE possui Sprint ativa sem status 'in_progress'."
            )
        selected_prefix = ("active_work",)
        selected_kind = "active"
    elif active_scalar not in {None, "none", "nenhuma"}:
        raise SnapshotError("PROJECT_STATE possui active_work.sprint ambíguo.")
    elif completed_id is not None:
        sprint_id = required_text(
            ("last_completed_sprint", "sprint", "id"), "última Sprint concluída"
        )
        sprint_title = required_text(
            ("last_completed_sprint", "sprint", "title"),
            "título da última Sprint concluída",
        )
        sprint_status = required_text(
            ("last_completed_sprint", "sprint", "status"),
            "status da última Sprint concluída",
        )
        if sprint_status != "completed":
            raise SnapshotError(
                "PROJECT_STATE possui última Sprint concluída sem status 'completed'."
            )
        selected_prefix = ("last_completed_sprint",)
        selected_kind = "completed"
    else:
        sprint_id = get(("last_completed_work", "sprint", "id"))
        sprint_title = get(("last_completed_work", "sprint", "title"))
        sprint_status = get(("last_completed_work", "sprint", "status"))
        selected_prefix = ("last_completed_work",)
        selected_kind = "legacy"

    sprint = (
        f"{sprint_id} — {sprint_title}"
        if NOT_IDENTIFIED not in {sprint_id, sprint_title}
        else sprint_id
    )

    if selected_kind == "legacy":
        epic_id = get(("last_completed_work", "epic", "id"))
        epic_name = get(("last_completed_work", "epic", "name"))
        epic = (
            f"{epic_id} — {epic_name}"
            if NOT_IDENTIFIED not in {epic_id, epic_name}
            else NOT_IDENTIFIED
        )
        epic_status = get(("last_completed_work", "epic", "status"))
        if values.get(("current_task", "sprint")) == sprint_id:
            task_id = get(("current_task", "id"))
            task_title = get(("current_task", "title"))
            task = (
                f"{task_id} — {task_title}"
                if NOT_IDENTIFIED not in {task_id, task_title}
                else task_title
            )
            task_status = get(("current_task", "status"))
        else:
            task = "nenhuma Task ou DT formal"
            task_status = "não aplicável"
        functional_item = NOT_IDENTIFIED
        functional_item_status = NOT_IDENTIFIED
        application_import = get(
            ("last_completed_work", "manual_runtime_validation", "result")
        )
    else:
        epic, epic_status = optional_entity(
            (*selected_prefix, "epic"), absent="nenhuma EPIC associada"
        )
        task, task_status = optional_entity(
            (*selected_prefix, "task"), absent="nenhuma Task ou DT formal"
        )
        if selected_kind == "active" and task_status == "não aplicável":
            current_sprint = values.get(("current_task", "sprint"))
            if current_sprint == sprint_id:
                task_id = required_text(("current_task", "id"), "Task ativa")
                task_title = required_text(
                    ("current_task", "title"), "título da Task ativa"
                )
                task_status = required_text(
                    ("current_task", "status"), "status da Task ativa"
                )
                task = f"{task_id} — {task_title}"
        item_value = values.get((*selected_prefix, "functional_item"))
        item_status = values.get((*selected_prefix, "functional_item_status"))
        if (item_value is None) != (item_status is None):
            raise SnapshotError("PROJECT_STATE possui item funcional incompleto.")
        if item_value is None:
            functional_item = NOT_IDENTIFIED
            functional_item_status = NOT_IDENTIFIED
        elif not all(
            isinstance(value, str) and value for value in (item_value, item_status)
        ):
            raise SnapshotError("PROJECT_STATE possui item funcional inválido.")
        else:
            functional_item = item_value
            functional_item_status = item_status
        application_import = get((*selected_prefix, "application_import"))

    planned_paths = {
        "epic_id": ("next_sprint", "epic", "id"),
        "epic_title": ("next_sprint", "epic", "title"),
        "sprint_id": ("next_sprint", "id"),
        "sprint_title": ("next_sprint", "title"),
        "status": ("next_sprint", "status"),
        "objective": ("next_sprint", "objective"),
        "first_task": ("next_sprint", "first_task", "title"),
        "first_task_id": ("next_sprint", "first_task", "id"),
        "implementation_started": ("next_sprint", "implementation_started"),
    }
    present_planned = {
        name: values[path] for name, path in planned_paths.items() if path in values
    }
    planned: dict[str, str] = {
        "next_epic": NOT_IDENTIFIED,
        "next_sprint": NOT_IDENTIFIED,
        "next_sprint_status": NOT_IDENTIFIED,
        "next_sprint_objective": NOT_IDENTIFIED,
        "next_sprint_first_task": NOT_IDENTIFIED,
        "next_task_status": NOT_IDENTIFIED,
        "next_sprint_implementation": NOT_IDENTIFIED,
    }
    if present_planned:
        missing = [name for name in planned_paths if name not in present_planned]
        if missing:
            raise SnapshotError(
                "PROJECT_STATE possui next_sprint incompleto; campos ausentes: "
                + ", ".join(missing)
            )
        strings = {
            name: value
            for name, value in present_planned.items()
            if name != "implementation_started"
        }
        invalid_strings = [
            name for name, value in strings.items() if not isinstance(value, str) or not value
        ]
        if invalid_strings:
            raise SnapshotError(
                "PROJECT_STATE possui campos textuais inválidos em next_sprint: "
                + ", ".join(invalid_strings)
            )
        if strings["status"] != "planned":
            raise SnapshotError(
                "PROJECT_STATE possui status inválido para a próxima Sprint: "
                f"{strings['status']!r}; esperado 'planned'."
            )
        implementation_started = present_planned["implementation_started"]
        if implementation_started is not False:
            raise SnapshotError(
                "PROJECT_STATE não comprova que a próxima Sprint permanece sem "
                "implementação iniciada."
            )
        task_paths = {
            "id": ("next_task", "id"),
            "title": ("next_task", "title"),
            "sprint_id": ("next_task", "sprint"),
            "status": ("next_task", "status"),
        }
        missing_task = [name for name, path in task_paths.items() if path not in values]
        if missing_task:
            raise SnapshotError(
                "PROJECT_STATE possui next_task incompleto; campos ausentes: "
                + ", ".join(missing_task)
            )
        task = {name: values[path] for name, path in task_paths.items()}
        invalid_task = [
            name for name, value in task.items() if not isinstance(value, str) or not value
        ]
        if invalid_task:
            raise SnapshotError(
                "PROJECT_STATE possui campos textuais inválidos em next_task: "
                + ", ".join(invalid_task)
            )
        if task["status"] != "planned":
            raise SnapshotError(
                "PROJECT_STATE possui status inválido para a próxima Task: "
                f"{task['status']!r}; esperado 'planned'."
            )
        expected = {
            "id": strings["first_task_id"],
            "title": strings["first_task"],
            "sprint_id": strings["sprint_id"],
            "status": strings["status"],
        }
        for name, value in task.items():
            if value != expected[name]:
                raise SnapshotError(
                    "PROJECT_STATE possui informação ambígua entre next_sprint e "
                    f"next_task: {name}."
                )
        planned = {
            "next_epic": f"{strings['epic_id']} — {strings['epic_title']}",
            "next_sprint": f"{strings['sprint_id']} — {strings['sprint_title']}",
            "next_sprint_status": strings["status"],
            "next_sprint_objective": strings["objective"],
            "next_sprint_first_task": (
                f"{strings['first_task_id']} — {strings['first_task']}"
            ),
            "next_task_status": task["status"],
            "next_sprint_implementation": "não",
        }
    master = head_text(root, "docs/00_PROJECT_MASTER.md", runner) or ""
    backlog = head_text(root, "docs/02_BACKLOG.md", runner) or ""
    active_sprint = (
        sprint
        if selected_kind == "active"
        else (
            "nenhuma"
            if "> **Sprint atual:** nenhuma" in master
            else NOT_IDENTIFIED
        )
    )
    no_formal_plan = (
        "Os itens abaixo vêm do `PROJECT_MASTER` e ainda não representam Sprints "
        "planejadas ou aprovadas."
    )
    planned_sprint = (
        "nenhuma"
        if active_sprint == "nenhuma"
        and not present_planned
        and no_formal_plan in backlog
        else planned["next_sprint"]
    )
    return {
        "project": get(("project", "name")),
        "epic": epic,
        "epic_status": epic_status,
        "sprint": sprint,
        "sprint_status": sprint_status,
        "task": task,
        "task_status": task_status,
        "functional_item": functional_item,
        "functional_item_status": functional_item_status,
        "active_sprint": active_sprint,
        "planned_sprint": planned_sprint,
        "next_task": get(("next_task", "title")),
        "ruff": get(("quality", "ruff", "result")),
        "pytest": get(("quality", "pytest", "result")),
        "pytest_passed": get(("quality", "pytest", "passed_tests")),
        "pytest_warnings": get(("quality", "pytest", "warnings")),
        "application_import": application_import,
        **planned,
    }


def current_limitations(root: Path, runner: Runner) -> list[str]:
    """Return normalized limitations only when the committed README proves them."""
    readme = head_text(root, "README.md", runner) or ""
    evidence = (
        "Banco de dados, runtime de agentes, memória, dashboard e\n"
        "integrações externas ainda não estão implementados."
    )
    if evidence not in readme:
        return [NOT_IDENTIFIED]
    return [
        "Banco de dados ainda não implementado.",
        "Runtime de agentes ainda não implementado.",
        "Memória ainda não implementada.",
        "Dashboard ainda não implementado.",
        "Integrações externas ainda não implementadas.",
    ]


def request_id_contract_lines(root: Path, runner: Runner) -> list[str]:
    """Describe Request ID behavior only when committed code proves every claim."""
    settings_source = head_text(root, "apps/backend/app/core/settings.py", runner) or ""
    middleware_source = (
        head_text(root, "apps/backend/app/core/observability/middleware.py", runner) or ""
    )
    context_source = (
        head_text(root, "apps/backend/app/core/observability/request_context.py", runner)
        or ""
    )
    filter_source = (
        head_text(root, "apps/backend/app/core/observability/filters.py", runner) or ""
    )
    evidence = (
        'REQUEST_ID_HEADER: str = "X-Request-ID"' in settings_source,
        "headers.get(settings.REQUEST_ID_HEADER) or str(uuid.uuid4())"
        in middleware_source,
        "response_headers[settings.REQUEST_ID_HEADER] = request_id"
        in middleware_source,
        "token = set_request_id(request_id)" in middleware_source,
        "_request_id: ContextVar[str] = ContextVar(" in context_source,
        "record.request_id = get_request_id()" in filter_source,
    )
    if not all(evidence):
        return [NOT_IDENTIFIED]
    return [
        "Header de correlação configurável por `Settings.REQUEST_ID_HEADER`; padrão "
        "`X-Request-ID`.",
        "Request ID gerado automaticamente quando ausente.",
        "Request ID enviado pelo cliente preservado.",
        "Request ID incluído no header da resposta.",
        "Contexto assíncrono de correlação baseado em `ContextVar`.",
        "Request ID do contexto injetado nos registros de log.",
    ]


def settings_contract_lines(
    root: Path,
    paths: list[str],
    runner: Runner,
) -> list[str]:
    """Describe the committed Settings/template contract without loading local env."""
    required_paths = {
        ".env.example",
        "apps/backend/app/core/settings.py",
        "tests/test_env_example.py",
    }
    if not required_paths.issubset(paths):
        return [NOT_IDENTIFIED]

    settings_source = head_text(root, "apps/backend/app/core/settings.py", runner) or ""
    template_source = head_text(root, ".env.example", runner) or ""
    test_source = head_text(root, "tests/test_env_example.py", runner) or ""
    state_source = head_text(root, "docs/01_PROJECT_STATE.yaml", runner) or ""
    try:
        tree = ast.parse(settings_source)
    except SyntaxError as error:
        raise SnapshotError(f"Settings inválido em HEAD: {error}") from error

    settings_class = next(
        (
            node
            for node in tree.body
            if isinstance(node, ast.ClassDef) and node.name == "Settings"
        ),
        None,
    )
    if settings_class is None:
        raise SnapshotError("Classe Settings não identificada em HEAD.")

    field_names: list[str] = []
    aliases: dict[str, str] = {}
    prefix = ""
    case_sensitive: bool | None = None
    for node in settings_class.body:
        if isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            name = node.target.id
            field_names.append(name)
            if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                if node.value.func.id == "Field":
                    for keyword in node.value.keywords:
                        if keyword.arg in {"validation_alias", "alias"}:
                            alias = literal_string(keyword.value)
                            if alias is None:
                                raise SnapshotError(
                                    f"Alias complexo não suportado em Settings.{name}."
                                )
                            aliases[name] = alias
                            break
        if (
            isinstance(node, ast.Assign)
            and any(
                isinstance(target, ast.Name) and target.id == "model_config"
                for target in node.targets
            )
            and isinstance(node.value, ast.Call)
        ):
            for keyword in node.value.keywords:
                if keyword.arg == "env_prefix":
                    value = literal_string(keyword.value)
                    if value is None:
                        raise SnapshotError("env_prefix complexo não suportado em Settings.")
                    prefix = value
                if keyword.arg == "case_sensitive":
                    value = keyword.value
                    if not (
                        isinstance(value, ast.Constant)
                        and isinstance(value.value, bool)
                    ):
                        raise SnapshotError(
                            "case_sensitive deve ser booleano literal em Settings."
                        )
                    case_sensitive = value.value

    if not field_names:
        raise SnapshotError("Campos externos de Settings não identificados.")
    if case_sensitive is None:
        raise SnapshotError(
            "case_sensitive ausente de SettingsConfigDict; default não inferido."
        )
    external_names = [f"{prefix}{aliases.get(name, name)}" for name in field_names]

    template_names: list[str] = []
    for raw_line in template_source.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise SnapshotError("Linha sem '=' identificada em .env.example.")
        template_names.append(line.split("=", 1)[0])
    normalize = (lambda key: key) if case_sensitive else str.casefold

    def normalized_names(names: list[str], source: str) -> dict[str, str]:
        normalized: dict[str, str] = {}
        collisions: list[str] = []
        for name in names:
            key = normalize(name)
            if key in normalized:
                collisions.append(f"{normalized[key]} / {name}")
            else:
                normalized[key] = name
        if collisions:
            raise SnapshotError(
                f"Colisões de chaves em {source}: {', '.join(sorted(collisions))}."
            )
        return normalized

    external_by_key = normalized_names(external_names, "Settings")
    template_by_key = normalized_names(template_names, ".env.example")
    missing = sorted(
        external_by_key[key] for key in external_by_key.keys() - template_by_key.keys()
    )
    additional = sorted(
        template_by_key[key] for key in template_by_key.keys() - external_by_key.keys()
    )
    if missing or additional:
        raise SnapshotError(
            "Contrato de .env.example divergente de Settings: "
            f"ausentes={missing or NONE}; adicionais={additional or NONE}; "
            f"case_sensitive={case_sensitive}."
        )

    state = parse_simple_yaml_mapping(state_source)
    sanitized = state.get(
        ("current_task", "implementation", "env_example_sanitized")
    )
    test_evidence = (
        "assert set(values) == expected_names" in test_source
        and 'Settings(_env_file=ENV_EXAMPLE, _env_file_encoding="utf-8")'
        in test_source
    )
    if sanitized is not True or not test_evidence:
        raise SnapshotError(
            "Sanitização ou validação Pydantic de .env.example não comprovada em HEAD."
        )

    variables = ", ".join(f"`{name}`" for name in external_names)
    sensitivity = "sensível" if case_sensitive else "não sensível"
    return [
        "`.env.example` presente, sanitizado e rastreado na projeção.",
        "Variáveis do template correspondem exatamente aos campos externos "
        "suportados por `Settings`.",
        f"Variáveis suportadas, na ordem declarada em `Settings`: {variables}.",
        "A formação dos nomes externos considera `env_prefix` e aliases simples "
        "(`validation_alias` ou `alias`); os nomes canônicos são preservados na "
        "renderização.",
        f"Comparação de chaves {sensitivity} a maiúsculas e minúsculas, conforme "
        f"`case_sensitive={str(case_sensitive).lower()}`.",
        "Aliases complexos e configurações ambíguas são rejeitados de forma "
        "fail-closed.",
        "Colisões no template ou nos nomes externos de `Settings`, assim como "
        "chaves ausentes, adicionais ou duplicadas, são rejeitadas.",
        "`.env.example` carregado e validado com sucesso por `pydantic-settings`.",
        "Contrato protegido por `tests/test_env_example.py`.",
        "Arquivo `.env` real ausente da projeção rastreada.",
    ]


def load_pyproject(root: Path, runner: Runner) -> dict:
    text = head_text(root, "pyproject.toml", runner)
    if text is None:
        return {}
    try:
        return tomllib.loads(text)
    except tomllib.TOMLDecodeError as error:
        raise SnapshotError(f"pyproject.toml inválido: {error}") from error


def parse_ls_tree(data: str) -> ProjectedTree:
    entries: list[TreeEntry] = []
    for record in data.split("\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split("\t", 1)
            mode, object_type, object_id = metadata.split(" ", 2)
        except ValueError as error:
            raise SnapshotError("Saída inválida de git ls-tree.") from error
        path = raw_path.replace("\\", "/")
        if path == CANONICAL_SNAPSHOT_PATH or not is_relevant(path):
            continue
        if not re.fullmatch(r"[0-7]{6}", mode):
            raise SnapshotError(f"Modo Git inválido em ls-tree: {mode}")
        if object_type not in {"blob", "tree", "commit"}:
            raise SnapshotError(f"Tipo de objeto Git inválido: {object_type}")
        if not re.fullmatch(r"[0-9a-fA-F]{40,64}", object_id):
            raise SnapshotError(f"Object ID inválido em ls-tree: {object_id}")
        entries.append(TreeEntry(path, mode, object_type, object_id.lower()))
    ordered = tuple(sorted(entries))
    normalized = "".join(
        f"{entry.mode} {entry.object_type} {entry.object_id}\t{entry.path}\n"
        for entry in ordered
    ).encode("utf-8")
    fingerprint = hashlib.sha256(normalized).hexdigest()
    return ProjectedTree(ordered, fingerprint)


def collect_projection(root: Path, runner: Runner) -> ProjectedTree:
    result = runner(("git", "ls-tree", "-r", "-z", "--full-tree", "HEAD"), root, None)
    if not result.succeeded:
        detail = result.stderr.strip() or f"código {result.returncode}"
        raise SnapshotError(f"Não foi possível ler a árvore commitada: {detail}")
    return parse_ls_tree(result.stdout)


def collect_paths(root: Path, runner: Runner) -> list[str]:
    return collect_projection(root, runner).paths


def tree_lines(paths: list[str]) -> list[str]:
    tree: dict[str, dict] = {}
    for path in paths:
        node = tree
        for part in path.replace("\\", "/").split("/"):
            node = node.setdefault(part, {})
    lines: list[str] = []

    def visit(node: dict[str, dict], prefix: str = "") -> None:
        items = sorted(node.items(), key=lambda item: (bool(item[1]), item[0].lower()))
        for position, (name, children) in enumerate(items):
            last = position == len(items) - 1
            lines.append(f"{prefix}{'└── ' if last else '├── '}{name}")
            if children:
                visit(children, prefix + ("    " if last else "│   "))

    visit(tree)
    return lines


def read_repository_text(root: Path, relative: str, runner: Runner) -> str:
    if not is_relevant(relative):
        return ""
    return head_text(root, relative, runner) or ""


def python_modules(paths: list[str] | None) -> list[str]:
    if paths is None:
        return []
    modules: set[str] = set()
    prefix = "apps/backend/"
    for path in paths:
        if not path.startswith(prefix) or not path.endswith(".py"):
            continue
        module = path[len(prefix) : -3].replace("/", ".")
        if module.endswith(".__init__"):
            module = module[: -len(".__init__")]
        modules.add(module)
    return sorted(modules)


def literal_string(node: ast.AST | None) -> str | None:
    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None


def fastapi_endpoints(
    root: Path,
    paths: list[str] | None,
    runner: Runner,
) -> list[tuple[str, str, str]]:
    if paths is None:
        return []
    prefixes: dict[tuple[str, str], str] = {}
    includes: list[tuple[tuple[str, str], tuple[str, str]]] = []
    routes: list[tuple[tuple[str, str], str, str, str]] = []
    for relative in paths:
        if not relative.startswith("apps/backend/app/") or not relative.endswith(".py"):
            continue
        module_name = relative[len("apps/backend/") : -3].replace("/", ".")
        if module_name.endswith(".__init__"):
            module_name = module_name[: -len(".__init__")]
        try:
            tree = ast.parse(read_repository_text(root, relative, runner), filename=relative)
        except SyntaxError:
            continue
        aliases: dict[str, tuple[str, str]] = {}
        for node in tree.body:
            if isinstance(node, ast.ImportFrom) and node.module:
                for alias in node.names:
                    aliases[alias.asname or alias.name] = (node.module, alias.name)
            if not isinstance(node, ast.Assign) or len(node.targets) != 1:
                continue
            target = node.targets[0]
            if not isinstance(target, ast.Name) or not isinstance(node.value, ast.Call):
                continue
            if not isinstance(node.value.func, ast.Name) or node.value.func.id != "APIRouter":
                continue
            prefix = ""
            for keyword in node.value.keywords:
                if keyword.arg == "prefix":
                    prefix = literal_string(keyword.value) or ""
            prefixes[(module_name, target.id)] = prefix
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for decorator in node.decorator_list:
                    if not isinstance(decorator, ast.Call) or not isinstance(
                        decorator.func, ast.Attribute
                    ):
                        continue
                    method = decorator.func.attr.upper()
                    if method not in {
                        "GET",
                        "POST",
                        "PUT",
                        "PATCH",
                        "DELETE",
                        "OPTIONS",
                        "HEAD",
                    }:
                        continue
                    if not isinstance(decorator.func.value, ast.Name):
                        continue
                    path = literal_string(decorator.args[0]) if decorator.args else None
                    if path is not None:
                        key = (module_name, decorator.func.value.id)
                        routes.append((key, method, path, relative))
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr != "include_router" or not node.args:
                continue
            if not isinstance(node.func.value, ast.Name) or not isinstance(node.args[0], ast.Name):
                continue
            caller = (module_name, node.func.value.id)
            target_alias = node.args[0].id
            includes.append((caller, aliases.get(target_alias, (module_name, target_alias))))
    mounts: dict[tuple[str, str], str] = {}
    for caller, target in includes:
        if caller not in prefixes:
            mounts.setdefault(target, "")
    for _ in range(len(includes) + 1):
        changed = False
        for caller, target in includes:
            if caller not in mounts:
                continue
            mount = f"{mounts[caller]}{prefixes.get(caller, '')}"
            if mounts.get(target) != mount:
                mounts[target] = mount
                changed = True
        if not changed:
            break
    result = []
    for key, method, path, source in routes:
        full_path = f"{mounts.get(key, '')}{prefixes.get(key, '')}{path}" or "/"
        result.append((method, full_path, source))
    return sorted(set(result))


def summarize_quality(result: CommandResult, tool: str) -> str:
    if result.unavailable:
        return f"Indisponível — {result.stderr.strip() or NOT_IDENTIFIED}"
    combined = f"{result.stdout}\n{result.stderr}"
    if tool == "ruff":
        return (
            "Aprovado — All checks passed!"
            if result.succeeded
            else f"Reprovado — código {result.returncode}"
        )
    passed = re.search(r"(\d+) passed", combined)
    failed = re.search(r"(\d+) failed", combined)
    warnings = re.search(r"(\d+) warning", combined)
    details = []
    if passed:
        details.append(f"{passed.group(1)} aprovado(s)")
    if failed:
        details.append(f"{failed.group(1)} reprovado(s)")
    if warnings:
        details.append(f"{warnings.group(1)} aviso(s)")
    status = "Aprovado" if result.succeeded else "Reprovado"
    return f"{status} — {', '.join(details) or f'código {result.returncode}'}"


def inspect_quality(root: Path, runner: Runner) -> QualityState:
    ruff = runner((sys.executable, "-m", "ruff", "check", "."), root, None)
    pytest = runner((sys.executable, "-m", "pytest"), root, None)
    env = os.environ.copy()
    env["PYTHONPATH"] = str(root / "apps" / "backend") + os.pathsep + env.get(
        "PYTHONPATH", ""
    )
    application = runner(
        (
            sys.executable,
            "-c",
            "from app.main import app; print(type(app).__name__, app.title, app.version)",
        ),
        root,
        env,
    )
    if application.unavailable:
        import_status = f"Indisponível — {application.stderr.strip() or NOT_IDENTIFIED}"
    elif application.succeeded:
        import_status = f"Aprovada — {application.stdout.strip() or 'FastAPI'}"
    else:
        import_status = f"Reprovada — código {application.returncode}"
    return QualityState(
        ruff=summarize_quality(ruff, "ruff"),
        pytest=summarize_quality(pytest, "pytest"),
        application_import=import_status,
    )


def adr_lines(root: Path, paths: list[str] | None, runner: Runner) -> list[str]:
    if paths is None:
        return [f"- {NOT_IDENTIFIED}"]
    result = []
    adr_paths = sorted(
        path for path in paths if path.startswith("docs/adr/ADR-") and path.endswith(".md")
    )
    for relative in adr_paths:
        text = read_repository_text(root, relative, runner)
        title = next(
            (line[2:].strip() for line in text.splitlines() if line.startswith("# ")),
            Path(relative).stem,
        )
        status = re.search(r"(?m)^- \*\*Status:\*\*\s*(.+)$", text)
        result.append(f"- {title} — {status.group(1).strip() if status else NOT_IDENTIFIED}")
    return result or [f"- {NOT_IDENTIFIED}"]


def debt_lines(root: Path, runner: Runner) -> list[str]:
    backlog = read_repository_text(root, "docs/02_BACKLOG.md", runner)
    results = []
    matches = list(re.finditer(r"(?m)^## (DT-\d+ — .+)$", backlog))
    for position, match in enumerate(matches):
        end = matches[position + 1].start() if position + 1 < len(matches) else len(backlog)
        section = backlog[match.end() : end]
        status = re.search(r"\*\*Status:\*\*\s*(.+)", section)
        value = status.group(1).strip() if status else NOT_IDENTIFIED
        if "Resolvida" not in value or "pendente" in value.lower():
            scope = ""
            if (
                "não integra formalmente" in section
                and "não foi ativada automaticamente" in section
            ):
                scope = " — separada do escopo encerrado e não ativada"
            results.append(f"- {match.group(1)} — {value}{scope}")
    return results or [f"- {NOT_IDENTIFIED}"]


def path_bullets(paths: tuple[str, ...] | None) -> str:
    if paths is None:
        return f"- {NOT_IDENTIFIED}"
    if not paths:
        return f"- {NONE}"
    return "\n".join(f"- `{path}`" for path in paths)


def render_snapshot(
    root: Path,
    output: Path,
    runner: Runner = run_command,
) -> str:
    """Build a canonical snapshot from the stable projected Git tree."""
    state = required_state(root, runner)
    pyproject = load_pyproject(root, runner).get("project", {})
    projection = collect_projection(root, runner)
    paths = projection.paths
    modules = python_modules(paths)
    endpoints = fastapi_endpoints(root, paths, runner)
    tree = "\n".join(tree_lines(paths))
    endpoint_text = (
        "\n".join(f"- `{method} {path}` — `{source}`" for method, path, source in endpoints)
        if endpoints
        else f"- {NOT_IDENTIFIED}"
    )
    dependencies = pyproject.get("dependencies", [])
    dependency_text = (
        "\n".join(f"- `{dependency}`" for dependency in dependencies)
        if isinstance(dependencies, list) and dependencies
        else f"- {NOT_IDENTIFIED}"
    )
    module_text = "\n".join(f"- `{module}`" for module in modules) or f"- {NOT_IDENTIFIED}"
    research_path = "docs/research/2026-07-12-stack-tecnologica.md"
    research_content = head_text(root, research_path, runner)
    research_status = (
        "documento de pesquisa tecnológica vazio"
        if research_content == ""
        else NOT_IDENTIFIED
    )
    document_lines = "\n".join(
        f"- `{document}` — {'presente em HEAD' if document in (paths or []) else NOT_IDENTIFIED}"
        for document in MAIN_DOCUMENTS
    )
    next_step = state["next_task"]
    committed_pytest = (
        f"{state['pytest']} — {state['pytest_passed']} aprovado(s), "
        f"{state['pytest_warnings']} aviso(s)"
    )
    observation = (
        "`docs/PROJECT_SNAPSHOT.md` é excluído da projeção para evitar "
        "autorreferência; o estado transitório é exibido somente no console."
    )
    limitation_text = "\n".join(f"- {item}" for item in current_limitations(root, runner))
    request_id_text = "\n".join(
        f"- {item}" for item in request_id_contract_lines(root, runner)
    )
    configuration_contract_text = "\n".join(
        f"- {item}" for item in settings_contract_lines(root, paths, runner)
    )
    planned_details = ""
    if state["planned_sprint"] != "nenhuma" and state["planned_sprint"] != NOT_IDENTIFIED:
        planned_details = (
            f"\n- EPIC planejada: {state['next_epic']}"
            f"\n- Status da Sprint planejada: {state['next_sprint_status']}"
            f"\n- Objetivo: {state['next_sprint_objective']}"
            f"\n- Primeira Task: {state['next_sprint_first_task']}"
            f"\n- Status da Task planejada: {state['next_task_status']}"
            f"\n- Implementação iniciada: {state['next_sprint_implementation']}"
        )
    functional_item_details = ""
    if state["functional_item"] != NOT_IDENTIFIED:
        functional_item_details = (
            f"\n- Item funcional: {state['functional_item']}"
            f"\n- Status do item funcional: {state['functional_item_status']}"
        )
    return f"""# Hermes AI OS  Project Snapshot

## 1. Identificação

- schema do snapshot: {SNAPSHOT_SCHEMA_VERSION}
- fingerprint SHA-256 da árvore projetada: `{projection.fingerprint}`
- arquivos na projeção: {len(projection.entries)}
- projeto: {state['project']}
- versão: {pyproject.get('version', NOT_IDENTIFIED)}
- estado analisado: projeção determinística da árvore commitada
- origem da projeção: entradas rastreadas em HEAD obtidas por `git ls-tree HEAD`
- ordenação da projeção: determinística pelo caminho relativo
- metadados excluídos: branch, upstream, hash, data e mensagem de commit
- observação: {observation}

## 2. Estado Atual

- EPIC: {state['epic']}
- Status da EPIC: {state['epic_status']}
- Sprint: {state['sprint']}
- Status da Sprint: {state['sprint_status']}
- Task: {state['task']}
- Status da Task: {state['task_status']}{functional_item_details}

## 3. Continuidade de Sprint

- Sprint ativa: {state['active_sprint']}
- Próxima Sprint planejada: {state['planned_sprint']}{planned_details}

## 4. Estrutura Relevante

```text
{tree}
```

## 5. Arquitetura Implementada

- Backend FastAPI em `apps/backend/app`.
- Configuração central em `app.core.settings`.
- API versionada em `app.api.v1`.
- Observabilidade central em `app.core.observability`.
- Módulos Python identificados:
{module_text}

## 6. Funcionalidades Verificadas

- Aplicação FastAPI: validação commitada registrada como `{state['application_import']}`.
- Endpoints identificados por inspeção AST do código Python.
- Middleware ASGI e observabilidade presentes no pacote `app.core.observability`.

## 7. Endpoints Identificados

{endpoint_text}

## 8. Configuração e Dependências

- Python requerido: `{pyproject.get('requires-python', NOT_IDENTIFIED)}`.
- Dependências diretas:
{dependency_text}
- Contrato de configuração reproduzível:
{configuration_contract_text}

## 9. Observabilidade

- Pacote: `app.core.observability`.
- Formatos identificados no código: `console` e `json`.
{request_id_text}

## 10. Qualidade

- Ruff: estado commitado `{state['ruff']}`.
- Pytest: estado commitado `{committed_pytest}`.
- importação da aplicação: estado commitado `{state['application_import']}`.

## 11. Documentação e ADRs

{document_lines}

{chr(10).join(adr_lines(root, paths, runner))}

## 12. Problemas Conhecidos

- Aviso de depreciação do `TestClient` relacionado ao `httpx`, não bloqueante.
- {research_status}.

## 13. Dívida Técnica

{chr(10).join(debt_lines(root, runner))}

## 14. Próximo Passo Documentado

{next_step}

## 15. Limitações Atuais

{limitation_text}
"""


def normalize_output(root: Path, value: Path) -> Path:
    return value if value.is_absolute() else root / value


def display_paths(label: str, paths: tuple[str, ...] | None) -> None:
    if paths is None:
        print(f"{label}: {NOT_IDENTIFIED}")
    elif not paths:
        print(f"{label}: {NONE}")
    else:
        print(f"{label}: {', '.join(paths)}")


def show_working_tree(git: GitState, output_relative: str | None) -> None:
    """Show the complete transient state, including the output path."""
    print("Estado transitório observado antes da escrita:")
    display_paths("  staged", git.staged)
    display_paths("  unstaged", git.unstaged)
    display_paths("  untracked", git.untracked)
    if output_relative:
        print(f"  arquivo de saída: {output_relative}")


def relevant_worktree_changes(git: GitState, output_relative: str | None) -> tuple[str, ...] | None:
    """Return changes other than the canonical output, or None when unknown."""
    groups = (git.staged, git.unstaged, git.untracked)
    if any(group is None for group in groups):
        return None
    changes = {
        path
        for group in groups
        if group is not None
        for path in group
        if path != output_relative
    }
    return tuple(sorted(changes))


def ensure_generation_allowed(
    git: GitState,
    output_relative: str | None,
    *,
    audit_working_tree: bool,
) -> None:
    changes = relevant_worktree_changes(git, output_relative)
    if changes is None and not audit_working_tree:
        raise SnapshotError("Estado da working tree indisponível; geração recusada.")
    if changes and not audit_working_tree:
        joined = ", ".join(changes)
        raise SnapshotError(f"Alterações relevantes na working tree: {joined}")


def apply_output(output: Path, expected: str, *, check: bool) -> int:
    """Write only output, or compare it without writing in check mode."""
    expected_bytes = expected.encode("utf-8")
    if check:
        if not output.is_file():
            print(f"Snapshot ausente: {output}", file=sys.stderr)
            return 1
        if output.read_bytes() != expected_bytes:
            print(f"Snapshot desatualizado: {output}", file=sys.stderr)
            return 1
        print(f"Snapshot atualizado: {output}")
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_bytes(expected_bytes)
    print(f"Snapshot gerado: {output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help="Caminho de saída, relativo à raiz Git ou absoluto.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Compara o snapshot sem escrever arquivos.",
    )
    parser.add_argument(
        "--audit-working-tree",
        action="store_true",
        help=(
            "Permite gerar para auditoria mesmo com alterações relevantes; "
            "o conteúdo continua baseado em HEAD."
        ),
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        root = find_git_root()
        output = normalize_output(root, args.output)
        output_relative = relative_output(root, output)
        git = inspect_git(root, output)
        show_working_tree(git, output_relative)
        ensure_generation_allowed(
            git,
            output_relative,
            audit_working_tree=args.audit_working_tree,
        )
        live_quality = inspect_quality(root, run_command)
        print(f"Ruff executado: {live_quality.ruff}")
        print(f"Pytest executado: {live_quality.pytest}")
        print(f"Importação executada: {live_quality.application_import}")
        expected = render_snapshot(root, output)
        return apply_output(output, expected, check=args.check)
    except SnapshotError as error:
        print(f"Falha interna: {error}", file=sys.stderr)
        return 2
    except (OSError, UnicodeError) as error:
        print(f"Falha interna de I/O: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
