#!/usr/bin/env python3
"""
LIL OS² CLI - Command-line interface for LIL OS²

Provides unified CLI commands for all LIL OS² functionality.
"""

from __future__ import annotations

import sys
import argparse
import time
from pathlib import Path

# Add scripts directory to path for imports
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

# Import script modules
import lil_os_reset_checks
import lil_os_rule_id_lint
import lil_os_critical_change_warning
import setup_wizard

# Import LIL OS² modules
from . import status
from . import decision_prompt
from . import help_system
from . import shell
from . import watch
from . import box_designer
from . import session
from . import cli_ux


def setup_command(args):
    """Run the setup wizard."""
    try:
        setup_wizard.main()
        return 0
    except SystemExit as e:
        return e.code if e.code is not None else 0


def lint_command(args):
    """Run rule ID linting."""
    use_rich = getattr(args, 'rich', False)
    use_stream = getattr(args, 'stream', False)
    
    if args.interactive:
        return run_interactive_validation("lint", lil_os_rule_id_lint.main, use_rich=use_rich)
    
    if use_rich or use_stream:
        return run_rich_validation("lint", lil_os_rule_id_lint.main, use_stream=use_stream)
    
    return lil_os_rule_id_lint.main()


def check_command(args):
    """Run reset checks."""
    use_rich = getattr(args, 'rich', False)
    use_stream = getattr(args, 'stream', False)
    
    if args.interactive:
        return run_interactive_validation("check", lil_os_reset_checks.main, use_rich=use_rich)
    
    if use_rich or use_stream:
        return run_rich_validation("check", lil_os_reset_checks.main, use_stream=use_stream)
    
    return lil_os_reset_checks.main()


def run_interactive_validation(command_name: str, validation_func, use_rich: bool = False):
    """Run validation in interactive mode, showing findings one at a time."""
    sys.path.insert(0, str(scripts_dir))
    from lil_os_utils import print_os_message, print_os_box, Finding
    
    if use_rich and cli_ux.is_rich_available():
        console = cli_ux.get_console()
        console.print(f"[bright_cyan]🔍 LIL OS²: Running {command_name} in interactive mode...[/bright_cyan]")
        console.print("[dim]Findings will be shown one at a time.[/dim]\n")
    else:
        print_os_message(f"Running {command_name} in interactive mode...", "INFO")
        print_os_message("Findings will be shown one at a time.", "INFO")
        print()
    
    # We need to capture findings, but the current functions print directly
    # For now, we'll run the validation and then provide interactive navigation
    # This is a simplified version - full implementation would require refactoring
    # the validation functions to return findings instead of printing
    
    if use_rich and cli_ux.is_rich_available():
        console.print("[dim]Interactive mode: Running validation...[/dim]")
    else:
        print_os_message("Interactive mode: Running validation...", "INFO")
    
    result = validation_func()
    
    if use_rich and cli_ux.is_rich_available():
        if result == 0:
            console.print("[bright_green]✅ All checks passed![/bright_green]")
        else:
            console.print("[bright_yellow]⚠️  Some issues were found. Review the output above.[/bright_yellow]")
            console.print("[dim]Use 'lil-os help' for guidance on fixing issues.[/dim]")
    else:
        if result == 0:
            print_os_message("All checks passed!", "SUCCESS")
        else:
            print_os_message("Some issues were found. Review the output above.", "WARN")
            print_os_message("Use 'lil-os help' for guidance on fixing issues.", "INFO")
    
    return result


def run_rich_validation(command_name: str, validation_func, use_stream: bool = False):
    """Run validation with Rich UI."""
    if not cli_ux.is_rich_available():
        # Fallback to regular execution
        return validation_func()
    
    console = cli_ux.get_console()
    
    if use_stream:
        # Use streaming output
        with cli_ux.StreamingOutput(console=console) as live:
            console.print(f"[bright_cyan]🔍 LIL OS²: Running {command_name}...[/bright_cyan]")
            result = validation_func()
    else:
        # Regular Rich output
        console.print(f"[bright_cyan]🔍 LIL OS²: Running {command_name}...[/bright_cyan]")
        result = validation_func()
    
    return result


