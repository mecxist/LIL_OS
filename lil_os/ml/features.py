#!/usr/bin/env python3
"""
LIL OS² ML Feature Engineering

Utilities for feature engineering and normalization.
"""

from __future__ import annotations

from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional
import json

from .schema import FeatureSet, save_feature_set
from .extractor import FeatureExtractor


def extract_current_features(
    repo_path: Optional[Path] = None,
    reports_dir: Optional[Path] = None,
    output_dir: Optional[Path] = None
) -> FeatureSet:
    """
    Extract current features and optionally save to disk.
    
    Args:
        repo_path: Path to git repository
        reports_dir: Directory containing validation reports
        output_dir: Directory to save feature file (if None, doesn't save)
        
    Returns:
        FeatureSet object
    """
    extractor = FeatureExtractor(repo_path=repo_path, reports_dir=reports_dir)
    feature_set = extractor.extract_features()
    
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = output_dir / f"{timestamp}_features.json"
        save_feature_set(feature_set, output_path)
    
    return feature_set


def extract_historical_features(
    days: int = 90,
    repo_path: Optional[Path] = None,
    reports_dir: Optional[Path] = None,
    output_dir: Optional[Path] = None
) -> List[FeatureSet]:
    """
    Extract features for historical time points.
    
    Note: This is a simplified version. A full implementation would:
    - Use git log to get commits at specific dates
    - Reconstruct state at each date
    - Extract features for each date
    
    For now, this just extracts current features.
    
    Args:
        days: Number of days of history to extract
        repo_path: Path to git repository
        reports_dir: Directory containing validation reports
        output_dir: Directory to save feature files
        
    Returns:
        List of FeatureSet objects
    """
    # Simplified: just extract current features
    # Full implementation would extract features for each day
    feature_set = extract_current_features(
        repo_path=repo_path,
        reports_dir=reports_dir,
        output_dir=output_dir
    )
    
    return [feature_set]
