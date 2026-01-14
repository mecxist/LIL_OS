#!/usr/bin/env python3
"""
Governance Decision Detector

Analyzes events to determine when governance decisions are needed.
Emits GOVERNANCE_DECISION_NEEDED events when governance files change
without corresponding decision log entries.
"""

from __future__ import annotations

import sys
import subprocess
import re
from pathlib import Path
from typing import List, Set, Optional
from datetime import datetime, timedelta

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os.events import Event, EventType, EventSeverity, get_event_bus
from lil_os_utils import read_text


class GovernanceDecisionDetector:
    """
    Detects when governance decisions are needed.
    
    Analyzes events to determine if governance files have been changed
    without corresponding decision log entries.
    """
    
    def __init__(self, event_bus=None):
        """
        Initialize governance decision detector.
        
        Args:
            event_bus: Event bus instance (uses global if None)
        """
        self.event_bus = event_bus or get_event_bus()
        self.running = False
        self._recent_governance_changes: List[Event] = []
        self._decision_log_entries: Set[str] = set()
        self._last_decision_log_check = datetime.now()
    
    def _git_available(self) -> bool:
        """Check if git is available."""
        try:
            subprocess.run(["git", "--version"], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False
    
    def _is_governance_file(self, file_path: str) -> bool:
        """Check if file is a governance file."""
        governance_files = [
            "docs/MASTER_RULES.md",
            "docs/GOVERNANCE.md",
            "docs/RESET_TRIGGERS.md",
            "docs/CONTEXT_BUDGET.md",
            ".cursorrules",
        ]
        return file_path in governance_files or any(file_path.endswith(f) for f in governance_files)
    
    def _check_decision_log_entry(self, file_path: str, commit_hash: Optional[str] = None) -> bool:
        """
        Check if decision log has entry for governance file change.
        
        Args:
            file_path: Path to governance file that changed
            commit_hash: Optional commit hash to check
            
        Returns:
            True if decision log entry found
        """
        decision_log = Path("docs/DECISION_LOG.md")
        if not decision_log.exists():
            return False
        
        decision_log_text = read_text(decision_log)
        file_name = Path(file_path).name
        
        # Check if file name is mentioned in decision log
        if file_name.lower() in decision_log_text.lower():
            # Check if entry is recent (within last 7 days)
            date_pattern = r"Date:\s*([^\n]+)"
            dates = re.findall(date_pattern, decision_log_text, re.IGNORECASE)
            
            if dates:
                try:
                    from dateutil import parser as date_parser
                    for date_str in dates[-5:]:  # Check last 5 entries
                        try:
                            entry_date = date_parser.parse(date_str.strip())
                            days_diff = abs((datetime.now() - entry_date).days)
                            if days_diff <= 7:
                                return True
                        except Exception:
                            pass
                except ImportError:
                    # dateutil not available, assume entry exists if file name mentioned
                    return True
        
        # Check commit hash if provided
        if commit_hash:
            short_hash = commit_hash[:7]
            if short_hash in decision_log_text or commit_hash in decision_log_text:
                return True
        
        return False
    
    def _handle_governance_file_changed(self, event: Event) -> None:
        """Handle GOVERNANCE_FILE_CHANGED event."""
        file_path = event.data.get("file", "")
        
        if not self._is_governance_file(file_path):
            return
        
        # Check if decision log entry exists
        commit_hash = event.data.get("commit_hash")
        has_entry = self._check_decision_log_entry(file_path, commit_hash)
        
        if not has_entry:
            # Emit governance decision needed event
            decision_event = Event(
                type=EventType.GOVERNANCE_DECISION_NEEDED,
                source="governance_detector",
                data={
                    "file": file_path,
                    "reason": "governance_file_changed",
                    "commit_hash": commit_hash,
                    "timestamp": event.timestamp.isoformat()
                },
                severity=EventSeverity.WARN,
                message=f"Governance file changed without decision log entry: {Path(file_path).name}"
            )
            self.event_bus.publish(decision_event)
    
    def _handle_validation_failed(self, event: Event) -> None:
        """Handle VALIDATION_FAILED event that might require governance decision."""
        script = event.data.get("script", "")
        exit_code = event.data.get("exit_code", 0)
        
        # Check if validation failure is related to governance
        if "governance" in script.lower() or "governance_file_changes_unlogged" in str(event.data):
            decision_event = Event(
                type=EventType.GOVERNANCE_DECISION_NEEDED,
                source="governance_detector",
                data={
                    "reason": "validation_failed",
                    "script": script,
                    "exit_code": exit_code,
                    "original_event": event.data
                },
                severity=EventSeverity.ERROR,
                message=f"Validation failed requiring governance decision: {script}"
            )
            self.event_bus.publish(decision_event)
    
    def _handle_decision_log_created(self, event: Event) -> None:
        """Handle DECISION_LOG_CREATED event - clear pending governance decisions."""
        # When decision log is created, we can clear related pending decisions
        # This is handled by the event subscriber
        pass
    
    def start(self) -> None:
        """Start governance decision detector."""
        if self.running:
            return
        
        self.running = True
        
        # Subscribe to relevant events
        self.event_bus.subscribe(EventType.GOVERNANCE_FILE_CHANGED, self._handle_governance_file_changed)
        self.event_bus.subscribe(EventType.VALIDATION_FAILED, self._handle_validation_failed)
        self.event_bus.subscribe(EventType.DECISION_LOG_CREATED, self._handle_decision_log_created)
        
        # Check existing governance file changes
        self._check_existing_changes()
    
    def stop(self) -> None:
        """Stop governance decision detector."""
        if not self.running:
            return
        
        # Unsubscribe from events
        self.event_bus.unsubscribe(EventType.GOVERNANCE_FILE_CHANGED, self._handle_governance_file_changed)
        self.event_bus.unsubscribe(EventType.VALIDATION_FAILED, self._handle_validation_failed)
        self.event_bus.unsubscribe(EventType.DECISION_LOG_CREATED, self._handle_decision_log_created)
        
        self.running = False
    
    def _check_existing_changes(self) -> None:
        """Check for existing governance file changes that need decision log entries."""
        if not self._git_available():
            return
        
        try:
            # Get recent commits that modified governance files
            since = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
            governance_files = [
                "docs/MASTER_RULES.md",
                "docs/GOVERNANCE.md",
                "docs/RESET_TRIGGERS.md",
                "docs/CONTEXT_BUDGET.md",
                ".cursorrules",
            ]
            
            for gov_file in governance_files:
                if not Path(gov_file).exists():
                    continue
                
                cmd = ["git", "log", f"--since={since}", "--format=%H|%ai", "--", gov_file]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0 and result.stdout.strip():
                    for line in result.stdout.strip().splitlines():
                        parts = line.split("|", 1)
                        if len(parts) >= 2:
                            commit_hash = parts[0]
                            commit_date = parts[1]
                            
                            # Check if decision log entry exists
                            if not self._check_decision_log_entry(gov_file, commit_hash):
                                decision_event = Event(
                                    type=EventType.GOVERNANCE_DECISION_NEEDED,
                                    source="governance_detector",
                                    data={
                                        "file": gov_file,
                                        "reason": "existing_change",
                                        "commit_hash": commit_hash,
                                        "commit_date": commit_date
                                    },
                                    severity=EventSeverity.WARN,
                                    message=f"Existing governance file change without decision log entry: {Path(gov_file).name}"
                                )
                                self.event_bus.publish(decision_event)
        except Exception as e:
            # Don't let errors break the detector
            pass
    
    def is_running(self) -> bool:
        """Check if detector is running."""
        return self.running

