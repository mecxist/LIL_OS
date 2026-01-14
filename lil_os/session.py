#!/usr/bin/env python3
"""
LIL OS² Session Management

Manages session history and context for CLI commands.
Stores session data in JSONL format in .lil_os/sessions/
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
from dataclasses import dataclass, asdict


@dataclass
class SessionEntry:
    """A single session entry."""
    timestamp: str
    command: str
    args: List[str]
    working_directory: str
    exit_code: int
    duration_seconds: float
    context: Optional[Dict[str, Any]] = None


class SessionManager:
    """Manages session history and context."""
    
    def __init__(self, sessions_dir: Optional[Path] = None):
        """
        Initialize session manager.
        
        Args:
            sessions_dir: Directory to store sessions (default: .lil_os/sessions/)
        """
        if sessions_dir is None:
            sessions_dir = Path(".lil_os/sessions")
        
        self.sessions_dir = sessions_dir
        self.sessions_dir.mkdir(parents=True, exist_ok=True)
        
        # Current session file (one per day)
        today = datetime.now().strftime("%Y-%m-%d")
        self.current_session_file = self.sessions_dir / f"session_{today}.jsonl"
    
    def save_entry(
        self,
        command: str,
        args: List[str],
        exit_code: int,
        duration_seconds: float,
        context: Optional[Dict[str, Any]] = None
    ):
        """
        Save a session entry.
        
        Args:
            command: Command name
            args: Command arguments
            exit_code: Exit code
            duration_seconds: Duration in seconds
            context: Optional context dictionary
        """
        entry = SessionEntry(
            timestamp=datetime.utcnow().isoformat() + "Z",
            command=command,
            args=args,
            working_directory=str(Path.cwd()),
            exit_code=exit_code,
            duration_seconds=duration_seconds,
            context=context
        )
        
        # Append to JSONL file
        with open(self.current_session_file, "a", encoding="utf-8") as f:
            json.dump(asdict(entry), f)
            f.write("\n")
    
    def get_recent_entries(self, limit: int = 50) -> List[SessionEntry]:
        """
        Get recent session entries.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of session entries (most recent first)
        """
        entries: List[SessionEntry] = []
        
        # Get all session files, sorted by date (newest first)
        session_files = sorted(
            self.sessions_dir.glob("session_*.jsonl"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        for session_file in session_files:
            if len(entries) >= limit:
                break
            
            try:
                with open(session_file, "r", encoding="utf-8") as f:
                    for line in f:
                        if line.strip():
                            data = json.loads(line)
                            entries.append(SessionEntry(**data))
                            if len(entries) >= limit:
                                break
            except Exception:
                # Skip corrupted files
                continue
        
        # Sort by timestamp (most recent first)
        entries.sort(key=lambda e: e.timestamp, reverse=True)
        return entries[:limit]
    
    def get_command_history(self, command: Optional[str] = None) -> List[SessionEntry]:
        """
        Get command history, optionally filtered by command name.
        
        Args:
            command: Optional command name to filter by
            
        Returns:
            List of session entries
        """
        entries = self.get_recent_entries(limit=1000)
        
        if command:
            entries = [e for e in entries if e.command == command]
        
        return entries
    
    def get_last_command(self) -> Optional[SessionEntry]:
        """Get the last executed command."""
        entries = self.get_recent_entries(limit=1)
        return entries[0] if entries else None
    
    def get_context(self) -> Dict[str, Any]:
        """
        Get current session context.
        
        Returns:
            Dictionary with context information
        """
        last_entry = self.get_last_command()
        
        context = {
            "working_directory": str(Path.cwd()),
            "last_command": last_entry.command if last_entry else None,
            "last_exit_code": last_entry.exit_code if last_entry else None,
            "last_timestamp": last_entry.timestamp if last_entry else None,
        }
        
        return context
    
    def clear_history(self, days: Optional[int] = None):
        """
        Clear session history.
        
        Args:
            days: If provided, only clear entries older than this many days
        """
        if days is None:
            # Clear all
            for session_file in self.sessions_dir.glob("session_*.jsonl"):
                session_file.unlink()
        else:
            # Clear old files
            cutoff = datetime.now().timestamp() - (days * 24 * 60 * 60)
            for session_file in self.sessions_dir.glob("session_*.jsonl"):
                if session_file.stat().st_mtime < cutoff:
                    session_file.unlink()
