#!/usr/bin/env python3
"""
CLI module for pre-pull safety checks.
"""

import subprocess
import sys
from datetime import datetime


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


def check_teammate_updates():
    """Check if there are updates available from the remote branch."""
    try:
        # Check if tracking branch exists
        subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "@{upstream}"],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError:
        # No remote tracking branch set
        print("No remote tracking branch set")
        return
    
    # Fetch latest info from remote first
    try:
        subprocess.run(
            ["git", "fetch"],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError:
        # If fetch fails, continue anyway
        pass
    
    try:
        # Count commits behind remote
        result = subprocess.run(
            ["git", "rev-list", "--count", "HEAD..@{upstream}"],
            capture_output=True,
            text=True,
            check=True
        )
        behind_count = int(result.stdout.strip())
        
        # Print status based on count
        if behind_count > 0:
            print("Teammate updates available: yes")
        else:
            print("Teammate updates available: no")
    except (subprocess.CalledProcessError, ValueError):
        # If counting fails, assume no updates available
        print("Teammate updates available: no")


def main():
    """Main function to run the safety check."""
    # Step 1: Check if we're in a git repository
    if not check_if_git_repo():
        print("Not a git repo")
        print("Decision: Do NOT get updates yet")
        sys.exit(1)
    
    # Step 2: Check if there's any unsaved work
    if has_unsaved_work():
        # There are uncommitted changes - warn the user
        print("Warning: You have unsaved work. Getting teammate updates right now could be risky.")
        print("Decision: Do NOT get updates yet")
        sys.exit(1)
    else:
        # No unsaved work - safe to pull
        print("Safe to get teammate updates")
    
    # Step 3: Check if teammate updates are available
    check_teammate_updates()
    
    # Step 4: Final decision
    print("Decision: Safe to get updates")


def safe_save():
    """Create a safety checkpoint by saving changes to a new branch."""
    # Step 1: Check if we're in a git repository
    if not check_if_git_repo():
        print("Not a git repo")
        sys.exit(1)
    
    # Step 2: Check if there are any local changes
    if not has_unsaved_work():
        print("No changes to save")
        sys.exit(0)
    
    # Step 3: Get the current branch name
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        original_branch = result.stdout.strip()
    except subprocess.CalledProcessError:
        # If we can't get branch name, use a default
        original_branch = "main"
    
    # Step 4: Create timestamp-based branch name
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    safety_branch = f"safety/{timestamp}"
    
    # Step 5: Create and switch to the new branch
    try:
        subprocess.run(
            ["git", "checkout", "-b", safety_branch],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError:
        print("Error: Could not create safety branch")
        sys.exit(1)
    
    # Step 6: Save all changes to the new branch
    try:
        # Add all changes
        subprocess.run(
            ["git", "add", "-A"],
            capture_output=True,
            check=True
        )
        # Save the changes
        subprocess.run(
            ["git", "commit", "-m", "Safety checkpoint"],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError:
        # If commit fails, try to go back to original branch
        subprocess.run(
            ["git", "checkout", original_branch],
            capture_output=True
        )
        print("Error: Could not save changes")
        sys.exit(1)
    
    # Step 7: Switch back to the original branch
    try:
        subprocess.run(
            ["git", "checkout", original_branch],
            capture_output=True,
            check=True
        )
    except subprocess.CalledProcessError:
        print("Error: Could not switch back to original branch")
        sys.exit(1)
    
    # Step 8: Print success message
    print(f"Safety checkpoint created: {safety_branch}")
