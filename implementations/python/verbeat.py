#!/usr/bin/env python3
"""
VerBeat - A 3D Versioning System for Real-World Dev Flow

This module provides a simple and efficient API for managing VerBeat versions.
VerBeat combines manual semantic milestones with automated time-based and
activity-driven versioning in the format: M.YYMM.C

Where:
- M: Manual version bump (semantic milestone)
- YYMM: Year and month (calendar context)
- C: Commit count for the current month (activity tempo)
"""

import sys
import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, List


def _get_verbeat_version() -> str:
    """Get the current VerBeat version from Git tags or version file."""
    # Try multiple possible project roots
    possible_roots = [
        _find_project_root(),  # Current directory and parents
        Path(
            __file__
        ).parent.parent.parent,  # Go up from implementations/python/verbeat.py
        Path.cwd().parent.parent,  # Go up from current directory
    ]

    for project_root in possible_roots:
        if project_root and project_root.exists():
            try:
                verbeat = VerBeat(project_root)
                return verbeat.get_current_version()
            except Exception:
                continue

    # Dynamic fallback - use current date instead of hardcoded month
    from datetime import datetime
    now = datetime.now()
    year = str(now.year)[-2:]
    month = f"{now.month:02d}"
    return f"1.{year}{month}.0"


def _find_project_root() -> Optional[Path]:
    """Find the project root directory containing verbeat.version."""
    current = Path.cwd()

    for path in [
        current,
        current.parent,
        current.parent.parent,
        current.parent.parent.parent,
    ]:
        if (path / "verbeat.version").exists():
            return path

    return None


class VerBeatError(Exception):
    """Base exception for all VerBeat operations."""


class VerBeatVersionFileError(VerBeatError):
    """Raised when there are issues with the verbeat.version file."""


class VerBeatGitError(VerBeatError):
    """Raised when Git operations fail."""


class VerBeatBranchError(VerBeatError):
    """Raised when version bump is attempted on a non-main branch."""


