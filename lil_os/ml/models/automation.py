"""
Automation Creep Detection Model

Detects when automation expands into human-judgment domains.
"""

from __future__ import annotations

from typing import List
from ..service import CreepResult
from ...core.context_budget import BudgetItem


class AutomationCreepModel:
    """
    ML model for detecting automation creep.
    
    Phase 1 MVP: Uses keyword-based detection with ML-ready architecture.
    Future: Will use semantic classification models.
    """
    
    def __init__(self):
        """Initialize automation creep detection model."""
        self.model_loaded = False
        # Human-judgment domain keywords (expanded)
        self.forbidden_keywords = {
            "judgment", "decision", "evaluate", "assess", "approve", "reject",
            "moral", "ethical", "value", "tradeoff", "irreversible", "harm",
            "audit", "review", "human", "person", "user", "stakeholder",
            "judge", "determine", "choose", "select", "prioritize", "rank",
            "discretion", "authority", "responsibility", "accountability",
            "consent", "permission", "authorization", "sanction",
        }
    
    def check(
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
        description_lower = automation_description.lower()
        
        # Phase 1: Keyword-based detection
        # Check for forbidden domain keywords
        detected_keywords = []
        for keyword in self.forbidden_keywords:
            if keyword in description_lower:
                detected_keywords.append(keyword)
        
        if detected_keywords:
            return CreepResult(
                creep_detected=True,
                confidence=0.7,  # Medium confidence for keyword-based
                explanation=f"Automation may be entering human-judgment domain (keywords: {', '.join(detected_keywords)})",
                affected_domain="human-judgment",
                recommendation="Review automation scope and ensure human oversight for decisions involving these concepts",
                details={
                    "method": "keyword_based",
                    "detected_keywords": detected_keywords,
                },
            )
        
        return CreepResult(
            creep_detected=False,
            confidence=0.5,
            explanation="No automation creep detected",
        )