def warn_command(args):
    """Run critical change warnings."""
    is_pre_commit = args.pre_commit
    argv = sys.argv[:1]  # Keep script name
    if is_pre_commit:
        argv.append("--pre-commit")
    sys.argv = argv
    return lil_os_critical_change_warning.main()


def status_command(args):
    """Display system status."""
    interactive = getattr(args, 'interactive', False)
    use_rich = getattr(args, 'rich', False)
    
    if use_rich and cli_ux.is_rich_available():
        # Use Rich UI for status
        return status.main(interactive=interactive, use_rich=True)
    
    return status.main(interactive=interactive)


def info_command(args):
    """Show system information."""
    sys.path.insert(0, str(scripts_dir))
    from lil_os_utils import print_os_box, print_os_message
    import platform
    
    content = []
    content.append(f"LIL OS² Version: 2.0.0")
    content.append(f"Python Version: {platform.python_version()}")
    content.append(f"Platform: {platform.system()} {platform.release()}")
    content.append("")
    content.append("Installation:")
    content.append("  • Package: lil-os")
    content.append("  • CLI: lil-os")
    content.append("")
    content.append("Documentation:")
    content.append("  • User Guide: docs/USER_GUIDE.md")
    content.append("  • Governance: docs/GOVERNANCE.md")
    content.append("  • Website: https://www.lilco.io")
    
    print_os_box("LIL OS² System Information", content, width=60)
    return 0


def version_command(args):
    """Show version information."""
    from lil_os_utils import print_os_message
    print_os_message("LIL OS² v2.0.0", "INFO")
    print_os_message("A constitutional substrate for AI-assisted software development", "INFO")
    return 0


def health_command(args):
    """Quick health check."""
    sys.path.insert(0, str(scripts_dir))
    from lil_os_utils import print_os_message, print_os_box
    from pathlib import Path
    
    issues = []
    checks = []
    
    # Check config files
    reset_config = Path("lil_os.reset_checks.yaml")
    rule_config = Path("lil_os.rule_id.yaml")
    
    if reset_config.exists():
        checks.append("✅ Reset checks config found")
    else:
        checks.append("❌ Reset checks config missing")
        issues.append("Missing: lil_os.reset_checks.yaml")
    
    if rule_config.exists():
        checks.append("✅ Rule ID config found")
    else:
        checks.append("❌ Rule ID config missing")
        issues.append("Missing: lil_os.rule_id.yaml")
    
    # Check decision log
    decision_log = Path("docs/DECISION_LOG.md")
    if decision_log.exists():
        checks.append("✅ Decision log found")
    else:
        checks.append("⚠️  Decision log missing")
        issues.append("Missing: docs/DECISION_LOG.md")
    
    # Check scripts
    scripts_dir_path = Path("scripts")
    required_scripts = [
        "lil_os_reset_checks.py",
        "lil_os_rule_id_lint.py",
        "lil_os_critical_change_warning.py",
    ]
    
    for script in required_scripts:
        if (scripts_dir_path / script).exists():
            checks.append(f"✅ {script} found")
        else:
            checks.append(f"❌ {script} missing")
            issues.append(f"Missing: scripts/{script}")
    
    content = checks.copy()
    if issues:
        content.append("")
        content.append("Issues found:")
        for issue in issues:
            content.append(f"  • {issue}")
        content.append("")
        content.append("Run 'lil-os setup' to fix issues")
    
    print_os_box("LIL OS² Health Check", content, width=60)
    
    return 1 if issues else 0


def log_decision_command(args):
    """Interactively create a decision log entry."""
    return decision_prompt.main()


def help_command(args):
    """Show help information."""
    return help_system.main(
        command=args.command if hasattr(args, 'command') and args.command else None,
        rule_id=args.rule_id if hasattr(args, 'rule_id') and args.rule_id else None,
        scenario=args.scenario if hasattr(args, 'scenario') and args.scenario else None
    )


def shell_command(args):
    """Launch interactive shell."""
    # Use enhanced shell by default, fallback to basic shell on error
    try:
        from . import shell_enhanced
        return shell_enhanced.main()
    except Exception as e:
        # Fallback to basic shell if enhanced shell fails
        print(f"Enhanced shell unavailable: {e}", file=sys.stderr)
        print("Falling back to basic shell...", file=sys.stderr)
        from . import shell
        return shell.main()