class VerBeat:
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.version_file = self.project_root / "verbeat.version"

    def _get_latest_tag_version(self) -> Optional[str]:
        """Get the latest VerBeat tag version."""
        try:
            import subprocess

            git_dir = self.project_root / ".git"
            if not git_dir.exists():
                return None

            try:
                subprocess.run(["git", "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                return None

            result = subprocess.run(
                ["git", "tag", "--list", "v*", "--sort=-version:refname"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )

            tags = result.stdout.strip().split("\n")
            if not tags or tags[0] == "":
                return None

            return tags[0]

        except subprocess.CalledProcessError:
            return None

    def _create_version_tag(self, version: str, comment: str = "") -> bool:
        """Create a Git tag for the given version."""
        try:
            import subprocess
            from datetime import datetime

            git_dir = self.project_root / ".git"
            if not git_dir.exists():
                return False

            try:
                subprocess.run(["git", "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                return False

            date_str = datetime.now().strftime("%Y-%m-%d")
            tag_message = f"VerBeat {version} ({date_str})"
            if comment:
                tag_message += f": {comment}"

            subprocess.run(
                ["git", "tag", "-a", f"v{version}", "-m", tag_message],
                cwd=self.project_root,
                check=True,
            )

            return True

        except subprocess.CalledProcessError:
            return False

    def get_calculated_version(self, date: Optional[datetime] = None) -> str:
        """Get the calculated version ignoring existing tags."""
        manual_version = self._get_manual_version()
        date_obj = date or datetime.now()
        commit_count = self._get_commit_count_for_month(date_obj)

        year = str(date_obj.year)[-2:]
        month = f"{date_obj.month:02d}"

        return f"{manual_version}.{year}{month}.{commit_count}"

    def get_current_version(self, date: Optional[datetime] = None) -> str:
        latest_tag = self._get_latest_tag_version()
        if latest_tag:
            return latest_tag[1:]

        manual_version = self._get_manual_version()
        date_obj = date or datetime.now()
        commit_count = self._get_commit_count_for_month(date_obj)

        year = str(date_obj.year)[-2:]
        month = f"{date_obj.month:02d}"

        return f"{manual_version}.{year}{month}.{commit_count}"

    def get_version_components(
        self, date: Optional[datetime] = None
    ) -> Tuple[int, str, int]:
        latest_tag = self._get_latest_tag_version()
        if latest_tag:
            version_str = latest_tag[1:]
            parts = version_str.split(".")
            if len(parts) == 3:
                try:
                    manual_version = int(parts[0])
                    yymm = parts[1]
                    commit_count = int(parts[2])
                    return manual_version, yymm, commit_count
                except ValueError:
                    pass

        manual_version = self._get_manual_version()
        date_obj = date or datetime.now()
        commit_count = self._get_commit_count_for_month(date_obj)

        year = str(date_obj.year)[-2:]
        month = f"{date_obj.month:02d}"
        yymm = f"{year}{month}"

        return manual_version, yymm, commit_count

    def _get_current_branch(self) -> str:
        """Get the current Git branch name."""
        try:
            import subprocess

            git_dir = self.project_root / ".git"
            if not git_dir.exists():
                return ""

            try:
                subprocess.run(["git", "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                return ""

            result = subprocess.run(
                ["git", "rev-parse", "--abbrev-ref", "HEAD"],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )

            return result.stdout.strip()

        except subprocess.CalledProcessError:
            return ""

    def _get_main_branch_name(self) -> str:
        """Get the main branch name (main or master)."""
        import subprocess

        main_branch = os.environ.get("VERBEAT_MAIN_BRANCH")
        if main_branch:
            return main_branch

        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "main"

        git_dir = self.project_root / ".git"
        if not git_dir.exists():
            return "main"

        try:
            result = subprocess.run(
                ["git", "show-ref", "--verify", "--quiet", "refs/heads/main"],
                cwd=self.project_root,
                capture_output=True,
                check=False,
            )
            if result.returncode == 0:
                return "main"

            result = subprocess.run(
                ["git", "show-ref", "--verify", "--quiet", "refs/heads/master"],
                cwd=self.project_root,
                capture_output=True,
                check=False,
            )
            if result.returncode == 0:
                return "master"

        except subprocess.CalledProcessError:
            pass

        return "main"

    def bump_manual_version(self, comment: str = "") -> int:
        current_branch = self._get_current_branch()
        main_branch = self._get_main_branch_name()

        if current_branch and current_branch != main_branch:
            raise VerBeatBranchError(
                f"Version bump is only allowed on the main branch ({main_branch}). "
                f"Current branch: {current_branch}. "
                "Set VERBEAT_MAIN_BRANCH environment variable to override the "
                "main branch name."
            )

        current_version = self._get_manual_version()
        new_version = current_version + 1

        lines = []
        if self.version_file.exists():
            with open(self.version_file, "r") as f:
                lines = f.readlines()

        comment_line = f" # {comment}" if comment else ""
        lines.append(f"{new_version}{comment_line}\n")

        try:
            with open(self.version_file, "w") as f:
                f.writelines(lines)
        except IOError as e:
            raise VerBeatVersionFileError(f"Cannot write to version file: {e}")

        return new_version

    def get_version_history(self) -> List[Tuple[int, str]]:
        if not self.version_file.exists():
            return []

        try:
            with open(self.version_file, "r") as f:
                lines = f.readlines()
        except IOError as e:
            raise VerBeatVersionFileError(f"Cannot read version file: {e}")

        history = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            parts = line.split("#", 1)
            version_str = parts[0].strip()
            comment = parts[1].strip() if len(parts) > 1 else ""

            try:
                version_num = int(version_str)
                history.append((version_num, comment))
            except ValueError:
                raise VerBeatVersionFileError(f"Invalid version number: {version_str}")

        return sorted(history, key=lambda x: x[0])

    def _get_manual_version(self) -> int:
        if not self.version_file.exists():
            raise VerBeatVersionFileError(
                f"Version file not found: {self.version_file}. "
                "Create a verbeat.version file with at least one version number."
            )

        history = self.get_version_history()
        if not history:
            raise VerBeatVersionFileError(
                f"No valid versions found in {self.version_file}. "
                "Add at least one version number (e.g., '1 # Initial release')."
            )

        return max(version for version, _ in history)

    def _get_commit_count_for_month(self, date: datetime) -> int:
        try:
            git_dir = self.project_root / ".git"
            if not git_dir.exists():
                return 0

            import subprocess

            try:
                subprocess.run(["git", "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                return 0

            try:
                result = subprocess.run(
                    ["git", "rev-list", "--count", "HEAD"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    check=True,
                )
                total_commits = int(result.stdout.strip())
                if total_commits == 0:
                    return 0
            except (subprocess.CalledProcessError, ValueError):
                return 0

            start_date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if date.month == 12:
                end_date = date.replace(year=date.year + 1, month=1, day=1)
            else:
                end_date = date.replace(month=date.month + 1, day=1)

            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")

            result = subprocess.run(
                [
                    "git",
                    "rev-list",
                    "--count",
                    f"--since={start_str}",
                    f"--until={end_str}",
                    "HEAD",
                ],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True,
            )

            return int(result.stdout.strip())

        except subprocess.CalledProcessError:
            return 0
        except ValueError:
            return 0
        except ImportError:
            return 0


def get_calculated_version(
    project_root: Optional[str] = None, date: Optional[datetime] = None
) -> str:
    """Get the calculated version ignoring existing tags."""
    if project_root:
        verbeat = VerBeat(project_root)
    else:
        project_root_path = _find_project_root()
        if not project_root_path:
            return "1.2507.0"
        verbeat = VerBeat(project_root_path)

    return verbeat.get_calculated_version(date)


def get_version(
    project_root: Optional[str] = None,
    date: Optional[datetime] = None,
    use_calculated: bool = False,
) -> str:
    """Get the current VerBeat version."""
    if use_calculated:
        return get_calculated_version(project_root, date)

    if project_root:
        verbeat = VerBeat(project_root)
    else:
        project_root_path = _find_project_root()
        if not project_root_path:
            return "1.2507.0"
        verbeat = VerBeat(project_root_path)

    return verbeat.get_current_version(date)


def bump_version(comment: str = "", project_root: Optional[str] = None) -> int:
    """Bump the manual version."""
    if project_root:
        verbeat = VerBeat(project_root)
    else:
        project_root_path = _find_project_root()
        if not project_root_path:
            raise VerBeatVersionFileError("No verbeat.version file found")
        verbeat = VerBeat(project_root_path)

    return verbeat.bump_manual_version(comment)


def get_version_components(
    project_root: Optional[str] = None, date: Optional[datetime] = None
) -> Tuple[int, str, int]:
    """Get the individual version components."""
    if project_root:
        verbeat = VerBeat(project_root)
    else:
        project_root_path = _find_project_root()
        if not project_root_path:
            return (1, "2507", 0)
        verbeat = VerBeat(project_root_path)

    return verbeat.get_version_components(date)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="VerBeat - A 3D Versioning System")
    parser.add_argument("command", choices=["version", "bump", "components", "init"])
    parser.add_argument("--project", help="Project root path")
    parser.add_argument("--date", help="Date for version calculation (YYYY-MM-DD)")
    parser.add_argument("comment", nargs="?", help="Comment for version bump or init")

    args = parser.parse_args()

    try:
        if args.command == "version":
            date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else None
            print(get_version(args.project, date))
        elif args.command == "bump":
            new_version = bump_version(args.comment or "", args.project)
            print(f"Bumped to version {new_version}")
        elif args.command == "components":
            date = datetime.strptime(args.date, "%Y-%m-%d") if args.date else None
            manual, yymm, commits = get_version_components(args.project, date)
            print(f"Manual: {manual}")
            print(f"Date: {yymm}")
            print(f"Commits: {commits}")
        elif args.command == "init":
            init_project(args.comment or "Initial release", args.project)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def init_project(comment: str = "Initial release", project_root: Optional[str] = None):
    """Initialize a new VerBeat project."""
    project_path = Path(project_root) if project_root else Path.cwd()
    version_file = project_path / "verbeat.version"

    if version_file.exists():
        print("Already initialized. Use 'verbeat version' to see current version.")
        return

    try:
        version_file.write_text(f"1 # {comment}\n")
        print(f"Created {version_file}")
        print(f"VerBeat initialized with version: {get_version(str(project_path))}")

    except Exception as e:
        raise VerBeatError(f"Failed to initialize project: {e}")


if __name__ == "__main__":
    main()
