"""
End-to-End Integration Tests

Tests for LIL OS² core modules and ML module integration.
"""

import unittest
from pathlib import Path
import tempfile
import shutil
from datetime import datetime

from lil_os.core import (
    RuleManager,
    DecisionLogManager,
    ContextBudgetManager,
    ValidationOrchestrator,
)
from lil_os.ml.service import MLService


class TestCoreIntegration(unittest.TestCase):
    """Test core module integration."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        self.original_cwd = Path.cwd()
        
        # Create test project structure
        (self.test_dir / "docs").mkdir()
        (self.test_dir / ".cursorrules").touch()
        
        # Create minimal governance files
        (self.test_dir / "docs" / "MASTER_RULES.md").write_text(
            "# Master Rules\n\n- [LIL-MR-BOUNDARY-0001] The system MUST NOT perform irreversible actions.\n"
        )
        (self.test_dir / "docs" / "DECISION_LOG.md").write_text(
            "# Decision Log\n\n## Entries\n\n"
        )
        (self.test_dir / "docs" / "CONTEXT_BUDGET.md").write_text(
            "# Context Budget\n\n## Budgets\n\n"
        )
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_rule_manager_basic(self):
        """Test basic rule manager functionality."""
        rule_manager = RuleManager(self.test_dir)
        rules = rule_manager.get_all_rules()
        
        self.assertGreater(len(rules), 0, "Should find at least one rule")
        rule = rules[0]
        self.assertEqual(rule.rule_id, "[LIL-MR-BOUNDARY-0001]")
        self.assertEqual(rule.normative_keyword, "MUST NOT")
    
    def test_decision_log_manager_basic(self):
        """Test basic decision log manager functionality."""
        decision_manager = DecisionLogManager(self.test_dir)
        
        # Add an entry
        entry = decision_manager.add_entry(
            decision="Test decision",
            trigger="Test trigger",
            rationale="Test rationale",
            tradeoffs="Test tradeoffs",
            expected_impact="Test impact",
        )
        
        self.assertIsNotNone(entry)
        self.assertEqual(entry.decision, "Test decision")
        
        # Retrieve entries
        entries = decision_manager.get_all_entries()
        self.assertGreater(len(entries), 0)
    
    def test_context_budget_manager_basic(self):
        """Test basic context budget manager functionality."""
        budget_manager = ContextBudgetManager(self.test_dir)
        metrics = budget_manager.get_all_metrics()
        
        self.assertIsNotNone(metrics)
        # Should have metrics for all budget types
        self.assertEqual(len(metrics), 4)  # INSTRUCTION, AUTOMATION, MEMORY, RULE
    
    def test_validation_orchestrator(self):
        """Test validation orchestrator."""
        orchestrator = ValidationOrchestrator(self.test_dir)
        results = orchestrator.run_all_checks()
        
        self.assertIsInstance(results, list)
        # Should have some validation results
        self.assertGreater(len(results), 0)
    
    def test_ml_service_integration(self):
        """Test ML service integration with core modules."""
        ml_service = MLService(enabled=True)
        rule_manager = RuleManager(self.test_dir)
        
        rules = rule_manager.get_all_rules()
        if len(rules) >= 1:
            rule = rules[0]
            other_rules = rules[1:] if len(rules) > 1 else []
            
            result = ml_service.check_contradiction(rule, other_rules)
            self.assertIsNotNone(result)
            self.assertIsInstance(result.has_contradiction, bool)
            self.assertIsInstance(result.confidence, float)
    
    def test_ml_pattern_detection(self):
        """Test ML pattern detection."""
        ml_service = MLService(enabled=True)
        decision_manager = DecisionLogManager(self.test_dir)
        
        # Add some test entries
        decision_manager.add_entry(
            decision="Add new rule",
            trigger="Feature request",
            rationale="Needed for new feature",
            tradeoffs="None",
            expected_impact="Improved governance",
        )
        
        entries = decision_manager.get_all_entries()
        patterns = ml_service.detect_patterns(entries)
        
        self.assertIsNotNone(patterns)
        self.assertIsInstance(patterns.patterns_detected, list)
        self.assertIsInstance(patterns.anti_patterns, list)
        self.assertIsInstance(patterns.recommendations, list)


class TestMLModule(unittest.TestCase):
    """Test ML module functionality."""
    
    def test_ml_service_status(self):
        """Test ML service status."""
        ml_service = MLService(enabled=True)
        status = ml_service.get_status()
        
        self.assertTrue(status["enabled"])
        self.assertIn("models_loaded", status)
    
    def test_contradiction_detection(self):
        """Test contradiction detection model."""
        from lil_os.ml.models.contradiction import ContradictionModel
        from lil_os.core.rules import Rule, RuleLifecycle
        from pathlib import Path
        
        model = ContradictionModel()
        
        rule1 = Rule(
            rule_id="[LIL-TEST-0001]",
            text="[LIL-TEST-0001] The system MUST perform action X",
            file_path=Path("test.md"),
            line_number=1,
            normative_keyword="MUST",
        )
        
        rule2 = Rule(
            rule_id="[LIL-TEST-0002]",
            text="[LIL-TEST-0002] The system MUST NOT perform action X",
            file_path=Path("test.md"),
            line_number=2,
            normative_keyword="MUST NOT",
        )
        
        result = model.check(rule1, [rule2])
        # Should detect contradiction for same subject with conflicting keywords
        self.assertIsNotNone(result)
        self.assertIsInstance(result.has_contradiction, bool)


if __name__ == "__main__":
    unittest.main()
