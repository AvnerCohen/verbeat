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

def _get_verbeat_version() -> str:
    """Get the current VerBeat version string."""
    try:
        # Try multiple possible locations for verbeat.version
        from pathlib import Path
        
        possible_paths = [
            # Current directory (if running from project root)
            Path("verbeat.version"),
            # Parent directory (if running from implementations/python)
            Path("../verbeat.version"),
            # Two levels up (if running from implementations/python)
            Path("../../verbeat.version"),
            # Three levels up (if running from implementations/python)
            Path("../../../verbeat.version"),
        ]
        
        for version_file in possible_paths:
            if version_file.exists():
                with open(version_file, 'r') as f:
                    lines = f.readlines()
                
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        version_str = line.split('#')[0].strip()
                        try:
                            manual_version = int(version_str)
                            
                            # Get current date
                            from datetime import datetime
                            now = datetime.now()
                            year = str(now.year)[-2:]
                            month = f"{now.month:02d}"
                            yymm = f"{year}{month}"
                            
                            # Get commit count (simplified - just return 0 for now)
                            commit_count = 0
                            
                            return f"{manual_version}.{yymm}.{commit_count}"
                        except ValueError:
                            pass
        
        # Fallback: try to use the VerBeat class
        verbeat = VerBeat()
        return verbeat.get_current_version()
    except Exception:
        return "1.0.0"

__version__ = _get_verbeat_version()


class VerBeatError(Exception):
    pass


class VerBeatVersionFileError(VerBeatError):
    pass


class VerBeatGitError(VerBeatError):
    pass


class VerBeat:
    def __init__(self, project_root: Optional[str] = None):
        self.project_root = Path(project_root) if project_root else Path.cwd()
        self.version_file = self.project_root / "verbeat.version"
    
    def get_current_version(self, date: Optional[datetime] = None) -> str:
        manual_version = self._get_manual_version()
        date_obj = date or datetime.now()
        commit_count = self._get_commit_count_for_month(date_obj)
        
        year = str(date_obj.year)[-2:]
        month = f"{date_obj.month:02d}"
        
        return f"{manual_version}.{year}{month}.{commit_count}"
    
    def get_version_components(self, date: Optional[datetime] = None) -> Tuple[int, str, int]:
        manual_version = self._get_manual_version()
        date_obj = date or datetime.now()
        commit_count = self._get_commit_count_for_month(date_obj)
        
        year = str(date_obj.year)[-2:]
        month = f"{date_obj.month:02d}"
        yymm = f"{year}{month}"
        
        return manual_version, yymm, commit_count
    
    def bump_manual_version(self, comment: str = "") -> int:
        current_version = self._get_manual_version()
        new_version = current_version + 1
        
        lines = []
        if self.version_file.exists():
            with open(self.version_file, 'r') as f:
                lines = f.readlines()
        
        comment_line = f" # {comment}" if comment else ""
        lines.append(f"{new_version}{comment_line}\n")
        
        try:
            with open(self.version_file, 'w') as f:
                f.writelines(lines)
        except IOError as e:
            raise VerBeatVersionFileError(f"Cannot write to version file: {e}")
        
        return new_version
    
    def get_version_history(self) -> List[Tuple[int, str]]:
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
                    check=True
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
            
        except subprocess.CalledProcessError:
            return 0
        except ValueError:
            return 0
        except ImportError:
            return 0


def get_version(project_root: Optional[str] = None, date: Optional[datetime] = None) -> str:
    verbeat = VerBeat(project_root)
    return verbeat.get_current_version(date)


def bump_version(comment: str = "", project_root: Optional[str] = None) -> int:
    verbeat = VerBeat(project_root)
    return verbeat.bump_manual_version(comment)


def get_version_components(project_root: Optional[str] = None, date: Optional[datetime] = None) -> Tuple[int, str, int]:
    verbeat = VerBeat(project_root)
    return verbeat.get_version_components(date)


def main():
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
        date_obj = None
        if args.date:
            try:
                date_obj = datetime.strptime(args.date, '%Y-%m-%d')
            except ValueError:
                print(f"Error: Invalid date format '{args.date}'. Use YYYY-MM-DD format.")
                sys.exit(1)
        
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