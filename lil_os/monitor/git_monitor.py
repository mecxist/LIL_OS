#!/usr/bin/env python3
"""
Git Monitor

Monitors git operations (staging, commits, branches) and detects
AI agent patterns in changes.
"""

from __future__ import annotations

import sys
import subprocess
import re
import time
from pathlib import Path
from typing import List, Dict, Optional, Set
from datetime import datetime

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os.events import Event, EventType, EventSeverity, get_event_bus
from lil_os_utils import read_text


class GitMonitor:
    """
    Git operation monitor for LIL OS².
    
    Monitors git staging, commits, and detects AI agent patterns.
    """
    
    def __init__(self, event_bus=None, detect_ai_agents: bool = True):
        """
        Initialize git monitor.
        
        Args:
            event_bus: Event bus instance (uses global if None)
            detect_ai_agents: Whether to detect AI agent patterns
        """
        self.event_bus = event_bus or get_event_bus()
        self.detect_ai_agents = detect_ai_agents
        self.running = False
        self._last_staged_files: Set[str] = set()
        self._last_commit_hash: Optional[str] = None
        self._last_check_time = time.time()
        self._ai_patterns = self._get_ai_patterns()
    
    def _get_ai_patterns(self) -> List[re.Pattern]:
        """Get regex patterns for detecting AI agent commits."""
        patterns = [
            re.compile(r'\b(ai|agent|assistant|claude|cursor|gpt|copilot)\b', re.IGNORECASE),
            re.compile(r'\b(generated|auto|automatic|automated)\b', re.IGNORECASE),
            re.compile(r'^feat\(.*\):.*', re.IGNORECASE),  # Conventional commits often from AI
            re.compile(r'^fix\(.*\):.*', re.IGNORECASE),
            re.compile(r'^refactor\(.*\):.*', re.IGNORECASE),
        ]
        return patterns
    
    def _git_available(self) -> bool:
        """Check if git is available."""
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _is_git_repo(self) -> bool:
        """Check if current directory is a git repository."""
        if not self._git_available():
            return False
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                capture_output=True,
                check=True
            )
            return result.returncode == 0
        except subprocess.CalledProcessError:
            return False
    
    def _get_staged_files(self) -> Set[str]:
        """Get currently staged files."""
        if not self._is_git_repo():
            return set()
        
        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                capture_output=True,
                text=True,
                check=True
            )
            files = {f.strip() for f in result.stdout.strip().splitlines() if f.strip()}
            return files
        except subprocess.CalledProcessError:
            return set()
    
    def _get_latest_commit(self) -> Optional[Dict]:
        """Get latest commit information."""
        if not self._is_git_repo():
            return None
        
        try:
            # Get commit hash
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                capture_output=True,
                text=True,
                check=True
            )
            commit_hash = result.stdout.strip()
            
            if commit_hash == self._last_commit_hash:
                return None  # No new commit
            
            # Get commit message and author
            result = subprocess.run(
                ["git", "log", "-1", "--format=%H|%an|%ae|%ai|%s", commit_hash],
                capture_output=True,
                text=True,
                check=True
            )
            
            if result.stdout.strip():
                parts = result.stdout.strip().split("|", 4)
                if len(parts) >= 5:
                    return {
                        "hash": parts[0],
                        "author": parts[1],
                        "email": parts[2],
                        "date": parts[3],
                        "message": parts[4]
                    }
        except subprocess.CalledProcessError:
            pass
        
        return None
    
    def _detect_ai_agent(self, commit_info: Dict) -> bool:
        """
        Detect if commit appears to be from an AI agent.
        
        Args:
            commit_info: Commit information dictionary
            
        Returns:
            True if AI agent pattern detected
        """
        if not self.detect_ai_agents:
            return False
        
        message = commit_info.get("message", "").lower()
        author = commit_info.get("author", "").lower()
        
        # Check message patterns
        for pattern in self._ai_patterns:
            if pattern.search(message):
                return True
        
        # Check for rapid commits (AI agents often make many commits quickly)
        # This is handled by the monitoring frequency
        
        # Check for .cursorrules changes (often indicates AI agent activity)
        # This is handled by file watcher
        
        return False
    
    def _check_staged_files(self) -> None:
        """Check for staged file changes."""
        current_staged = self._get_staged_files()
        
        # Find newly staged files
        newly_staged = current_staged - self._last_staged_files
        
        if newly_staged:
            for file_path in newly_staged:
                event = Event(
                    type=EventType.GIT_STAGE,
                    source="git_monitor",
                    data={"file": file_path},
                    severity=EventSeverity.INFO,
                    message=f"File staged: {Path(file_path).name}"
                )
                self.event_bus.publish(event)
        
        # Find unstaged files
        unstaged = self._last_staged_files - current_staged
        if unstaged:
            # Files were unstaged, but we don't emit events for that
            pass
        
        self._last_staged_files = current_staged
    
    def _check_commits(self) -> None:
        """Check for new commits."""
        commit_info = self._get_latest_commit()
        
        if commit_info:
            self._last_commit_hash = commit_info["hash"]
            
            # Check if AI agent
            is_ai_agent = self._detect_ai_agent(commit_info)
            
            # Emit commit event
            event = Event(
                type=EventType.GIT_COMMIT,
                source="git_monitor",
                data={
                    "hash": commit_info["hash"],
                    "author": commit_info["author"],
                    "message": commit_info["message"],
                    "date": commit_info["date"]
                },
                severity=EventSeverity.INFO,
                message=f"Commit: {commit_info['message'][:50]}"
            )
            self.event_bus.publish(event)
            
            # Emit AI agent action if detected
            if is_ai_agent:
                event = Event(
                    type=EventType.AI_AGENT_ACTION,
                    source="git_monitor",
                    data={
                        "commit_hash": commit_info["hash"],
                        "message": commit_info["message"],
                        "author": commit_info["author"]
                    },
                    severity=EventSeverity.INFO,
                    message=f"AI agent action detected: {commit_info['message'][:50]}"
                )
                self.event_bus.publish(event)
    
    def start(self) -> None:
        """Start monitoring git operations."""
        if self.running:
            return
        
        if not self._is_git_repo():
            # Not a git repo, can't monitor
            event = Event(
                type=EventType.DAEMON_STARTED,
                source="git_monitor",
                data={"component": "git_monitor", "status": "disabled", "reason": "not_git_repo"},
                severity=EventSeverity.WARN,
                message="Git monitor disabled: not a git repository"
            )
            self.event_bus.publish(event)
            return
        
        self.running = True
        
        # Initialize state
        self._last_staged_files = self._get_staged_files()
        self._last_commit_hash = None
        commit_info = self._get_latest_commit()
        if commit_info:
            self._last_commit_hash = commit_info["hash"]
        
        # Start monitoring loop in background thread
        import threading
        
        def monitor_loop():
            while self.running:
                try:
                    self._check_staged_files()
                    self._check_commits()
                except Exception as e:
                    # Don't let errors stop monitoring
                    event = Event(
                        type=EventType.VALIDATION_FAILED,
                        source="git_monitor",
                        data={"error": str(e)},
                        severity=EventSeverity.ERROR,
                        message=f"Git monitor error: {e}"
                    )
                    self.event_bus.publish(event)
                
                time.sleep(2.0)  # Check every 2 seconds
        
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()
        
        event = Event(
            type=EventType.DAEMON_STARTED,
            source="git_monitor",
            data={"component": "git_monitor"},
            severity=EventSeverity.INFO,
            message="Git monitor started"
        )
        self.event_bus.publish(event)
    
    def stop(self) -> None:
        """Stop monitoring git operations."""
        self.running = False
    
    def is_running(self) -> bool:
        """Check if monitor is running."""
        return self.running

