#!/usr/bin/env python3
"""
LIL OS² ML Model Evaluator

Evaluation framework for anomaly detection models.
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass

from .schema import FeatureSet
from .detector import AnomalyDetector


@dataclass
class EvaluationMetrics:
    """Evaluation metrics for anomaly detection."""
    precision: float
    recall: float
    f1_score: float
    false_positive_rate: float
    true_positives: int
    false_positives: int
    true_negatives: int
    false_negatives: int


class ModelEvaluator:
    """Evaluator for anomaly detection models."""
    
    def __init__(self, detector: AnomalyDetector):
        """
        Initialize evaluator.
        
        Args:
            detector: Trained AnomalyDetector instance
        """
        self.detector = detector
    
    def evaluate(
        self,
        feature_sets: List[FeatureSet],
        labels: List[bool]
    ) -> EvaluationMetrics:
        """
        Evaluate model on labeled data.
        
        Args:
            feature_sets: List of feature sets to evaluate
            labels: List of true labels (True = anomaly, False = normal)
            
        Returns:
            EvaluationMetrics object
        """
        if len(feature_sets) != len(labels):
            raise ValueError("Feature sets and labels must have same length")
        
        tp = fp = tn = fn = 0
        
        for feature_set, true_label in zip(feature_sets, labels):
            is_anomaly, score = self.detector.predict(feature_set)
            
            if true_label and is_anomaly:
                tp += 1
            elif true_label and not is_anomaly:
                fn += 1
            elif not true_label and is_anomaly:
                fp += 1
            else:
                tn += 1
        
        # Calculate metrics
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0
        
        return EvaluationMetrics(
            precision=precision,
            recall=recall,
            f1_score=f1,
            false_positive_rate=fpr,
            true_positives=tp,
            false_positives=fp,
            true_negatives=tn,
            false_negatives=fn,
        )
    
    def cross_validate(
        self,
        feature_sets: List[FeatureSet],
        labels: List[bool],
        n_splits: int = 5
    ) -> Dict[str, float]:
        """
        Perform cross-validation evaluation.
        
        Args:
            feature_sets: List of feature sets
            labels: List of true labels
            n_splits: Number of folds (default: 5)
            
        Returns:
            Dictionary with average metrics across folds
        """
        # Simple k-fold cross-validation
        # Note: This is a simplified version. For production, use sklearn's KFold
        
        fold_size = len(feature_sets) // n_splits
        metrics_list = []
        
        for i in range(n_splits):
            start_idx = i * fold_size
            end_idx = start_idx + fold_size if i < n_splits - 1 else len(feature_sets)
            
            # Split data
            test_features = feature_sets[start_idx:end_idx]
            test_labels = labels[start_idx:end_idx]
            train_features = feature_sets[:start_idx] + feature_sets[end_idx:]
            train_labels = labels[:start_idx] + labels[end_idx:]
            
            # Train on fold
            fold_detector = AnomalyDetector()
            fold_detector.train(train_features)
            
            # Evaluate on test set
            fold_evaluator = ModelEvaluator(fold_detector)
            metrics = fold_evaluator.evaluate(test_features, test_labels)
            metrics_list.append(metrics)
        
        # Average metrics
        return {
            "precision": sum(m.precision for m in metrics_list) / len(metrics_list),
            "recall": sum(m.recall for m in metrics_list) / len(metrics_list),
            "f1_score": sum(m.f1_score for m in metrics_list) / len(metrics_list),
            "false_positive_rate": sum(m.false_positive_rate for m in metrics_list) / len(metrics_list),
        }