def watch_command(args):
    """Monitor governance files for changes."""
    return watch.main()


def designer_command(args):
    """Run the interactive box designer."""
    from . import box_designer
    return box_designer.main()


def daemon_command(args):
    """Manage background daemon."""
    from . import daemon
    import sys
    # Create a mock sys.argv for daemon.main()
    original_argv = sys.argv
    try:
        sys.argv = ["lil-os", "daemon", args.action]
        if hasattr(args, 'config') and args.config:
            sys.argv.extend(["--config", str(args.config)])
        return daemon.main()
    finally:
        sys.argv = original_argv


def rules_command(args):
    """Manage rules."""
    from .core import RuleManager
    from lil_os_utils import print_os_message, print_os_box, Colors
    
    rule_manager = RuleManager()
    
    if args.subcommand == "list":
        rules = rule_manager.get_all_rules()
        if not rules:
            print_os_message("No rules found", "INFO")
            return 0
        
        content = []
        for rule in sorted(rules, key=lambda r: r.rule_id):
            lifecycle_color = {
                "active": Colors.GREEN,
                "deprecated": Colors.YELLOW,
                "draft": Colors.CYAN,
                "removed": Colors.RED,
            }.get(rule.lifecycle.value, Colors.WHITE)
            
            content.append(
                f"  {rule.rule_id} {lifecycle_color}[{rule.lifecycle.value.upper()}]{Colors.RESET} "
                f"- {rule.text[:60]}..."
            )
        
        print_os_box("Rules", content, width=100)
        print_os_message(f"Total: {len(rules)} rules", "INFO")
        return 0
    
    elif args.subcommand == "show":
        if not args.rule_id:
            print_os_message("Rule ID required", "ERROR")
            return 1
        
        rule = rule_manager.get_rule(args.rule_id)
        if not rule:
            print_os_message(f"Rule {args.rule_id} not found", "ERROR")
            return 1
        
        content = [
            f"  Rule ID: {rule.rule_id}",
            f"  Lifecycle: {rule.lifecycle.value}",
            f"  File: {rule.file_path} (line {rule.line_number})",
            f"  Normative: {rule.normative_keyword}",
            f"  Text: {rule.text}",
        ]
        
        if rule.dependencies:
            content.append(f"  Dependencies: {', '.join(sorted(rule.dependencies))}")
        if rule.dependents:
            content.append(f"  Dependents: {', '.join(sorted(rule.dependents))}")
        
        print_os_box(f"Rule: {args.rule_id}", content, width=100)
        return 0
    
    elif args.subcommand == "dependencies":
        if not args.rule_id:
            print_os_message("Rule ID required", "ERROR")
            return 1
        
        rule = rule_manager.get_rule(args.rule_id)
        if not rule:
            print_os_message(f"Rule {args.rule_id} not found", "ERROR")
            return 1
        
        deps = rule_manager.get_rule_dependencies(args.rule_id)
        dependents = rule_manager.get_rule_dependents(args.rule_id)
        
        content = []
        if deps:
            content.append("  Dependencies:")
            for dep in deps:
                content.append(f"    - {dep.rule_id}: {dep.text[:50]}...")
        else:
            content.append("  No dependencies")
        
        content.append("")
        
        if dependents:
            content.append("  Dependents:")
            for dep in dependents:
                content.append(f"    - {dep.rule_id}: {dep.text[:50]}...")
        else:
            content.append("  No dependents")
        
        print_os_box(f"Dependencies for {args.rule_id}", content, width=100)
        return 0
    
    elif args.subcommand == "impact":
        if not args.rule_id:
            print_os_message("Rule ID required", "ERROR")
            return 1
        
        impact = rule_manager.analyze_rule_impact(args.rule_id)
        if not impact:
            print_os_message(f"Rule {args.rule_id} not found", "ERROR")
            return 1
        
        content = [
            f"  Rule: {impact['rule_id']}",
            f"  Estimated Impact: {impact['estimated_impact'].upper()}",
            f"  Total Affected Rules: {impact['total_affected_rules']}",
            f"  Direct Dependents: {len(impact['direct_dependents'])}",
            f"  Transitive Dependents: {len(impact['transitive_dependents'])}",
            f"  Affected Files: {len(impact['affected_files'])}",
        ]
        
        if impact['direct_dependents']:
            content.append("  Direct Dependents:")
            for dep_id in impact['direct_dependents']:
                content.append(f"    - {dep_id}")
        
        print_os_box(f"Impact Analysis: {args.rule_id}", content, width=100)
        return 0
    
    elif args.subcommand == "contradictions":
        contradictions = rule_manager.find_contradictions()
        if not contradictions:
            print_os_message("No contradictions found", "SUCCESS")
            return 0
        
        content = []
        for contradiction in contradictions:
            content.append(
                f"  {contradiction['rule1']} vs {contradiction['rule2']}"
            )
            content.append(f"    {contradiction['explanation']}")
            content.append("")
        
        print_os_box("Rule Contradictions", content, width=100)
        print_os_message(f"Found {len(contradictions)} potential contradictions", "WARN")
        return 1
    
    return 0


