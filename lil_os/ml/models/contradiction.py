"""
Contradiction Detection Model

Detects semantic contradictions between rules using ML.
"""

from __future__ import annotations

from typing import List
from ..service import ContradictionResult
from ...core.rules import Rule


class ContradictionModel:
    """
    ML model for detecting semantic rule contradictions.
    
    Phase 1 MVP: Uses pattern-based detection with ML-ready architecture.
    Future: Will use semantic embeddings and classification models.
    """
    
    def __init__(self):
        """Initialize contradiction detection model."""
        self.model_loaded = False
        # Phase 1: Simple pattern-based detection
        # Phase 2+: Load trained ML model
    
    def check(
        self,
        rule: Rule,
        existing_rules: List[Rule]
    ) -> ContradictionResult:
        """
        Check for contradictions between a rule and existing rules.
        
        Args:
            rule: The rule to check
            existing_rules: List of existing rules to check against
        
        Returns:
            ContradictionResult with detection results
        """
        conflicting_rules = []
        
        # Phase 1: Pattern-based detection
        # Extract rule subject
        rule_subject = rule.extract_subject()
        
        for existing_rule in existing_rules:
            if existing_rule.rule_id == rule.rule_id:
                continue
            
            existing_subject = existing_rule.extract_subject()
            
            # Simple similarity check (Phase 1)
            # Future: Use semantic embeddings
            if self._subjects_similar(rule_subject, existing_subject):
                # Check for conflicting normative keywords
                if self._keywords_conflict(rule.normative_keyword, existing_rule.normative_keyword):
                    conflicting_rules.append(existing_rule.rule_id)
        
        if conflicting_rules:
            return ContradictionResult(
                has_contradiction=True,
                confidence=0.7,  # Medium confidence for pattern-based
                explanation=f"Potential contradiction detected with {len(conflicting_rules)} rule(s)",
                conflicting_rules=conflicting_rules,
                details={
                    "method": "pattern_based",
                    "rule_subject": rule_subject,
                },
            )
        
        return ContradictionResult(
            has_contradiction=False,
            confidence=0.5,
            explanation="No contradictions detected",
            conflicting_rules=[],
        )
    
    def _subjects_similar(self, subject1: str, subject2: str) -> bool:
        """Check if two rule subjects are similar (improved word overlap with stemming)."""
        words1 = set(subject1.split())
        words2 = set(subject2.split())
        
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                     'could', 'may', 'might', 'must', 'can', 'cannot'}
        words1 = words1 - stop_words
        words2 = words2 - stop_words
        
        if not words1 or not words2:
            return False
        
        # Simple stemming: remove common suffixes
        def stem(word):
            for suffix in ['ing', 'ed', 's', 'es', 'ly']:
                if word.endswith(suffix) and len(word) > len(suffix) + 2:
                    return word[:-len(suffix)]
            return word
        
        words1_stemmed = {stem(w.lower()) for w in words1}
        words2_stemmed = {stem(w.lower()) for w in words2}
        
        # Check for significant word overlap
        overlap = len(words1_stemmed & words2_stemmed)
        total_unique = len(words1_stemmed | words2_stemmed)
        
        if total_unique == 0:
            return False
        
        similarity = overlap / total_unique
        # Improved threshold: require at least 2 matching words or 40% similarity
        return similarity > 0.4 or overlap >= 2
    
    def _keywords_conflict(self, keyword1: str, keyword2: str) -> bool:
        """Check if two normative keywords conflict."""
        must_keywords = {"MUST", "MUST NOT"}
        should_keywords = {"SHOULD", "SHOULD NOT"}
        
        # MUST vs MUST NOT = conflict
        if keyword1 in must_keywords and keyword2 in must_keywords:
            return keyword1 != keyword2
        
        # Same keyword = no conflict
        if keyword1 == keyword2:
            return False
        
        # Different keywords on same subject = potential conflict
        # (This is simplified - full ML model would be more nuanced)
        return True
