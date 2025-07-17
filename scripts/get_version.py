#!/usr/bin/env python3

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'implementations', 'python'))

from verbeat import get_version

if __name__ == "__main__":
    try:
        version = get_version()
        print(version)
    except Exception as e:
        print("1.0000.0") 