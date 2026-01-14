#!/usr/bin/env python3
"""
LIL OS² Background Daemon

Orchestrates all monitoring components and manages the event bus.
Provides start/stop/status functionality for background monitoring.
"""

from __future__ import annotations

import sys
import signal
import threading
import time
from pathlib import Path
from typing import Optional, Dict

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os.events import Event, EventType, EventSeverity, get_event_bus
from lil_os.monitor import FileWatcher, GitMonitor, ValidationMonitor
from lil_os.governance_detector import GovernanceDecisionDetector
from lil_os_utils import print_os_message, load_simple_yaml, Colors


class LILOSDaemon:
    """
    Background daemon for LIL OS² monitoring.
    
    Orchestrates file watching, git monitoring, and validation monitoring.
    """
    
    def __init__(self, config_path: Optional[Path] = None, event_bus=None):
        """
        Initialize daemon.
        
        Args:
            config_path: Path to daemon config file (optional)
            event_bus: Event bus instance (uses global if None)
        """
        self.event_bus = event_bus or get_event_bus()
        self.config_path = config_path or Path("lil_os.daemon.yaml")
        self.config = self._load_config()
        
        # Initialize monitors
        self.file_watcher: Optional[FileWatcher] = None
        self.git_monitor: Optional[GitMonitor] = None
        self.validation_monitor: Optional[ValidationMonitor] = None
        self.governance_detector: Optional[GovernanceDecisionDetector] = None
        
        self.running = False
        self._shutdown_event = threading.Event()
        
        # Setup signal handlers
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _load_config(self) -> dict:
        """Load daemon configuration."""
        if self.config_path.exists():
            try:
                return load_simple_yaml(self.config_path)
            except Exception as e:
                print_os_message(f"Error loading daemon config: {e}", "WARN")
        
        # Return default config
        return {
            "daemon": {
                "enabled": True,
                "watch_interval": 2.0,
                "event_history_size": 1000
            },
            "monitoring": {
                "file_watcher": {
                    "enabled": True,
                    "watch_paths": ["docs/", ".cursorrules"]
                },
                "git_monitor": {
                    "enabled": True,
                    "detect_ai_agents": True
                },
                "validation_monitor": {
                    "enabled": True
                }
            }
        }
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        print_os_message(f"Received signal {signum}, shutting down...", "INFO")
        self.stop()
    
    def start(self) -> None:
        """Start all monitoring components."""
        if self.running:
            print_os_message("Daemon is already running", "WARN")
            return
        
        daemon_config = self.config.get("daemon", {})
        if not daemon_config.get("enabled", True):
            print_os_message("Daemon is disabled in configuration", "WARN")
            return
        
        monitoring_config = self.config.get("monitoring", {})
        
        # Start file watcher
        file_watcher_config = monitoring_config.get("file_watcher", {})
        if file_watcher_config.get("enabled", True):
            watch_paths = file_watcher_config.get("watch_paths", ["docs/", ".cursorrules"])
            self.file_watcher = FileWatcher(
                event_bus=self.event_bus,
                watch_paths=watch_paths
            )
            self.file_watcher.start()
            print_os_message("File watcher started", "INFO")
        
        # Start git monitor
        git_monitor_config = monitoring_config.get("git_monitor", {})
        if git_monitor_config.get("enabled", True):
            detect_ai = git_monitor_config.get("detect_ai_agents", True)
            self.git_monitor = GitMonitor(
                event_bus=self.event_bus,
                detect_ai_agents=detect_ai
            )
            self.git_monitor.start()
            print_os_message("Git monitor started", "INFO")
        
        # Start validation monitor
        validation_config = monitoring_config.get("validation_monitor", {})
        if validation_config.get("enabled", True):
            self.validation_monitor = ValidationMonitor(event_bus=self.event_bus)
            self.validation_monitor.start()
            print_os_message("Validation monitor started", "INFO")
        
        # Start governance decision detector
        self.governance_detector = GovernanceDecisionDetector(event_bus=self.event_bus)
        self.governance_detector.start()
        print_os_message("Governance decision detector started", "INFO")
        
        self.running = True
        
        # Emit daemon started event
        event = Event(
            type=EventType.DAEMON_STARTED,
            source="daemon",
            data={
                "file_watcher": self.file_watcher.is_running() if self.file_watcher else False,
                "git_monitor": self.git_monitor.is_running() if self.git_monitor else False,
                "validation_monitor": self.validation_monitor.is_running() if self.validation_monitor else False,
                "governance_detector": self.governance_detector.is_running() if self.governance_detector else False
            },
            severity=EventSeverity.INFO,
            message="LIL OS² daemon started"
        )
        self.event_bus.publish(event)
        
        print_os_message("LIL OS² daemon started successfully", "SUCCESS")
    
    def stop(self) -> None:
        """Stop all monitoring components."""
        if not self.running:
            return
        
        print_os_message("Stopping daemon...", "INFO")
        
        # Stop monitors
        if self.file_watcher:
            self.file_watcher.stop()
            print_os_message("File watcher stopped", "INFO")
        
        if self.git_monitor:
            self.git_monitor.stop()
            print_os_message("Git monitor stopped", "INFO")
        
        if self.validation_monitor:
            self.validation_monitor.stop()
            print_os_message("Validation monitor stopped", "INFO")
        
        if self.governance_detector:
            self.governance_detector.stop()
            print_os_message("Governance decision detector stopped", "INFO")
        
        self.running = False
        self._shutdown_event.set()
        
        # Emit daemon stopped event
        event = Event(
            type=EventType.DAEMON_STOPPED,
            source="daemon",
            data={},
            severity=EventSeverity.INFO,
            message="LIL OS² daemon stopped"
        )
        self.event_bus.publish(event)
        
        print_os_message("Daemon stopped", "INFO")
    
    def status(self) -> Dict:
        """
        Get daemon status.
        
        Returns:
            Dictionary with status information
        """
        return {
            "running": self.running,
            "file_watcher": {
                "running": self.file_watcher.is_running() if self.file_watcher else False
            },
            "git_monitor": {
                "running": self.git_monitor.is_running() if self.git_monitor else False
            },
            "validation_monitor": {
                "running": self.validation_monitor.is_running() if self.validation_monitor else False
            },
            "governance_detector": {
                "running": self.governance_detector.is_running() if self.governance_detector else False
            },
            "event_count": self.event_bus.get_event_count()
        }
    
    def run(self) -> None:
        """
        Run daemon in foreground (blocking).
        
        Use this for running daemon in a terminal.
        """
        self.start()
        
        try:
            # Keep running until shutdown signal
            while self.running and not self._shutdown_event.is_set():
                time.sleep(1.0)
        except KeyboardInterrupt:
            print_os_message("Interrupted by user", "INFO")
        finally:
            self.stop()
    
    def is_running(self) -> bool:
        """Check if daemon is running."""
        return self.running


