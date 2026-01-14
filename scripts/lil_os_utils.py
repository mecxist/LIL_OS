#!/usr/bin/env python3
"""
LIL OS² Shared Utilities

Common utilities used across LIL OS² scripts. This module consolidates duplicate
code to reduce maintenance burden and ensure consistency.

Dependencies: Python 3.10+ (standard library only)
"""

from __future__ import annotations

import time
import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Tuple, Dict, Any


# ----------------------------
# ANSI Color Codes
# ----------------------------
class Colors:
    """ANSI color codes for terminal output."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    
    # Text colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'


# ----------------------------
# Finding Dataclass
# ----------------------------
@dataclass
class Finding:
    """Represents a validation finding or check result."""
    level: str  # HARD_FAIL | WARN | INFO
    code: str
    message: str
    details: Optional[dict] = None


# ----------------------------
# YAML Parser
# ----------------------------
def load_simple_yaml(path: Path) -> dict:
    """
    Simple YAML parser for LIL OS² configuration files.
    
    Handles:
    - Nested dictionaries
    - Lists
    - String, integer, and boolean values
    - Quoted strings with escape sequences
    - Comments (lines starting with #)
    
    This is a minimal parser designed specifically for LIL OS² config files.
    For complex YAML, use a proper YAML library.
    """
    text = path.read_text(encoding="utf-8")
    lines = [ln.rstrip("\n") for ln in text.splitlines() if ln.strip() and not ln.strip().startswith("#")]
    root: dict = {}
    stack: List[Tuple[int, dict | list]] = [(0, root)]
    current_key_stack: List[Optional[str]] = [None]

    def parse_value(v: str):
        """Parse a YAML value, handling types and escape sequences."""
        v = v.strip()
        # Integer
        if v.isdigit():
            return int(v)
        # Boolean
        if v.lower() == 'true':
            return True
        if v.lower() == 'false':
            return False
        # Quoted strings
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            result = v[1:-1]
            # Handle escape sequences for double-quoted strings (YAML-style)
            if v.startswith('"'):
                # Unescape common regex patterns
                result = result.replace('\\[', '[').replace('\\]', ']')
                result = result.replace('\\d', r'\d')
                result = result.replace('\\\\', '\\')
            return result
        return v

    for ln in lines:
        indent = len(ln) - len(ln.lstrip(" "))
        ln = ln.lstrip(" ")
        while stack and indent < stack[-1][0]:
            stack.pop()
            current_key_stack.pop()

        container = stack[-1][1]

        if ln.startswith("- "):
            item = parse_value(ln[2:])
            if not isinstance(container, list):
                key = current_key_stack[-1]
                if key is None or not isinstance(container, dict):
                    raise ValueError(f"List item without list context near: {ln}")
                if key not in container or not isinstance(container[key], list):
                    container[key] = []
                container = container[key]
                stack.append((indent, container))
                current_key_stack.append(key)
            container.append(item)
            continue

        if ":" in ln:
            key, rest = ln.split(":", 1)
            key = key.strip()
            rest = rest.strip()
            if isinstance(container, list):
                raise ValueError(f"Unexpected mapping inside list near: {ln}")
            if rest == "":
                container[key] = {}
                stack.append((indent + 2, container[key]))
                current_key_stack.append(key)
            else:
                container[key] = parse_value(rest)
                current_key_stack[-1] = key
            continue

        raise ValueError(f"Unparseable line: {ln}")

    return root


def normalize_yaml_list(value: dict | list) -> list:
    """
    Normalize YAML parser output for list values.
    
    The YAML parser sometimes creates nested dicts for lists (e.g., 
    {'forbidden_domains': [...]}). This function extracts the actual list.
    
    Args:
        value: The value from YAML parser (may be dict or list)
        
    Returns:
        The list value, or empty list if not found
    """
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        # Check if it's a nested structure like {'key': [...]}
        if len(value) == 1:
            first_value = next(iter(value.values()))
            if isinstance(first_value, list):
                return first_value
        # Otherwise, return values as list
        return list(value.values()) if value else []
    return []


# ----------------------------
# File I/O
# ----------------------------
def read_text(path: Path) -> str:
    """
    Read text file with error handling.
    
    Args:
        path: Path to file
        
    Returns:
        File contents as string, or empty string if file doesn't exist
    """
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


# ----------------------------
# Timing Utilities
# ----------------------------
class Timer:
    """Context manager for timing operations."""
    def __init__(self):
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, *args):
        self.end_time = time.time()
    
    @property
    def elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0.0
        end = self.end_time if self.end_time else time.time()
        return end - self.start_time
    
    def format_elapsed(self) -> str:
        """Format elapsed time as human-readable string."""
        elapsed = self.elapsed
        if elapsed < 1.0:
            return f"{elapsed * 1000:.0f}ms"
        return f"{elapsed:.2f}s"


# ----------------------------
# Reporting Utilities
# ----------------------------
def generate_report(
    check_name: str,
    findings: List[Finding],
    timer: Timer,
    config: Optional[Dict[str, Any]] = None
) -> Optional[Dict[str, Any]]:
    """
    Generate a report dictionary for validation results.
    
    Args:
        check_name: Name of the check that was run
        findings: List of findings from the check
        timer: Timer instance with timing information
        config: Optional configuration dict with reporting settings
        
    Returns:
        Report dictionary, or None if reporting is disabled
    """
    if config is None:
        config = {}
    
    reporting = config.get("reporting", {})
    if not reporting.get("generate_reports", False):
        return None
    
    hard = [f for f in findings if f.level == "HARD_FAIL"]
    warn = [f for f in findings if f.level == "WARN"]
    info = [f for f in findings if f.level == "INFO"]
    
    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "check_name": check_name,
        "status": "fail" if hard else ("warn" if warn else "pass"),
        "summary": {
            "hard_fails": len(hard),
            "warnings": len(warn),
            "info": len(info),
            "total": len(findings)
        },
        "findings": [
            {
                "level": f.level,
                "code": f.code,
                "message": f.message,
                "details": f.details
            }
            for f in findings
        ],
        "timing": {
            "elapsed_seconds": timer.elapsed,
            "elapsed_formatted": timer.format_elapsed()
        }
    }
    
    # Add git info if available
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        report["git_commit"] = result.stdout.strip()
    except Exception:
        pass
    
    return report


def save_report(report: Dict[str, Any], config: Optional[Dict[str, Any]] = None) -> Optional[Path]:
    """
    Save report to file system.
    
    Args:
        report: Report dictionary from generate_report()
        config: Optional configuration dict with reporting settings
        
    Returns:
        Path to saved report file, or None if saving failed/disabled
    """
    if report is None or config is None:
        return None
    
    reporting = config.get("reporting", {})
    if not reporting.get("generate_reports", False):
        return None
    
    report_location = Path(reporting.get("report_location", ".lil_os/reports"))
    report_location.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.utcnow().strftime("%Y-%m-%d_%H-%M-%S")
    check_name_safe = report["check_name"].replace(" ", "_").lower()
    
    # Save JSON report
    json_path = report_location / f"{timestamp}_{check_name_safe}_report.json"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    
    # Save markdown summary if requested
    formats = reporting.get("report_format", ["json"])
    if "markdown" in formats:
        md_path = report_location / f"{timestamp}_{check_name_safe}_summary.md"
        md_content = generate_markdown_summary(report)
        md_path.write_text(md_content, encoding="utf-8")
    
    # Create/update latest symlink
    latest_path = report_location / f"latest_{check_name_safe}_report.json"
    try:
        if latest_path.exists() or latest_path.is_symlink():
            latest_path.unlink()
        latest_path.symlink_to(json_path.name)
    except Exception:
        # Symlinks might not work on all systems, that's okay
        pass
    
    return json_path


def generate_markdown_summary(report: Dict[str, Any]) -> str:
    """Generate a human-readable markdown summary from a report."""
    status_emoji = {
        "pass": "✅",
        "warn": "⚠️",
        "fail": "❌"
    }
    emoji = status_emoji.get(report["status"], "ℹ️")
    
    md = f"""# LIL OS² Validation Report

**Check:** {report['check_name']}
**Date:** {report['timestamp']}
**Status:** {emoji} {report['status'].upper()}
**Duration:** {report['timing']['elapsed_formatted']}
"""
    
    if "git_commit" in report:
        md += f"**Commit:** `{report['git_commit'][:8]}`\n"
    
    summary = report["summary"]
    md += f"""
## Summary

- **Hard Fails:** {summary['hard_fails']}
- **Warnings:** {summary['warnings']}
- **Info:** {summary['info']}
- **Total Findings:** {summary['total']}

"""
    
    if report["findings"]:
        md += "## Findings\n\n"
        for finding in report["findings"]:
            level_emoji = {
                "HARD_FAIL": "❌",
                "WARN": "⚠️",
                "INFO": "ℹ️"
            }
            emoji = level_emoji.get(finding["level"], "•")
            md += f"### {emoji} [{finding['level']}] {finding['code']}\n\n"
            md += f"{finding['message']}\n\n"
            if finding.get("details"):
                md += "```json\n"
                md += json.dumps(finding["details"], indent=2)
                md += "\n```\n\n"
    
    return md


def print_startup_banner(check_name: str, show_banner: bool = True):
    """Print startup banner for a check."""
    if not show_banner:
        return
        print(f"{Colors.BRIGHT_CYAN}🔍 LIL OS²: Running {check_name}...{Colors.RESET}")


def print_success_message(check_name: str, findings: List[Finding], timer: Timer, show_success: bool = True):
    """Print success message when checks pass."""
    if not show_success:
        return
    
    hard = [f for f in findings if f.level == "HARD_FAIL"]
    warn = [f for f in findings if f.level == "WARN"]
    
    if hard:
        # Don't print success if there are hard fails
        return
    
    if warn:
        print(f"{Colors.BRIGHT_YELLOW}⚠️  LIL OS²: {check_name} completed with {len(warn)} warning(s) in {timer.format_elapsed()}{Colors.RESET}")
    else:
        print(f"{Colors.BRIGHT_GREEN}✅ LIL OS²: {check_name} passed in {timer.format_elapsed()}{Colors.RESET}")


# ----------------------------
# OS-Like Output Utilities
# ----------------------------
def print_os_message(message: str, level: str = "INFO"):
    """
    Print a message with OS-like formatting and [LIL OS] prefix.
    
    Args:
        message: The message to print
        level: Message level (INFO, WARN, ERROR, SUCCESS)
    """
    level_colors = {
        "INFO": Colors.BRIGHT_CYAN,
        "WARN": Colors.BRIGHT_YELLOW,
        "ERROR": Colors.BRIGHT_RED,
        "SUCCESS": Colors.BRIGHT_GREEN,
    }
    color = level_colors.get(level, Colors.BRIGHT_CYAN)
    prefix = f"{color}[LIL OS²]{Colors.RESET}"
    print(f"{prefix} {message}")


def format_os_finding(finding: Finding) -> str:
    """
    Convert a Finding object to OS-like formatted string.
    
    Args:
        finding: The Finding object to format
        
    Returns:
        Formatted string with OS-like structure
    """
    level_colors = {
        "HARD_FAIL": Colors.BRIGHT_RED,
        "WARN": Colors.BRIGHT_YELLOW,
        "INFO": Colors.BRIGHT_CYAN,
    }
    level_labels = {
        "HARD_FAIL": "ERROR",
        "WARN": "WARNING",
        "INFO": "INFO",
    }
    
    color = level_colors.get(finding.level, Colors.BRIGHT_CYAN)
    label = level_labels.get(finding.level, finding.level)
    
    lines = []
    lines.append(f"{color}[LIL OS²] {label}: {finding.code}{Colors.RESET}")
    lines.append(f"{Colors.DIM}[LIL OS²]{Colors.RESET} {finding.message}")

    if finding.details:
        lines.append(f"{Colors.DIM}[LIL OS²]{Colors.RESET} Details:")
        import json
        details_str = json.dumps(finding.details, indent=2)
        for detail_line in details_str.splitlines():
            lines.append(f"{Colors.DIM}[LIL OS²]   {detail_line}{Colors.RESET}")
    
    return "\n".join(lines)


def print_os_error(finding: Finding, include_actions: bool = True):
    """
    Print an error with OS-like structure and actionable steps.
    
    Args:
        finding: The Finding object representing the error
        include_actions: Whether to include actionable steps
    """
    print(format_os_finding(finding))
    
    if include_actions and finding.level == "HARD_FAIL":
        print(f"{Colors.DIM}[LIL OS²]{Colors.RESET} Action required:")
        print(f"{Colors.DIM}[LIL OS²]{Colors.RESET}   1. Review the error details above")
        print(f"{Colors.DIM}[LIL OS²]{Colors.RESET}   2. Fix the issue")
        print(f"{Colors.DIM}[LIL OS²]{Colors.RESET}   3. Run validation again: {Colors.BRIGHT_CYAN}lil-os check{Colors.RESET}")
        print(f"{Colors.DIM}[LIL OS²]{Colors.RESET} For help: {Colors.BRIGHT_CYAN}lil-os explain {finding.code}{Colors.RESET}")
        print()


def strip_ansi(text: str) -> str:
    """
    Remove ANSI escape sequences from a string.
    
    Args:
        text: String that may contain ANSI codes
        
    Returns:
        String with ANSI codes removed
    """
    import re
    # Pattern to match ANSI escape sequences
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


def print_os_box(title: str, content: List[str], width: int = 60, show_separator: bool = True):
    """
    Print a box-drawn border with title and content.
    
    Args:
        title: Box title
        content: List of content lines
        width: Box width in characters
        show_separator: Whether to show separator line after title
    """
    # Ensure width is at least title length + padding
    min_width = len(title) + 4
    width = max(width, min_width)
    
    # Top border with double line
    print(f"{Colors.BRIGHT_CYAN}╔{'═' * (width - 2)}╗{Colors.RESET}")
    
    # Title with better formatting
    title_padding = width - len(title) - 4
    left_pad = title_padding // 2
    right_pad = title_padding - left_pad
    print(f"{Colors.BRIGHT_CYAN}║{Colors.RESET}{' ' * left_pad}{Colors.BOLD}{Colors.BRIGHT_WHITE}{title}{Colors.RESET}{' ' * right_pad}{Colors.BRIGHT_CYAN}║{Colors.RESET}")
    
    # Separator
    if show_separator:
        print(f"{Colors.BRIGHT_CYAN}╠{'═' * (width - 2)}╣{Colors.RESET}")
    
    # Content with better formatting
    for i, line in enumerate(content):
        # Handle empty lines
        if not line.strip():
            print(f"{Colors.BRIGHT_CYAN}║{Colors.RESET}{' ' * (width - 2)}{Colors.BRIGHT_CYAN}║{Colors.RESET}")
            continue
        
        # Get visible length (without ANSI codes) for padding calculation
        visible_length = len(strip_ansi(line))
        
        # Truncate if needed (check visible length, not total length)
        display_line = line
        visible_length = len(strip_ansi(display_line))
        if visible_length > width - 4:
            # Need to truncate, but preserve ANSI codes
            # This is tricky - for now, just truncate the raw line
            # A better approach would preserve ANSI codes, but that's complex
            if Colors.RESET not in line:
                # No color codes, safe to truncate
                if len(display_line) > width - 4:
                    display_line = display_line[:width - 7] + "..."
        
        # Build formatted line with colors FIRST, then calculate padding
        if "━━━" in display_line:
            # Section separator - use bright cyan
            colored_content = f"{Colors.BRIGHT_CYAN}{display_line}{Colors.RESET}"
        elif display_line.startswith("  [") and "]" in display_line:
            # Menu item - make it bright and visible
            colored_content = f"{Colors.BRIGHT_WHITE}{display_line}{Colors.RESET}"
        elif display_line.startswith("  •"):
            # Bullet point - use white for visibility
            colored_content = f"{Colors.WHITE}{display_line}{Colors.RESET}"
        elif display_line.startswith("  ") and ("●" in display_line or "✅" in display_line or "⚠️" in display_line):
            # Indented line with emoji - keep visible
            colored_content = f"{Colors.WHITE}{display_line}{Colors.RESET}"
        elif display_line.startswith("  "):
            # Other indented line - slightly dimmed
            colored_content = f"{Colors.DIM}{display_line}{Colors.RESET}"
        elif ":" in display_line and not display_line.startswith(" "):
            # Key-value pair - apply colors
            parts = display_line.split(":", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                # Reconstruct exactly as original but with colors
                # Find where the colon is in the original
                colon_pos = display_line.find(":")
                key_part = display_line[:colon_pos].strip()
                value_part = display_line[colon_pos+1:].strip()
                # Standard format: "key: value"
                colored_content = f"{Colors.BRIGHT_WHITE}{key_part}:{Colors.RESET} {Colors.CYAN}{value_part}{Colors.RESET}"
            else:
                colored_content = display_line
        else:
            colored_content = display_line
        
        # Calculate padding based on VISIBLE length of colored content (ANSI codes don't count)
        visible_len = len(strip_ansi(colored_content))
        padding = max(0, width - visible_len - 4)  # -4 for "║ " and " ║"
        
        # Build final formatted line
        formatted_line = f"{Colors.BRIGHT_CYAN}║{Colors.RESET} {colored_content}{' ' * padding} {Colors.BRIGHT_CYAN}║{Colors.RESET}"
        
        print(formatted_line)
    
    # Bottom border
    print(f"{Colors.BRIGHT_CYAN}╚{'═' * (width - 2)}╝{Colors.RESET}")


# ----------------------------
# Rich UI Helpers
# ----------------------------
def print_rich_panel(
    title: str,
    content: List[str],
    border_style: str = "bright_cyan",
    title_style: str = "bold white"
):
    """
    Print a Rich panel (if Rich is available) or fallback to print_os_box.
    
    Args:
        title: Panel title
        content: List of content lines
        border_style: Rich border style
        title_style: Rich title style
    """
    try:
        from lil_os.cli_ux import print_rich_panel as rich_panel_func
        rich_panel_func(title, content, border_style, title_style)
    except (ImportError, AttributeError):
        # Fallback to existing print_os_box
        print_os_box(title, content, width=60)

