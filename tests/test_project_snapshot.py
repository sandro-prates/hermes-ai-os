from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

import pytest

from tools.project_snapshot import (
    CommandResult,
    GitState,
    SnapshotError,
    apply_output,
    collect_paths,
    collect_projection,
    ensure_generation_allowed,
    find_git_root,
    inspect_git,
    parse_ls_tree,
    parse_porcelain,
    parse_simple_yaml_mapping,
    render_snapshot,
    required_state,
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
  sprint:
    id: SPRINT-02
  manual_runtime_validation:
    result: passed
current_task:
  title: README e onboarding reproduzível do Hermes AI OS
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

    assert state["task"] == "README e onboarding reproduzível do Hermes AI OS"
    assert state["status"] == "completed"
    assert state["next_task"] == "Não identificado"


def test_snapshot_uses_committed_head_and_is_deterministic(tmp_path: Path) -> None:
    committed_state = """project:
  name: Hermes AI OS
last_completed_work:
  epic:
    id: EPIC-003
    name: Logging System
  sprint:
    id: SPRINT-02
  manual_runtime_validation:
    result: passed
current_task:
  title: README e onboarding reproduzível do Hermes AI OS
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
    committed_files = {
        "docs/01_PROJECT_STATE.yaml": committed_state,
        "pyproject.toml": """[project]
name = "hermes-ai-os"
version = "0.0.1"
requires-python = ">=3.12,<3.15"
dependencies = ["fastapi>=0.139,<1.0"]
""",
        "apps/backend/app/main.py": '@app.get("/")\ndef root(): ...\n',
        "docs/02_BACKLOG.md": "# Backlog\n",
        "docs/00_PROJECT_MASTER.md": "# Master\n",
        "docs/03_CHANGELOG.md": "# Changelog\n",
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
    assert "fingerprint SHA-256" in first
    assert "status: completed" in first
    assert "WRONG WORKTREE VALUE" not in first
    assert ".env.example" not in first
    assert str(tmp_path) not in first
    assert "working tree: limpa" not in first
    assert "último commit" not in first
    assert "data do commit" not in first


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
