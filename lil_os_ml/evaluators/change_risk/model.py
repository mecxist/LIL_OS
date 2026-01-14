#!/usr/bin/env python3
"""
Change Risk Model - Random Forest Classifier

Simple Random Forest model for change risk prediction.
"""

from __future__ import annotations

import pickle
import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

try:
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.metrics import classification_report, accuracy_score
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    RandomForestClassifier = None


class ChangeRiskModel:
    """Random Forest model for change risk prediction."""
    
    def __init__(self):
        """Initialize the model."""
        if not SKLEARN_AVAILABLE:
            raise ImportError("scikit-learn is required. Install with: pip install scikit-learn")
        
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.feature_names: List[str] = []
        self.trained = False
    
    def train(self, X: List[Dict[str, Any]], y: List[str]) -> Dict[str, Any]:
        """
        Train the model.
        
        Args:
            X: List of feature dictionaries
            y: List of labels ("low", "medium", "high")
            
        Returns:
            Dictionary with training metrics
        """
        if not X or not y:
            return {"error": "No training data provided"}
        
        # Convert features to array
        if not self.feature_names:
            # Extract feature names from first sample
            self.feature_names = sorted(X[0].keys())
        
        X_array = [[x.get(f, 0) for f in self.feature_names] for x in X]
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_array, y, test_size=0.2, random_state=42
        )
        
        # Train
        self.model.fit(X_train, y_train)
        self.trained = True
        
        # Evaluate
        y_pred = self.model.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred, output_dict=True)
        
        return {
            "accuracy": accuracy,
            "classification_report": report,
            "n_samples": len(X),
            "n_features": len(self.feature_names)
        }
    
    def predict(self, X: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Predict risk levels for features.
        
        Args:
            X: List of feature dictionaries
            
        Returns:
            List of predictions with risk level and probability
        """
        if not self.trained:
            return [{"risk_level": "unknown", "risk_score": 0.0} for _ in X]
        
        # Convert to array
        X_array = [[x.get(f, 0) for f in self.feature_names] for x in X]
        
        # Predict
        predictions = self.model.predict(X_array)
        probabilities = self.model.predict_proba(X_array)
        
        # Map to risk scores (low=0.3, medium=0.6, high=0.9)
        risk_map = {"low": 0.3, "medium": 0.6, "high": 0.9}
        
        results = []
        for pred, prob in zip(predictions, probabilities):
            risk_level = pred
            # Get probability of high risk
            if hasattr(self.model, "classes_"):
                high_idx = list(self.model.classes_).index("high") if "high" in self.model.classes_ else 0
                risk_score = prob[high_idx] if high_idx < len(prob) else 0.5
            else:
                risk_score = risk_map.get(risk_level, 0.5)
            
            results.append({
                "risk_level": risk_level,
                "risk_score": float(risk_score)
            })
        
        return results
    
    def save(self, model_path: Path, metadata: Optional[Dict[str, Any]] = None):
        """Save model to disk."""
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model
        pickle_path = model_path / "model.pkl"
        with open(pickle_path, "wb") as f:
            pickle.dump(self.model, f)
        
        # Save metadata
        meta = {
            "feature_names": self.feature_names,
            "trained": self.trained,
            "trained_at": datetime.utcnow().isoformat() + "Z",
            **(metadata or {})
        }
        
        meta_path = model_path / "metadata.json"
        with open(meta_path, "w", encoding="utf-8") as f:
            json.dump(meta, f, indent=2)
    
    def load(self, model_path: Path) -> bool:
        """Load model from disk."""
        pickle_path = model_path / "model.pkl"
        meta_path = model_path / "metadata.json"
        
        if not pickle_path.exists() or not meta_path.exists():
            return False
        
        try:
            # Load model
            with open(pickle_path, "rb") as f:
                self.model = pickle.load(f)
            
            # Load metadata
            with open(meta_path, "r", encoding="utf-8") as f:
                meta = json.load(f)
                self.feature_names = meta.get("feature_names", [])
                self.trained = meta.get("trained", False)
            
            return True
        except Exception:
            return False
