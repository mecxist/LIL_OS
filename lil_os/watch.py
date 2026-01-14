#!/usr/bin/env python3
"""
LIL OS² Watch Mode

Monitors governance files for changes and shows OS-like notifications.
"""

from __future__ import annotations

import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Set, List, Optional

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os_utils import print_os_message, print_os_box, Colors


def git_available() -> bool:
    """Check if git is available."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_governance_files() -> Set[Path]:
    """Get set of governance files to monitor."""
    return {
        Path("docs/MASTER_RULES.md"),
        Path("docs/GOVERNANCE.md"),
        Path("docs/RESET_TRIGGERS.md"),
        Path("docs/CONTEXT_BUDGET.md"),
        Path("docs/DECISION_LOG.md"),
        Path(".cursorrules"),
    }


def get_file_hash(file_path: Path) -> Optional[str]:
    """Get a simple hash of file contents for change detection."""
    if not file_path.exists():
        return None
    
    try:
        content = file_path.read_text(encoding="utf-8")
        # Simple hash: use file size and modification time
        stat = file_path.stat()
        return f"{stat.st_size}_{stat.st_mtime}"
    except Exception:
        return None


def check_for_changes(previous_hashes: Dict[Path, str]) -> tuple[Dict[Path, str], List[Path]]:
    """
    Check for file changes and return updated hashes.
    
    Returns:
        Tuple of (updated hash dictionary, list of changed files)
    """
    current_hashes: Dict[Path, str] = {}
    changed_files: List[Path] = []
    
    for file_path in get_governance_files():
        current_hash = get_file_hash(file_path)
        current_hashes[file_path] = current_hash
        
        if file_path in previous_hashes:
            if previous_hashes[file_path] != current_hash:
                changed_files.append(file_path)
        elif current_hash is not None:
            # New file detected
            changed_files.append(file_path)
    
    return current_hashes, changed_files


def notify_change(file_path: Path):
    """Show OS-like notification for file change."""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print_os_message(f"[{timestamp}] File changed: {file_path}", "WARN")
    
    # Check if it's a governance file
    governance_files = [
        "docs/MASTER_RULES.md",
        "docs/GOVERNANCE.md",
        "docs/RESET_TRIGGERS.md",
        "docs/CONTEXT_BUDGET.md",
        ".cursorrules",
    ]
    
    if str(file_path) in governance_files:
        print_os_message("Governance file modified - decision log entry may be required", "WARN")
        print_os_message("Run 'lil-os log-decision' to create an entry", "INFO")
    elif str(file_path) == "docs/DECISION_LOG.md":
        print_os_message("Decision log updated", "INFO")
    
    print()


def watch_loop(interval: float = 2.0):
    """Main watch loop."""
    print_os_message("Starting file watcher...", "INFO")
    print_os_message("Monitoring governance files for changes", "INFO")
    print_os_message("Press Ctrl+C to stop", "INFO")
    print()
    
    previous_hashes: Dict[Path, str] = {}
    
    # Initialize hashes
    for file_path in get_governance_files():
        previous_hashes[file_path] = get_file_hash(file_path)
    
    try:
        while True:
            time.sleep(interval)
            
            current_hashes, changed_files = check_for_changes(previous_hashes)
            
            for changed_file in changed_files:
                notify_change(changed_file)
            
            previous_hashes = current_hashes
            
    except KeyboardInterrupt:
        print()
        print_os_message("Watch mode stopped", "INFO")
        return 0


def main() -> int:
    """Main entry point for watch command."""
    try:
        return watch_loop()
    except Exception as e:
        print_os_message(f"Error: {e}", "ERROR")
        return 1


if __name__ == "__main__":
    sys.exit(main())

