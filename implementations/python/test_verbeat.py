#!/usr/bin/env python3

import os
import tempfile
import shutil
from pathlib import Path
from datetime import datetime

from verbeat import VerBeat, get_version, bump_version, get_version_components


def test_basic_functionality():
    print("Testing basic functionality...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        version_file = temp_path / "verbeat.version"
        with open(version_file, 'w') as f:
            f.write("1 # Initial release\n")
            f.write("2 # Breaking API changes\n")
        
        verbeat = VerBeat(temp_path)
        
        version = verbeat.get_current_version()
        print(f"  Current version: {version}")
        
        manual, yymm, commits = verbeat.get_version_components()
        print(f"  Manual: {manual}, Date: {yymm}, Commits: {commits}")
        
        history = verbeat.get_version_history()
        print(f"  Version history: {history}")
        
        new_version = verbeat.bump_manual_version("Test bump")
        print(f"  Bumped to version: {new_version}")
        
        with open(version_file, 'r') as f:
            content = f.read()
            print(f"  Updated version file:\n{content}")
        
        print("  ✓ Basic functionality test passed")


def test_convenience_functions():
    print("Testing convenience functions...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        version_file = temp_path / "verbeat.version"
        with open(version_file, 'w') as f:
            f.write("1 # Initial release\n")
        
        version = get_version(temp_path)
        print(f"  get_version(): {version}")
        
        manual, yymm, commits = get_version_components(temp_path)
        print(f"  get_version_components(): ({manual}, {yymm}, {commits})")
        
        new_version = bump_version("Test", temp_path)
        print(f"  bump_version(): {new_version}")
        
        print("  ✓ Convenience functions test passed")


def test_date_specific_version():
    print("Testing date-specific version...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        version_file = temp_path / "verbeat.version"
        with open(version_file, 'w') as f:
            f.write("1 # Initial release\n")
        
        test_date = datetime(2025, 7, 15)
        version = get_version(temp_path, test_date)
        print(f"  Version for {test_date.date()}: {version}")
        
        expected = "1.2507.0"
        if version == expected:
            print(f"  ✓ Date-specific version test passed: {version}")
        else:
            print(f"  ✗ Date-specific version test failed: expected {expected}, got {version}")


def test_error_handling():
    print("Testing error handling...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        try:
            verbeat = VerBeat(temp_path)
            version = verbeat.get_current_version()
            print(f"  ✗ Should have raised error for missing version file")
        except Exception as e:
            print(f"  ✓ Correctly raised error for missing version file: {type(e).__name__}")
        
        version_file = temp_path / "verbeat.version"
        with open(version_file, 'w') as f:
            f.write("")
        
        try:
            verbeat = VerBeat(temp_path)
            version = verbeat.get_current_version()
            print(f"  ✗ Should have raised error for empty version file")
        except Exception as e:
            print(f"  ✓ Correctly raised error for empty version file: {type(e).__name__}")
        
        print("  ✓ Error handling test passed")


def main():
    print("Running VerBeat Python implementation tests...\n")
    
    try:
        test_basic_functionality()
        print()
        
        test_convenience_functions()
        print()
        
        test_date_specific_version()
        print()
        
        test_error_handling()
        print()
        
        print("🎉 All tests passed!")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 