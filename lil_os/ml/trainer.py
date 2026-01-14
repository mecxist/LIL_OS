#!/usr/bin/env python3
"""
LIL OS² ML Model Trainer

Training pipeline for anomaly detection models.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime
from typing import List, Optional, Dict, Any
import json

from .schema import FeatureSet, load_feature_set, save_feature_set
from .detector import AnomalyDetector


class ModelTrainer:
    """Trainer for anomaly detection models."""
    
    def __init__(
        self,
        features_dir: Optional[Path] = None,
        models_dir: Optional[Path] = None
    ):
        """
        Initialize model trainer.
        
        Args:
            features_dir: Directory containing feature files (default: .lil_os/ml/features)
            models_dir: Directory to save models (default: .lil_os/ml/models)
        """
        self.features_dir = features_dir or Path(".lil_os/ml/features")
        self.models_dir = models_dir or Path(".lil_os/ml/models")
        self.models_dir.mkdir(parents=True, exist_ok=True)
    
    def load_historical_features(self, days: int = 90) -> List[FeatureSet]:
        """
        Load historical features from disk.
        
        Args:
            days: Number of days of history to load (default: 90)
            
        Returns:
            List of FeatureSet objects
        """
        if not self.features_dir.exists():
            return []
        
        feature_sets = []
        cutoff_date = datetime.now().timestamp() - (days * 24 * 60 * 60)
        
        for feature_file in sorted(self.features_dir.glob("*.json"), reverse=True):
            try:
                # Only load files newer than cutoff
                if feature_file.stat().st_mtime < cutoff_date:
                    continue
                
                feature_set = load_feature_set(feature_file)
                feature_sets.append(feature_set)
            except Exception:
                # Skip corrupted files
                continue
        
        return sorted(feature_sets, key=lambda fs: fs.timestamp)
    
    def train_model(
        self,
        feature_sets: Optional[List[FeatureSet]] = None,
        days: int = 90,
        contamination: float = 0.1,
        force: bool = False
    ) -> tuple[Path, Dict[str, Any]]:
        """
        Train anomaly detection model.
        
        Args:
            feature_sets: Optional pre-loaded feature sets (if None, loads from disk)
            days: Number of days of history to use (default: 90)
            contamination: Expected proportion of anomalies (default: 0.1)
            force: Force retraining even if model exists (default: False)
            
        Returns:
            Tuple of (model_path, metadata)
        """
        # Load features if not provided
        if feature_sets is None:
            feature_sets = self.load_historical_features(days=days)
        
        if len(feature_sets) < 10:
            raise ValueError(
                f"Insufficient training data: {len(feature_sets)} feature sets. "
                "Need at least 10 for meaningful training."
            )
        
        # Generate model filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        model_filename = f"model_v{timestamp}_isolation_forest.pkl"
        model_path = self.models_dir / model_filename
        
        # Check if model exists
        if model_path.exists() and not force:
            raise FileExistsError(
                f"Model already exists: {model_path}. Use --force to retrain."
            )
        
        # Train model
        detector = AnomalyDetector()
        threshold, metadata = detector.train(
            feature_sets=feature_sets,
            contamination=contamination
        )
        
        # Add training metadata
        metadata.update({
            "version": "1.0",
            "algorithm": "IsolationForest",
            "trained_at": datetime.utcnow().isoformat() + "Z",
            "feature_set_version": "1.0",
            "features_used": FeatureSet.get_feature_names(),
        })
        
        # Save model
        metadata_path = model_path.with_suffix(".json")
        detector.save_model(model_path, metadata_path)
        
        return model_path, metadata
    
    def get_latest_model(self) -> Optional[Path]:
        """Get path to latest trained model."""
        if not self.models_dir.exists():
            return None
        
        model_files = list(self.models_dir.glob("model_*.pkl"))
        if not model_files:
            return None
        
        # Sort by modification time (newest first)
        return max(model_files, key=lambda p: p.stat().st_mtime)
