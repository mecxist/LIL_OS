#!/usr/bin/env python3
"""
LIL OS² Help System

Provides context-aware help, rule explanations, and scenario-based guides.
"""

from __future__ import annotations

import sys
import re
from pathlib import Path
from typing import Optional, Dict, List

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os_utils import print_os_message, print_os_box, read_text, Colors


def explain_rule(rule_id: str) -> bool:
    """
    Explain a specific rule ID.
    
    Args:
        rule_id: The rule ID to explain (e.g., LIL-CR-PROCESS-0001)
        
    Returns:
        True if rule was found and explained, False otherwise
    """
    # Search for rule in governance files
    search_files = [
        Path("docs/MASTER_RULES.md"),
        Path("docs/GOVERNANCE.md"),
        Path("docs/RESET_TRIGGERS.md"),
        Path("docs/CONTEXT_BUDGET.md"),
        Path(".cursorrules"),
    ]
    
    for file_path in search_files:
        if not file_path.exists():
            continue
        
        text = read_text(file_path)
        
        # Look for rule ID in text
        pattern = re.escape(rule_id)
        if re.search(pattern, text):
            # Extract the line with the rule
            lines = text.splitlines()
            for i, line in enumerate(lines):
                if rule_id in line:
                    # Get context (previous and next few lines)
                    start = max(0, i - 2)
                    end = min(len(lines), i + 5)
                    context = lines[start:end]
                    
                    content = []
                    content.append(f"Rule ID: {rule_id}")
                    content.append(f"Found in: {file_path}")
                    content.append("")
                    content.append("Rule:")
                    for ctx_line in context:
                        content.append(f"  {ctx_line}")
                    
                    print_os_box(f"Rule Explanation: {rule_id}", content, width=70)
                    return True
    
    print_os_message(f"Rule ID '{rule_id}' not found in governance files.", "WARN")
    print_os_message("Try searching in: docs/MASTER_RULES.md, docs/GOVERNANCE.md, .cursorrules", "INFO")
    return False


def show_command_help(command: str) -> bool:
    """
    Show help for a specific command.
    
    Args:
        command: The command name
        
    Returns:
        True if command help was shown, False otherwise
    """
    help_texts = {
        "setup": [
            "Run the LIL OS² setup wizard.",
            "",
            "This command will:",
            "  • Create necessary directories",
            "  • Set up decision log",
            "  • Configure pre-commit hooks",
            "  • Configure reporting",
            "",
            "Usage: lil-os setup"
        ],
        "status": [
            "Show LIL OS² system status.",
            "",
            "Displays:",
            "  • Version information",
            "  • Active rule count",
            "  • Last validation time",
            "  • Decision log entry count",
            "  • System health",
            "",
            "Usage: lil-os status"
        ],
        "lint": [
            "Check rule IDs for format and consistency.",
            "",
            "Validates:",
            "  • Rule ID format",
            "  • Rule ID uniqueness",
            "  • Normative keywords",
            "  • Dangling references",
            "",
            "Usage:",
            "  lil-os lint",
            "  lil-os lint --interactive"
        ],
        "check": [
            "Run reset trigger checks.",
            "",
            "Checks for:",
            "  • Rule accretion velocity",
            "  • Rule contradictions",
            "  • Justification decay",
            "  • Context budget overflow",
            "  • Automation creep",
            "  • Security issues",
            "",
            "Usage:",
            "  lil-os check",
            "  lil-os check --interactive"
        ],
        "warn": [
            "Check for critical changes before commit.",
            "",
            "Warns about:",
            "  • Governance file modifications",
            "  • Missing decision log entries",
            "  • Large changes",
            "  • Potential secrets",
            "",
            "Usage:",
            "  lil-os warn",
            "  lil-os warn --pre-commit"
        ],
        "log-decision": [
            "Interactively create a decision log entry.",
            "",
            "Prompts for:",
            "  • Decision description",
            "  • Trigger",
            "  • Rationale",
            "  • Tradeoffs",
            "  • Expected impact",
            "  • Review date",
            "",
            "Usage: lil-os log-decision"
        ],
        "info": [
            "Show system information.",
            "",
            "Displays:",
            "  • Version",
            "  • Platform information",
            "  • Installation details",
            "  • Documentation links",
            "",
            "Usage: lil-os info"
        ],
        "version": [
            "Show version information.",
            "",
            "Usage: lil-os version"
        ],
        "health": [
            "Quick health check.",
            "",
            "Checks:",
            "  • Config files exist",
            "  • Decision log exists",
            "  • Scripts are present",
            "",
            "Usage: lil-os health"
        ],
    }
    
    if command not in help_texts:
        print_os_message(f"Unknown command: {command}", "ERROR")
        print_os_message("Available commands: setup, status, lint, check, warn, log-decision, info, version, health", "INFO")
        return False
    
    print_os_box(f"Help: {command}", help_texts[command], width=70)
    return True


