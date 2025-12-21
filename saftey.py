#!/usr/bin/env python3
"""
Pre-pull safety check script.
Checks if it's safe to get updates from teammates before pulling changes.
"""

import subprocess
import sys


def check_if_git_repo():
    """Check if the current directory is inside a git repository."""
    try:
        # This command will fail if we're not in a git repo
        subprocess.run(
            ["git", "rev-parse", "--git-dir"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Not a git repo, or git is not installed
        return False


def has_unsaved_work():
    """Check if there are any uncommitted changes in the repository."""
    try:
        # Get a simple list of changed files (empty string means no changes)
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True,
            check=True
        )
        # If there's any output, there are unsaved changes
        return len(result.stdout.strip()) > 0
    except subprocess.CalledProcessError:
        # If this fails, assume there might be unsaved work to be safe
        return True


def main():
    """Main function to run the safety check."""
    # Step 1: Check if we're in a git repository
    if not check_if_git_repo():
        print("Not a git repo")
        sys.exit(1)
    
    # Step 2: Check if there's any unsaved work
    if has_unsaved_work():
        # There are uncommitted changes - warn the user
        print("Warning: You have unsaved work. Getting teammate updates right now could be risky.")
        sys.exit(1)
    else:
        # No unsaved work - safe to pull
        print("Safe to get teammate updates")


if __name__ == "__main__":
    main()
