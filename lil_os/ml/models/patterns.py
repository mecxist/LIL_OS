"""
Pattern Recognition Model

Detects patterns and anti-patterns in decision logs.
"""

from __future__ import annotations

from typing import List
from datetime import datetime, timedelta
from ..service import PatternResult
from ...core.decisions import DecisionEntry


class PatternRecognitionModel:
    """
    ML model for detecting patterns in decision logs.
    
    Phase 1 MVP: Uses simple pattern detection with ML-ready architecture.
    Future: Will use sequence models and clustering.
    """
    
    def __init__(self):
        """Initialize pattern recognition model."""
        self.model_loaded = False
    
    def detect(self, decision_entries: List[DecisionEntry]) -> PatternResult:
        """
        Detect patterns and anti-patterns in decision logs.
        
        Args:
            decision_entries: List of decision log entries to analyze
        
        Returns:
            PatternResult with detected patterns and recommendations
        """
        if not decision_entries:
            return PatternResult(
                patterns_detected=[],
                anti_patterns=[],
                recommendations=[],
            )
        
        patterns = []
        anti_patterns = []
        recommendations = []
        
        # Pattern 1: Frequent rule overrides
        override_count = sum(1 for e in decision_entries if "override" in e.decision.lower())
        if override_count > len(decision_entries) * 0.2:  # More than 20% are overrides
            anti_patterns.append({
                "type": "frequent_overrides",
                "description": f"High rate of rule overrides ({override_count}/{len(decision_entries)})",
                "severity": "medium",
            })
            recommendations.append("Review rules that are frequently overridden - they may be too restrictive")
        
        # Pattern 2: Rapid decision-making
        if len(decision_entries) >= 2:
            dates = sorted([e.date for e in decision_entries])
            time_span = (dates[-1] - dates[0]).days
            if time_span > 0:
                decisions_per_day = len(decision_entries) / time_span
                if decisions_per_day > 2:  # More than 2 decisions per day
                    patterns.append({
                        "type": "rapid_decision_making",
                        "description": f"High decision frequency: {decisions_per_day:.1f} decisions/day",
                        "severity": "info",
                    })
        
        # Pattern 3: Missing reviews
        entries_needing_review = [e for e in decision_entries if e.review_date and e.review_date < datetime.now() and not e.actual_impact]
        if entries_needing_review:
            anti_patterns.append({
                "type": "missing_reviews",
                "description": f"{len(entries_needing_review)} decision entries overdue for review",
                "severity": "medium",
            })
            recommendations.append("Review overdue decision entries and update actual impact")
        
        # Pattern 4: Rule additions without removals
        rule_additions = sum(1 for e in decision_entries if "add" in e.decision.lower() and "rule" in e.decision.lower())
        rule_removals = sum(1 for e in decision_entries if ("remove" in e.decision.lower() or "delete" in e.decision.lower()) and "rule" in e.decision.lower())
        
        if rule_additions > 0 and rule_removals == 0:
            anti_patterns.append({
                "type": "rule_accumulation",
                "description": f"Rules added ({rule_additions}) but none removed",
                "severity": "low",
            })
            recommendations.append("Consider removing obsolete rules to prevent rule bloat")
        
        return PatternResult(
            patterns_detected=patterns,
            anti_patterns=anti_patterns,
            recommendations=recommendations,
            details={
                "total_entries": len(decision_entries),
                "method": "pattern_based",
            },
        )
