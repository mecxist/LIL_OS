#!/usr/bin/env python3
"""
LIL OS² CLI UX - Rich-based UI components

Provides Rich library-based UI components for enhanced terminal experience:
- Panels with formatted content
- Tables for findings
- Interactive prompts
- Streaming output support
"""

from __future__ import annotations

from typing import List, Optional, Dict, Any, Callable
from pathlib import Path
from dataclasses import dataclass

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, Confirm
    from rich.live import Live
    from rich.text import Text
    from rich.layout import Layout
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    # Fallback classes if Rich is not available
    class Console:
        def __init__(self, *args, **kwargs):
            pass
        def print(self, *args, **kwargs):
            print(*args)
    
    class Panel:
        def __init__(self, *args, **kwargs):
            pass
    
    class Table:
        def __init__(self, *args, **kwargs):
            pass
    
    class Prompt:
        @staticmethod
        def ask(*args, **kwargs):
            return input(*args)
    
    class Confirm:
        @staticmethod
        def ask(*args, **kwargs):
            response = input(*args).lower()
            return response in ('y', 'yes')
    
    class Live:
        def __init__(self, *args, **kwargs):
            pass
        def __enter__(self):
            return self
        def __exit__(self, *args):
            pass
        def update(self, *args):
            pass


@dataclass
class RichPanel:
    """Wrapper for Rich Panel with consistent styling."""
    
    title: str
    content: List[str]
    border_style: str = "bright_cyan"
    title_style: str = "bold white"
    
    def render(self, console: Optional[Console] = None) -> Panel:
        """Render the panel using Rich."""
        if not RICH_AVAILABLE:
            # Fallback to plain text
            lines = [f"=== {self.title} ==="]
            lines.extend(self.content)
            return "\n".join(lines)
        
        if console is None:
            console = Console()
        
        # Format content
        text_content = "\n".join(self.content)
        
        return Panel(
            text_content,
            title=self.title,
            border_style=self.border_style,
            title_style=self.title_style,
            box=box.ROUNDED
        )
    
    def print(self, console: Optional[Console] = None):
        """Print the panel to console."""
        if not RICH_AVAILABLE:
            print(self.render())
            return
        
        if console is None:
            console = Console()
        
        panel = self.render(console)
        console.print(panel)


@dataclass
class RichTable:
    """Wrapper for Rich Table for displaying findings."""
    
    title: str
    columns: List[str]
    rows: List[List[str]]
    show_header: bool = True
    
    def render(self, console: Optional[Console] = None) -> Table:
        """Render the table using Rich."""
        if not RICH_AVAILABLE:
            # Fallback to plain text
            lines = [f"=== {self.title} ==="]
            if self.show_header:
                lines.append(" | ".join(self.columns))
                lines.append("-" * 60)
            for row in self.rows:
                lines.append(" | ".join(str(cell) for cell in row))
            return "\n".join(lines)
        
        if console is None:
            console = Console()
        
        table = Table(title=self.title, show_header=self.show_header, box=box.ROUNDED)
        
        # Add columns
        for col in self.columns:
            table.add_column(col, style="cyan" if self.show_header else "white")
        
        # Add rows
        for row in self.rows:
            table.add_row(*[str(cell) for cell in row])
        
        return table
    
    def print(self, console: Optional[Console] = None):
        """Print the table to console."""
        if not RICH_AVAILABLE:
            print(self.render())
            return
        
        if console is None:
            console = Console()
        
        table = self.render(console)
        console.print(table)


class InteractivePrompt:
    """Interactive prompt wrapper using Rich."""
    
    @staticmethod
    def ask(
        question: str,
        default: Optional[str] = None,
        choices: Optional[List[str]] = None,
        console: Optional[Console] = None
    ) -> str:
        """Ask a question with optional choices."""
        if not RICH_AVAILABLE:
            prompt_text = question
            if default:
                prompt_text += f" [{default}]"
            if choices:
                prompt_text += f" ({'/'.join(choices)})"
            prompt_text += ": "
            response = input(prompt_text).strip()
            return response or default or ""
        
        if console is None:
            console = Console()
        
        return Prompt.ask(question, default=default, choices=choices, console=console)
    
    @staticmethod
    def confirm(
        question: str,
        default: bool = True,
        console: Optional[Console] = None
    ) -> bool:
        """Ask a yes/no question."""
        if not RICH_AVAILABLE:
            prompt_text = question
            prompt_text += " (y/n)" if default else " (n/y)"
            prompt_text += f" [{'Y' if default else 'N'}]: "
            response = input(prompt_text).strip().lower()
            if not response:
                return default
            return response in ('y', 'yes')
        
        if console is None:
            console = Console()
        
        return Confirm.ask(question, default=default, console=console)


