#!/usr/bin/env python3
"""
Entry point for running the app as a module: python3 -m app pre-pull
"""

import sys
from app.cli import main, safe_save

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "pre-pull":
        main()
    elif len(sys.argv) > 1 and sys.argv[1] == "safe-save":
        safe_save()
    else:
        print("Usage: python3 -m app pre-pull")
        sys.exit(1)
