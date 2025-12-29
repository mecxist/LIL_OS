#!/usr/bin/env python3
"""
LIL OS Shared Utilities

Common utilities used across LIL OS scripts. This module consolidates duplicate
code to reduce maintenance burden and ensure consistency.

Dependencies: Python 3.10+ (standard library only)
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Tuple


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
    Simple YAML parser for LIL OS configuration files.
    
    Handles:
    - Nested dictionaries
    - Lists
    - String, integer, and boolean values
    - Quoted strings with escape sequences
    - Comments (lines starting with #)
    
    This is a minimal parser designed specifically for LIL OS config files.
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