class StreamingOutput:
    """Context manager for streaming output with Rich Live."""
    
    def __init__(self, renderable: Any = None, console: Optional[Console] = None):
        self.renderable = renderable
        self.console = console or Console()
        self.live: Optional[Live] = None
    
    def __enter__(self):
        if RICH_AVAILABLE:
            self.live = Live(self.renderable or "", console=self.console, refresh_per_second=10)
            self.live.__enter__()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.live:
            self.live.__exit__(exc_type, exc_val, exc_tb)
    
    def update(self, renderable: Any):
        """Update the live display."""
        if self.live:
            self.live.update(renderable)
        else:
            # Fallback: just print
            if hasattr(renderable, '__str__'):
                print(str(renderable))
            else:
                print(renderable)


def print_rich_panel(
    title: str,
    content: List[str],
    border_style: str = "bright_cyan",
    title_style: str = "bold white"
):
    """Helper function to print a Rich panel."""
    panel = RichPanel(title=title, content=content, border_style=border_style, title_style=title_style)
    panel.print()


def print_rich_table(
    title: str,
    columns: List[str],
    rows: List[List[str]],
    show_header: bool = True
):
    """Helper function to print a Rich table."""
    table = RichTable(title=title, columns=columns, rows=rows, show_header=show_header)
    table.print()


def is_rich_available() -> bool:
    """Check if Rich library is available."""
    return RICH_AVAILABLE


def get_console() -> Console:
    """Get a Rich Console instance."""
    if not RICH_AVAILABLE:
        raise ImportError("Rich library is not available. Install with: pip install rich")
    return Console()


def create_findings_table(findings: List[Dict[str, Any]]) -> Table:
    """Create a Rich table for validation findings."""
    if not RICH_AVAILABLE:
        return None
    
    table = Table(title="Findings", show_header=True, box=box.ROUNDED)
    table.add_column("Level", style="cyan", width=12)
    table.add_column("Code", style="yellow", width=20)
    table.add_column("Message", style="white", width=60)
    
    for finding in findings:
        level = finding.get("level", "INFO")
        code = finding.get("code", "")
        message = finding.get("message", "")
        
        # Color code by level
        level_style = {
            "HARD_FAIL": "bright_red",
            "WARN": "bright_yellow",
            "INFO": "bright_cyan",
        }.get(level, "white")
        
        table.add_row(
            Text(level, style=level_style),
            code,
            message[:60] + "..." if len(message) > 60 else message
        )
    
    return table


def format_report_content(report_data: Dict[str, Any]) -> str:
    """Format report data as text content for panel display."""
    lines = []
    
    # Header info
    check_name = report_data.get("check_name", "Unknown")
    status = report_data.get("status", "unknown")
    timestamp = report_data.get("timestamp", "")
    
    status_emoji = {
        "pass": "✅",
        "warn": "⚠️",
        "fail": "❌"
    }.get(status, "ℹ️")
    
    lines.append(f"Check: {check_name}")
    lines.append(f"Status: {status_emoji} {status.upper()}")
    if timestamp:
        lines.append(f"Date: {timestamp}")
    
    # Summary
    summary = report_data.get("summary", {})
    if summary:
        lines.append("")
        lines.append("Summary:")
        lines.append(f"  • Hard Fails: {summary.get('hard_fails', 0)}")
        lines.append(f"  • Warnings: {summary.get('warnings', 0)}")
        lines.append(f"  • Info: {summary.get('info', 0)}")
        lines.append(f"  • Total: {summary.get('total', 0)}")
    
    # Timing
    timing = report_data.get("timing", {})
    if timing:
        lines.append("")
        lines.append(f"Duration: {timing.get('elapsed_formatted', 'N/A')}")
    
    # Findings (first 5)
    findings = report_data.get("findings", [])
    if findings:
        lines.append("")
        lines.append("Findings:")
        for finding in findings[:5]:
            level = finding.get("level", "INFO")
            code = finding.get("code", "")
            message = finding.get("message", "")
            
            level_emoji = {
                "HARD_FAIL": "❌",
                "WARN": "⚠️",
                "INFO": "ℹ️"
            }.get(level, "•")
            
            lines.append(f"  {level_emoji} [{level}] {code}: {message[:50]}")
        
        if len(findings) > 5:
            lines.append(f"  ... and {len(findings) - 5} more findings")
    
    return "\n".join(lines)
