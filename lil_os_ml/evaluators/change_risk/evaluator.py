#!/usr/bin/env python3
"""
Change Risk Evaluator

Supervised classifier for predicting change risk levels.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict, Any

from ..base import MLEvaluator, EvaluationResult
from ...signals.collector import Signal
from .features import extract_features_batch
from .model import ChangeRiskModel


class ChangeRiskEvaluator(MLEvaluator):
    """Evaluator for change risk prediction."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize change risk evaluator."""
        super().__init__("change_risk", config)
        self.model_wrapper = ChangeRiskModel()
        self.models_dir = Path(config.get("models_dir", ".lil_os/ml/models/change_risk"))
    
    def evaluate(self, signals: List[Signal]) -> EvaluationResult:
        """Evaluate change risk for signals."""
        if not self.model_wrapper.trained:
            # Try to load model
            if not self.load_model(self.models_dir):
                return EvaluationResult(
                    module_name=self.module_name,
                    status="error",
                    score=0.0,
                    findings=[{"message": "Model not trained or loaded"}]
                )
        
        # Extract features
        commit_signals = [s for s in signals if s.signal_type == "commit"]
        if not commit_signals:
            return EvaluationResult(
                module_name=self.module_name,
                status="pass",
                score=0.0,
                findings=[]
            )
        
        features = extract_features_batch(commit_signals)
        if not features:
            return EvaluationResult(
                module_name=self.module_name,
                status="pass",
                score=0.0,
                findings=[]
            )
        
        # Predict
        predictions = self.model_wrapper.predict(features)
        
        # Generate findings
        findings = []
        threshold = self.get_threshold()
        
        for signal, pred in zip(commit_signals, predictions):
            risk_score = pred["risk_score"]
            risk_level = pred["risk_level"]
            
            if risk_score >= threshold:
                findings.append({
                    "commit": signal.data.get("commit_hash", "unknown")[:8],
                    "risk_score": risk_score,
                    "risk_level": risk_level,
                    "message": signal.data.get("message", "")[:100],
                    "factors": self._get_risk_factors(signal, features[commit_signals.index(signal)])
                })
        
        # Determine status
        if not findings:
            status = "pass"
        elif self.get_mode() == "ci_block":
            status = "fail"
        else:
            status = "warn"
        
        return EvaluationResult(
            module_name=self.module_name,
            status=status,
            score=max([f["risk_score"] for f in findings], default=0.0),
            findings=findings
        )
    
    def _get_risk_factors(self, signal: Signal, features: Dict[str, Any]) -> List[str]:
        """Get list of risk factors for a signal."""
        factors = []
        
        if features.get("diff_size", 0) > 500:
            factors.append("large_diff")
        if features.get("files_changed", 0) > 10:
            factors.append("many_files")
        if features.get("touches_governance", 0) == 1:
            factors.append("touches_governance")
        
        return factors
    
    def train(self, signals: List[Signal], labels: Optional[List[str]] = None) -> Dict[str, Any]:
        """Train the model."""
        # For now, use simple heuristic-based labels if not provided
        if labels is None:
            commit_signals = [s for s in signals if s.signal_type == "commit"]
            features = extract_features_batch(commit_signals)
            
            # Simple heuristic: large diffs = high risk
            labels = []
            for feat in features:
                if feat.get("diff_size", 0) > 500 or feat.get("touches_governance", 0) == 1:
                    labels.append("high")
                elif feat.get("diff_size", 0) > 100:
                    labels.append("medium")
                else:
                    labels.append("low")
        
        # Train
        commit_signals = [s for s in signals if s.signal_type == "commit"]
        features = extract_features_batch(commit_signals)
        
        if len(features) != len(labels):
            return {"error": "Mismatch between features and labels"}
        
        metrics = self.model_wrapper.train(features, labels)
        
        # Save model
        self.save_model(self.models_dir)
        
        return metrics
    
    def load_model(self, model_path: Path) -> bool:
        """Load model from disk."""
        return self.model_wrapper.load(model_path)
    
    def save_model(self, model_path: Path) -> bool:
        """Save model to disk."""
        try:
            self.model_wrapper.save(model_path)
            return True
        except Exception:
            return False
