#!/usr/bin/env python3
"""
LIL OS² Interactive Shell (DEPRECATED)

Provides a persistent shell interface for LIL OS² commands.

DEPRECATED: This is the basic shell. The enhanced shell (shell_enhanced.py)
is now the default. This file is kept as a fallback only.
"""

from __future__ import annotations

import sys
import shlex
from pathlib import Path
from typing import List, Optional

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os_utils import print_os_message, print_os_box, Colors


class LILOSShell:
    """Interactive shell for LIL OS²."""
    
    def __init__(self):
        self.version = "2.0.0"
        self.history: List[str] = []
        self.running = True
    
    def print_banner(self):
        """Print shell banner."""
        content = [
            f"LIL OS² Interactive Shell v{self.version}",
            "Type 'help' for commands, 'exit' to leave"
        ]
        print_os_box("", content, width=60)
        print()
    
    def get_prompt(self) -> str:
        """Get the shell prompt."""
        return f"{Colors.BRIGHT_CYAN}LIL OS²>{Colors.RESET} "
    
    def parse_command(self, line: str) -> tuple[str, List[str]]:
        """Parse a command line into command and arguments."""
        parts = shlex.split(line.strip())
        if not parts:
            return "", []
        return parts[0], parts[1:]
    
    def execute_command(self, command: str, args: List[str]) -> int:
        """Execute a shell command."""
        # Import CLI functions
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
                return cli.log_decision_command(mock_args)
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
            "  help            Show this help",
            "  exit/quit       Exit shell",
            "",
            "Note: Commands work the same as 'lil-os <command>'"
        ]
        print_os_box("Shell Commands", content, width=60)
    
    def run(self):
        """Run the interactive shell."""
        self.print_banner()
        
        try:
            while self.running:
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
        
        return 0


def main() -> int:
    """Main entry point for shell."""
    shell = LILOSShell()
    return shell.run()


if __name__ == "__main__":
    sys.exit(main())

