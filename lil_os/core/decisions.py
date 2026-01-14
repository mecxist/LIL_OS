"""
LIL OS² Core: Decision Logging

Enhanced decision logging with viewer, search, filtering, and impact tracking.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set


@dataclass
class DecisionEntry:
    """Represents a decision log entry."""
    date: datetime
    decision: str
    trigger: str
    rationale: str
    tradeoffs: str
    expected_impact: str
    review_date: Optional[datetime] = None
    entry_number: Optional[int] = None
    related_rules: Set[str] = field(default_factory=set)  # Rule IDs mentioned
    tags: Set[str] = field(default_factory=set)  # Custom tags
    actual_impact: Optional[str] = None  # Filled in after review
    
    def to_markdown(self) -> str:
        """Convert decision entry to markdown format."""
        lines = [
            f"### {self.date.strftime('%Y-%m-%d')}: {self.decision[:50]}...",
            "",
            f"Date: {self.date.strftime('%Y-%m-%d')}",
            f"Decision: {self.decision}",
            f"Trigger: {self.trigger}",
            f"Rationale: {self.rationale}",
            f"Tradeoffs: {self.tradeoffs}",
            f"Expected Impact: {self.expected_impact}",
        ]
        
        if self.review_date:
            lines.append(f"Review Date: {self.review_date.strftime('%Y-%m-%d')}")
        else:
            lines.append("Review Date: N/A")
        
        if self.actual_impact:
            lines.append(f"Actual Impact: {self.actual_impact}")
        
        if self.related_rules:
            lines.append(f"Related Rules: {', '.join(sorted(self.related_rules))}")
        
        if self.tags:
            lines.append(f"Tags: {', '.join(sorted(self.tags))}")
        
        lines.append("")
        return "\n".join(lines)


class DecisionLogManager:
    """
    Manages decision log entries with search, filtering, and impact tracking.
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize decision log manager.
        
        Args:
            project_root: Root directory of the project (defaults to current directory)
        """
        self.project_root = project_root or Path.cwd()
        self.decision_log_path = self.project_root / "docs" / "DECISION_LOG.md"
        self._entries: List[DecisionEntry] = []
        self._load_entries()
    
    def _load_entries(self) -> None:
        """Load all decision log entries from the file."""
        self._entries.clear()
        
        if not self.decision_log_path.exists():
            return
        
        text = self.decision_log_path.read_text(encoding="utf-8")
        self._entries = self._parse_entries(text)
    
    def _parse_entries(self, text: str) -> List[DecisionEntry]:
        """Parse decision log entries from markdown text."""
        entries = []
        
        # Split by entry separators (### headers)
        entry_pattern = re.compile(r'^### (\d{4}-\d{2}-\d{2}): (.+)$', re.MULTILINE)
        matches = list(entry_pattern.finditer(text))
        
        for i, match in enumerate(matches):
            start_pos = match.start()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            entry_text = text[start_pos:end_pos]
            
            entry = self._parse_single_entry(entry_text, i + 1)
            if entry:
                entries.append(entry)
        
        return entries
    
    def _parse_single_entry(self, text: str, entry_number: int) -> Optional[DecisionEntry]:
        """Parse a single decision log entry."""
        # Extract date from header
        date_match = re.search(r'^### (\d{4}-\d{2}-\d{2}):', text, re.MULTILINE)
        if not date_match:
            return None
        
        try:
            date = datetime.strptime(date_match.group(1), "%Y-%m-%d")
        except ValueError:
            return None
        
        # Extract fields
        decision = self._extract_field(text, "Decision:")
        trigger = self._extract_field(text, "Trigger:")
        rationale = self._extract_field(text, "Rationale:")
        tradeoffs = self._extract_field(text, "Tradeoffs:")
        expected_impact = self._extract_field(text, "Expected Impact:")
        review_date_str = self._extract_field(text, "Review Date:")
        actual_impact = self._extract_field(text, "Actual Impact:")
        related_rules_str = self._extract_field(text, "Related Rules:")
        tags_str = self._extract_field(text, "Tags:")
        
        # Parse review date
        review_date = None
        if review_date_str and review_date_str != "N/A":
            try:
                review_date = datetime.strptime(review_date_str.strip(), "%Y-%m-%d")
            except ValueError:
                pass
        
        # Parse related rules
        related_rules = set()
        if related_rules_str:
            # Extract rule IDs like [LIL-XXX-YYY-0001]
            rule_id_pattern = re.compile(r'\[LIL-[^\]]+\]')
            related_rules = set(rule_id_pattern.findall(related_rules_str))
        
        # Parse tags
        tags = set()
        if tags_str:
            tags = {tag.strip() for tag in tags_str.split(",")}
        
        return DecisionEntry(
            date=date,
            decision=decision or "",
            trigger=trigger or "",
            rationale=rationale or "",
            tradeoffs=tradeoffs or "",
            expected_impact=expected_impact or "",
            review_date=review_date,
            entry_number=entry_number,
            related_rules=related_rules,
            tags=tags,
            actual_impact=actual_impact,
        )
    
    def _extract_field(self, text: str, field_name: str) -> Optional[str]:
        """Extract a field value from decision log text."""
        pattern = re.compile(rf'^{re.escape(field_name)}\s+(.+)$', re.MULTILINE)
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
        return None
    
    def add_entry(
        self,
        decision: str,
        trigger: str,
        rationale: str,
        tradeoffs: str,
        expected_impact: str,
        review_date: Optional[datetime] = None,
        related_rules: Optional[Set[str]] = None,
        tags: Optional[Set[str]] = None,
    ) -> DecisionEntry:
        """
        Add a new decision log entry.
        
        Args:
            decision: The decision made
            trigger: What triggered this decision
            rationale: Why this decision was made
            tradeoffs: What tradeoffs were considered
            expected_impact: Expected impact of this decision
            review_date: Optional review date
            related_rules: Set of rule IDs related to this decision
            tags: Custom tags for categorization
        
        Returns:
            The created DecisionEntry
        """
        entry = DecisionEntry(
            date=datetime.now(),
            decision=decision,
            trigger=trigger,
            rationale=rationale,
            tradeoffs=tradeoffs,
            expected_impact=expected_impact,
            review_date=review_date,
            entry_number=len(self._entries) + 1,
            related_rules=related_rules or set(),
            tags=tags or set(),
        )
        
        self._entries.append(entry)
        self._save_entries()
        return entry
    
    def _save_entries(self) -> None:
        """Save all entries to the decision log file."""
        # Ensure directory exists
        self.decision_log_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Build markdown content
        lines = [
            "# Decision Log (v1.0)",
            "",
            "## Purpose",
            "Records intent-level decisions that alter meaning, authority, or trajectory. Prevents silent drift.",
            "",
            "## What Belongs Here",
            "Required:",
            "- changes governed by GOVERNANCE.md",
            "- emergency overrides",
            "- automation expansions",
            "- metric changes / success-criteria shifts",
            "",
            "Not required:",
            "- bug fixes, refactors, style changes",
            "",
            "## Required Fields",
            "Each entry MUST include:",
            "- Date:",
            "- Decision:",
            "- Trigger:",
            "- Rationale:",
            "- Tradeoffs:",
            "- Expected Impact:",
            "- Review Date: (recommended; optional if N/A)",
            "",
            "---",
            "",
            "## Entries",
            "",
            "<!-- Actual decision log entries go below this line -->",
            "",
        ]
        
        # Add entries
        for entry in sorted(self._entries, key=lambda e: e.date, reverse=True):
            lines.append(entry.to_markdown())
            lines.append("---")
            lines.append("")
        
        # Write to file
        self.decision_log_path.write_text("\n".join(lines), encoding="utf-8")
    
    def get_entry(self, entry_number: int) -> Optional[DecisionEntry]:
        """Get a decision entry by number."""
        for entry in self._entries:
            if entry.entry_number == entry_number:
                return entry
        return None
    
    def get_all_entries(self) -> List[DecisionEntry]:
        """Get all decision entries."""
        return list(self._entries)
    
    def search(self, query: str) -> List[DecisionEntry]:
        """
        Search decision entries by text query.
        
        Args:
            query: Search query (searches in decision, trigger, rationale, tradeoffs, expected_impact)
        
        Returns:
            List of matching entries
        """
        query_lower = query.lower()
        results = []
        
        for entry in self._entries:
            searchable_text = " ".join([
                entry.decision,
                entry.trigger,
                entry.rationale,
                entry.tradeoffs,
                entry.expected_impact,
            ]).lower()
            
            if query_lower in searchable_text:
                results.append(entry)
        
        return results
    
    def filter_by_date_range(
        self, start_date: datetime, end_date: datetime
    ) -> List[DecisionEntry]:
        """Filter entries by date range."""
        return [
            entry
            for entry in self._entries
            if start_date <= entry.date <= end_date
        ]
    
    def filter_by_tag(self, tag: str) -> List[DecisionEntry]:
        """Filter entries by tag."""
        return [entry for entry in self._entries if tag in entry.tags]
    
    def filter_by_rule(self, rule_id: str) -> List[DecisionEntry]:
        """Filter entries related to a specific rule."""
        return [entry for entry in self._entries if rule_id in entry.related_rules]
    
    def get_entries_needing_review(self) -> List[DecisionEntry]:
        """Get entries that have a review date in the past or today."""
        today = datetime.now().date()
        return [
            entry
            for entry in self._entries
            if entry.review_date
            and entry.review_date.date() <= today
            and not entry.actual_impact  # Not yet reviewed
        ]
    
    def update_actual_impact(self, entry_number: int, actual_impact: str) -> bool:
        """
        Update the actual impact of a decision entry after review.
        
        Args:
            entry_number: Entry number to update
            actual_impact: Actual impact observed
        
        Returns:
            True if entry was found and updated, False otherwise
        """
        entry = self.get_entry(entry_number)
        if not entry:
            return False
        
        entry.actual_impact = actual_impact
        self._save_entries()
        return True
    
    def get_impact_analytics(self) -> Dict[str, any]:
        """
        Get analytics about decision impacts.
        
        Returns:
            Dictionary with analytics including:
            - total_entries: Total number of entries
            - entries_with_review: Number of entries that have been reviewed
            - entries_needing_review: Number of entries needing review
            - most_common_tags: Most common tags
            - most_referenced_rules: Most referenced rules
        """
        total = len(self._entries)
        reviewed = sum(1 for e in self._entries if e.actual_impact)
        needing_review = len(self.get_entries_needing_review())
        
        # Count tags
        tag_counts: Dict[str, int] = {}
        for entry in self._entries:
            for tag in entry.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        
        # Count rule references
        rule_counts: Dict[str, int] = {}
        for entry in self._entries:
            for rule_id in entry.related_rules:
                rule_counts[rule_id] = rule_counts.get(rule_id, 0) + 1
        
        return {
            "total_entries": total,
            "entries_with_review": reviewed,
            "entries_needing_review": needing_review,
            "most_common_tags": sorted(
                tag_counts.items(), key=lambda x: x[1], reverse=True
            )[:10],
            "most_referenced_rules": sorted(
                rule_counts.items(), key=lambda x: x[1], reverse=True
            )[:10],
        }
    
    def refresh(self) -> None:
        """Reload entries from file (useful after file changes)."""
        self._load_entries()