def show_guide(scenario: str) -> bool:
    """
    Show scenario-based guide.
    
    Args:
        scenario: The scenario name
        
    Returns:
        True if guide was shown, False otherwise
    """
    guides = {
        "first-setup": [
            "First Time Setup Guide",
            "",
            "1. Run: lil-os setup",
            "2. Follow the interactive prompts",
            "3. Review docs/USER_GUIDE.md",
            "4. Start coding normally",
            "",
            "LIL OS² only steps in for important decisions."
        ],
        "governance-change": [
            "Making a Governance Change",
            "",
            "1. Modify governance files (GOVERNANCE.md, MASTER_RULES.md, etc.)",
            "2. Run: lil-os log-decision",
            "3. Fill in the required fields",
            "4. Review and save",
            "5. Commit your changes",
            "",
            "The decision log entry documents why you made the change."
        ],
        "fixing-errors": [
            "Fixing Validation Errors",
            "",
            "1. Run: lil-os check (or lil-os lint)",
            "2. Review the error messages",
            "3. Each error includes actionable steps",
            "4. Fix the issues",
            "5. Run validation again",
            "",
            "Use 'lil-os explain [rule-id]' for rule details."
        ],
        "understanding-rules": [
            "Understanding Rules",
            "",
            "1. Use: lil-os explain [rule-id]",
            "2. Read docs/MASTER_RULES.md",
            "3. Check docs/GOVERNANCE.md",
            "4. Review docs/RULE_IDS.md",
            "",
            "Rules are identified by IDs like: LIL-CR-PROCESS-0001"
        ],
    }
    
    if scenario not in guides:
        print_os_message(f"Unknown scenario: {scenario}", "ERROR")
        print_os_message("Available scenarios: first-setup, governance-change, fixing-errors, understanding-rules", "INFO")
        return False
    
    print_os_box(guides[scenario][0], guides[scenario][1:], width=70)
    return True


def show_general_help():
    """Show general help information."""
    content = [
        "LIL OS² - A constitutional substrate for AI-assisted software development",
        "",
        "Available Commands:",
        "  setup          Run the setup wizard",
        "  status         Show system status",
        "  lint           Check rule IDs",
        "  check          Run reset trigger checks",
        "  warn           Check for critical changes",
        "  log-decision   Create decision log entry",
        "  info           Show system information",
        "  version        Show version",
        "  health         Quick health check",
        "  help           Show this help",
        "",
        "Get Help:",
        "  lil-os help [command]     Help for specific command",
        "  lil-os explain [rule-id]  Explain a rule",
        "  lil-os guide [scenario]   Scenario-based guide",
        "",
        "Examples:",
        "  lil-os help check",
        "  lil-os explain LIL-CR-PROCESS-0001",
        "  lil-os guide first-setup"
    ]
    
    print_os_box("LIL OS² Help", content, width=70)


def main(command: Optional[str] = None, rule_id: Optional[str] = None, scenario: Optional[str] = None) -> int:
    """Main entry point for help system."""
    try:
        if rule_id:
            if not explain_rule(rule_id):
                return 1
        elif scenario:
            if not show_guide(scenario):
                return 1
        elif command:
            if not show_command_help(command):
                return 1
        else:
            show_general_help()
        
        return 0
    except Exception as e:
        print_os_message(f"Error: {e}", "ERROR")
        return 1


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--command", help="Command to get help for")
    parser.add_argument("--rule-id", help="Rule ID to explain")
    parser.add_argument("--scenario", help="Scenario guide to show")
    args = parser.parse_args()
    sys.exit(main(args.command, args.rule_id, args.scenario))

