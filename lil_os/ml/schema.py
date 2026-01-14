#!/usr/bin/env python3
"""
LIL OS² ML Data Schema

Defines data schemas for drift detection features.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from datetime import datetime
from pathlib import Path
import json


@dataclass
class GitFeatures:
    """Features extracted from git history."""
    commits_last_7d: int = 0
    commits_last_30d: int = 0
    governance_files_touched: int = 0
    rule_changes: int = 0
    decision_log_entries: int = 0
    ai_agent_commits_ratio: float = 0.0
    avg_files_per_commit: float = 0.0


@dataclass
class ValidationFeatures:
    """Features extracted from validation reports."""
    validation_runs_last_7d: int = 0
    pass_rate_7d: float = 0.0
    avg_findings_per_run: float = 0.0
    hard_fails_7d: int = 0
    warnings_7d: int = 0
    avg_validation_time_seconds: float = 0.0


@dataclass
class GovernanceFeatures:
    """Features extracted from governance files."""
    rules_added_30d: int = 0
    rules_removed_30d: int = 0
    context_budget_utilization: float = 0.0
    reset_triggers_activated_30d: int = 0


@dataclass
class FeatureSet:
    """Complete feature set for a point in time."""
    timestamp: str
    git_features: GitFeatures
    validation_features: ValidationFeatures
    governance_features: GovernanceFeatures
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "timestamp": self.timestamp,
            "git_features": asdict(self.git_features),
            "validation_features": asdict(self.validation_features),
            "governance_features": asdict(self.governance_features),
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> FeatureSet:
        """Create from dictionary."""
        return cls(
            timestamp=data["timestamp"],
            git_features=GitFeatures(**data["git_features"]),
            validation_features=ValidationFeatures(**data["validation_features"]),
            governance_features=GovernanceFeatures(**data["governance_features"]),
        )
    
    def to_feature_vector(self) -> list[float]:
        """Convert to feature vector for ML models."""
        return [
            # Git features
            float(self.git_features.commits_last_7d),
            float(self.git_features.commits_last_30d),
            float(self.git_features.governance_files_touched),
            float(self.git_features.rule_changes),
            float(self.git_features.decision_log_entries),
            float(self.git_features.ai_agent_commits_ratio),
            float(self.git_features.avg_files_per_commit),
            # Validation features
            float(self.validation_features.validation_runs_last_7d),
            float(self.validation_features.pass_rate_7d),
            float(self.validation_features.avg_findings_per_run),
            float(self.validation_features.hard_fails_7d),
            float(self.validation_features.warnings_7d),
            float(self.validation_features.avg_validation_time_seconds),
            # Governance features
            float(self.governance_features.rules_added_30d),
            float(self.governance_features.rules_removed_30d),
            float(self.governance_features.context_budget_utilization),
            float(self.governance_features.reset_triggers_activated_30d),
        ]
    
    @classmethod
    def get_feature_names(cls) -> list[str]:
        """Get list of feature names in order."""
        return [
            "commits_last_7d",
            "commits_last_30d",
            "governance_files_touched",
            "rule_changes",
            "decision_log_entries",
            "ai_agent_commits_ratio",
            "avg_files_per_commit",
            "validation_runs_last_7d",
            "pass_rate_7d",
            "avg_findings_per_run",
            "hard_fails_7d",
            "warnings_7d",
            "avg_validation_time_seconds",
            "rules_added_30d",
            "rules_removed_30d",
            "context_budget_utilization",
            "reset_triggers_activated_30d",
        ]


def save_feature_set(feature_set: FeatureSet, output_path: Path) -> None:
    """Save feature set to JSON file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(feature_set.to_dict(), indent=2),
        encoding="utf-8"
    )


def load_feature_set(input_path: Path) -> FeatureSet:
    """Load feature set from JSON file."""
    data = json.loads(input_path.read_text(encoding="utf-8"))
    return FeatureSet.from_dict(data)