def decisions_command(args):
    """Manage decision log."""
    from .core import DecisionLogManager
    from lil_os_utils import print_os_message, print_os_box, Colors
    
    decision_manager = DecisionLogManager()
    
    if args.subcommand == "list":
        entries = decision_manager.get_all_entries()
        if not entries:
            print_os_message("No decision log entries found", "INFO")
            return 0
        
        content = []
        for entry in sorted(entries, key=lambda e: e.date, reverse=True):
            date_str = entry.date.strftime("%Y-%m-%d")
            content.append(
                f"  [{date_str}] Entry #{entry.entry_number}: {entry.decision[:60]}..."
            )
        
        print_os_box("Decision Log Entries", content, width=100)
        print_os_message(f"Total: {len(entries)} entries", "INFO")
        return 0
    
    elif args.subcommand == "show":
        if not args.entry_number:
            print_os_message("Entry number required", "ERROR")
            return 1
        
        entry = decision_manager.get_entry(args.entry_number)
        if not entry:
            print_os_message(f"Entry #{args.entry_number} not found", "ERROR")
            return 1
        
        content = [
            f"  Entry #{entry.entry_number}",
            f"  Date: {entry.date.strftime('%Y-%m-%d')}",
            f"  Decision: {entry.decision}",
            f"  Trigger: {entry.trigger}",
            f"  Rationale: {entry.rationale}",
            f"  Tradeoffs: {entry.tradeoffs}",
            f"  Expected Impact: {entry.expected_impact}",
        ]
        
        if entry.review_date:
            content.append(f"  Review Date: {entry.review_date.strftime('%Y-%m-%d')}")
        if entry.actual_impact:
            content.append(f"  Actual Impact: {entry.actual_impact}")
        if entry.related_rules:
            content.append(f"  Related Rules: {', '.join(sorted(entry.related_rules))}")
        if entry.tags:
            content.append(f"  Tags: {', '.join(sorted(entry.tags))}")
        
        print_os_box(f"Decision Log Entry #{args.entry_number}", content, width=100)
        return 0
    
    elif args.subcommand == "search":
        if not args.query:
            print_os_message("Search query required", "ERROR")
            return 1
        
        results = decision_manager.search(args.query)
        if not results:
            print_os_message(f"No entries found matching '{args.query}'", "INFO")
            return 0
        
        content = []
        for entry in results:
            date_str = entry.date.strftime("%Y-%m-%d")
            content.append(
                f"  [{date_str}] Entry #{entry.entry_number}: {entry.decision[:60]}..."
            )
        
        print_os_box(f"Search Results: '{args.query}'", content, width=100)
        print_os_message(f"Found {len(results)} matching entries", "INFO")
        return 0
    
    elif args.subcommand == "review":
        needing_review = decision_manager.get_entries_needing_review()
        if not needing_review:
            print_os_message("No entries need review", "SUCCESS")
            return 0
        
        content = []
        for entry in sorted(needing_review, key=lambda e: e.review_date):
            date_str = entry.date.strftime("%Y-%m-%d")
            review_str = entry.review_date.strftime("%Y-%m-%d") if entry.review_date else "N/A"
            content.append(
                f"  Entry #{entry.entry_number} [{date_str}] - Review due: {review_str}"
            )
            content.append(f"    {entry.decision[:60]}...")
            content.append("")
        
        print_os_box("Entries Needing Review", content, width=100)
        print_os_message(f"{len(needing_review)} entries need review", "WARN")
        return 1
    
    elif args.subcommand == "analytics":
        analytics = decision_manager.get_impact_analytics()
        
        content = [
            f"  Total Entries: {analytics['total_entries']}",
            f"  Entries with Review: {analytics['entries_with_review']}",
            f"  Entries Needing Review: {analytics['entries_needing_review']}",
            "",
            "  Most Common Tags:",
        ]
        
        for tag, count in analytics['most_common_tags']:
            content.append(f"    - {tag}: {count}")
        
        content.append("")
        content.append("  Most Referenced Rules:")
        for rule_id, count in analytics['most_referenced_rules']:
            content.append(f"    - {rule_id}: {count}")
        
        print_os_box("Decision Log Analytics", content, width=100)
        return 0
    
    return 0


