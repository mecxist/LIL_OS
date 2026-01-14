#!/usr/bin/env python3
"""Drift feature extraction."""

from __future__ import annotations

from typing import Dict, Any, List
from collections import defaultdict

from ...signals.collector import Signal


def extract_time_series_features(signals: List[Signal]) -> List[Dict[str, Any]]:
    """Extract time series features for drift detection."""
    # Group by time windows
    report_signals = [s for s in signals if s.signal_type == "validation_report"]
    
    if len(report_signals) < 2:
        return []
    
    # Calculate rates over time
    features_list = []
    
    # Window size (last N reports)
    window_size = min(10, len(report_signals))
    window = report_signals[:window_size]
    
    # Calculate failure rate
    failures = sum(1 for s in window if s.data.get("status") == "fail")
    failure_rate = failures / len(window) if window else 0.0
    
    # Calculate violation rate
    total_violations = sum(s.data.get("summary", {}).get("hard_fails", 0) for s in window)
    violation_rate = total_violations / len(window) if window else 0.0
    
    # File change patterns (from commit signals if available)
    commit_signals = [s for s in signals if s.signal_type == "commit"]
    commit_frequency = len(commit_signals) / 7.0 if commit_signals else 0.0  # per week
    
    features = {
        "validation_failure_rate": failure_rate,
        "rule_violation_rate": violation_rate,
        "commit_frequency": commit_frequency,
    }
    
    features_list.append(features)
    return features_list
