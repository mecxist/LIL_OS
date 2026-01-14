#!/usr/bin/env python3
"""
Change Risk Feature Extraction

Extracts features from git commits and validation reports for change risk prediction.
"""

from __future__ import annotations

from typing import Dict, Any, List
from pathlib import Path

from ...signals.collector import Signal


def extract_features(signal: Signal) -> Dict[str, Any]:
    """
    Extract features from a signal for change risk prediction.
    
    Args:
        signal: Signal object (should be a commit signal)
        
    Returns:
        Dictionary of features
    """
    if signal.signal_type != "commit":
        return {}
    
    data = signal.data
    stats = data.get("stats", {})
    changed_files = data.get("changed_files", [])
    
    # Basic features
    features = {
        "diff_size": stats.get("total_lines", 0),
        "files_changed": stats.get("files_changed", 0),
        "additions": stats.get("additions", 0),
        "deletions": stats.get("deletions", 0),
    }
    
    # Check if touches governance files
    governance_patterns = ["docs/", ".cursorrules", "GOVERNANCE", "MASTER_RULES"]
    touches_governance = any(
        any(pattern in f for pattern in governance_patterns)
        for f in changed_files
    )
    features["touches_governance"] = 1 if touches_governance else 0
    
    # Change type detection (simple heuristic)
    message = data.get("message", "").lower()
    if any(word in message for word in ["fix", "bug", "patch"]):
        change_type = "fix"
    elif any(word in message for word in ["refactor", "cleanup", "restructure"]):
        change_type = "refactor"
    elif any(word in message for word in ["doc", "readme", "comment"]):
        change_type = "docs"
    else:
        change_type = "feature"
    
    type_map = {"feature": 0, "fix": 1, "refactor": 2, "docs": 3}
    features["change_type"] = type_map.get(change_type, 0)
    
    # File type distribution
    file_extensions = {}
    for f in changed_files:
        ext = Path(f).suffix or "no_ext"
        file_extensions[ext] = file_extensions.get(ext, 0) + 1
    
    features["py_files"] = file_extensions.get(".py", 0)
    features["yaml_files"] = file_extensions.get(".yaml", 0) + file_extensions.get(".yml", 0)
    features["md_files"] = file_extensions.get(".md", 0)
    
    return features


def extract_features_batch(signals: List[Signal]) -> List[Dict[str, Any]]:
    """
    Extract features from multiple signals.
    
    Args:
        signals: List of Signal objects
        
    Returns:
        List of feature dictionaries
    """
    return [extract_features(s) for s in signals if s.signal_type == "commit"]
