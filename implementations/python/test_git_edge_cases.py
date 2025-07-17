#!/usr/bin/env python3

import os
import tempfile
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

from verbeat import VerBeat, get_version, get_version_components


def test_outside_git_repo():
    print("Testing outside Git repository...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        version_file = temp_path / "verbeat.version"
        with open(version_file, 'w') as f:
            f.write("1 # Initial release\n")
        
        try:
            version = get_version(temp_path)
            manual, yymm, commits = get_version_components(temp_path)
            
            print(f"  Version: {version}")
            print(f"  Manual: {manual}, Date: {yymm}, Commits: {commits}")
            
            assert commits == 0, f"Expected 0 commits, got {commits}"
            assert version.endswith(".0"), f"Expected version to end with .0, got {version}"
            
            print("  ✓ Outside Git repo test passed")
            
        except Exception as e:
            print(f"  ✗ Outside Git repo test failed: {e}")
            raise


def test_empty_git_repo():
    print("Testing empty Git repository...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        subprocess.run(["git", "init"], cwd=temp_path, check=True)
        
        version_file = temp_path / "verbeat.version"
        with open(version_file, 'w') as f:
            f.write("1 # Initial release\n")
        
        try:
            version = get_version(temp_path)
            manual, yymm, commits = get_version_components(temp_path)
            
            print(f"  Version: {version}")
            print(f"  Manual: {manual}, Date: {yymm}, Commits: {commits}")
            
            assert commits == 0, f"Expected 0 commits, got {commits}"
            assert version.endswith(".0"), f"Expected version to end with .0, got {version}"
            
            print("  ✓ Empty Git repo test passed")
            
        except Exception as e:
            print(f"  ✗ Empty Git repo test failed: {e}")
            raise


def test_git_repo_with_commits():
    print("Testing Git repository with commits...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        subprocess.run(["git", "init"], cwd=temp_path, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=temp_path, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=temp_path, check=True)
        
        version_file = temp_path / "verbeat.version"
        with open(version_file, 'w') as f:
            f.write("1 # Initial release\n")
        
        subprocess.run(["git", "add", "verbeat.version"], cwd=temp_path, check=True)
        subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=temp_path, check=True)
        
        try:
            version = get_version(temp_path)
            manual, yymm, commits = get_version_components(temp_path)
            
            print(f"  Version: {version}")
            print(f"  Manual: {manual}, Date: {yymm}, Commits: {commits}")
            
            assert commits >= 1, f"Expected at least 1 commit, got {commits}"
            assert not version.endswith(".0"), f"Expected version to not end with .0, got {version}"
            
            print("  ✓ Git repo with commits test passed")
            
        except Exception as e:
            print(f"  ✗ Git repo with commits test failed: {e}")
            raise


def test_git_not_installed():
    print("Testing without Git installed...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        version_file = temp_path / "verbeat.version"
        with open(version_file, 'w') as f:
            f.write("1 # Initial release\n")
        
        original_path = os.environ.get('PATH', '')
        os.environ['PATH'] = '/nonexistent'
        
        try:
            version = get_version(temp_path)
            manual, yymm, commits = get_version_components(temp_path)
            
            print(f"  Version: {version}")
            print(f"  Manual: {manual}, Date: {yymm}, Commits: {commits}")
            
            assert commits == 0, f"Expected 0 commits, got {commits}"
            assert version.endswith(".0"), f"Expected version to end with .0, got {version}"
            
            print("  ✓ Git not installed test passed")
            
        except Exception as e:
            print(f"  ✗ Git not installed test failed: {e}")
            raise
        finally:
            os.environ['PATH'] = original_path


def test_git_command_failure():
    print("Testing Git command failure...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        version_file = temp_path / "verbeat.version"
        with open(version_file, 'w') as f:
            f.write("1 # Initial release\n")
        
        git_dir = temp_path / ".git"
        git_dir.mkdir()
        
        try:
            version = get_version(temp_path)
            manual, yymm, commits = get_version_components(temp_path)
            
            print(f"  Version: {version}")
            print(f"  Manual: {manual}, Date: {yymm}, Commits: {commits}")
            
            assert commits == 0, f"Expected 0 commits, got {commits}"
            assert version.endswith(".0"), f"Expected version to end with .0, got {version}"
            
            print("  ✓ Git command failure test passed")
            
        except Exception as e:
            print(f"  ✗ Git command failure test failed: {e}")
            raise


def main():
    print("Running VerBeat Git edge case tests...\n")
    
    try:
        test_outside_git_repo()
        print()
        
        test_empty_git_repo()
        print()
        
        test_git_repo_with_commits()
        print()
        
        test_git_not_installed()
        print()
        
        test_git_command_failure()
        print()
        
        print("🎉 All Git edge case tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 