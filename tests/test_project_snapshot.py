from __future__ import annotations

from pathlib import Path

import pytest

from tools.project_snapshot import (
    CommandResult,
    GitState,
    SnapshotError,
    apply_output,
    find_git_root,
    inspect_git,
    parse_porcelain,
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


def test_git_state_excludes_own_output(tmp_path: Path) -> None:
    output = tmp_path / "docs" / "PROJECT_SNAPSHOT.md"

    def runner(args: tuple[str, ...], cwd: Path, env: dict[str, str] | None) -> CommandResult:
        if args[:2] == ("git", "status"):
            data = "?? docs/PROJECT_SNAPSHOT.md\0?? tools/project_snapshot.py\0"
            return result(args, stdout=data)
        return result(args, stdout="value\n")

    state = inspect_git(tmp_path, output, runner)

    assert state.untracked == ("tools/project_snapshot.py",)
    assert state.clean is False
    assert state.observed_before_output_write is True


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


def test_git_state_type_documents_unknown_values() -> None:
    state = GitState(None, None, None, None, None, None, None, None)

    assert state.clean is None
