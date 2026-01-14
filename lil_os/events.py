#!/usr/bin/env python3
"""
LIL OS² Event System

Central event bus for all LIL OS² activities. Provides pub/sub pattern
for monitoring, logging, and governance decision detection.
"""

from __future__ import annotations

import threading
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Callable, Optional
from collections import defaultdict
from enum import Enum


class EventType(Enum):
    """Event type enumeration."""
    FILE_CHANGED = "FILE_CHANGED"
    GOVERNANCE_FILE_CHANGED = "GOVERNANCE_FILE_CHANGED"
    GIT_COMMIT = "GIT_COMMIT"
    GIT_STAGE = "GIT_STAGE"
    VALIDATION_RUN = "VALIDATION_RUN"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    VALIDATION_PASSED = "VALIDATION_PASSED"
    GOVERNANCE_DECISION_NEEDED = "GOVERNANCE_DECISION_NEEDED"
    AI_AGENT_ACTION = "AI_AGENT_ACTION"
    DECISION_LOG_CREATED = "DECISION_LOG_CREATED"
    DAEMON_STARTED = "DAEMON_STARTED"
    DAEMON_STOPPED = "DAEMON_STOPPED"


class EventSeverity(Enum):
    """Event severity levels."""
    INFO = "INFO"
    WARN = "WARN"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class Event:
    """Represents a single event in the LIL OS² system."""
    type: EventType
    timestamp: datetime = field(default_factory=datetime.now)
    source: str = ""
    data: dict = field(default_factory=dict)
    severity: EventSeverity = EventSeverity.INFO
    message: str = ""
    
    def __str__(self) -> str:
        """String representation of event."""
        time_str = self.timestamp.strftime("%H:%M:%S")
        return f"[{time_str}] [{self.severity.value}] {self.type.value}: {self.message or 'No message'}"


class EventBus:
    """
    Central event bus for LIL OS².
    
    Provides pub/sub pattern for event distribution.
    Thread-safe for use with background daemon and shell.
    """
    
    def __init__(self, max_history: int = 1000):
        """
        Initialize event bus.
        
        Args:
            max_history: Maximum number of events to keep in history
        """
        self._subscribers: Dict[EventType, List[Callable[[Event], None]]] = defaultdict(list)
        self._all_subscribers: List[Callable[[Event], None]] = []
        self._event_history: List[Event] = []
        self._max_history = max_history
        self._lock = threading.Lock()
    
    def publish(self, event: Event) -> None:
        """
        Publish an event to all subscribers.
        
        Args:
            event: The event to publish
        """
        with self._lock:
            # Add to history
            self._event_history.append(event)
            
            # Trim history if needed
            if len(self._event_history) > self._max_history:
                self._event_history = self._event_history[-self._max_history:]
            
            # Notify type-specific subscribers
            if event.type in self._subscribers:
                for callback in self._subscribers[event.type]:
                    try:
                        callback(event)
                    except Exception as e:
                        # Don't let subscriber errors break the event bus
                        print(f"Error in event subscriber: {e}")
            
            # Notify all-event subscribers
            for callback in self._all_subscribers:
                try:
                    callback(event)
                except Exception as e:
                    print(f"Error in event subscriber: {e}")
    
    def subscribe(self, event_type: Optional[EventType] = None, callback: Optional[Callable[[Event], None]] = None) -> None:
        """
        Subscribe to events.
        
        Args:
            event_type: Specific event type to subscribe to, or None for all events
            callback: Function to call when event is published
        """
        if callback is None:
            raise ValueError("Callback is required")
        
        with self._lock:
            if event_type is None:
                self._all_subscribers.append(callback)
            else:
                self._subscribers[event_type].append(callback)
    
    def unsubscribe(self, event_type: Optional[EventType] = None, callback: Optional[Callable[[Event], None]] = None) -> None:
        """
        Unsubscribe from events.
        
        Args:
            event_type: Specific event type, or None for all events
            callback: Function to remove from subscribers
        """
        if callback is None:
            return
        
        with self._lock:
            if event_type is None:
                if callback in self._all_subscribers:
                    self._all_subscribers.remove(callback)
            else:
                if event_type in self._subscribers:
                    if callback in self._subscribers[event_type]:
                        self._subscribers[event_type].remove(callback)
    
    def get_recent_events(self, limit: int = 100, event_type: Optional[EventType] = None) -> List[Event]:
        """
        Get recent events from history.
        
        Args:
            limit: Maximum number of events to return
            event_type: Filter by event type, or None for all types
            
        Returns:
            List of recent events, most recent first
        """
        with self._lock:
            events = self._event_history.copy()
            
            # Filter by type if specified
            if event_type is not None:
                events = [e for e in events if e.type == event_type]
            
            # Return most recent events
            return list(reversed(events[-limit:]))
    
    def get_event_count(self, event_type: Optional[EventType] = None) -> int:
        """
        Get count of events in history.
        
        Args:
            event_type: Filter by event type, or None for all types
            
        Returns:
            Number of events
        """
        with self._lock:
            if event_type is None:
                return len(self._event_history)
            return sum(1 for e in self._event_history if e.type == event_type)
    
    def clear_history(self) -> None:
        """Clear event history."""
        with self._lock:
            self._event_history.clear()


# Global event bus instance
_global_event_bus: Optional[EventBus] = None


def get_event_bus() -> EventBus:
    """
    Get the global event bus instance.
    
    Returns:
        Global EventBus instance
    """
    global _global_event_bus
    if _global_event_bus is None:
        _global_event_bus = EventBus()
    return _global_event_bus


def reset_event_bus() -> None:
    """Reset the global event bus (useful for testing)."""
    global _global_event_bus
    _global_event_bus = None

