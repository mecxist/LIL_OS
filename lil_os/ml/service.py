"""
LIL OS² ML Service Interface

Main interface for ML module services.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from ..core.rules import Rule
from ..core.decisions import DecisionEntry
from ..core.context_budget import BudgetItem


@dataclass
class ContradictionResult:
    """Result of contradiction detection."""
    has_contradiction: bool
    confidence: float
    explanation: str
    conflicting_rules: List[str]
    details: Optional[Dict[str, Any]] = None


@dataclass
class CreepResult:
    """Result of automation creep detection."""
    creep_detected: bool
    confidence: float
    explanation: str
    affected_domain: Optional[str] = None
    recommendation: Optional[str] = None
    details: Optional[Dict[str, Any]] = None


@dataclass
class PatternResult:
    """Result of pattern recognition."""
    patterns_detected: List[Dict[str, Any]]
    anti_patterns: List[Dict[str, Any]]
    recommendations: List[str]
    details: Optional[Dict[str, Any]] = None


class MLService:
    """
    Main ML service interface for LIL OS².
    
    Provides ML-powered analysis for:
    - Semantic rule contradiction detection
    - Automation creep detection
    - Pattern recognition in decision logs
    """
    
    def __init__(self, enabled: bool = True):
        """
        Initialize ML service.
        
        Args:
            enabled: Whether ML features are enabled (default: True)
        """
        self.enabled = enabled
        self._contradiction_model = None
        self._automation_model = None
        self._pattern_model = None
        
        if enabled:
            self._initialize_models()
    
    def _initialize_models(self) -> None:
        """Initialize ML models."""
        from .models.contradiction import ContradictionModel
        from .models.automation import AutomationCreepModel
        from .models.patterns import PatternRecognitionModel
        
        self._contradiction_model = ContradictionModel()
        self._automation_model = AutomationCreepModel()
        self._pattern_model = PatternRecognitionModel()
    
    def check_contradiction(
        self,
        rule: Rule,
        existing_rules: List[Rule]
    ) -> ContradictionResult:
        """
        Check for semantic contradictions between a rule and existing rules.
        
        Args:
            rule: The rule to check
            existing_rules: List of existing rules to check against
        
        Returns:
            ContradictionResult with detection results
        """
        if not self.enabled or not self._contradiction_model:
            return ContradictionResult(
                has_contradiction=False,
                confidence=0.0,
                explanation="ML module not enabled",
                conflicting_rules=[],
            )
        
        try:
            result = self._contradiction_model.check(rule, existing_rules)
            # Log decision
            try:
                from .monitoring.logging import get_ml_logger
                logger = get_ml_logger()
                logger.log_decision(
                    model_name="contradiction",
                    input_data={"rule_id": rule.rule_id, "existing_count": len(existing_rules)},
                    prediction=result.has_contradiction,
                    confidence=result.confidence,
                    explanation=result.explanation,
                )
            except Exception:
                pass  # Don't fail if logging fails
            return result
        except Exception as e:
            # Return safe default on error
            return ContradictionResult(
                has_contradiction=False,
                confidence=0.0,
                explanation=f"Error during contradiction check: {str(e)}",
                conflicting_rules=[],
            )
    
    def check_automation_creep(
        self,
        automation_description: str,
        context_budget_items: List[BudgetItem]
    ) -> CreepResult:
        """
        Check for automation creep into human-judgment domains.
        
        Args:
            automation_description: Description of the automation
            context_budget_items: Current context budget items
        
        Returns:
            CreepResult with detection results
        """
        if not self.enabled or not self._automation_model:
            return CreepResult(
                creep_detected=False,
                confidence=0.0,
                explanation="ML module not enabled",
            )
        
        try:
            result = self._automation_model.check(automation_description, context_budget_items)
            # Log decision
            try:
                from .monitoring.logging import get_ml_logger
                logger = get_ml_logger()
                logger.log_decision(
                    model_name="automation_creep",
                    input_data={"description_length": len(automation_description)},
                    prediction=result.creep_detected,
                    confidence=result.confidence,
                    explanation=result.explanation,
                )
            except Exception:
                pass
            return result
        except Exception as e:
            return CreepResult(
                creep_detected=False,
                confidence=0.0,
                explanation=f"Error during creep check: {str(e)}",
            )
    
    def detect_patterns(
        self,
        decision_entries: List[DecisionEntry]
    ) -> PatternResult:
        """
        Detect patterns and anti-patterns in decision logs.
        
        Args:
            decision_entries: List of decision log entries to analyze
        
        Returns:
            PatternResult with detected patterns and recommendations
        """
        if not self.enabled or not self._pattern_model:
            return PatternResult(
                patterns_detected=[],
                anti_patterns=[],
                recommendations=[],
            )
        
        try:
            result = self._pattern_model.detect(decision_entries)
            # Log decision
            try:
                from .monitoring.logging import get_ml_logger
                logger = get_ml_logger()
                logger.log_decision(
                    model_name="pattern_recognition",
                    input_data={"entry_count": len(decision_entries)},
                    prediction=len(result.anti_patterns) > 0,
                    confidence=0.7 if result.anti_patterns else 0.5,
                    explanation=f"Detected {len(result.patterns_detected)} patterns and {len(result.anti_patterns)} anti-patterns",
                )
            except Exception:
                pass
            return result
        except Exception as e:
            return PatternResult(
                patterns_detected=[],
                anti_patterns=[],
                recommendations=[f"Error during pattern detection: {str(e)}"],
            )
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get ML service status.
        
        Returns:
            Dictionary with service status information
        """
        return {
            "enabled": self.enabled,
            "models_loaded": {
                "contradiction": self._contradiction_model is not None,
                "automation": self._automation_model is not None,
                "patterns": self._pattern_model is not None,
            },
        }
