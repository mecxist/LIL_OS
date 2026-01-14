#!/usr/bin/env python3
"""
LIL OS² Status Command

Displays comprehensive system status including governance state,
validation history, rule counts, and system health.
"""

from __future__ import annotations

import sys
import re
from pathlib import Path
from datetime import datetime
from typing import List, Optional

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os_utils import (
    Colors, load_simple_yaml, read_text, print_os_box, print_os_message, strip_ansi
)


def count_rules_in_file(file_path: Path) -> int:
    """Count rule IDs in a file."""
    if not file_path.exists():
        return 0
    text = read_text(file_path)
    # Match rule ID pattern
    pattern = r'\[LIL-[A-Z]+-[A-Z]+-\d{4}\]'
    matches = re.findall(pattern, text)
    return len(set(matches))


def count_decision_log_entries(decision_log: Path) -> int:
    """Count entries in decision log."""
    if not decision_log.exists():
        return 0
    text = read_text(decision_log)
    # Count entries by looking for Date: fields (each entry should have one)
    date_pattern = r'^Date:\s*'
    matches = re.findall(date_pattern, text, re.MULTILINE)
    return len(matches)


def get_recent_validation_time(reports_dir: Path) -> Optional[str]:
    """Get time of most recent validation from reports."""
    if not reports_dir.exists():
        return None
    
    report_files = list(reports_dir.glob("*_report.json"))
    if not report_files:
        return None
    
    # Sort by modification time
    report_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    most_recent = report_files[0]
    
    # Get modification time
    mtime = most_recent.stat().st_mtime
    time_diff = datetime.now().timestamp() - mtime
    
    if time_diff < 60:
        return f"{int(time_diff)} seconds ago"
    elif time_diff < 3600:
        return f"{int(time_diff / 60)} minutes ago"
    elif time_diff < 86400:
        return f"{int(time_diff / 3600)} hours ago"
    else:
        return f"{int(time_diff / 86400)} days ago"


def get_system_health() -> tuple[str, str]:
    """
    Determine system health status.
    
    Returns:
        Tuple of (status, emoji)
    """
    # Check if config files exist
    config_files = [
        Path("lil_os.reset_checks.yaml"),
        Path("lil_os.rule_id.yaml"),
    ]
    
    missing_configs = [f for f in config_files if not f.exists()]
    if missing_configs:
        return ("CONFIG_MISSING", "⚠️")
    
    # Check if decision log exists
    decision_log = Path("docs/DECISION_LOG.md")
    if not decision_log.exists():
        return ("INCOMPLETE", "⚠️")
    
    return ("GOOD", "✅")


def get_status() -> dict:
    """Collect all status information."""
    status = {}
    
    # Version
    status["version"] = "0.1.1"
    
    # System health
    health_status, health_emoji = get_system_health()
    status["health"] = {"status": health_status, "emoji": health_emoji}
    
    # Count rules
    rule_files = [
        Path("docs/MASTER_RULES.md"),
        Path("docs/GOVERNANCE.md"),
        Path("docs/RESET_TRIGGERS.md"),
        Path("docs/CONTEXT_BUDGET.md"),
        Path(".cursorrules"),
    ]
    
    total_rules = sum(count_rules_in_file(f) for f in rule_files)
    status["rules"] = total_rules
    
    # Decision log entries
    decision_log = Path("docs/DECISION_LOG.md")
    status["decision_log_entries"] = count_decision_log_entries(decision_log)
    
    # Recent validation
    reports_dir = Path(".lil_os/reports")
    status["last_validation"] = get_recent_validation_time(reports_dir)
    
    # Config status
    status["configs"] = {
        "reset_checks": Path("lil_os.reset_checks.yaml").exists(),
        "rule_id": Path("lil_os.rule_id.yaml").exists(),
    }
    
    return status


def display_status(interactive: bool = False, use_rich: bool = False):
    """Display formatted status information."""
    status = get_status()
    
    # Enhanced visual layout with better formatting
    content = []
    content.append("")
    content.append(f"Version: {status['version']}")
    content.append(f"Status: {status['health']['status']}")
    content.append("")
    content.append("━━━ Governance ━━━")
    content.append("")
    content.append(f"  ● Rules: {status['rules']} active")
    
    if status['last_validation']:
        content.append(f"  ● Last validation: {status['last_validation']}")
    else:
        content.append("  ● Last validation: Never")
    
    content.append(f"  ● Decision log: {status['decision_log_entries']} entries")
    content.append("")
    content.append("━━━ System Health ━━━")
    content.append("")
    content.append(f"  {status['health']['emoji']} {status['health']['status']}")
    content.append("")
    
    # Use Rich UI if available and requested
    if use_rich:
        try:
            from . import cli_ux
            if cli_ux.is_rich_available():
                cli_ux.print_rich_panel("LIL OS² System Status", content)
                if interactive:
                    show_interactive_menu(use_rich=True)
                return
        except ImportError:
            pass
    
    # Use enhanced box with better formatting
    # Calculate optimal width based on content
    max_line_len = max(len(strip_ansi(line)) for line in content if line.strip())
    optimal_width = max(50, min(70, max_line_len + 20))  # Content + padding, but reasonable bounds
    print_os_box("LIL OS² System Status", content, width=optimal_width)
    
    # Show interactive menu if requested
    if interactive:
        show_interactive_menu()


