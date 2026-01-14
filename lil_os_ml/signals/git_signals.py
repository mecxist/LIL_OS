#!/usr/bin/env python3
"""
Git Signal Collector

Collects signals from git commits, diffs, and file changes.
"""

from __future__ import annotations

import subprocess
import re
from pathlib import Path
from typing import List, Dict, Any, Optional

from .collector import SignalCollector, Signal


class GitSignalCollector(SignalCollector):
    """Collects signals from git repository."""
    
    def __init__(self, repo_path: Optional[Path] = None):
        """
        Initialize git signal collector.
        
        Args:
            repo_path: Path to git repository (default: current directory)
        """
        super().__init__("git")
        self.repo_path = repo_path or Path.cwd()
    
    def _is_git_repo(self) -> bool:
        """Check if current directory is a git repository."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "--git-dir"],
                cwd=self.repo_path,
                capture_output=True,
                check=True
            )
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _run_git_command(self, command: List[str]) -> Optional[str]:
        """Run a git command and return output."""
        try:
            result = subprocess.run(
                ["git"] + command,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None
    
    def collect_commits(self, limit: int = 50, since: Optional[str] = None) -> List[Signal]:
        """
        Collect signals from git commits.
        
        Args:
            limit: Maximum number of commits to process
            since: ISO timestamp to filter commits after
            
        Returns:
            List of commit signals
        """
        if not self._is_git_repo():
            return []
        
        signals = []
        
        # Build git log command
        cmd = ["log", "--pretty=format:%H|%an|%ae|%ad|%s", "--date=iso"]
        if since:
            cmd.append(f"--since={since}")
        cmd.append(f"-{limit}")
        
        log_output = self._run_git_command(cmd)
        if not log_output:
            return []
        
        for line in log_output.splitlines():
            parts = line.split("|", 4)
            if len(parts) < 5:
                continue
            
            commit_hash, author_name, author_email, date, message = parts
            
            # Get commit stats
            stats = self._get_commit_stats(commit_hash)
            
            # Get changed files
            changed_files = self._get_changed_files(commit_hash)
            
            signal_data = {
                "commit_hash": commit_hash,
                "author_name": author_name,
                "author_email": author_email,
                "date": date,
                "message": message,
                "stats": stats,
                "changed_files": changed_files,
            }
            
            signals.append(self._create_signal("commit", signal_data))
        
        return signals
    
    def _get_commit_stats(self, commit_hash: str) -> Dict[str, int]:
        """Get commit statistics (lines added/deleted)."""
        output = self._run_git_command(["show", "--stat", "--format=", commit_hash])
        if not output:
            return {"additions": 0, "deletions": 0, "files_changed": 0}
        
        # Parse stat output
        additions = 0
        deletions = 0
        files_changed = 0
        
        for line in output.splitlines():
            if "|" in line:
                files_changed += 1
                # Extract numbers from lines like " 5 files changed, 10 insertions(+), 2 deletions(-)"
                match = re.search(r'(\d+)\s+insertions?', line)
                if match:
                    additions += int(match.group(1))
                match = re.search(r'(\d+)\s+deletions?', line)
                if match:
                    deletions += int(match.group(1))
        
        return {
            "additions": additions,
            "deletions": deletions,
            "files_changed": files_changed,
            "total_lines": additions + deletions
        }
    
    def _get_changed_files(self, commit_hash: str) -> List[str]:
        """Get list of changed files in a commit."""
        output = self._run_git_command(["diff-tree", "--no-commit-id", "--name-only", "-r", commit_hash])
        if not output:
            return []
        
        return [f.strip() for f in output.splitlines() if f.strip()]
    
    def collect(self, limit: int = 50, since: Optional[str] = None, **kwargs) -> List[Signal]:
        """
        Collect signals from git.
        
        Args:
            limit: Maximum number of commits to process
            since: ISO timestamp to filter commits after
            **kwargs: Additional arguments (ignored)
            
        Returns:
            List of signals
        """
        return self.collect_commits(limit=limit, since=since)