def ml_command(args):
    """Manage ML modules."""
    try:
        from lil_os_ml import cli as ml_cli
    except ImportError:
        from scripts.lil_os_utils import print_os_message
        print_os_message("ML modules not available. Install with: pip install lil-os[ml]", "ERROR")
        return 1
    
    subcommand = getattr(args, 'subcommand', None)
    
    if subcommand == "status":
        return ml_cli.ml_status_command(args)
    elif subcommand == "run":
        return ml_cli.ml_run_command(args)
    elif subcommand == "enable":
        return ml_cli.ml_enable_command(args)
    elif subcommand == "disable":
        return ml_cli.ml_disable_command(args)
    elif subcommand == "train":
        return ml_cli.ml_train_command(args)
    else:
        from scripts.lil_os_utils import print_os_message
        print_os_message(f"Unknown ML subcommand: {subcommand}", "ERROR")
        return 1


def budget_command(args):
    """Manage context budgets."""
    from .core import ContextBudgetManager, BudgetType
    from lil_os_utils import print_os_message, print_os_box, Colors
    
    budget_manager = ContextBudgetManager()
    
    if args.subcommand == "status":
        metrics = budget_manager.get_all_metrics()
        
        content = []
        for budget_type, metric in metrics.items():
            status_color = {
                "healthy": Colors.GREEN,
                "warning": Colors.YELLOW,
                "critical": Colors.RED,
                "exceeded": Colors.BRIGHT_RED,
            }.get(metric.status.value, Colors.WHITE)
            
            content.append(
                f"  {budget_type.value.capitalize()}: "
                f"{status_color}{metric.status.value.upper()}{Colors.RESET} "
                f"({metric.total_cost} items)"
            )
            content.append(
                f"    Items: {metric.total_items} | "
                f"Needs Review: {metric.items_without_review} | "
                f"Overdue: {metric.items_overdue_review} | "
                f"Recent: {metric.recent_additions}"
            )
            content.append("")
        
        print_os_box("Context Budget Status", content, width=100)
        return 0
    
    elif args.subcommand == "alerts":
        alerts = budget_manager.check_alerts()
        if not alerts:
            print_os_message("No budget alerts", "SUCCESS")
            return 0
        
        content = []
        for alert in alerts:
            severity_color = {
                "critical": Colors.BRIGHT_RED,
                "high": Colors.RED,
                "medium": Colors.YELLOW,
                "low": Colors.CYAN,
            }.get(alert["severity"], Colors.WHITE)
            
            content.append(
                f"  {severity_color}[{alert['severity'].upper()}]{Colors.RESET} "
                f"{alert['budget_type']}: {alert['message']}"
            )
            content.append(f"    Recommendation: {alert['recommendation']}")
            content.append("")
        
        print_os_box("Budget Alerts", content, width=100)
        print_os_message(f"Found {len(alerts)} alerts", "WARN")
        return 1
    
    elif args.subcommand == "visualize":
        visualization = budget_manager.get_visualization_data()
        
        content = []
        for budget_type, data in visualization["budgets"].items():
            percentage = data["percentage"]
            bar_length = int(percentage / 5)  # 20 chars max
            bar = "█" * bar_length + "░" * (20 - bar_length)
            
            status_color = {
                "healthy": Colors.GREEN,
                "warning": Colors.YELLOW,
                "critical": Colors.RED,
                "exceeded": Colors.BRIGHT_RED,
            }.get(data["status"], Colors.WHITE)
            
            content.append(f"  {budget_type.capitalize()}:")
            content.append(
                f"    {bar} {percentage:.1f}% "
                f"({data['current']}/{data['max']}) "
                f"{status_color}[{data['status'].upper()}]{Colors.RESET}"
            )
            content.append("")
        
        if visualization["recommendations"]:
            content.append("  Recommendations:")
            for rec in visualization["recommendations"]:
                content.append(f"    - {rec['action']}")
        
        print_os_box("Context Budget Visualization", content, width=100)
        return 0
    
    return 0