def show_interactive_menu(use_rich: bool = False):
    """Show interactive menu with quick actions."""
    menu_items = [
        ("1", "Run validation", "lil-os check"),
        ("2", "Check rule IDs", "lil-os lint"),
        ("3", "View decision log", "cat docs/DECISION_LOG.md | head -50"),
        ("4", "Create decision entry", "lil-os log-decision"),
        ("5", "System health check", "lil-os health"),
        ("6", "Show help", "lil-os help"),
        ("7", "Launch shell", "lil-os shell"),
        ("0", "Exit", None),
    ]
    
    # Use Rich UI if available and requested
    if use_rich:
        try:
            from . import cli_ux
            if cli_ux.is_rich_available():
                console = cli_ux.get_console()
                console.print()
                console.print("[bright_cyan]Quick Actions:[/bright_cyan]")
                console.print()
                
                menu_content = []
                for key, label, command in menu_items:
                    menu_content.append(f"  [{key}] {label}")
                
                cli_ux.print_rich_panel("Menu", menu_content)
                console.print()
                
                try:
                    choice = cli_ux.InteractivePrompt.ask(
                        "[bright_cyan][LIL OS²][/bright_cyan] Select an option (or press Enter to exit)",
                        default="0",
                        choices=[item[0] for item in menu_items] + [""],
                        console=console
                    )
                    
                    if not choice or choice == "0":
                        console.print("[bright_green]Goodbye![/bright_green]")
                        return
                    
                    # Find selected menu item
                    selected = next((item for item in menu_items if item[0] == choice), None)
                    if selected:
                        _, label, command = selected
                        if command:
                            console.print()
                            console.print(f"[bright_cyan]To run:[/bright_cyan] {command}")
                            console.print("[dim]Run the command above, or use 'lil-os shell' for interactive mode.[/dim]")
                        else:
                            console.print("[dim]Exiting...[/dim]")
                    else:
                        console.print(f"[bright_yellow]Invalid choice: {choice}[/bright_yellow]")
                        console.print("[dim]Valid options: 0-7[/dim]")
                except (KeyboardInterrupt, EOFError):
                    console.print()
                    console.print("[dim]Cancelled.[/dim]")
                except Exception as e:
                    console.print(f"[bright_red]Error: {e}[/bright_red]")
                return
        except ImportError:
            pass
    
    # Fallback to regular menu
    print()
    print_os_message("Quick Actions:", "INFO")
    print()
    
    # Display menu in a box with better formatting
    menu_content = []
    menu_content.append("")
    for key, label, command in menu_items:
        # Use bullet point for better visual
        menu_content.append(f"  [{key}] {label}")
    menu_content.append("")
    
    print_os_box("Menu", menu_content, width=52, show_separator=False)
    print()
    
    try:
        choice = input(f"{Colors.BRIGHT_CYAN}[LIL OS²]{Colors.RESET} Select an option (or press Enter to exit): ").strip()
        
        if not choice or choice == "0":
            print_os_message("Goodbye!", "INFO")
            return
        
        # Find selected menu item
        selected = next((item for item in menu_items if item[0] == choice), None)
        if selected:
            _, label, command = selected
            if command:
                print()
                print_os_message(f"To run: {Colors.BRIGHT_CYAN}{command}{Colors.RESET}", "INFO")
                print_os_message("Run the command above, or use 'lil-os shell' for interactive mode.", "INFO")
            else:
                print_os_message("Exiting...", "INFO")
        else:
            print_os_message(f"Invalid choice: {choice}", "WARN")
            print_os_message("Valid options: 0-7", "INFO")
    except (KeyboardInterrupt, EOFError):
        print()
        print_os_message("Cancelled.", "INFO")
    except Exception as e:
        print_os_message(f"Error: {e}", "ERROR")


def main(interactive: bool = False, use_rich: bool = False) -> int:
    """Main entry point for status command."""
    try:
        display_status(interactive=interactive, use_rich=use_rich)
        return 0
    except Exception as e:
        print_os_message(f"Error getting status: {e}", "ERROR")
        return 1


if __name__ == "__main__":
    sys.exit(main())

