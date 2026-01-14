#!/usr/bin/env python3
"""
Validation Monitor

Monitors validation script runs and captures results.
"""

from __future__ import annotations

import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os.events import Event, EventType, EventSeverity, get_event_bus


class ValidationMonitor:
    """
    Validation script monitor for LIL OS².
    
    Monitors validation script executions and captures results.
    """
    
    def __init__(self, event_bus=None):
        """
        Initialize validation monitor.
        
        Args:
            event_bus: Event bus instance (uses global if None)
        """
        self.event_bus = event_bus or get_event_bus()
        self.running = False
    
    def monitor_validation_run(self, script_name: str, exit_code: int, output: str = "", duration: float = 0.0) -> None:
        """
        Monitor a validation script run.
        
        Args:
            script_name: Name of the validation script
            exit_code: Exit code from script
            output: Script output (optional)
            duration: Execution duration in seconds
        """
        if exit_code == 0:
            event = Event(
                type=EventType.VALIDATION_PASSED,
                source="validation_monitor",
                data={
                    "script": script_name,
                    "exit_code": exit_code,
                    "duration": duration
                },
                severity=EventSeverity.INFO,
                message=f"Validation passed: {script_name}"
            )
        else:
            event = Event(
                type=EventType.VALIDATION_FAILED,
                source="validation_monitor",
                data={
                    "script": script_name,
                    "exit_code": exit_code,
                    "output": output[:500] if output else "",  # Truncate long output
                    "duration": duration
                },
                severity=EventSeverity.ERROR,
                message=f"Validation failed: {script_name}"
            )
        
        self.event_bus.publish(event)
    
    def start(self) -> None:
        """Start validation monitor."""
        if self.running:
            return
        
        self.running = True
        
        event = Event(
            type=EventType.DAEMON_STARTED,
            source="validation_monitor",
            data={"component": "validation_monitor"},
            severity=EventSeverity.INFO,
            message="Validation monitor started"
        )
        self.event_bus.publish(event)
    
    def stop(self) -> None:
        """Stop validation monitor."""
        self.running = False
    
    def is_running(self) -> bool:
        """Check if monitor is running."""
        return self.running

