#!/usr/bin/env python3
"""Tests for session management."""

import tempfile
from pathlib import Path
from lil_os.session import SessionManager, SessionEntry


def test_session_manager():
    """Test SessionManager basic functionality."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sessions_dir = Path(tmpdir) / "sessions"
        manager = SessionManager(sessions_dir)
        
        # Save entry
        manager.save_entry(
            command="test",
            args=["--flag"],
            exit_code=0,
            duration_seconds=1.5
        )
        
        # Get entries
        entries = manager.get_recent_entries(limit=10)
        assert len(entries) == 1
        assert entries[0].command == "test"
        assert entries[0].exit_code == 0


def test_session_context():
    """Test session context retrieval."""
    with tempfile.TemporaryDirectory() as tmpdir:
        sessions_dir = Path(tmpdir) / "sessions"
        manager = SessionManager(sessions_dir)
        
        context = manager.get_context()
        assert "working_directory" in context
        assert "last_command" in context
