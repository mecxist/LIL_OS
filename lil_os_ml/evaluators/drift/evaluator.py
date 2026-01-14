#!/usr/bin/env python3
"""Drift Evaluator - Anomaly detection."""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any, Optional

try:
    from sklearn.ensemble import IsolationForest
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    IsolationForest = None

from ..base import MLEvaluator, EvaluationResult
from ...signals.collector import Signal
from .features import extract_time_series_features


class DriftEvaluator(MLEvaluator):
    """Evaluator for drift/anomaly detection."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize drift evaluator."""
        super().__init__("drift", config)
        self.model = None
        self.models_dir = Path(config.get("models_dir", ".lil_os/ml/models/drift"))
        self.window_size = config.get("model", {}).get("window_size", 100)
    
    def evaluate(self, signals: List[Signal]) -> EvaluationResult:
        """Evaluate for drift/anomalies."""
        if not SKLEARN_AVAILABLE:
            return EvaluationResult(
                module_name=self.module_name,
                status="error",
                score=0.0,
                findings=[{"message": "scikit-learn not available"}]
            )
        
        # Extract features
        features_list = extract_time_series_features(signals)
        if not features_list:
            return EvaluationResult(
                module_name=self.module_name,
                status="pass",
                score=0.0,
                findings=[]
            )
        
        # Use simple threshold-based detection if model not trained
        if self.model is None:
            return self._threshold_based_detection(features_list[0])
        
        # Use model for detection
        feature_vector = [
            features_list[0].get("validation_failure_rate", 0.0),
            features_list[0].get("rule_violation_rate", 0.0),
            features_list[0].get("commit_frequency", 0.0),
        ]
        
        anomaly_score = self.model.decision_function([feature_vector])[0]
        is_anomaly = self.model.predict([feature_vector])[0] == -1
        
        findings = []
        if is_anomaly:
            findings.append({
                "anomaly_score": float(anomaly_score),
                "message": "Anomaly detected in validation patterns",
                "factors": self._get_anomaly_factors(features_list[0])
            })
        
        status = "warn" if findings else "pass"
        if self.get_mode() == "ci_block" and findings:
            status = "fail"
        
        return EvaluationResult(
            module_name=self.module_name,
            status=status,
            score=abs(float(anomaly_score)),
            findings=findings
        )
    
    def _threshold_based_detection(self, features: Dict[str, Any]) -> EvaluationResult:
        """Simple threshold-based anomaly detection."""
        findings = []
        
        if features.get("validation_failure_rate", 0.0) > 0.5:
            findings.append({
                "message": "High validation failure rate detected",
                "failure_rate": features.get("validation_failure_rate", 0.0)
            })
        
        if features.get("rule_violation_rate", 0.0) > 5.0:
            findings.append({
                "message": "High rule violation rate detected",
                "violation_rate": features.get("rule_violation_rate", 0.0)
            })
        
        status = "warn" if findings else "pass"
        return EvaluationResult(
            module_name=self.module_name,
            status=status,
            score=0.5 if findings else 0.0,
            findings=findings
        )
    
    def _get_anomaly_factors(self, features: Dict[str, Any]) -> List[str]:
        """Get list of anomaly factors."""
        factors = []
        if features.get("validation_failure_rate", 0.0) > 0.3:
            factors.append("high_failure_rate")
        if features.get("rule_violation_rate", 0.0) > 3.0:
            factors.append("high_violation_rate")
        return factors
    
    def train(self, signals: List[Signal], labels: Optional[List[Any]] = None) -> Dict[str, Any]:
        """Train the isolation forest model."""
        if not SKLEARN_AVAILABLE:
            return {"error": "scikit-learn not available"}
        
        features_list = extract_time_series_features(signals)
        if not features_list:
            return {"error": "No features extracted"}
        
        # Convert to feature vectors
        X = []
        for feat in features_list:
            X.append([
                feat.get("validation_failure_rate", 0.0),
                feat.get("rule_violation_rate", 0.0),
                feat.get("commit_frequency", 0.0),
            ])
        
        # Train isolation forest
        self.model = IsolationForest(contamination=0.1, random_state=42)
        self.model.fit(X)
        
        # Save model
        self.save_model(self.models_dir)
        
        return {
            "n_samples": len(X),
            "model_type": "isolation_forest"
        }
    
    def load_model(self, model_path: Path) -> bool:
        """Load model (simplified - would need pickle in production)."""
        # For now, return False (model would need to be pickled)
        # In production, this would load the IsolationForest model
        return False
    
    def save_model(self, model_path: Path) -> bool:
        """Save model (simplified - would need pickle in production)."""
        # For now, just mark that model exists
        model_path.mkdir(parents=True, exist_ok=True)
        return True