def main() -> int:
    """Main entry point for daemon."""
    import argparse
    
    parser = argparse.ArgumentParser(description="LIL OS² Background Daemon")
    parser.add_argument(
        "action",
        choices=["start", "stop", "status", "run"],
        help="Daemon action"
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to daemon config file"
    )
    
    args = parser.parse_args()
    
    daemon = LILOSDaemon(config_path=args.config)
    
    if args.action == "start":
        daemon.start()
        # Keep running
        try:
            while daemon.running:
                time.sleep(1.0)
        except KeyboardInterrupt:
            daemon.stop()
        return 0
    elif args.action == "stop":
        daemon.stop()
        return 0
    elif args.action == "status":
        status = daemon.status()
        print_os_message(f"Daemon status: {'Running' if status['running'] else 'Stopped'}", "INFO")
        print_os_message(f"File watcher: {'Running' if status['file_watcher']['running'] else 'Stopped'}", "INFO")
        print_os_message(f"Git monitor: {'Running' if status['git_monitor']['running'] else 'Stopped'}", "INFO")
        print_os_message(f"Validation monitor: {'Running' if status['validation_monitor']['running'] else 'Stopped'}", "INFO")
        print_os_message(f"Event count: {status['event_count']}", "INFO")
        return 0
    elif args.action == "run":
        daemon.run()
        return 0
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

