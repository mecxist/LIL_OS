"""
ML Decision Logging

Log ML model decisions for audit and analysis.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
import json


@dataclass
class MLDecisionLog:
    """Log entry for an ML model decision."""
    timestamp: datetime
    model_name: str
    input_data: Dict[str, Any]
    prediction: Any
    confidence: float
    explanation: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class MLLogger:
    """
    Logger for ML model decisions.
    """
    
    def __init__(self, log_file: Optional[Path] = None):
        """
        Initialize ML logger.
        
        Args:
            log_file: Optional file path to log to (defaults to in-memory only)
        """
        self.log_file = log_file
        self.logs: List[MLDecisionLog] = []
        self.max_logs = 1000  # Keep last 1000 logs in memory
    
    def log_decision(
        self,
        model_name: str,
        input_data: Dict[str, Any],
        prediction: Any,
        confidence: float,
        explanation: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Log an ML model decision.
        
        Args:
            model_name: Name of the model
            input_data: Input data to the model
            prediction: Model prediction
            confidence: Model confidence
            explanation: Optional explanation
            metadata: Optional metadata
        """
        log_entry = MLDecisionLog(
            timestamp=datetime.now(),
            model_name=model_name,
            input_data=input_data,
            prediction=prediction,
            confidence=confidence,
            explanation=explanation,
            metadata=metadata,
        )
        
        self.logs.append(log_entry)
        
        # Keep only last max_logs entries
        if len(self.logs) > self.max_logs:
            self.logs = self.logs[-self.max_logs:]
        
        # Write to file if specified
        if self.log_file:
            self._write_to_file(log_entry)
    
    def _write_to_file(self, log_entry: MLDecisionLog) -> None:
        """Write log entry to file."""
        if not self.log_file:
            return
        
        # Ensure directory exists
        self.log_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Append to log file (JSON lines format)
        log_data = {
            "timestamp": log_entry.timestamp.isoformat(),
            "model_name": log_entry.model_name,
            "input_data": log_entry.input_data,
            "prediction": str(log_entry.prediction),
            "confidence": log_entry.confidence,
            "explanation": log_entry.explanation,
            "metadata": log_entry.metadata,
        }
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_data) + "\n")
    
    def get_recent_logs(self, limit: int = 100) -> List[MLDecisionLog]:
        """Get recent log entries."""
        return self.logs[-limit:]
    
    def get_logs_by_model(self, model_name: str) -> List[MLDecisionLog]:
        """Get all logs for a specific model."""
        return [log for log in self.logs if log.model_name == model_name]


# Global logger instance
_global_logger = MLLogger()


def get_ml_logger() -> MLLogger:
    """Get the global ML logger instance."""
    return _global_logger
