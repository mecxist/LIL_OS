"""
LIL OS² - A constitutional substrate for AI-assisted software development

LIL OS² governs change (evolution over time) in AI-assisted systems by managing
three critical dimensions: intent (what your project is meant to do), authority
(who can make what decisions), and context (the rules, instructions, and automation
that guide behavior).
"""

__version__ = "2.0.0"

# Backwards compatibility: Export core modules
try:
    from .core import (
        RuleManager,
        Rule,
        RuleLifecycle,
        DecisionLogManager,
        DecisionEntry,
        ContextBudgetManager,
        BudgetStatus,
        ValidationOrchestrator,
    )
    __all__ = [
        "RuleManager",
        "Rule",
        "RuleLifecycle",
        "DecisionLogManager",
        "DecisionEntry",
        "ContextBudgetManager",
        "BudgetStatus",
        "ValidationOrchestrator",
    ]
except ImportError:
    # Fallback for v0.1.1 compatibility
    __all__ = []

