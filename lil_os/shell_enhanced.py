#!/usr/bin/env python3
"""
LIL OS² Enhanced Interactive Shell

Provides a persistent shell interface with activity feed, governance prompts,
and real-time monitoring integration.
"""

from __future__ import annotations

import sys
import shlex
import threading
import queue
from pathlib import Path
from typing import List, Optional, Dict
from datetime import datetime
from collections import deque

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os_utils import print_os_message, print_os_box, Colors, strip_ansi
from lil_os.events import Event, EventType, EventSeverity, get_event_bus
from lil_os.daemon import LILOSDaemon


class EnhancedLILOSShell:
    """Enhanced interactive shell for LIL OS² with activity feed and governance prompts."""
    
    def __init__(self):
        self.version = "2.0.0"
        self.history: List[str] = []
        self.running = True
        self.event_bus = get_event_bus()
        self.daemon: Optional[LILOSDaemon] = None
        
        # Activity feed
        self.activity_feed: deque = deque(maxlen=100)
        self.activity_lock = threading.Lock()
        
        # Governance prompts
        self.pending_prompts: List[Event] = []
        self.prompts_lock = threading.Lock()
        
        # Event subscription
        self._event_queue = queue.Queue()
        self._event_thread: Optional[threading.Thread] = None
        
        # Status
        self.last_validation_status = "unknown"
        self.pending_decisions_count = 0
    
    def _event_handler(self, event: Event) -> None:
        """Handle incoming events."""
        # Add to activity feed
        with self.activity_lock:
            self.activity_feed.append(event)
        
        # Handle governance decision needed
        if event.type == EventType.GOVERNANCE_DECISION_NEEDED:
            with self.prompts_lock:
                self.pending_prompts.append(event)
                self.pending_decisions_count = len(self.pending_prompts)
        
        # Update validation status
        if event.type == EventType.VALIDATION_PASSED:
            self.last_validation_status = "passed"
        elif event.type == EventType.VALIDATION_FAILED:
            self.last_validation_status = "failed"
    
    def _start_event_listener(self) -> None:
        """Start background event listener thread."""
        def listen_loop():
            self.event_bus.subscribe(None, self._event_handler)  # Subscribe to all events
            # Keep thread alive
            import time
            while self.running:
                try:
                    # Check for events (non-blocking)
                    time.sleep(0.1)
                except Exception:
                    break
        
        import time
        self._event_thread = threading.Thread(target=listen_loop, daemon=True)
        self._event_thread.start()
    
    def print_banner(self):
        """Print shell banner."""
        content = [
            f"LIL OS² Enhanced Shell v{self.version}",
            "",
            "Features:",
            "  • Real-time activity feed",
            "  • Governance decision prompts",
            "  • Background monitoring",
            "",
            "Type 'help' for commands, 'exit' to leave"
        ]
        print_os_box("", content, width=60)
        print()
    
    def get_prompt(self) -> str:
        """Get the shell prompt with status."""
        status_indicator = "●" if self.daemon and self.daemon.is_running() else "○"
        status_color = Colors.BRIGHT_GREEN if self.daemon and self.daemon.is_running() else Colors.DIM
        
        prompt_parts = [
            f"{Colors.BRIGHT_CYAN}LIL OS²{Colors.RESET}",
            f"{status_color}{status_indicator}{Colors.RESET}",
        ]
        
        if self.pending_decisions_count > 0:
            prompt_parts.append(f"{Colors.BRIGHT_YELLOW}[{self.pending_decisions_count}]{Colors.RESET}")
        
        prompt_parts.append(">")
        return " ".join(prompt_parts) + " "
    
    def display_status_bar(self) -> None:
        """Display status bar with daemon and validation info."""
        status_parts = []
        
        # Daemon status
        if self.daemon and self.daemon.is_running():
            status_parts.append(f"{Colors.BRIGHT_GREEN}●{Colors.RESET} Daemon")
        else:
            status_parts.append(f"{Colors.DIM}○{Colors.RESET} Daemon")
        
        # Validation status
        if self.last_validation_status == "passed":
            status_parts.append(f"{Colors.BRIGHT_GREEN}✓{Colors.RESET} Validation")
        elif self.last_validation_status == "failed":
            status_parts.append(f"{Colors.BRIGHT_RED}✗{Colors.RESET} Validation")
        else:
            status_parts.append(f"{Colors.DIM}○{Colors.RESET} Validation")
        
        # Pending decisions
        if self.pending_decisions_count > 0:
            status_parts.append(f"{Colors.BRIGHT_YELLOW}⚠{Colors.RESET} {self.pending_decisions_count} pending")
        
        status_line = " | ".join(status_parts)
        print(f"{Colors.DIM}{status_line}{Colors.RESET}")
    
    def display_activity_feed(self, limit: int = 20) -> None:
        """Display recent activity feed."""
        with self.activity_lock:
            recent_events = list(self.activity_feed)[-limit:]
        
        if not recent_events:
            print_os_message("No recent activity", "INFO")
            return
        
        content = []
        for event in recent_events:
            time_str = event.timestamp.strftime("%H:%M:%S")
            
            # Color by severity
            if event.severity == EventSeverity.ERROR or event.severity == EventSeverity.CRITICAL:
                color = Colors.BRIGHT_RED
            elif event.severity == EventSeverity.WARN:
                color = Colors.BRIGHT_YELLOW
            else:
                color = Colors.BRIGHT_CYAN
            
            # Format event
            event_type_short = event.type.value.replace("_", " ")[:20]
            message = event.message or event.type.value
            content.append(f"  [{time_str}] {color}{event_type_short}{Colors.RESET}: {message[:50]}")
        
        print_os_box("Activity Feed", content, width=80)
    
    def display_governance_prompts(self) -> None:
        """Display pending governance decision prompts."""
        with self.prompts_lock:
            prompts = self.pending_prompts.copy()
        
        if not prompts:
            return
        
        for prompt in prompts:
            self._display_governance_prompt(prompt)
    
    def _display_governance_prompt(self, event: Event) -> None:
        """Display a single governance prompt."""
        file_path = event.data.get("file", "Unknown")
        reason = event.data.get("reason", "unknown")
        
        content = [
            "",
            f"{Colors.BRIGHT_YELLOW}⚠ Governance Decision Required ⚠{Colors.RESET}",
            "",
            f"File: {Colors.BRIGHT_WHITE}{Path(file_path).name}{Colors.RESET}",
            f"Reason: {reason}",
            "",
            "A governance file has been modified without a corresponding",
            "decision log entry. This requires documentation per GOVERNANCE.md",
            "",
            "Actions:",
            "  1. Create decision log entry (type 'log-decision')",
            "  2. Dismiss this prompt (type 'dismiss <id>')",
            "  3. View details (type 'prompt details')",
            ""
        ]
        
        print_os_box("Governance Prompt", content, width=70)
        print()
    
    def parse_command(self, line: str) -> tuple[str, List[str]]:
        """Parse a command line into command and arguments."""
        parts = shlex.split(line.strip())
        if not parts:
            return "", []
        return parts[0], parts[1:]
    
    def execute_command(self, command: str, args: List[str]) -> int:
        """Execute a shell command."""
        from . import cli
        
        # Create a mock args object
        class MockArgs:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)
        
        try:
            if command == "exit" or command == "quit":
                self.running = False
                print_os_message("Goodbye!", "INFO")
                return 0
            elif command == "help":
                self.show_help()
                return 0
            elif command == "activity":
                limit = int(args[0]) if args and args[0].isdigit() else 20
                self.display_activity_feed(limit=limit)
                return 0
            elif command == "events":
                self._show_events(args)
                return 0
            elif command == "prompt":
                if args and args[0] == "details":
                    self._show_prompt_details()
                else:
                    self.display_governance_prompts()
                return 0
            elif command == "daemon":
                return self._handle_daemon_command(args)
            elif command == "status":
                mock_args = MockArgs()
                return cli.status_command(mock_args)
            elif command == "info":
                mock_args = MockArgs()
                return cli.info_command(mock_args)
            elif command == "version":
                mock_args = MockArgs()
                return cli.version_command(mock_args)
            elif command == "health":
                mock_args = MockArgs()
                return cli.health_command(mock_args)
            elif command == "lint":
                mock_args = MockArgs(interactive="--interactive" in args)
                return cli.lint_command(mock_args)
            elif command == "check":
                mock_args = MockArgs(interactive="--interactive" in args)
                return cli.check_command(mock_args)
            elif command == "warn":
                mock_args = MockArgs(pre_commit="--pre-commit" in args)
                return cli.warn_command(mock_args)
            elif command == "log-decision":
                mock_args = MockArgs()
                result = cli.log_decision_command(mock_args)
                # Clear prompts after creating decision log
                if result == 0:
                    with self.prompts_lock:
                        self.pending_prompts.clear()
                        self.pending_decisions_count = 0
                return result
            elif command == "setup":
                mock_args = MockArgs()
                return cli.setup_command(mock_args)
            elif command == "explain":
                if args:
                    mock_args = MockArgs(rule_id=args[0], command=None, scenario=None)
                    return cli.help_command(mock_args)
                else:
                    print_os_message("Usage: explain <rule-id>", "ERROR")
                    return 1
            elif command == "guide":
                if args:
                    mock_args = MockArgs(scenario=args[0], command=None, rule_id=None)
                    return cli.help_command(mock_args)
                else:
                    print_os_message("Usage: guide <scenario>", "ERROR")
                    return 1
            elif command == "":
                return 0
            else:
                print_os_message(f"Unknown command: {command}", "ERROR")
                print_os_message("Type 'help' for available commands", "INFO")
                return 1
        except KeyboardInterrupt:
            print_os_message("\nOperation cancelled. Type 'exit' to leave shell.", "WARN")
            return 0
        except Exception as e:
            print_os_message(f"Error: {e}", "ERROR")
            return 1
    
    def _handle_daemon_command(self, args: List[str]) -> int:
        """Handle daemon subcommands."""
        if not args:
            print_os_message("Usage: daemon <start|stop|status|restart>", "ERROR")
            return 1
        
        subcommand = args[0]
        
        if subcommand == "start":
            if self.daemon and self.daemon.is_running():
                print_os_message("Daemon is already running", "WARN")
                return 0
            self.daemon = LILOSDaemon(event_bus=self.event_bus)
            self.daemon.start()
            return 0
        elif subcommand == "stop":
            if not self.daemon or not self.daemon.is_running():
                print_os_message("Daemon is not running", "WARN")
                return 0
            self.daemon.stop()
            return 0
        elif subcommand == "status":
            if not self.daemon:
                print_os_message("Daemon not initialized", "WARN")
                return 1
            status = self.daemon.status()
            print_os_message(f"Daemon: {'Running' if status['running'] else 'Stopped'}", "INFO")
            print_os_message(f"File watcher: {'Running' if status['file_watcher']['running'] else 'Stopped'}", "INFO")
            print_os_message(f"Git monitor: {'Running' if status['git_monitor']['running'] else 'Stopped'}", "INFO")
            print_os_message(f"Validation monitor: {'Running' if status['validation_monitor']['running'] else 'Stopped'}", "INFO")
            print_os_message(f"Governance detector: {'Running' if status['governance_detector']['running'] else 'Stopped'}", "INFO")
            print_os_message(f"Event count: {status['event_count']}", "INFO")
            return 0
        elif subcommand == "restart":
            if self.daemon and self.daemon.is_running():
                self.daemon.stop()
            self.daemon = LILOSDaemon(event_bus=self.event_bus)
            self.daemon.start()
            return 0
        else:
            print_os_message(f"Unknown daemon command: {subcommand}", "ERROR")
            return 1
    
    def _show_events(self, args: List[str]) -> None:
        """Show recent events with optional filtering."""
        event_type = None
        limit = 50
        
        # Parse args
        i = 0
        while i < len(args):
            if args[i] == "--type" and i + 1 < len(args):
                try:
                    event_type = EventType[args[i + 1]]
                except KeyError:
                    print_os_message(f"Unknown event type: {args[i + 1]}", "ERROR")
                    return
                i += 2
            elif args[i] == "--limit" and i + 1 < len(args):
                limit = int(args[i + 1])
                i += 2
            else:
                i += 1
        
        events = self.event_bus.get_recent_events(limit=limit, event_type=event_type)
        
        if not events:
            print_os_message("No events found", "INFO")
            return
        
        content = []
        for event in reversed(events):  # Most recent first
            time_str = event.timestamp.strftime("%H:%M:%S")
            severity_color = {
                EventSeverity.INFO: Colors.BRIGHT_CYAN,
                EventSeverity.WARN: Colors.BRIGHT_YELLOW,
                EventSeverity.ERROR: Colors.BRIGHT_RED,
                EventSeverity.CRITICAL: Colors.BRIGHT_RED,
            }.get(event.severity, Colors.WHITE)
            
            content.append(f"  [{time_str}] {severity_color}{event.severity.value}{Colors.RESET} {event.type.value}: {event.message[:60]}")
        
        print_os_box("Recent Events", content, width=80)
    
    def _show_prompt_details(self) -> None:
        """Show details of pending governance prompts."""
        with self.prompts_lock:
            prompts = self.pending_prompts.copy()
        
        if not prompts:
            print_os_message("No pending governance prompts", "INFO")
            return
        
        for i, prompt in enumerate(prompts, 1):
            content = [
                f"Prompt #{i}",
                "",
                f"File: {prompt.data.get('file', 'Unknown')}",
                f"Reason: {prompt.data.get('reason', 'unknown')}",
                f"Timestamp: {prompt.timestamp.strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "Data:",
            ]
            
            for key, value in prompt.data.items():
                content.append(f"  {key}: {value}")
            
            print_os_box("Governance Prompt Details", content, width=70)
            print()
    
    def show_help(self):
        """Show shell help."""
        content = [
            "Available Commands:",
            "",
            "  status          Show system status",
            "  info            Show system information",
            "  version         Show version",
            "  health          Quick health check",
            "  lint            Check rule IDs",
            "  check           Run reset trigger checks",
            "  warn            Check for critical changes",
            "  log-decision    Create decision log entry",
            "  setup           Run setup wizard",
            "  explain <id>    Explain a rule ID",
            "  guide <name>    Show scenario guide",
            "",
            "Enhanced Commands:",
            "  activity [N]    Show activity feed (last N events, default 20)",
            "  events          List recent events (--type TYPE --limit N)",
            "  prompt          Show governance prompts",
            "  prompt details  Show detailed prompt information",
            "  daemon start    Start background daemon",
            "  daemon stop     Stop background daemon",
            "  daemon status   Show daemon status",
            "  daemon restart  Restart background daemon",
            "",
            "  help            Show this help",
            "  exit/quit       Exit shell",
            "",
            "Note: Enhanced shell includes real-time monitoring and governance prompts"
        ]
        print_os_box("Shell Commands", content, width=70)
    
    def run(self):
        """Run the interactive shell."""
        self.print_banner()
        
        # Start event listener
        self._start_event_listener()
        
        # Auto-start daemon
        try:
            self.daemon = LILOSDaemon(event_bus=self.event_bus)
            self.daemon.start()
            print_os_message("Background daemon started automatically", "INFO")
        except Exception as e:
            print_os_message(f"Could not start daemon: {e}", "WARN")
        
        try:
            while self.running:
                # Show status bar
                self.display_status_bar()
                
                # Show pending prompts if any
                if self.pending_decisions_count > 0:
                    self.display_governance_prompts()
                
                try:
                    line = input(self.get_prompt())
                    self.history.append(line)
                    
                    command, args = self.parse_command(line)
                    self.execute_command(command, args)
                    print()  # Add spacing between commands
                except EOFError:
                    # Handle Ctrl+D
                    print()
                    self.running = False
                    print_os_message("Goodbye!", "INFO")
                    break
                except KeyboardInterrupt:
                    # Handle Ctrl+C
                    print()
                    print_os_message("Type 'exit' to leave shell, or continue with commands.", "INFO")
        except Exception as e:
            print_os_message(f"Fatal error: {e}", "ERROR")
            return 1
        finally:
            # Cleanup
            if self.daemon:
                self.daemon.stop()
        
        return 0


def main() -> int:
    """Main entry point for enhanced shell."""
    shell = EnhancedLILOSShell()
    return shell.run()


if __name__ == "__main__":
    sys.exit(main())

