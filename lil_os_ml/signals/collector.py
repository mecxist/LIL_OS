#!/usr/bin/env python3
"""
Signal Collector Base Class

Abstract base class for collecting signals from various sources.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime
from dataclasses import dataclass


@dataclass
class Signal:
    """A single signal data point."""
    timestamp: str
    source: str
    signal_type: str
    data: Dict[str, Any]
    metadata: Optional[Dict[str, Any]] = None


class SignalCollector(ABC):
    """Abstract base class for signal collectors."""
    
    def __init__(self, source_name: str):
        """
        Initialize signal collector.
        
        Args:
            source_name: Name of the signal source (e.g., "git", "reports")
        """
        self.source_name = source_name
    
    @abstractmethod
    def collect(self, **kwargs) -> List[Signal]:
        """
        Collect signals from the source.
        
        Args:
            **kwargs: Collector-specific arguments
            
        Returns:
            List of Signal objects
        """
        pass
    
    def _create_signal(
        self,
        signal_type: str,
        data: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> Signal:
        """
        Create a Signal object with current timestamp.
        
        Args:
            signal_type: Type of signal (e.g., "commit", "validation_report")
            data: Signal data
            metadata: Optional metadata
            
        Returns:
            Signal object
        """
        return Signal(
            timestamp=datetime.utcnow().isoformat() + "Z",
            source=self.source_name,
            signal_type=signal_type,
            data=data,
            metadata=metadata
        )
