"""
LIL OS² Core: Rule Management

Enhanced rule management with lifecycle tracking, dependencies, and impact analysis.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set


class RuleLifecycle(Enum):
    """Rule lifecycle states."""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    REMOVED = "removed"


@dataclass
class Rule:
    """Represents a governance rule with enhanced metadata."""
    rule_id: str
    text: str
    file_path: Path
    line_number: int
    normative_keyword: str
    lifecycle: RuleLifecycle = RuleLifecycle.ACTIVE
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    deprecated_at: Optional[datetime] = None
    dependencies: Set[str] = field(default_factory=set)  # Rule IDs this depends on
    dependents: Set[str] = field(default_factory=set)  # Rule IDs that depend on this
    impact_scope: Optional[str] = None  # What this rule impacts (e.g., "validation", "automation")
    
    def extract_subject(self) -> str:
        """Extract the subject of a rule (what the rule is about)."""
        text = self.text
        # Remove rule ID
        text = re.sub(r'\[LIL-[^\]]+\]', '', text)
        # Remove normative keywords
        for keyword in ["MUST NOT", "MUST", "SHOULD NOT", "SHOULD", "MAY"]:
            text = text.replace(keyword, '')
        # Normalize
        text = re.sub(r'\s+', ' ', text).strip().lower()
        text = text.strip('.,;:')
        return text


class RuleManager:
    """
    Manages governance rules with lifecycle tracking, dependencies, and impact analysis.
    """
    
    def __init__(self, project_root: Optional[Path] = None):
        """
        Initialize rule manager.
        
        Args:
            project_root: Root directory of the project (defaults to current directory)
        """
        self.project_root = project_root or Path.cwd()
        self._rules: Dict[str, Rule] = {}
        self._rule_id_pattern = re.compile(
            r'\[LIL-(MR|GOV|CB|RT|WF|QL|SEC|DATA|API|PERF|CR)-'
            r'(BOUNDARY|AUTH|PROCESS|SAFETY|SCOPE|FORMAT|BUDGET|LOG|RESET)-\d{4}\]'
        )
        self._normative_keywords = ["MUST NOT", "MUST", "SHOULD NOT", "SHOULD", "MAY"]
        self._load_rules()
    
    def _load_rules(self) -> None:
        """Load all rules from governance files."""
        self._rules.clear()
        rule_files = self._get_rule_files()
        
        for rule_file in rule_files:
            if not rule_file.exists():
                continue
            
            text = rule_file.read_text(encoding="utf-8")
            for line_num, line in enumerate(text.splitlines(), start=1):
                rule = self._parse_rule_line(line, rule_file, line_num)
                if rule:
                    self._rules[rule.rule_id] = rule
        
        # Build dependency graph
        self._build_dependency_graph()
    
    def _get_rule_files(self) -> List[Path]:
        """Get list of governance files that may contain rules."""
        base = self.project_root
        return [
            base / "docs" / "MASTER_RULES.md",
            base / "docs" / "GOVERNANCE.md",
            base / "docs" / "RESET_TRIGGERS.md",
            base / "docs" / "CONTEXT_BUDGET.md",
            base / ".cursorrules",
        ]
    
    def _parse_rule_line(self, line: str, file_path: Path, line_number: int) -> Optional[Rule]:
        """Parse a single line to extract a rule if present."""
        rule_id_match = self._rule_id_pattern.search(line)
        if not rule_id_match:
            return None
        
        rule_id = rule_id_match.group(0)
        
        # Find normative keyword
        normative_keyword = None
        for keyword in self._normative_keywords:
            if keyword in line.upper():
                normative_keyword = keyword
                break
        
        if not normative_keyword:
            return None
        
        # Check if rule is deprecated
        lifecycle = RuleLifecycle.ACTIVE
        if "(DEPRECATED)" in line.upper() or "[DEPRECATED]" in line.upper():
            lifecycle = RuleLifecycle.DEPRECATED
        
        return Rule(
            rule_id=rule_id,
            text=line.strip(),
            file_path=file_path,
            line_number=line_number,
            normative_keyword=normative_keyword,
            lifecycle=lifecycle,
            created_at=datetime.now(),  # TODO: Extract from git history or decision log
        )
    
    def _build_dependency_graph(self) -> None:
        """Build dependency graph by analyzing rule references."""
        for rule_id, rule in self._rules.items():
            # Look for references to other rules in the rule text
            referenced_rules = self._rule_id_pattern.findall(rule.text)
            for ref_match in self._rule_id_pattern.finditer(rule.text):
                ref_id = ref_match.group(0)
                if ref_id != rule_id and ref_id in self._rules:
                    rule.dependencies.add(ref_id)
                    self._rules[ref_id].dependents.add(rule_id)
    
    def get_rule(self, rule_id: str) -> Optional[Rule]:
        """Get a rule by ID."""
        return self._rules.get(rule_id)
    
    def get_all_rules(self) -> List[Rule]:
        """Get all rules."""
        return list(self._rules.values())
    
    def get_rules_by_file(self, file_path: Path) -> List[Rule]:
        """Get all rules from a specific file."""
        return [r for r in self._rules.values() if r.file_path == file_path]
    
    def get_rules_by_lifecycle(self, lifecycle: RuleLifecycle) -> List[Rule]:
        """Get all rules with a specific lifecycle state."""
        return [r for r in self._rules.values() if r.lifecycle == lifecycle]
    
    def get_rule_dependencies(self, rule_id: str) -> List[Rule]:
        """Get all rules that a rule depends on."""
        rule = self._rules.get(rule_id)
        if not rule:
            return []
        return [self._rules[dep_id] for dep_id in rule.dependencies if dep_id in self._rules]
    
    def get_rule_dependents(self, rule_id: str) -> List[Rule]:
        """Get all rules that depend on a rule."""
        rule = self._rules.get(rule_id)
        if not rule:
            return []
        return [self._rules[dep_id] for dep_id in rule.dependents if dep_id in self._rules]
    
    def analyze_rule_impact(self, rule_id: str) -> Dict[str, any]:
        """
        Analyze the impact of a rule change.
        
        Returns:
            Dictionary with impact analysis including:
            - direct_dependents: Rules that directly depend on this rule
            - transitive_dependents: Rules that transitively depend on this rule
            - affected_files: Files that would be affected
            - estimated_impact: Estimated impact level (low, medium, high)
        """
        rule = self._rules.get(rule_id)
        if not rule:
            return {}
        
        direct_dependents = list(rule.dependents)
        transitive_dependents = set()
        
        # Find transitive dependents
        visited = {rule_id}
        queue = list(rule.dependents)
        while queue:
            dep_id = queue.pop(0)
            if dep_id in visited:
                continue
            visited.add(dep_id)
            if dep_id in self._rules:
                transitive_dependents.add(dep_id)
                queue.extend(self._rules[dep_id].dependents)
        
        affected_files = {rule.file_path}
        for dep_id in direct_dependents:
            if dep_id in self._rules:
                affected_files.add(self._rules[dep_id].file_path)
        
        # Estimate impact
        total_affected = len(direct_dependents) + len(transitive_dependents)
        if total_affected == 0:
            impact_level = "low"
        elif total_affected < 5:
            impact_level = "medium"
        else:
            impact_level = "high"
        
        return {
            "rule_id": rule_id,
            "direct_dependents": direct_dependents,
            "transitive_dependents": list(transitive_dependents),
            "affected_files": list(affected_files),
            "estimated_impact": impact_level,
            "total_affected_rules": total_affected,
        }
    
    def refresh(self) -> None:
        """Reload rules from files (useful after file changes)."""
        self._load_rules()
    
    def find_contradictions(self) -> List[Dict[str, any]]:
        """
        Find potential rule contradictions.
        
        Returns:
            List of contradiction findings with rule pairs and explanations.
        """
        contradictions = []
        rules = list(self._rules.values())
        
        # Simple pattern-based contradiction detection
        # Enhanced ML-based detection will be in the ML module
        for i, rule1 in enumerate(rules):
            for rule2 in rules[i+1:]:
                if self._check_contradiction(rule1, rule2):
                    contradictions.append({
                        "rule1": rule1.rule_id,
                        "rule2": rule2.rule_id,
                        "rule1_text": rule1.text,
                        "rule2_text": rule2.text,
                        "confidence": "medium",  # Pattern-based, not semantic
                        "explanation": f"Potential contradiction between {rule1.rule_id} and {rule2.rule_id}",
                    })
        
        return contradictions
    
    def _check_contradiction(self, rule1: Rule, rule2: Rule) -> bool:
        """Check if two rules contradict each other (basic pattern matching)."""
        # Extract subjects
        subject1 = rule1.extract_subject()
        subject2 = rule2.extract_subject()
        
        # Simple check: if subjects are similar but normative keywords conflict
        if subject1 == subject2:
            # Check for conflicting keywords
            must_keywords = {"MUST", "MUST NOT"}
            should_keywords = {"SHOULD", "SHOULD NOT"}
            
            kw1 = rule1.normative_keyword
            kw2 = rule2.normative_keyword
            
            # MUST vs MUST NOT on same subject = contradiction
            if kw1 in must_keywords and kw2 in must_keywords and kw1 != kw2:
                return True
        
        return False
