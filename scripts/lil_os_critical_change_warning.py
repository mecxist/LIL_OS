#!/usr/bin/env python3
"""
LIL OS Critical Change Warning System

Provides non-blocking warnings to inexperienced developers when they're about to make
important or critical changes. Designed to catch issues before commits, especially
for users who don't use pull requests.

This script is designed to be run:
- As a pre-commit hook (warns but doesn't block)
- Manually before making important changes
- As part of the validation workflow

Exit codes:
- 0: No critical issues found (or warnings only)
- 1: Critical issues found (but doesn't block - just warns)
"""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path
from typing import List, Tuple, Optional
from datetime import datetime

# Import shared utilities
from lil_os_utils import Colors

def git_available() -> bool:
    """Check if git is available."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def get_staged_files() -> List[Path]:
    """Get list of staged files that are being committed."""
    if not git_available():
        return []
    
    try:
        result = subprocess.run(
            ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True
        )
        return [Path(f) for f in result.stdout.strip().splitlines() if f.strip()]
    except subprocess.CalledProcessError:
        return []

def get_modified_files() -> List[Path]:
    """Get list of modified files (for manual runs)."""
    if not git_available():
        return []
    
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", "--diff-filter=ACM"],
            capture_output=True,
            text=True,
            check=True
        )
        return [Path(f) for f in result.stdout.strip().splitlines() if f.strip()]
    except subprocess.CalledProcessError:
        return []

def is_governance_file(file_path: Path) -> bool:
    """Check if a file is a governance file."""
    governance_files = [
        "docs/MASTER_RULES.md",
        "docs/GOVERNANCE.md",
        "docs/RESET_TRIGGERS.md",
        "docs/CONTEXT_BUDGET.md",
        ".cursorrules",
    ]
    return str(file_path) in governance_files

def is_decision_log(file_path: Path) -> bool:
    """Check if a file is the decision log."""
    return str(file_path) == "docs/DECISION_LOG.md"

def check_governance_file_changes(files: List[Path]) -> List[str]:
    """Check if governance files are being modified."""
    warnings = []
    governance_files = [f for f in files if is_governance_file(f)]
    
    if governance_files:
        warnings.append(
            f"{Colors.BRIGHT_YELLOW}⚠️  WARNING: You're modifying governance files:{Colors.RESET}\n"
            f"   {', '.join(str(f) for f in governance_files)}\n"
            f"   {Colors.YELLOW}These are critical files that define your project's rules.{Colors.RESET}\n"
            f"   {Colors.CYAN}Before committing, make sure you:{Colors.RESET}\n"
            f"   1. Have a decision log entry explaining why you're changing these rules\n"
            f"   2. Understand the impact of these changes\n"
            f"   3. Have considered the tradeoffs\n"
            f"   {Colors.DIM}See docs/GOVERNANCE.md for more information{Colors.RESET}\n"
        )
    
    return warnings

def check_decision_log_entry(files: List[Path]) -> List[str]:
    """Check if decision log has a new entry when governance files are modified."""
    warnings = []
    governance_files = [f for f in files if is_governance_file(f)]
    decision_log_modified = any(is_decision_log(f) for f in files)
    
    if governance_files and not decision_log_modified:
        warnings.append(
            f"{Colors.BRIGHT_RED}⚠️  IMPORTANT: You're modifying governance files but haven't updated the decision log!{Colors.RESET}\n"
            f"   {Colors.YELLOW}Governance file changes require a decision log entry.{Colors.RESET}\n"
            f"   {Colors.CYAN}Please add an entry to docs/DECISION_LOG.md that explains:{Colors.RESET}\n"
            f"   - Why you're making this change\n"
            f"   - Who benefits from this change\n"
            f"   - What tradeoffs you're accepting\n"
            f"   - What alternatives you considered\n"
            f"   {Colors.DIM}See docs/DECISION_LOG.md for the required format{Colors.RESET}\n"
        )
    
    return warnings

def check_large_changes(files: List[Path]) -> List[str]:
    """Check for unusually large changes that might indicate important decisions."""
    warnings = []
    
    if not git_available():
        return warnings
    
    large_threshold = 50  # lines changed
    
    for file_path in files:
        if not file_path.exists():
            continue
        
        try:
            # Check staged changes
            result = subprocess.run(
                ["git", "diff", "--cached", "--numstat", str(file_path)],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0 and result.stdout.strip():
                parts = result.stdout.strip().split()
                if len(parts) >= 2:
                    try:
                        added = int(parts[0])
                        deleted = int(parts[1])
                        total = added + deleted
                        
                        if total > large_threshold and is_governance_file(file_path):
                            warnings.append(
                                f"{Colors.BRIGHT_YELLOW}⚠️  Large change detected in {file_path}{Colors.RESET}\n"
                                f"   {total} lines changed ({added} added, {deleted} deleted)\n"
                                f"   {Colors.CYAN}This is a significant change. Make sure you've logged it in the decision log.{Colors.RESET}\n"
                            )
                    except ValueError:
                        pass
        except Exception:
            pass
    
    return warnings

def check_secrets_in_changes(files: List[Path]) -> List[str]:
    """Quick check for obvious secrets in changed files."""
    warnings = []
    secret_patterns = [
        (r'api[_-]?key\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{32,}["\']?', 'API key'),
        (r'secret[_-]?key\s*[:=]\s*["\']?[a-zA-Z0-9_\-]{32,}["\']?', 'Secret key'),
        (r'password\s*[:=]\s*["\']?.{12,}["\']?', 'Password'),
        (r'-----BEGIN.*PRIVATE KEY-----', 'Private key'),
    ]
    
    import re
    
    for file_path in files:
        if not file_path.exists() or file_path.name == "SECURITY.md":
            continue
        
        try:
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            
            for pattern, secret_type in secret_patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    warnings.append(
                        f"{Colors.BRIGHT_RED}⚠️  SECURITY WARNING: Possible {secret_type} found in {file_path}{Colors.RESET}\n"
                        f"   {Colors.YELLOW}Never commit secrets to version control!{Colors.RESET}\n"
                        f"   {Colors.CYAN}Use environment variables or secret management tools instead.{Colors.RESET}\n"
                    )
                    break  # Only warn once per file
        except Exception:
            pass
    
    return warnings

def print_warnings(warnings: List[str], is_pre_commit: bool = False):
    """Print all warnings in a user-friendly format."""
    if not warnings:
        if not is_pre_commit:
            print(f"{Colors.BRIGHT_GREEN}✅ No critical change warnings{Colors.RESET}")
        return
    
    print(f"\n{Colors.BRIGHT_CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.BOLD}  LIL OS Critical Change Warnings{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'='*70}{Colors.RESET}\n")
    
    for warning in warnings:
        print(warning)
        print()
    
    print(f"{Colors.BRIGHT_CYAN}{'='*70}{Colors.RESET}")
    print(f"{Colors.DIM}Note: These are warnings, not errors. Your commit will proceed.{Colors.RESET}")
    print(f"{Colors.DIM}However, please review these warnings carefully before committing.{Colors.RESET}")
    print(f"{Colors.BRIGHT_CYAN}{'='*70}{Colors.RESET}\n")

def main() -> int:
    """Main function."""
    # Check if we're in a git repository
    if not git_available():
        print(f"{Colors.YELLOW}⚠️  Git not available. Skipping critical change warnings.{Colors.RESET}")
        return 0
    
    # Determine if this is a pre-commit hook or manual run
    is_pre_commit = "--pre-commit" in sys.argv
    
    # Get files to check
    if is_pre_commit:
        files = get_staged_files()
    else:
        files = get_modified_files()
        if not files:
            # Check staged files as fallback
            files = get_staged_files()
    
    if not files:
        if not is_pre_commit:
            print(f"{Colors.DIM}No modified files to check.{Colors.RESET}")
        return 0
    
    # Collect all warnings
    warnings = []
    warnings.extend(check_governance_file_changes(files))
    warnings.extend(check_decision_log_entry(files))
    warnings.extend(check_large_changes(files))
    warnings.extend(check_secrets_in_changes(files))
    
    # Print warnings
    print_warnings(warnings, is_pre_commit)
    
    # Return 0 (success) even with warnings - we're warning, not blocking
    return 0

if __name__ == "__main__":
    sys.exit(main())

