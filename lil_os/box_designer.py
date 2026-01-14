#!/usr/bin/env python3
"""
LIL OS Box Designer

Interactive tool for designing and testing box layouts.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os_utils import print_os_box, Colors, print_os_message


def interactive_designer():
    """Interactive box designer."""
    print_os_message("LIL OS² Box Designer", "INFO")
    print_os_message("Design and test box layouts interactively", "INFO")
    print()
    
    while True:
        print()
        print_os_message("Options:", "INFO")
        print("  1. Test current status box")
        print("  2. Test custom box")
        print("  3. Test with different widths")
        print("  4. Exit")
        print()
        
        try:
            choice = input(f"{Colors.BRIGHT_CYAN}[LIL OS²]{Colors.RESET} Select option: ").strip()
            
            if choice == "1":
                test_status_box()
            elif choice == "2":
                test_custom_box()
            elif choice == "3":
                test_widths()
            elif choice == "4" or choice == "":
                print_os_message("Goodbye!", "INFO")
                break
            else:
                print_os_message(f"Invalid choice: {choice}", "WARN")
        except (KeyboardInterrupt, EOFError):
            print()
            print_os_message("Goodbye!", "INFO")
            break
        except Exception as e:
            print_os_message(f"Error: {e}", "ERROR")


def test_status_box():
    """Test the status box layout."""
    print()
    print_os_message("Testing Status Box (width=64)", "INFO")
    print()
    
    content = []
    content.append("")
    content.append("Version: 0.1.1")
    content.append("Status: GOOD")
    content.append("")
    content.append("━━━ Governance ━━━")
    content.append("")
    content.append("  ● Rules: 11 active")
    content.append("  ● Last validation: 8 hours ago")
    content.append("  ● Decision log: 2 entries")
    content.append("")
    content.append("━━━ System Health ━━━")
    content.append("")
    content.append("  ✅ GOOD")
    content.append("")
    
    print_os_box("LIL OS² System Status", content, width=64)


def test_custom_box():
    """Test a custom box with user input."""
    print()
    print_os_message("Create Custom Box", "INFO")
    print()
    
    try:
        title = input("Box title: ").strip() or "Custom Box"
        width = int(input("Box width (default 60): ").strip() or "60")
        
        print()
        print("Enter content lines (empty line to finish):")
        content = []
        while True:
            line = input("> ").strip()
            if not line:
                break
            content.append(line)
        
        if not content:
            content = ["No content provided"]
        
        print()
        print_os_box(title, content, width=width)
    except ValueError:
        print_os_message("Invalid width, using default 60", "WARN")
        print_os_box("Custom Box", ["Invalid input"], width=60)
    except (KeyboardInterrupt, EOFError):
        print_os_message("Cancelled", "INFO")


def test_widths():
    """Test boxes with different widths."""
    print()
    print_os_message("Testing Different Widths", "INFO")
    print()
    
    test_content = [
        "Short line",
        "This is a medium length line",
        "Version: 0.1.1",
        "Status: GOOD",
        "  ● Rules: 11 active",
        "━━━ Section ━━━",
    ]
    
    widths = [40, 50, 60, 64, 70, 80]
    
    for width in widths:
        print()
        print_os_message(f"Width: {width}", "INFO")
        print_os_box(f"Test Box ({width} chars)", test_content, width=width)
        print()
        input("Press Enter to continue...")


def main() -> int:
    """Main entry point."""
    try:
        interactive_designer()
        return 0
    except Exception as e:
        print_os_message(f"Error: {e}", "ERROR")
        return 1


if __name__ == "__main__":
    sys.exit(main())

