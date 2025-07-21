#!/usr/bin/env python3

import sys
import os
import tempfile
import subprocess
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from verbeat import get_version, get_version_components


def test_outside_git_repo():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        version_file = temp_path / "verbeat.version"
        with open(version_file, "w") as f:
            f.write("1 # Initial release\n")

        version = get_version(temp_path)
        manual, yymm, commits = get_version_components(temp_path)

        assert commits == 0
        assert version.endswith(".0")


def test_empty_git_repo():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        subprocess.run(["git", "init"], cwd=temp_path, check=True)

        version_file = temp_path / "verbeat.version"
        with open(version_file, "w") as f:
            f.write("1 # Initial release\n")

        version = get_version(temp_path)
        manual, yymm, commits = get_version_components(temp_path)

        assert commits == 0
        assert version.endswith(".0")


def test_git_repo_with_commits():
    print("Testing Git repository with commits...")

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        subprocess.run(["git", "init"], cwd=temp_path, check=True)
        subprocess.run(
            ["git", "config", "user.name", "Test User"], cwd=temp_path, check=True
        )
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=temp_path,
            check=True,
        )

        version_file = temp_path / "verbeat.version"
        with open(version_file, "w") as f:
            f.write("1 # Initial release\n")

        subprocess.run(["git", "add", "verbeat.version"], cwd=temp_path, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"], cwd=temp_path, check=True
        )

        try:
            version = get_version(temp_path)
            manual, yymm, commits = get_version_components(temp_path)

            print(f"  Version: {version}")
            print(f"  Manual: {manual}, Date: {yymm}, Commits: {commits}")

            assert commits >= 1, f"Expected at least 1 commit, got {commits}"
            assert not version.endswith(
                ".0"
            ), f"Expected version to not end with .0, got {version}"

            print("  ✓ Git repo with commits test passed")

        except Exception as e:
            print(f"  ✗ Git repo with commits test failed: {e}")
            raise


def test_git_not_installed():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        version_file = temp_path / "verbeat.version"
        with open(version_file, "w") as f:
            f.write("1 # Initial release\n")

        original_path = os.environ.get("PATH", "")
        os.environ["PATH"] = "/nonexistent"

        try:
            version = get_version(temp_path)
            manual, yymm, commits = get_version_components(temp_path)

            assert commits == 0
            assert version.endswith(".0")
        finally:
            os.environ["PATH"] = original_path


def test_git_command_failure():
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        version_file = temp_path / "verbeat.version"
        with open(version_file, "w") as f:
            f.write("1 # Initial release\n")

        git_dir = temp_path / ".git"
        git_dir.mkdir()

        version = get_version(temp_path)
        manual, yymm, commits = get_version_components(temp_path)

        assert commits == 0
        assert version.endswith(".0")
