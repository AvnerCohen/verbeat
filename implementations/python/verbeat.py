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

import os
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Tuple, List


class VerBeatError(Exception):
    """Base exception for VerBeat operations."""
    pass


class VerBeatVersionFileError(VerBeatError):
    """Raised when there are issues with the verbeat.version file."""
    pass


class VerBeatGitError(VerBeatError):
    """Raised when there are issues with Git operations."""
    pass


class VerBeat:
    """
    Main VerBeat class for version management.
    
    Provides a simple API for reading version files, calculating commit counts,
    and generating VerBeat version strings.
    """
    
    def __init__(self, project_root: Optional[str] = None):
        """
        Initialize VerBeat for a project.
        
        Args:
            project_root: Path to project root. Defaults to current directory.
        """
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.version_file = self.project_root / "verbeat.version"
    
    def get_current_version(self, date: Optional[datetime] = None) -> str:
        """
        Get the current VerBeat version string.
        
        Args:
            date: Date to use for version calculation. Defaults to current date.
            
        Returns:
            VerBeat version string in format M.YYMM.C
            
        Raises:
            VerBeatVersionFileError: If version file is missing or invalid
            VerBeatGitError: If Git operations fail
        """
        manual_version = self._get_manual_version()
        date_obj = date or datetime.now()
        commit_count = self._get_commit_count_for_month(date_obj)
        
        year = str(date_obj.year)[-2:]  # Last 2 digits
        month = f"{date_obj.month:02d}"  # Zero-padded month
        
        return f"{manual_version}.{year}{month}.{commit_count}"
    
    def get_version_components(self, date: Optional[datetime] = None) -> Tuple[int, str, int]:
        """
        Get the individual components of the current version.
        
        Args:
            date: Date to use for version calculation. Defaults to current date.
            
        Returns:
            Tuple of (manual_version, yymm, commit_count)
        """
        manual_version = self._get_manual_version()
        date_obj = date or datetime.now()
        commit_count = self._get_commit_count_for_month(date_obj)
        
        year = str(date_obj.year)[-2:]
        month = f"{date_obj.month:02d}"
        yymm = f"{year}{month}"
        
        return manual_version, yymm, commit_count
    
    def bump_manual_version(self, comment: str = "") -> int:
        """
        Bump the manual version and add a comment.
        
        Args:
            comment: Comment describing the version bump
            
        Returns:
            The new manual version number
            
        Raises:
            VerBeatVersionFileError: If version file cannot be written
        """
        current_version = self._get_manual_version()
        new_version = current_version + 1
        
        # Read existing content
        lines = []
        if self.version_file.exists():
            with open(self.version_file, 'r') as f:
                lines = f.readlines()
        
        # Add new version
        comment_line = f" # {comment}" if comment else ""
        lines.append(f"{new_version}{comment_line}\n")
        
        # Write back to file
        try:
            with open(self.version_file, 'w') as f:
                f.writelines(lines)
        except IOError as e:
            raise VerBeatVersionFileError(f"Cannot write to version file: {e}")
        
        return new_version
    
    def get_version_history(self) -> List[Tuple[int, str]]:
        """
        Get the history of manual versions and their comments.
        
        Returns:
            List of tuples (version_number, comment)
            
        Raises:
            VerBeatVersionFileError: If version file is invalid
        """
        if not self.version_file.exists():
            return []
        
        try:
            with open(self.version_file, 'r') as f:
                lines = f.readlines()
        except IOError as e:
            raise VerBeatVersionFileError(f"Cannot read version file: {e}")
        
        history = []
        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            
            # Parse version and comment
            parts = line.split('#', 1)
            version_str = parts[0].strip()
            comment = parts[1].strip() if len(parts) > 1 else ""
            
            try:
                version_num = int(version_str)
                history.append((version_num, comment))
            except ValueError:
                raise VerBeatVersionFileError(f"Invalid version number: {version_str}")
        
        return sorted(history, key=lambda x: x[0])
    
    def _get_manual_version(self) -> int:
        """
        Get the current manual version from the version file.
        
        Returns:
            The highest version number from the file
            
        Raises:
            VerBeatVersionFileError: If version file is missing or invalid
        """
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
        """
        Get the number of commits for a specific month.
        
        Args:
            date: Date to get commit count for
            
        Returns:
            Number of commits in that month
            
        Raises:
            VerBeatGitError: If Git operations fail
        """
        try:
            # Check if we're in a Git repository
            git_dir = self.project_root / ".git"
            if not git_dir.exists():
                return 0
            
            # Check if Git is available
            import subprocess
            try:
                subprocess.run(["git", "--version"], capture_output=True, check=True)
            except (subprocess.CalledProcessError, FileNotFoundError):
                return 0
            
            # Check if we have any commits
            try:
                result = subprocess.run(
                    ["git", "rev-list", "--count", "HEAD"],
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    check=True
                )
                total_commits = int(result.stdout.strip())
                if total_commits == 0:
                    return 0
            except (subprocess.CalledProcessError, ValueError):
                return 0
            
            # Get start and end of month
            start_date = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            if date.month == 12:
                end_date = date.replace(year=date.year + 1, month=1, day=1)
            else:
                end_date = date.replace(month=date.month + 1, day=1)
            
            # Format dates for git log
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            # Count commits in date range
            result = subprocess.run(
                [
                    "git", "rev-list", "--count", 
                    f"--since={start_str}", 
                    f"--until={end_str}", 
                    "HEAD"
                ],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            
            return int(result.stdout.strip())
            
        except subprocess.CalledProcessError as e:
            # Don't raise error for Git issues, just return 0
            return 0
        except ValueError as e:
            # Don't raise error for parsing issues, just return 0
            return 0
        except ImportError:
            # Git not available, return 0
            return 0


def get_version(project_root: Optional[str] = None, date: Optional[datetime] = None) -> str:
    """
    Convenience function to get current VerBeat version.
    
    Args:
        project_root: Path to project root. Defaults to current directory.
        date: Date to use for version calculation. Defaults to current date.
        
    Returns:
        VerBeat version string
    """
    verbeat = VerBeat(project_root)
    return verbeat.get_current_version(date)


def bump_version(comment: str = "", project_root: Optional[str] = None) -> int:
    """
    Convenience function to bump manual version.
    
    Args:
        comment: Comment describing the version bump
        project_root: Path to project root. Defaults to current directory.
        
    Returns:
        The new manual version number
    """
    verbeat = VerBeat(project_root)
    return verbeat.bump_manual_version(comment)


def get_version_components(project_root: Optional[str] = None, date: Optional[datetime] = None) -> Tuple[int, str, int]:
    """
    Convenience function to get version components.
    
    Args:
        project_root: Path to project root. Defaults to current directory.
        date: Date to use for version calculation. Defaults to current date.
        
    Returns:
        Tuple of (manual_version, yymm, commit_count)
    """
    verbeat = VerBeat(project_root)
    return verbeat.get_version_components(date)


def main():
    """Command-line interface for VerBeat."""
    parser = argparse.ArgumentParser(
        description="VerBeat - A 3D Versioning System for Real-World Dev Flow",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  verbeat version                    # Show current version
  verbeat bump "New feature"        # Bump manual version
  verbeat components                # Show version components
  verbeat version --project /path   # Use specific project path
        """
    )
    
    parser.add_argument(
        'command',
        choices=['version', 'bump', 'components'],
        help='Command to execute'
    )
    
    parser.add_argument(
        'comment',
        nargs='?',
        default='',
        help='Comment for version bump (only used with bump command)'
    )
    
    parser.add_argument(
        '--project',
        help='Path to project root (defaults to current directory)'
    )
    
    parser.add_argument(
        '--date',
        help='Date to use for version calculation (YYYY-MM-DD format)'
    )
    
    args = parser.parse_args()
    
    try:
        # Parse date if provided
        date_obj = None
        if args.date:
            try:
                date_obj = datetime.strptime(args.date, '%Y-%m-%d')
            except ValueError:
                print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD format.")
                sys.exit(1)
        
        # Execute command
        if args.command == 'version':
            version = get_version(args.project, date_obj)
            print(version)
        
        elif args.command == 'components':
            manual, yymm, commits = get_version_components(args.project, date_obj)
            print(f"Manual: {manual}")
            print(f"Date: {yymm}")
            print(f"Commits: {commits}")
        
        elif args.command == 'bump':
            new_version = bump_version(args.comment, args.project)
            print(new_version)
    
    except VerBeatError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 