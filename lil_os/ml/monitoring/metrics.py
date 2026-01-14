"""
ML Model Performance Metrics

Track prediction accuracy, false positive/negative rates, and model performance.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional
from collections import defaultdict


@dataclass
class ModelMetrics:
    """Metrics for a single ML model."""
    model_name: str
    total_predictions: int = 0
    true_positives: int = 0
    false_positives: int = 0
    true_negatives: int = 0
    false_negatives: int = 0
    average_confidence: float = 0.0
    last_updated: Optional[datetime] = None
    
    @property
    def accuracy(self) -> float:
        """Calculate accuracy."""
        total = self.total_predictions
        if total == 0:
            return 0.0
        return (self.true_positives + self.true_negatives) / total
    
    @property
    def precision(self) -> float:
        """Calculate precision."""
        positives = self.true_positives + self.false_positives
        if positives == 0:
            return 0.0
        return self.true_positives / positives
    
    @property
    def recall(self) -> float:
        """Calculate recall."""
        actual_positives = self.true_positives + self.false_negatives
        if actual_positives == 0:
            return 0.0
        return self.true_positives / actual_positives
    
    @property
    def f1_score(self) -> float:
        """Calculate F1 score."""
        p = self.precision
        r = self.recall
        if p + r == 0:
            return 0.0
        return 2 * (p * r) / (p + r)


class MetricsCollector:
    """
    Collects and tracks ML model performance metrics.
    """
    
    def __init__(self):
        """Initialize metrics collector."""
        self.metrics: Dict[str, ModelMetrics] = {}
    
    def record_prediction(
        self,
        model_name: str,
        predicted: bool,
        actual: bool,
        confidence: float,
    ) -> None:
        """
        Record a prediction result.
        
        Args:
            model_name: Name of the model
            predicted: What the model predicted
            actual: What actually happened
            confidence: Model confidence (0.0-1.0)
        """
        if model_name not in self.metrics:
            self.metrics[model_name] = ModelMetrics(model_name=model_name)
        
        metrics = self.metrics[model_name]
        metrics.total_predictions += 1
        metrics.last_updated = datetime.now()
        
        # Update running average confidence
        total = metrics.total_predictions
        metrics.average_confidence = (
            (metrics.average_confidence * (total - 1) + confidence) / total
        )
        
        # Update confusion matrix
        if predicted and actual:
            metrics.true_positives += 1
        elif predicted and not actual:
            metrics.false_positives += 1
        elif not predicted and not actual:
            metrics.true_negatives += 1
        else:  # not predicted and actual
            metrics.false_negatives += 1
    
    def get_metrics(self, model_name: str) -> Optional[ModelMetrics]:
        """Get metrics for a specific model."""
        return self.metrics.get(model_name)
    
    def get_all_metrics(self) -> Dict[str, ModelMetrics]:
        """Get all metrics."""
        return dict(self.metrics)
    
    def get_summary(self) -> Dict[str, any]:
        """Get summary of all metrics."""
        summary = {
            "total_models": len(self.metrics),
            "models": {},
        }
        
        for model_name, metrics in self.metrics.items():
            summary["models"][model_name] = {
                "accuracy": metrics.accuracy,
                "precision": metrics.precision,
                "recall": metrics.recall,
                "f1_score": metrics.f1_score,
                "total_predictions": metrics.total_predictions,
                "average_confidence": metrics.average_confidence,
                "false_positive_rate": (
                    metrics.false_positives / metrics.total_predictions
                    if metrics.total_predictions > 0 else 0.0
                ),
                "false_negative_rate": (
                    metrics.false_negatives / metrics.total_predictions
                    if metrics.total_predictions > 0 else 0.0
                ),
            }
        
        return summary


# Global metrics collector instance
_global_collector = MetricsCollector()


def get_metrics_collector() -> MetricsCollector:
    """Get the global metrics collector instance."""
    return _global_collector
