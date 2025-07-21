#!/usr/bin/env python3
"""
Update website version from latest Git tag.

This script reads the latest VerBeat Git tag and updates current_version.json
for use by the website and other display systems.
"""

import json
import sys
import os
from pathlib import Path

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'implementations', 'python'))

from verbeat import VerBeat


def update_website_version():
    """Update current_version.json with the latest version."""
    try:
        project_root = Path(__file__).parent.parent
        
        verbeat = VerBeat(project_root)
        
        current_version = verbeat.get_current_version()
        
        version_data = {
            "current_version": current_version
        }
        
        version_file = project_root / "current_version.json"
        with open(version_file, "w") as f:
            json.dump(version_data, f, indent=2)
        
        print(f"Updated current_version.json with version: {current_version}")
        return True
        
    except Exception as e:
        print(f"Error updating website version: {e}")
        return False


if __name__ == "__main__":
    success = update_website_version()
    sys.exit(0 if success else 1) 