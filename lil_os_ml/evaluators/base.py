#!/usr/bin/env python3
"""
ML Evaluator Base Class

Abstract base class for ML evaluators.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime

from ..signals.collector import Signal


@dataclass
class EvaluationResult:
    """Result of an ML evaluation."""
    module_name: str
    status: str  # "pass" | "warn" | "fail" | "error"
    score: float  # 0.0 to 1.0
    findings: List[Dict[str, Any]]
    metadata: Optional[Dict[str, Any]] = None
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat() + "Z"


class MLEvaluator(ABC):
    """Abstract base class for ML evaluators."""
    
    def __init__(self, module_name: str, config: Dict[str, Any]):
        """
        Initialize ML evaluator.
        
        Args:
            module_name: Name of the ML module
            config: Configuration dictionary
        """
        self.module_name = module_name
        self.config = config
        self.model = None
        self.model_path: Optional[Path] = None
    
    @abstractmethod
    def evaluate(self, signals: List[Signal]) -> EvaluationResult:
        """
        Evaluate signals and return results.
        
        Args:
            signals: List of signals to evaluate
            
        Returns:
            EvaluationResult object
        """
        pass
    
    @abstractmethod
    def train(self, signals: List[Signal], labels: Optional[List[Any]] = None) -> Dict[str, Any]:
        """
        Train the model on signals.
        
        Args:
            signals: Training signals
            labels: Optional labels for supervised learning
            
        Returns:
            Dictionary with training metrics
        """
        pass
    
    @abstractmethod
    def load_model(self, model_path: Path) -> bool:
        """
        Load a trained model from disk.
        
        Args:
            model_path: Path to model file
            
        Returns:
            True if model loaded successfully
        """
        pass
    
    @abstractmethod
    def save_model(self, model_path: Path) -> bool:
        """
        Save the trained model to disk.
        
        Args:
            model_path: Path to save model
            
        Returns:
            True if model saved successfully
        """
        pass
    
    def is_enabled(self) -> bool:
        """Check if this evaluator is enabled in config."""
        return self.config.get("enabled", False)
    
    def get_mode(self) -> str:
        """Get the mode (warn, require_review, ci_block)."""
        return self.config.get("mode", "warn")
    
    def get_threshold(self) -> float:
        """Get the threshold for this evaluator."""
        return self.config.get("threshold", 0.7)
