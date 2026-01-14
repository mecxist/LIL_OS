"""
LIL OS² Core Module

Core governance functionality for LIL OS² v2.0:
- Rule management with lifecycle tracking
- Enhanced decision logging
- Real-time context budget monitoring
- Validation orchestration
"""

from .rules import RuleManager, Rule, RuleLifecycle
from .decisions import DecisionLogManager, DecisionEntry
from .context_budget import ContextBudgetManager, BudgetStatus
from .validation import ValidationOrchestrator

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
