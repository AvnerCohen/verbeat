#!/usr/bin/env python3

import sys
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from verbeat import (
    VerBeat,
    get_version,
    bump_version,
    get_version_components,
    VerBeatBranchError,
    VerBeatVersionFileError,
)


def test_basic_functionality():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        version_file = temp_path / "verbeat.version"
        with open(version_file, "w") as f:
            f.write("1 # Initial release\n")
            f.write("2 # Breaking API changes\n")

        verbeat = VerBeat(temp_path)

        version = verbeat.get_current_version()
        assert version == "2.2508.0"

        manual, yymm, commits = verbeat.get_version_components()
        assert manual == 2
        assert yymm == "2508"
        assert commits == 0

        history = verbeat.get_version_history()
        assert history == [(1, "Initial release"), (2, "Breaking API changes")]

        new_version = verbeat.bump_manual_version("Test bump")
        assert new_version == 3

        with open(version_file, "r") as f:
            content = f.read()
            assert "3 # Test bump" in content


def test_convenience_functions():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        version_file = temp_path / "verbeat.version"
        with open(version_file, "w") as f:
            f.write("1 # Initial release\n")

        version = get_version(temp_path)
        assert version == "1.2508.0"

        manual, yymm, commits = get_version_components(temp_path)
        assert manual == 1
        assert yymm == "2508"
        assert commits == 0

        new_version = bump_version("Test", temp_path)
        assert new_version == 2


def test_date_specific_version():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        version_file = temp_path / "verbeat.version"
        with open(version_file, "w") as f:
            f.write("1 # Initial release\n")

        test_date = datetime(2025, 7, 15)
        version = get_version(temp_path, test_date)
        assert version == "1.2507.0"


def test_error_handling():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        with pytest.raises(VerBeatVersionFileError):
            verbeat = VerBeat(temp_path)
            verbeat.get_current_version()

        version_file = temp_path / "verbeat.version"
        with open(version_file, "w") as f:
            f.write("")

        with pytest.raises(VerBeatVersionFileError):
            verbeat = VerBeat(temp_path)
            verbeat.get_current_version()


def test_branch_restriction():
    """Test branch restriction functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        import subprocess

        subprocess.run(["git", "init"], cwd=temp_path, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Test User"], cwd=temp_path, check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=temp_path,
            check=True,
        )

        (temp_path / "verbeat.version").write_text("1 # Initial release\n")
        subprocess.run(["git", "add", "verbeat.version"], cwd=temp_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"], cwd=temp_path, check=True
        )

        subprocess.run(
            ["git", "checkout", "-b", "feature-branch"], cwd=temp_path, check=True
        )

        from verbeat import VerBeat

        verbeat = VerBeat(temp_path)

        try:
            verbeat.bump_manual_version("Test bump")
            print("  ✗ Branch restriction test failed: should have raised error")
        except VerBeatBranchError as e:
            print(f"  ✓ Correctly raised VerBeatBranchError: {e}")


def test_init_command():
    """Test init command functionality."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        from verbeat import init_project

        init_project("Test project initialization", str(temp_path))

        version_file = temp_path / "verbeat.version"
        assert version_file.exists()
        assert version_file.read_text().strip() == "1 # Test project initialization"

        from verbeat import VerBeat

        verbeat = VerBeat(temp_path)
        assert verbeat.get_current_version() == "1.2508.0"


def test_init_command_existing_file():
    """Test init command when verbeat.version already exists."""
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        (temp_path / "verbeat.version").write_text("1 # Existing file\n")

        from verbeat import init_project

        init_project("Should not overwrite", str(temp_path))

        version_file = temp_path / "verbeat.version"
        assert version_file.read_text().strip() == "1 # Existing file"


