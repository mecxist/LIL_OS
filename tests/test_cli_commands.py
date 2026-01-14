"""
CLI Command Tests

Tests for CLI command functionality.
"""

import unittest
import sys
from pathlib import Path
import tempfile
import shutil

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestCLICommands(unittest.TestCase):
    """Test CLI commands."""
    
    def setUp(self):
        """Set up test environment."""
        self.test_dir = Path(tempfile.mkdtemp())
        # Create minimal project structure
        (self.test_dir / "docs").mkdir()
        (self.test_dir / ".cursorrules").touch()
    
    def tearDown(self):
        """Clean up test environment."""
        shutil.rmtree(self.test_dir)
    
    def test_rules_command_imports(self):
        """Test that rules command can be imported."""
        try:
            from lil_os.cli import rules_command
            self.assertTrue(callable(rules_command))
        except ImportError as e:
            self.fail(f"Failed to import rules_command: {e}")
    
    def test_decisions_command_imports(self):
        """Test that decisions command can be imported."""
        try:
            from lil_os.cli import decisions_command
            self.assertTrue(callable(decisions_command))
        except ImportError as e:
            self.fail(f"Failed to import decisions_command: {e}")
    
    def test_budget_command_imports(self):
        """Test that budget command can be imported."""
        try:
            from lil_os.cli import budget_command
            self.assertTrue(callable(budget_command))
        except ImportError as e:
            self.fail(f"Failed to import budget_command: {e}")
    
    def test_ml_command_imports(self):
        """Test that ML command can be imported."""
        try:
            from lil_os.cli import ml_command
            self.assertTrue(callable(ml_command))
        except ImportError as e:
            self.fail(f"Failed to import ml_command: {e}")


if __name__ == "__main__":
    unittest.main()
