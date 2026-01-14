#!/usr/bin/env python3
"""
LIL OS² Interactive Decision Logging

Provides interactive prompts for creating decision log entries
when governance files are modified.
"""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os_utils import (
    Colors, print_os_message, print_os_box, read_text
)


def git_available() -> bool:
    """Check if git is available."""
    try:
        subprocess.run(["git", "--version"], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def get_staged_files() -> List[Path]:
    """Get list of staged files."""
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


def detect_governance_changes() -> List[Path]:
    """Detect if governance files have been modified."""
    staged = get_staged_files()
    return [f for f in staged if is_governance_file(f)]


def prompt_for_field(field_name: str, required: bool = True, suggestions: Optional[List[str]] = None) -> str:
    """Prompt user for a field value."""
    prompt = f"{Colors.BRIGHT_CYAN}[LIL OS²]{Colors.RESET} {field_name}"
    if suggestions:
        prompt += f" (suggestions: {', '.join(suggestions[:3])})"
    if not required:
        prompt += " (optional)"
    prompt += ": "
    
    value = input(prompt).strip()
    
    if required and not value:
        print_os_message(f"{field_name} is required. Please provide a value.", "WARN")
        return prompt_for_field(field_name, required, suggestions)
    
    return value


def prompt_multiline(field_name: str, required: bool = True) -> str:
    """Prompt for multi-line input."""
    print_os_message(f"{field_name} (press Enter twice when done):", "INFO")
    lines = []
    empty_count = 0
    
    while True:
        line = input()
        if not line.strip():
            empty_count += 1
            if empty_count >= 2:
                break
        else:
            empty_count = 0
            lines.append(line)
    
    value = "\n".join(lines).strip()
    
    if required and not value:
        print_os_message(f"{field_name} is required. Please provide a value.", "WARN")
        return prompt_multiline(field_name, required)
    
    return value


def create_decision_log_entry() -> Optional[str]:
    """Interactively create a decision log entry."""
    # Check for governance changes
    governance_files = detect_governance_changes()
    
    if not governance_files:
        # Check modified files (not staged)
        if git_available():
            try:
                result = subprocess.run(
                    ["git", "diff", "--name-only", "--diff-filter=ACM"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                modified = [Path(f) for f in result.stdout.strip().splitlines() if f.strip()]
                governance_files = [f for f in modified if is_governance_file(f)]
            except subprocess.CalledProcessError:
                pass
    
    if governance_files:
        print_os_message("Governance change detected", "WARN")
        print_os_message(f"Modified files: {', '.join(str(f) for f in governance_files)}", "INFO")
        print()
    
    print_os_box("Create Decision Log Entry", [
        "A decision log entry is required for governance changes.",
        "",
        "Please provide the following information:"
    ], width=60)
    print()
    
    # Auto-fill date
    date = datetime.now().strftime("%Y-%m-%d")
    print_os_message(f"Date: {date} (auto-filled)", "INFO")
    
    # Prompt for required fields
    decision = prompt_for_field("Decision", required=True)
    trigger = prompt_for_field("Trigger", required=True, suggestions=[
        "Governance file modification",
        "Rule addition",
        "Rule modification",
        "Context budget change",
        "Reset trigger activation"
    ])
    
    print()
    rationale = prompt_multiline("Rationale", required=True)
    
    print()
    tradeoffs = prompt_multiline("Tradeoffs", required=True)
    
    print()
    expected_impact = prompt_multiline("Expected Impact", required=True)
    
    print()
    review_date = prompt_for_field("Review Date", required=False, suggestions=["30 days", "90 days", "N/A"])
    
    # Build entry
    entry = f"""
## {date}

**Decision:** {decision}

**Trigger:** {trigger}

**Rationale:**
{rationale}

**Tradeoffs:**
{tradeoffs}

**Expected Impact:**
{expected_impact}

**Review Date:** {review_date if review_date else "N/A"}

---
"""
    
    # Show preview
    print()
    print_os_box("Preview", entry.split("\n"), width=70)
    print()
    
    confirm = input(f"{Colors.BRIGHT_CYAN}[LIL OS²]{Colors.RESET} Save this entry? [Y/n]: ").strip().lower()
    
    if confirm and confirm != 'y':
        print_os_message("Entry cancelled.", "INFO")
        return None
    
    return entry


def append_to_decision_log(entry: str) -> bool:
    """Append entry to decision log."""
    decision_log = Path("docs/DECISION_LOG.md")
    
    if not decision_log.exists():
        print_os_message("Decision log not found. Creating it...", "WARN")
        # Create basic structure
        decision_log.parent.mkdir(parents=True, exist_ok=True)
        content = """# Decision Log (v1.0)

## Purpose
Records intent-level decisions that alter meaning, authority, or trajectory.

## Entries

"""
        decision_log.write_text(content, encoding="utf-8")
    
    # Read existing content
    content = read_text(decision_log)
    
    # Find "## Entries" section or append at end
    if "## Entries" in content:
        # Insert after "## Entries" section
        parts = content.split("## Entries", 1)
        if len(parts) == 2:
            new_content = parts[0] + "## Entries" + parts[1] + entry
        else:
            new_content = content + entry
    else:
        new_content = content + "\n## Entries\n" + entry
    
    decision_log.write_text(new_content, encoding="utf-8")
    return True


def main() -> int:
    """Main entry point for decision logging."""
    try:
        entry = create_decision_log_entry()
        
        if entry:
            if append_to_decision_log(entry):
                print_os_message("Decision log entry created successfully!", "SUCCESS")
                print_os_message(f"Entry saved to: docs/DECISION_LOG.md", "INFO")
                return 0
            else:
                print_os_message("Failed to save entry.", "ERROR")
                return 1
        else:
            return 0
    except KeyboardInterrupt:
        print_os_message("\nOperation cancelled by user.", "WARN")
        return 130
    except Exception as e:
        print_os_message(f"Error: {e}", "ERROR")
        return 1


if __name__ == "__main__":
    sys.exit(main())