def test_tag_based_version():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        version_file = temp_path / "verbeat.version"
        with open(version_file, "w") as f:
            f.write("1 # Initial release\n")

        import subprocess

        subprocess.run(["git", "init"], cwd=temp_path, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Test User"], cwd=temp_path, check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=temp_path,
            check=True,
        )

        subprocess.run(["git", "add", "verbeat.version"], cwd=temp_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"], cwd=temp_path, check=True
        )

        subprocess.run(
            [
                "git",
                "tag",
                "-a",
                "v1.2508.5",
                "-m",
                "VerBeat 1.2508.5 (2025-08-15): Test tag",
            ],
            cwd=temp_path,
            check=True,
        )

        verbeat = VerBeat(temp_path)

        version = verbeat.get_current_version()
        assert version == "1.2508.5"

        manual, yymm, commits = verbeat.get_version_components()
        assert (manual, yymm, commits) == (1, "2508", 5)


def test_get_calculated_version_ignores_tags(tmp_path):
    """Test that get_calculated_version ignores existing tags."""
    project_root = tmp_path / "project"
    project_root.mkdir()

    verbeat_file = project_root / "verbeat.version"
    verbeat_file.write_text("2 # Test project\n")

    git_dir = project_root / ".git"
    git_dir.mkdir()

    subprocess.run(["git", "init"], cwd=project_root, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=project_root, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=project_root,
        check=True,
    )

    for i in range(5):
        test_file = project_root / f"file{i}.txt"
        test_file.write_text(f"content {i}")
        subprocess.run(["git", "add", str(test_file)], cwd=project_root, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"commit {i}"], cwd=project_root, check=True
        )

    subprocess.run(
        ["git", "tag", "-a", "v2.2508.2", "-m", "Old tag"], cwd=project_root, check=True
    )

    verbeat = VerBeat(str(project_root))

    current_version = verbeat.get_current_version()
    calculated_version = verbeat.get_calculated_version()

    assert current_version == "2.2508.2"
    assert calculated_version == "2.2508.5"


def test_get_calculated_version_function(tmp_path):
    """Test the module-level get_calculated_version function."""
    project_root = tmp_path / "project"
    project_root.mkdir()

    verbeat_file = project_root / "verbeat.version"
    verbeat_file.write_text("1 # Test project\n")

    git_dir = project_root / ".git"
    git_dir.mkdir()

    subprocess.run(["git", "init"], cwd=project_root, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=project_root, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=project_root,
        check=True,
    )

    for i in range(3):
        test_file = project_root / f"file{i}.txt"
        test_file.write_text(f"content {i}")
        subprocess.run(["git", "add", str(test_file)], cwd=project_root, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"commit {i}"], cwd=project_root, check=True
        )

    subprocess.run(
        ["git", "tag", "-a", "v1.2508.1", "-m", "Old tag"], cwd=project_root, check=True
    )

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from verbeat import get_calculated_version, get_version

    calculated_version = get_calculated_version(str(project_root))
    current_version = get_version(str(project_root))

    assert calculated_version == "1.2508.3"
    assert current_version == "1.2508.1"


def test_get_version_with_use_calculated_param(tmp_path):
    """Test get_version with use_calculated parameter."""
    project_root = tmp_path / "project"
    project_root.mkdir()

    verbeat_file = project_root / "verbeat.version"
    verbeat_file.write_text("3 # Test project\n")

    git_dir = project_root / ".git"
    git_dir.mkdir()

    subprocess.run(["git", "init"], cwd=project_root, check=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=project_root, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=project_root,
        check=True,
    )

    for i in range(4):
        test_file = project_root / f"file{i}.txt"
        test_file.write_text(f"content {i}")
        subprocess.run(["git", "add", str(test_file)], cwd=project_root, check=True)
        subprocess.run(
            ["git", "commit", "-m", f"commit {i}"], cwd=project_root, check=True
        )

    subprocess.run(
        ["git", "tag", "-a", "v3.2508.2", "-m", "Old tag"], cwd=project_root, check=True
    )

    sys.path.insert(0, str(Path(__file__).parent.parent))
    from verbeat import get_version

    current_version = get_version(str(project_root))
    calculated_version = get_version(str(project_root), use_calculated=True)

    assert current_version == "3.2508.2"
    assert calculated_version == "3.2508.4"