def activity_command(args):
    """Show activity feed."""
    from lil_os.events import get_event_bus, EventType
    from lil_os_utils import print_os_box, Colors
    
    event_bus = get_event_bus()
    limit = args.limit if hasattr(args, 'limit') and args.limit else 50
    event_type = None
    
    if hasattr(args, 'type') and args.type:
        try:
            event_type = EventType[args.type]
        except KeyError:
            print_os_message(f"Unknown event type: {args.type}", "ERROR")
            return 1
    
    events = event_bus.get_recent_events(limit=limit, event_type=event_type)
    
    if not events:
        print_os_message("No events found", "INFO")
        return 0
    
    content = []
    for event in reversed(events):  # Most recent first
        time_str = event.timestamp.strftime("%H:%M:%S")
        severity_color = {
            "INFO": Colors.BRIGHT_CYAN,
            "WARN": Colors.BRIGHT_YELLOW,
            "ERROR": Colors.BRIGHT_RED,
            "CRITICAL": Colors.BRIGHT_RED,
        }.get(event.severity.value, Colors.WHITE)
        
        content.append(f"  [{time_str}] {severity_color}{event.severity.value}{Colors.RESET} {event.type.value}: {event.message[:60]}")
    
    print_os_box("Activity Feed", content, width=80)
    return 0


