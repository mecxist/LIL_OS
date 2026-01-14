#!/usr/bin/env python3
"""
LIL OS² ML Anomaly Detector

IsolationForest-based anomaly detection for drift detection.
"""

from __future__ import annotations

import pickle
from pathlib import Path
from typing import Optional, Tuple
import json

try:
    from sklearn.ensemble import IsolationForest
    from sklearn.preprocessing import StandardScaler
    import numpy as np
    SKLEARN_AVAILABLE = True
except ImportError:
    SKLEARN_AVAILABLE = False
    IsolationForest = None
    StandardScaler = None
    np = None

from .schema import FeatureSet, load_feature_set, save_feature_set


class AnomalyDetector:
    """Anomaly detector using IsolationForest."""
    
    def __init__(self, model_path: Optional[Path] = None):
        """
        Initialize anomaly detector.
        
        Args:
            model_path: Path to saved model (optional)
        """
        if not SKLEARN_AVAILABLE:
            raise ImportError(
                "scikit-learn is required for anomaly detection. "
                "Install with: pip install scikit-learn"
            )
        
        self.model: Optional[IsolationForest] = None
        self.scaler: Optional[StandardScaler] = None
        self.threshold: float = 0.7
        self.model_path = model_path
        self.metadata: Optional[dict] = None
        
        if model_path and model_path.exists():
            self.load_model(model_path)
    
    def train(
        self,
        feature_sets: list[FeatureSet],
        contamination: float = 0.1,
        n_estimators: int = 100,
        random_state: int = 42
    ) -> Tuple[float, dict]:
        """
        Train the anomaly detection model.
        
        Args:
            feature_sets: List of feature sets for training
            contamination: Expected proportion of anomalies (default: 0.1)
            n_estimators: Number of trees in forest (default: 100)
            random_state: Random seed for reproducibility (default: 42)
            
        Returns:
            Tuple of (threshold, metadata dictionary)
        """
        if not feature_sets:
            raise ValueError("No feature sets provided for training")
        
        # Convert to feature vectors
        X = np.array([fs.to_feature_vector() for fs in feature_sets])
        
        # Normalize features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train IsolationForest
        self.model = IsolationForest(
            contamination=contamination,
            n_estimators=n_estimators,
            random_state=random_state
        )
        self.model.fit(X_scaled)
        
        # Calculate anomaly scores for training set
        scores = self.model.score_samples(X_scaled)
        # IsolationForest returns negative scores (lower = more anomalous)
        # Convert to positive scores (higher = more anomalous)
        anomaly_scores = -scores
        
        # Set threshold at 95th percentile
        self.threshold = float(np.percentile(anomaly_scores, 95))
        
        # Calculate metadata
        self.metadata = {
            "training_samples": len(feature_sets),
            "contamination": contamination,
            "n_estimators": n_estimators,
            "threshold": self.threshold,
            "min_score": float(np.min(anomaly_scores)),
            "max_score": float(np.max(anomaly_scores)),
            "mean_score": float(np.mean(anomaly_scores)),
            "std_score": float(np.std(anomaly_scores)),
        }
        
        return self.threshold, self.metadata
    
    def predict(self, feature_set: FeatureSet) -> Tuple[bool, float]:
        """
        Predict if a feature set is anomalous.
        
        Args:
            feature_set: Feature set to evaluate
            
        Returns:
            Tuple of (is_anomaly, anomaly_score)
        """
        if self.model is None or self.scaler is None:
            raise ValueError("Model not trained. Call train() first.")
        
        # Convert to feature vector
        X = np.array([feature_set.to_feature_vector()])
        
        # Normalize
        X_scaled = self.scaler.transform(X)
        
        # Get anomaly score
        score = self.model.score_samples(X_scaled)[0]
        # Convert to positive score (higher = more anomalous)
        anomaly_score = -score
        
        # Check if above threshold
        is_anomaly = anomaly_score > self.threshold
        
        return is_anomaly, float(anomaly_score)
    
    def save_model(self, model_path: Path, metadata_path: Optional[Path] = None):
        """
        Save trained model to disk.
        
        Args:
            model_path: Path to save model pickle file
            metadata_path: Path to save metadata JSON (default: model_path with .json extension)
        """
        if self.model is None or self.scaler is None:
            raise ValueError("No model to save. Train model first.")
        
        model_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Save model and scaler
        model_data = {
            "model": self.model,
            "scaler": self.scaler,
            "threshold": self.threshold,
        }
        
        with open(model_path, "wb") as f:
            pickle.dump(model_data, f)
        
        # Save metadata
        if metadata_path is None:
            metadata_path = model_path.with_suffix(".json")
        
        if self.metadata:
            metadata_path.write_text(
                json.dumps(self.metadata, indent=2),
                encoding="utf-8"
            )
    
    def load_model(self, model_path: Path):
        """
        Load trained model from disk.
        
        Args:
            model_path: Path to model pickle file
        """
        if not model_path.exists():
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        with open(model_path, "rb") as f:
            model_data = pickle.load(f)
        
        self.model = model_data["model"]
        self.scaler = model_data["scaler"]
        self.threshold = model_data.get("threshold", 0.7)
        
        # Try to load metadata
        metadata_path = model_path.with_suffix(".json")
        if metadata_path.exists():
            self.metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        else:
            self.metadata = None
