#!/usr/bin/env python3
"""
File System Watcher

Monitors governance files and other important files for changes.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import List, Set, Dict, Optional
from datetime import datetime

# Add scripts directory to path
scripts_dir = Path(__file__).parent.parent.parent / "scripts"
sys.path.insert(0, str(scripts_dir))

from lil_os.events import Event, EventType, EventSeverity, get_event_bus

try:
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler, FileSystemEvent
    WATCHDOG_AVAILABLE = True
except ImportError:
    WATCHDOG_AVAILABLE = False
    # Fallback to polling-based watching
    Observer = None
    FileSystemEventHandler = None
    FileSystemEvent = None


# Conditionally define handler class based on watchdog availability
if WATCHDOG_AVAILABLE:
    class GovernanceFileHandler(FileSystemEventHandler):
        """Handler for file system events."""
        
        def __init__(self, event_bus, governance_files: Set[str]):
            """
            Initialize handler.
            
            Args:
                event_bus: Event bus to publish events to
                governance_files: Set of governance file paths to watch
            """
            self.event_bus = event_bus
            self.governance_files = governance_files
            self._last_modified: Dict[str, float] = {}
        
        def _is_governance_file(self, file_path: str) -> bool:
            """Check if file is a governance file."""
            return file_path in self.governance_files
        
        def _should_emit_event(self, file_path: str) -> bool:
            """
            Check if we should emit an event (avoid duplicate events).
            
            Args:
                file_path: Path to file
                
            Returns:
                True if event should be emitted
            """
            import time
            current_time = time.time()
            
            # Emit event if:
            # 1. We haven't seen this file before, or
            # 2. It's been more than 1 second since last event (debounce)
            if file_path not in self._last_modified:
                self._last_modified[file_path] = current_time
                return True
            
            if current_time - self._last_modified[file_path] > 1.0:
                self._last_modified[file_path] = current_time
                return True
            
            return False
        
        def on_modified(self, event: FileSystemEvent) -> None:
            """Handle file modification."""
            if event.is_directory:
                return
            
            file_path = str(event.src_path)
            
            if not self._should_emit_event(file_path):
                return
            
            if self._is_governance_file(file_path):
                # Governance file changed
                event_obj = Event(
                    type=EventType.GOVERNANCE_FILE_CHANGED,
                    source="file_watcher",
                    data={"file": file_path},
                    severity=EventSeverity.WARN,
                    message=f"Governance file modified: {Path(file_path).name}"
                )
                self.event_bus.publish(event_obj)
            else:
                # Regular file changed
                event_obj = Event(
                    type=EventType.FILE_CHANGED,
                    source="file_watcher",
                    data={"file": file_path},
                    severity=EventSeverity.INFO,
                    message=f"File modified: {Path(file_path).name}"
                )
                self.event_bus.publish(event_obj)
        
        def on_created(self, event: FileSystemEvent) -> None:
            """Handle file creation."""
            if event.is_directory:
                return
            
            file_path = str(event.src_path)
            
            if self._is_governance_file(file_path):
                event_obj = Event(
                    type=EventType.GOVERNANCE_FILE_CHANGED,
                    source="file_watcher",
                    data={"file": file_path, "action": "created"},
                    severity=EventSeverity.WARN,
                    message=f"Governance file created: {Path(file_path).name}"
                )
                self.event_bus.publish(event_obj)
else:
    # Dummy class when watchdog is not available (won't be used in watchdog mode)
    class GovernanceFileHandler:
        """Dummy handler when watchdog is not available."""
        def __init__(self, event_bus, governance_files: Set[str]):
            pass


class FileWatcher:
    """
    File system watcher for LIL OS².
    
    Monitors governance files and other important files for changes.
    """
    
    def __init__(self, event_bus=None, watch_paths: List[str] = None):
        """
        Initialize file watcher.
        
        Args:
            event_bus: Event bus instance (uses global if None)
            watch_paths: Paths to watch (defaults to governance files)
        """
        self.event_bus = event_bus or get_event_bus()
        self.watch_paths = watch_paths or self._get_default_watch_paths()
        self.governance_files = self._get_governance_files()
        self.observer: Optional[Observer] = None
        self.handler: Optional[GovernanceFileHandler] = None
        self.running = False
    
    def _get_default_watch_paths(self) -> List[str]:
        """Get default paths to watch."""
        base_path = Path.cwd()
        return [
            str(base_path / "docs"),
            str(base_path / ".cursorrules"),
        ]
    
    def _get_governance_files(self) -> Set[str]:
        """Get set of governance file paths."""
        base_path = Path.cwd()
        governance_files = [
            str(base_path / "docs" / "MASTER_RULES.md"),
            str(base_path / "docs" / "GOVERNANCE.md"),
            str(base_path / "docs" / "RESET_TRIGGERS.md"),
            str(base_path / "docs" / "CONTEXT_BUDGET.md"),
            str(base_path / ".cursorrules"),
            str(base_path / "docs" / "DECISION_LOG.md"),
        ]
        return set(governance_files)
    
    def start(self) -> None:
        """Start watching files."""
        if not WATCHDOG_AVAILABLE:
            # Fallback to polling-based watching
            self._start_polling()
            return
        
        if self.running:
            return
        
        self.handler = GovernanceFileHandler(self.event_bus, self.governance_files)
        self.observer = Observer()
        
        # Watch each path
        for path_str in self.watch_paths:
            path = Path(path_str)
            if path.exists():
                self.observer.schedule(self.handler, str(path.parent if path.is_file() else path), recursive=False)
        
        self.observer.start()
        self.running = True
        
        # Emit daemon started event
        event = Event(
            type=EventType.DAEMON_STARTED,
            source="file_watcher",
            data={"component": "file_watcher"},
            severity=EventSeverity.INFO,
            message="File watcher started"
        )
        self.event_bus.publish(event)
    
    def stop(self) -> None:
        """Stop watching files."""
        if not self.running:
            return
        
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=2.0)
            self.observer = None
        
        self.handler = None
        self.running = False
    
    def _start_polling(self) -> None:
        """
        Fallback polling-based file watching.
        
        Used when watchdog library is not available.
        """
        import time
        import hashlib
        
        self.running = True
        file_hashes: Dict[str, str] = {}
        
        def get_file_hash(file_path: Path) -> str:
            """Get hash of file contents."""
            try:
                if file_path.exists() and file_path.is_file():
                    content = file_path.read_bytes()
                    return hashlib.md5(content).hexdigest()
            except Exception:
                pass
            return ""
        
        def check_files():
            """Check for file changes."""
            for file_path_str in self.governance_files:
                file_path = Path(file_path_str)
                current_hash = get_file_hash(file_path)
                
                if file_path_str in file_hashes:
                    if file_hashes[file_path_str] != current_hash:
                        # File changed
                        event = Event(
                            type=EventType.GOVERNANCE_FILE_CHANGED,
                            source="file_watcher",
                            data={"file": file_path_str},
                            severity=EventSeverity.WARN,
                            message=f"Governance file modified: {file_path.name}"
                        )
                        self.event_bus.publish(event)
                        file_hashes[file_path_str] = current_hash
                else:
                    # New file
                    if current_hash:
                        file_hashes[file_path_str] = current_hash
        
        # Start polling in background thread
        import threading
        
        def poll_loop():
            while self.running:
                check_files()
                time.sleep(2.0)  # Poll every 2 seconds
        
        thread = threading.Thread(target=poll_loop, daemon=True)
        thread.start()
        
        event = Event(
            type=EventType.DAEMON_STARTED,
            source="file_watcher",
            data={"component": "file_watcher", "mode": "polling"},
            severity=EventSeverity.INFO,
            message="File watcher started (polling mode)"
        )
        self.event_bus.publish(event)
    
    def is_running(self) -> bool:
        """Check if watcher is running."""
        return self.running

