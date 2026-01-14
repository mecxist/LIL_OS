"""
LIL OS² Core: Context Budget Management

Real-time context budget monitoring with alerts and visualization.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set


class BudgetType(Enum):
    """Types of context budgets."""
    INSTRUCTION = "instruction"
    AUTOMATION = "automation"
    MEMORY = "memory"
    RULE = "rule"


class BudgetStatus(Enum):
    """Budget status levels."""
    HEALTHY = "healthy"
    WARNING = "warning"
    CRITICAL = "critical"
    EXCEEDED = "exceeded"


@dataclass
class BudgetItem:
    """Represents a single budget item."""
    item_type: BudgetType
    description: str
    file_path: Optional[Path] = None
    line_number: Optional[int] = None
    added_date: Optional[datetime] = None
    review_date: Optional[datetime] = None
    justification: Optional[str] = None
    cost: int = 1  # Relative cost of this item


@dataclass
class BudgetMetrics:
    """Metrics for a budget type."""
    total_items: int = 0
    total_cost: int = 0
    items_without_review: int = 0
    items_overdue_review: int = 0
    recent_additions: int = 0  # Items added in last 30 days
    status: BudgetStatus = BudgetStatus.HEALTHY


class ContextBudgetManager:
    """
    Manages context budgets with real-time monitoring, alerts, and visualization.
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize context budget manager.
        
        Args:
            project_root: Root directory of the project (defaults to current directory)
        """
        self.project_root = project_root or Path.cwd()
        self.context_budget_path = self.project_root / "docs" / "CONTEXT_BUDGET.md"
        self._budgets: Dict[BudgetType, List[BudgetItem]] = {
            BudgetType.INSTRUCTION: [],
            BudgetType.AUTOMATION: [],
            BudgetType.MEMORY: [],
            BudgetType.RULE: [],
        }
        self._thresholds: Dict[BudgetType, Dict[str, int]] = {
            BudgetType.INSTRUCTION: {"warning": 50, "critical": 75, "max": 100},
            BudgetType.AUTOMATION: {"warning": 20, "critical": 30, "max": 40},
            BudgetType.MEMORY: {"warning": 30, "critical": 45, "max": 60},
            BudgetType.RULE: {"warning": 100, "critical": 150, "max": 200},
        }
        self._load_budgets()
    
    def _load_budgets(self) -> None:
        """Load context budgets from files."""
        # Clear existing budgets
        for budget_type in BudgetType:
            self._budgets[budget_type].clear()
        
        # Load from context budget file
        if self.context_budget_path.exists():
            self._parse_context_budget_file()
        
        # Load rules as rule budget items
        self._load_rule_budget()
        
        # Load automation items
        self._load_automation_budget()
    
    def _parse_context_budget_file(self) -> None:
        """Parse the CONTEXT_BUDGET.md file."""
        # This is a simplified parser - in production, would parse the full structure
        text = self.context_budget_path.read_text(encoding="utf-8")
        
        # For now, we'll track items based on file analysis
        # Full implementation would parse structured budget entries
    
    def _load_rule_budget(self) -> None:
        """Load rules as rule budget items."""
        from .rules import RuleManager
        
        rule_manager = RuleManager(self.project_root)
        rules = rule_manager.get_all_rules()
        
        for rule in rules:
            item = BudgetItem(
                item_type=BudgetType.RULE,
                description=rule.text[:100],  # First 100 chars
                file_path=rule.file_path,
                line_number=rule.line_number,
                added_date=rule.created_at,
                cost=1,
            )
            self._budgets[BudgetType.RULE].append(item)
    
    def _load_automation_budget(self) -> None:
        """Load automation items from context budget and automation files."""
        # Check for automation in context budget
        if self.context_budget_path.exists():
            text = self.context_budget_path.read_text(encoding="utf-8")
            
            # Look for automation sections
            # This is simplified - full implementation would parse structured entries
            if "automation" in text.lower():
                # Count automation-related content
                # In production, would parse actual automation definitions
                pass
    
    def get_budget_metrics(self, budget_type: BudgetType) -> BudgetMetrics:
        """Get metrics for a specific budget type."""
        items = self._budgets[budget_type]
        total_items = len(items)
        total_cost = sum(item.cost for item in items)
        
        now = datetime.now()
        items_without_review = sum(
            1 for item in items if not item.review_date
        )
        items_overdue_review = sum(
            1
            for item in items
            if item.review_date and item.review_date < now
        )
        
        # Items added in last 30 days
        thirty_days_ago = datetime.fromtimestamp(now.timestamp() - 30 * 24 * 60 * 60)
        recent_additions = sum(
            1
            for item in items
            if item.added_date and item.added_date >= thirty_days_ago
        )
        
        # Determine status
        thresholds = self._thresholds[budget_type]
        if total_cost >= thresholds["max"]:
            status = BudgetStatus.EXCEEDED
        elif total_cost >= thresholds["critical"]:
            status = BudgetStatus.CRITICAL
        elif total_cost >= thresholds["warning"]:
            status = BudgetStatus.WARNING
        else:
            status = BudgetStatus.HEALTHY
        
        return BudgetMetrics(
            total_items=total_items,
            total_cost=total_cost,
            items_without_review=items_without_review,
            items_overdue_review=items_overdue_review,
            recent_additions=recent_additions,
            status=status,
        )
    
    def get_all_metrics(self) -> Dict[BudgetType, BudgetMetrics]:
        """Get metrics for all budget types."""
        return {
            budget_type: self.get_budget_metrics(budget_type)
            for budget_type in BudgetType
        }
    
    def check_alerts(self) -> List[Dict[str, any]]:
        """
        Check for budget alerts.
        
        Returns:
            List of alert dictionaries with type, severity, message, and recommendations
        """
        alerts = []
        
        for budget_type, metrics in self.get_all_metrics().items():
            if metrics.status == BudgetStatus.EXCEEDED:
                alerts.append({
                    "type": "budget_exceeded",
                    "budget_type": budget_type.value,
                    "severity": "critical",
                    "message": f"{budget_type.value.capitalize()} budget exceeded: {metrics.total_cost} items",
                    "recommendation": f"Review and remove unnecessary {budget_type.value} items immediately",
                    "current_value": metrics.total_cost,
                    "max_value": self._thresholds[budget_type]["max"],
                })
            elif metrics.status == BudgetStatus.CRITICAL:
                alerts.append({
                    "type": "budget_critical",
                    "budget_type": budget_type.value,
                    "severity": "high",
                    "message": f"{budget_type.value.capitalize()} budget critical: {metrics.total_cost} items",
                    "recommendation": f"Review {budget_type.value} items and plan removals",
                    "current_value": metrics.total_cost,
                    "threshold": self._thresholds[budget_type]["critical"],
                })
            elif metrics.status == BudgetStatus.WARNING:
                alerts.append({
                    "type": "budget_warning",
                    "budget_type": budget_type.value,
                    "severity": "medium",
                    "message": f"{budget_type.value.capitalize()} budget warning: {metrics.total_cost} items",
                    "recommendation": f"Monitor {budget_type.value} growth and plan reviews",
                    "current_value": metrics.total_cost,
                    "threshold": self._thresholds[budget_type]["warning"],
                })
            
            # Check for items needing review
            if metrics.items_overdue_review > 0:
                alerts.append({
                    "type": "review_overdue",
                    "budget_type": budget_type.value,
                    "severity": "medium",
                    "message": f"{metrics.items_overdue_review} {budget_type.value} items overdue for review",
                    "recommendation": "Review and update or remove overdue items",
                    "count": metrics.items_overdue_review,
                })
            
            # Check for rapid growth
            if metrics.recent_additions > 10:
                alerts.append({
                    "type": "rapid_growth",
                    "budget_type": budget_type.value,
                    "severity": "medium",
                    "message": f"{metrics.recent_additions} {budget_type.value} items added in last 30 days",
                    "recommendation": "Review recent additions and ensure they're justified",
                    "count": metrics.recent_additions,
                })
        
        return alerts
    
    def get_visualization_data(self) -> Dict[str, any]:
        """
        Get data for budget visualization.
        
        Returns:
            Dictionary with visualization data including:
            - budgets: Budget data for each type
            - trends: Growth trends
            - recommendations: Actionable recommendations
        """
        metrics = self.get_all_metrics()
        
        visualization = {
            "budgets": {},
            "trends": {},
            "recommendations": [],
        }
        
        for budget_type, metric in metrics.items():
            thresholds = self._thresholds[budget_type]
            visualization["budgets"][budget_type.value] = {
                "current": metric.total_cost,
                "warning": thresholds["warning"],
                "critical": thresholds["critical"],
                "max": thresholds["max"],
                "status": metric.status.value,
                "items": metric.total_items,
                "needs_review": metric.items_without_review,
                "overdue": metric.items_overdue_review,
                "recent_growth": metric.recent_additions,
            }
            
            # Calculate percentage
            percentage = (metric.total_cost / thresholds["max"]) * 100
            visualization["budgets"][budget_type.value]["percentage"] = min(percentage, 100)
        
        # Generate recommendations
        alerts = self.check_alerts()
        for alert in alerts:
            if alert["severity"] in ["critical", "high"]:
                visualization["recommendations"].append({
                    "priority": "high",
                    "action": alert["recommendation"],
                    "budget_type": alert["budget_type"],
                })
        
        return visualization
    
    def add_budget_item(
        self,
        budget_type: BudgetType,
        description: str,
        file_path: Optional[Path] = None,
        justification: Optional[str] = None,
        cost: int = 1,
        review_date: Optional[datetime] = None,
    ) -> BudgetItem:
        """
        Add a new budget item.
        
        Args:
            budget_type: Type of budget item
            description: Description of the item
            file_path: Optional file path where item is defined
            justification: Optional justification for the item
            cost: Cost of the item (default 1)
            review_date: Optional review date
        
        Returns:
            The created BudgetItem
        """
        item = BudgetItem(
            item_type=budget_type,
            description=description,
            file_path=file_path,
            added_date=datetime.now(),
            justification=justification,
            cost=cost,
            review_date=review_date,
        )
        
        self._budgets[budget_type].append(item)
        return item
    
    def remove_budget_item(self, budget_type: BudgetType, description: str) -> bool:
        """
        Remove a budget item.
        
        Args:
            budget_type: Type of budget item
            description: Description to match
        
        Returns:
            True if item was found and removed, False otherwise
        """
        items = self._budgets[budget_type]
        for i, item in enumerate(items):
            if item.description == description:
                items.pop(i)
                return True
        return False
    
    def refresh(self) -> None:
        """Reload budgets from files (useful after file changes)."""
        self._load_budgets()