def main():
    """Main CLI entry point."""
    # Initialize session manager
    session_manager = session.SessionManager()
    start_time = time.time()
    start_args = sys.argv[1:] if len(sys.argv) > 1 else []
    
    parser = argparse.ArgumentParser(
        prog="lil-os",
        description="LIL OS² - A constitutional substrate for AI-assisted software development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  lil-os setup              Run the setup wizard
  lil-os status             Show system status
  lil-os lint               Check rule IDs
  lil-os check              Run reset trigger checks
  lil-os warn               Check for critical changes
  lil-os warn --pre-commit  Run warnings in pre-commit mode
  lil-os info               Show system information
  lil-os version            Show version
  lil-os health             Quick health check
  lil-os log-decision       Interactively create decision log entry
  lil-os shell              Launch interactive shell
  lil-os watch              Monitor governance files for changes
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Setup command
    setup_parser = subparsers.add_parser("setup", help="Run the setup wizard")
    setup_parser.set_defaults(func=setup_command)
    
    # Lint command
    lint_parser = subparsers.add_parser("lint", help="Check rule IDs for format and consistency")
    lint_parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode (show findings one at a time)"
    )
    lint_parser.add_argument(
        "--rich",
        action="store_true",
        help="Use Rich library for enhanced UI"
    )
    lint_parser.add_argument(
        "--stream",
        action="store_true",
        help="Use streaming output (requires --rich)"
    )
    lint_parser.set_defaults(func=lint_command)
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Run reset trigger checks")
    check_parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run in interactive mode (show findings one at a time)"
    )
    check_parser.add_argument(
        "--rich",
        action="store_true",
        help="Use Rich library for enhanced UI"
    )
    check_parser.add_argument(
        "--stream",
        action="store_true",
        help="Use streaming output (requires --rich)"
    )
    check_parser.set_defaults(func=check_command)
    
    # Warn command
    warn_parser = subparsers.add_parser("warn", help="Check for critical changes")
    warn_parser.add_argument(
        "--pre-commit",
        action="store_true",
        help="Run in pre-commit mode (checks staged files)"
    )
    warn_parser.set_defaults(func=warn_command)
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show system status")
    status_parser.add_argument(
        "--interactive",
        "-i",
        action="store_true",
        help="Show interactive menu after status"
    )
    status_parser.add_argument(
        "--rich",
        action="store_true",
        help="Use Rich library for enhanced UI"
    )
    status_parser.set_defaults(func=status_command)
    
    # Info command
    info_parser = subparsers.add_parser("info", help="Show system information")
    info_parser.set_defaults(func=info_command)
    
    # Version command
    version_parser = subparsers.add_parser("version", help="Show version information")
    version_parser.set_defaults(func=version_command)
    
    # Health command
    health_parser = subparsers.add_parser("health", help="Quick health check")
    health_parser.set_defaults(func=health_command)
    
    # Log-decision command
    log_parser = subparsers.add_parser("log-decision", help="Interactively create a decision log entry")
    log_parser.set_defaults(func=log_decision_command)
    
    # Help command
    help_parser = subparsers.add_parser("help", help="Show help information")
    help_parser.add_argument("command", nargs="?", help="Command to get help for")
    help_parser.add_argument("--explain", dest="rule_id", help="Explain a rule ID")
    help_parser.add_argument("--guide", dest="scenario", help="Show scenario guide")
    help_parser.set_defaults(func=help_command)
    
    # Shell command
    shell_parser = subparsers.add_parser("shell", help="Launch interactive shell")
    shell_parser.set_defaults(func=shell_command)
    
    # Watch command
    watch_parser = subparsers.add_parser("watch", help="Monitor governance files for changes")
    watch_parser.add_argument(
        "--interval",
        type=float,
        default=2.0,
        help="Check interval in seconds (default: 2.0)"
    )
    watch_parser.set_defaults(func=watch_command)
    
    # Box designer command
    designer_parser = subparsers.add_parser("design", help="Interactive box designer tool")
    designer_parser.set_defaults(func=designer_command)
    
    # Daemon command
    daemon_parser = subparsers.add_parser("daemon", help="Manage background daemon")
    daemon_parser.add_argument(
        "action",
        choices=["start", "stop", "status", "run"],
        help="Daemon action"
    )
    daemon_parser.add_argument(
        "--config",
        type=Path,
        help="Path to daemon config file"
    )
    daemon_parser.set_defaults(func=daemon_command)
    
    # Activity command
    activity_parser = subparsers.add_parser("activity", help="Show activity feed")
    activity_parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Maximum number of events to show (default: 50)"
    )
    activity_parser.add_argument(
        "--type",
        help="Filter by event type"
    )
    activity_parser.set_defaults(func=activity_command)
    
    # Rules command
    rules_parser = subparsers.add_parser("rules", help="Manage governance rules")
    rules_subparsers = rules_parser.add_subparsers(dest="subcommand", help="Rule subcommands")
    
    rules_list_parser = rules_subparsers.add_parser("list", help="List all rules")
    rules_list_parser.set_defaults(func=rules_command)
    
    rules_show_parser = rules_subparsers.add_parser("show", help="Show rule details")
    rules_show_parser.add_argument("rule_id", help="Rule ID to show")
    rules_show_parser.set_defaults(func=rules_command)
    
    rules_deps_parser = rules_subparsers.add_parser("dependencies", help="Show rule dependencies")
    rules_deps_parser.add_argument("rule_id", help="Rule ID")
    rules_deps_parser.set_defaults(func=rules_command)
    
    rules_impact_parser = rules_subparsers.add_parser("impact", help="Analyze rule impact")
    rules_impact_parser.add_argument("rule_id", help="Rule ID")
    rules_impact_parser.set_defaults(func=rules_command)
    
    rules_contradictions_parser = rules_subparsers.add_parser("contradictions", help="Find rule contradictions")
    rules_contradictions_parser.set_defaults(func=rules_command)
    
    # Decisions command
    decisions_parser = subparsers.add_parser("decisions", help="Manage decision log")
    decisions_subparsers = decisions_parser.add_subparsers(dest="subcommand", help="Decision subcommands")
    
    decisions_list_parser = decisions_subparsers.add_parser("list", help="List all decision entries")
    decisions_list_parser.set_defaults(func=decisions_command)
    
    decisions_show_parser = decisions_subparsers.add_parser("show", help="Show decision entry details")
    decisions_show_parser.add_argument("entry_number", type=int, help="Entry number to show")
    decisions_show_parser.set_defaults(func=decisions_command)
    
    decisions_search_parser = decisions_subparsers.add_parser("search", help="Search decision entries")
    decisions_search_parser.add_argument("query", help="Search query")
    decisions_search_parser.set_defaults(func=decisions_command)
    
    decisions_review_parser = decisions_subparsers.add_parser("review", help="Show entries needing review")
    decisions_review_parser.set_defaults(func=decisions_command)
    
    decisions_analytics_parser = decisions_subparsers.add_parser("analytics", help="Show decision log analytics")
    decisions_analytics_parser.set_defaults(func=decisions_command)
    
    # Budget command
    budget_parser = subparsers.add_parser("budget", help="Manage context budgets")
    budget_subparsers = budget_parser.add_subparsers(dest="subcommand", help="Budget subcommands")
    
    budget_status_parser = budget_subparsers.add_parser("status", help="Show budget status")
    budget_status_parser.set_defaults(func=budget_command)
    
    budget_alerts_parser = budget_subparsers.add_parser("alerts", help="Show budget alerts")
    budget_alerts_parser.set_defaults(func=budget_command)
    
    budget_visualize_parser = budget_subparsers.add_parser("visualize", help="Visualize budgets")
    budget_visualize_parser.set_defaults(func=budget_command)
    
    # ML command
    ml_parser = subparsers.add_parser("ml", help="ML module commands")
    ml_subparsers = ml_parser.add_subparsers(dest="subcommand", help="ML subcommands")
    
    ml_status_parser = ml_subparsers.add_parser("status", help="Show ML modules status")
    ml_status_parser.set_defaults(func=ml_command)
    
    ml_run_parser = ml_subparsers.add_parser("run", help="Run ML evaluations")
    ml_run_parser.add_argument("--all", action="store_true", help="Run all enabled modules")
    ml_run_parser.add_argument("--module", help="Run specific module")
    ml_run_parser.add_argument("--json", action="store_true", help="Output JSON")
    ml_run_parser.add_argument("--md", action="store_true", help="Output Markdown")
    ml_run_parser.set_defaults(func=ml_command)
    
    ml_enable_parser = ml_subparsers.add_parser("enable", help="Enable an ML module")
    ml_enable_parser.add_argument("module", help="Module name (change_risk, drift, rag_quality)")
    ml_enable_parser.set_defaults(func=ml_command)
    
    ml_disable_parser = ml_subparsers.add_parser("disable", help="Disable an ML module")
    ml_disable_parser.add_argument("module", help="Module name (change_risk, drift, rag_quality)")
    ml_disable_parser.set_defaults(func=ml_command)
    
    ml_train_parser = ml_subparsers.add_parser("train", help="Train ML models")
    ml_train_parser.add_argument("--module", help="Train specific module")
    ml_train_parser.set_defaults(func=ml_command)
    
    # Parse arguments
    args = parser.parse_args()
    
    if not hasattr(args, "func"):
        parser.print_help()
        exit_code = 1
    else:
        try:
            exit_code = args.func(args)
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user", file=sys.stderr)
            exit_code = 130
        except Exception as e:
            print(f"\nError: {e}", file=sys.stderr)
            exit_code = 1
    
    # Save session entry
    duration = time.time() - start_time
    try:
        command_name = args.command if hasattr(args, 'command') and args.command else "help"
        session_manager.save_entry(
            command=command_name,
            args=start_args[1:] if len(start_args) > 1 else [],
            exit_code=exit_code,
            duration_seconds=duration
        )
    except Exception:
        # Don't fail if session saving fails
        pass
    
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

