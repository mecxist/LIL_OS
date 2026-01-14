"""
LIL OS² Core: Validation Orchestration

Orchestrates validation checks and integrates with ML module.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Callable, Any

from .rules import RuleManager, RuleLifecycle
from .decisions import DecisionLogManager
from .context_budget import ContextBudgetManager

# Optional ML module import
try:
    from ..ml.service import MLService
    ML_AVAILABLE = True
except ImportError:
    ML_AVAILABLE = False
    MLService = None


@dataclass
class ValidationResult:
    """Result of a validation check."""
    check_name: str
    passed: bool
    message: str
    details: Optional[Dict[str, Any]] = None
    severity: str = "info"  # info, warning, error


class ValidationOrchestrator:
    """
    Orchestrates validation checks across LIL OS² components.
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize validation orchestrator.
        
        Args:
            project_root: Root directory of the project (defaults to current directory)
        """
        self.project_root = project_root or Path.cwd()
        self.rule_manager = RuleManager(project_root)
        self.decision_manager = DecisionLogManager(project_root)
        self.budget_manager = ContextBudgetManager(project_root)
        self._ml_service: Optional[MLService] = None
        
        # Auto-initialize ML service if available
        if ML_AVAILABLE and MLService:
            try:
                self._ml_service = MLService(enabled=True)
            except Exception:
                # ML module not fully configured, continue without it
                pass
    
    def set_ml_service(self, ml_service: MLService) -> None:
        """Set the ML service for enhanced validation."""
        self._ml_service = ml_service
    
    def run_all_checks(self) -> List[ValidationResult]:
        """
        Run all validation checks.
        
        Returns:
            List of validation results
        """
        results = []
        
        # Rule validation
        results.extend(self.validate_rules())
        
        # Decision log validation
        results.extend(self.validate_decision_log())
        
        # Context budget validation
        results.extend(self.validate_context_budgets())
        
        # ML-enhanced checks (if available)
        if self._ml_service:
            results.extend(self.run_ml_checks())
        
        return results
    
    def validate_rules(self) -> List[ValidationResult]:
        """Validate rules."""
        results = []
        
        # Check for contradictions
        contradictions = self.rule_manager.find_contradictions()
        if contradictions:
            for contradiction in contradictions:
                results.append(ValidationResult(
                    check_name="rule_contradiction",
                    passed=False,
                    message=f"Potential contradiction: {contradiction['rule1']} vs {contradiction['rule2']}",
                    details=contradiction,
                    severity="warning",
                ))
        else:
            results.append(ValidationResult(
                check_name="rule_contradiction",
                passed=True,
                message="No rule contradictions found",
            ))
        
        # Check for deprecated rules
        deprecated = self.rule_manager.get_rules_by_lifecycle(RuleLifecycle.DEPRECATED)
        all_rules = self.rule_manager.get_all_rules()
        if not all_rules:
            results.append(ValidationResult(
                check_name="rules_exist",
                passed=False,
                message="No rules found in governance files",
                severity="warning",
            ))
        else:
            results.append(ValidationResult(
                check_name="rules_exist",
                passed=True,
                message=f"Found {len(all_rules)} rules",
                details={"count": len(all_rules)},
            ))
        
        return results
    
    def validate_decision_log(self) -> List[ValidationResult]:
        """Validate decision log."""
        results = []
        
        entries = self.decision_manager.get_all_entries()
        if not entries:
            results.append(ValidationResult(
                check_name="decision_log_exists",
                passed=True,
                message="Decision log exists (empty)",
            ))
        else:
            results.append(ValidationResult(
                check_name="decision_log_exists",
                passed=True,
                message=f"Decision log has {len(entries)} entries",
                details={"count": len(entries)},
            ))
            
            # Check for entries needing review
            needing_review = self.decision_manager.get_entries_needing_review()
            if needing_review:
                results.append(ValidationResult(
                    check_name="decision_reviews",
                    passed=False,
                    message=f"{len(needing_review)} decision entries need review",
                    details={"count": len(needing_review)},
                    severity="warning",
                ))
            else:
                results.append(ValidationResult(
                    check_name="decision_reviews",
                    passed=True,
                    message="All decision entries are up to date",
                ))
        
        return results
    
    def validate_context_budgets(self) -> List[ValidationResult]:
        """Validate context budgets."""
        results = []
        
        alerts = self.budget_manager.check_alerts()
        
        if not alerts:
            results.append(ValidationResult(
                check_name="context_budgets",
                passed=True,
                message="All context budgets are healthy",
            ))
        else:
            for alert in alerts:
                results.append(ValidationResult(
                    check_name=f"context_budget_{alert['type']}",
                    passed=alert["severity"] not in ["critical", "high"],
                    message=alert["message"],
                    details=alert,
                    severity=alert["severity"],
                ))
        
        return results
    
    def run_ml_checks(self) -> List[ValidationResult]:
        """Run ML-enhanced validation checks."""
        results = []
        
        if not self._ml_service:
            return results
        
        # ML contradiction detection
        try:
            all_rules = self.rule_manager.get_all_rules()
            for rule in all_rules:
                other_rules = [r for r in all_rules if r.rule_id != rule.rule_id]
                contradiction = self._ml_service.check_contradiction(rule, other_rules)
                
                if contradiction.has_contradiction:
                    results.append(ValidationResult(
                        check_name="ml_contradiction",
                        passed=False,
                        message=f"ML-detected contradiction: {contradiction.explanation}",
                        details={
                            "rule_id": rule.rule_id,
                            "confidence": contradiction.confidence,
                            "conflicting_rules": contradiction.conflicting_rules,
                        },
                        severity="warning",
                    ))
        except Exception as e:
            results.append(ValidationResult(
                check_name="ml_contradiction",
                passed=False,
                message=f"ML contradiction check failed: {str(e)}",
                severity="error",
            ))
        
        # ML pattern detection
        try:
            decision_entries = self.decision_manager.get_all_entries()
            patterns = self._ml_service.detect_patterns(decision_entries)
            
            if patterns.anti_patterns:
                for anti_pattern in patterns.anti_patterns:
                    results.append(ValidationResult(
                        check_name="ml_anti_pattern",
                        passed=False,
                        message=f"Anti-pattern detected: {anti_pattern.get('description', 'Unknown')}",
                        details=anti_pattern,
                        severity=anti_pattern.get('severity', 'warning'),
                    ))
        except Exception as e:
            results.append(ValidationResult(
                check_name="ml_patterns",
                passed=False,
                message=f"ML pattern detection failed: {str(e)}",
                severity="error",
            ))
        
        return results
    
    def get_validation_summary(self) -> Dict[str, Any]:
        """
        Get a summary of validation results.
        
        Returns:
            Dictionary with summary including:
            - total_checks: Total number of checks
            - passed: Number of passed checks
            - failed: Number of failed checks
            - warnings: Number of warnings
            - errors: Number of errors
        """
        results = self.run_all_checks()
        
        summary = {
            "total_checks": len(results),
            "passed": sum(1 for r in results if r.passed),
            "failed": sum(1 for r in results if not r.passed),
            "warnings": sum(1 for r in results if r.severity == "warning"),
            "errors": sum(1 for r in results if r.severity == "error"),
            "results": [
                {
                    "check": r.check_name,
                    "passed": r.passed,
                    "message": r.message,
                    "severity": r.severity,
                }
                for r in results
            ],
        }
        
        return summary
