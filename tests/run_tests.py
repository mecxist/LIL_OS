#!/usr/bin/env python3
"""
Test Runner for LIL OS²

Run all tests and generate a test report.
"""

import unittest
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def run_tests():
    """Run all tests."""
    # Discover and run tests
    loader = unittest.TestLoader()
    suite = loader.discover(
        start_dir=str(Path(__file__).parent),
        pattern="test_*.py",
        top_level_dir=str(project_root),
    )
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on test results
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
