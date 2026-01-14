#!/usr/bin/env python3
"""
LIL OS² ML Data Extractor

Extracts features from git history and validation reports for drift detection.
"""

from __future__ import annotations

import subprocess
import json
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
from collections import defaultdict

from .schema import FeatureSet, GitFeatures, ValidationFeatures, GovernanceFeatures


class GitExtractor:
    """Extract features from git history."""
    
    def __init__(self, repo_path: Optional[Path] = None):
        """
        Initialize git extractor.
        
        Args:
            repo_path: Path to git repository (default: current directory)
        """
        self.repo_path = repo_path or Path.cwd()
    
    def get_commits_since(self, days: int) -> List[Dict[str, Any]]:
        """
        Get commits from the last N days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of commit dictionaries with keys: hash, date, author, message, files
        """
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        
        try:
            # Get commit log with file changes
            result = subprocess.run(
                [
                    "git", "log",
                    f"--since={since_date}",
                    "--pretty=format:%H|%ai|%an|%s",
                    "--name-only",
                    "--no-merges"
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return []
        
        commits = []
        lines = result.stdout.strip().split("\n")
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            if not line:
                i += 1
                continue
            
            # Parse commit header
            if "|" in line:
                parts = line.split("|", 3)
                if len(parts) >= 4:
                    commit_hash, date_str, author, message = parts
                    
                    # Get files changed
                    files = []
                    i += 1
                    while i < len(lines) and lines[i].strip() and "|" not in lines[i]:
                        files.append(lines[i].strip())
                        i += 1
                    
                    commits.append({
                        "hash": commit_hash,
                        "date": date_str,
                        "author": author,
                        "message": message,
                        "files": files
                    })
                    continue
            i += 1
        
        return commits
    
    def is_governance_file(self, file_path: str) -> bool:
        """Check if a file is a governance file."""
        governance_patterns = [
            "docs/GOVERNANCE.md",
            "docs/RULE_IDS.md",
            "docs/MASTER_RULES.md",
            "docs/CONTEXT_BUDGET.md",
            "docs/RESET_TRIGGERS.md",
            "docs/DECISION_LOG.md",
            ".cursorrules",
        ]
        return any(file_path.endswith(pattern) or pattern in file_path for pattern in governance_patterns)
    
    def is_ai_agent_commit(self, commit: Dict[str, Any]) -> bool:
        """Detect if commit is from an AI agent."""
        # Simple heuristics - can be enhanced
        author = commit.get("author", "").lower()
        message = commit.get("message", "").lower()
        
        ai_indicators = [
            "ai",
            "assistant",
            "copilot",
            "cursor",
            "claude",
            "gpt",
            "automatic",
            "auto-",
        ]
        
        return any(indicator in author or indicator in message for indicator in ai_indicators)
    
    def extract_git_features(self, days: int = 30) -> GitFeatures:
        """
        Extract git features for the last N days.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            GitFeatures object
        """
        commits_30d = self.get_commits_since(days)
        commits_7d = [c for c in commits_30d 
                     if (datetime.now() - datetime.fromisoformat(c["date"].replace(" ", "T").split("+")[0])).days <= 7]
        
        # Count governance file touches
        governance_touches = set()
        rule_changes = 0
        decision_log_entries = 0
        
        for commit in commits_30d:
            for file_path in commit.get("files", []):
                if self.is_governance_file(file_path):
                    governance_touches.add(file_path)
                    if "RULE" in file_path.upper() or "RULE_IDS" in file_path:
                        rule_changes += 1
                    if "DECISION_LOG" in file_path.upper():
                        decision_log_entries += 1
        
        # Calculate AI agent commit ratio
        ai_commits = sum(1 for c in commits_30d if self.is_ai_agent_commit(c))
        ai_ratio = ai_commits / len(commits_30d) if commits_30d else 0.0
        
        # Calculate average files per commit
        total_files = sum(len(c.get("files", [])) for c in commits_30d)
        avg_files = total_files / len(commits_30d) if commits_30d else 0.0
        
        return GitFeatures(
            commits_last_7d=len(commits_7d),
            commits_last_30d=len(commits_30d),
            governance_files_touched=len(governance_touches),
            rule_changes=rule_changes,
            decision_log_entries=decision_log_entries,
            ai_agent_commits_ratio=ai_ratio,
            avg_files_per_commit=avg_files,
        )


class ReportExtractor:
    """Extract features from validation reports."""
    
    def __init__(self, reports_dir: Optional[Path] = None):
        """
        Initialize report extractor.
        
        Args:
            reports_dir: Directory containing validation reports (default: .lil_os/reports)
        """
        self.reports_dir = reports_dir or Path(".lil_os/reports")
    
    def get_reports_since(self, days: int) -> List[Dict[str, Any]]:
        """
        Get validation reports from the last N days.
        
        Args:
            days: Number of days to look back
            
        Returns:
            List of report dictionaries
        """
        if not self.reports_dir.exists():
            return []
        
        cutoff_date = datetime.now() - timedelta(days=days)
        reports = []
        
        for report_file in self.reports_dir.glob("*.json"):
            try:
                # Parse timestamp from filename (format: YYYY-MM-DD_HH-MM-SS_checkname_report.json)
                parts = report_file.stem.split("_")
                if len(parts) >= 3:
                    date_str = f"{parts[0]}_{parts[1]}"
                    report_date = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
                    
                    if report_date >= cutoff_date:
                        report_data = json.loads(report_file.read_text(encoding="utf-8"))
                        report_data["_file_path"] = str(report_file)
                        report_data["_date"] = report_date
                        reports.append(report_data)
            except Exception:
                # Skip corrupted files
                continue
        
        return sorted(reports, key=lambda r: r.get("_date", datetime.min), reverse=True)
    
    def extract_validation_features(self, days: int = 7) -> ValidationFeatures:
        """
        Extract validation features for the last N days.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            ValidationFeatures object
        """
        reports = self.get_reports_since(days)
        
        if not reports:
            return ValidationFeatures()
        
        # Calculate metrics
        total_findings = 0
        hard_fails = 0
        warnings = 0
        total_time = 0.0
        passed = 0
        
        for report in reports:
            summary = report.get("summary", {})
            total_findings += summary.get("total", 0)
            hard_fails += summary.get("hard_fails", 0)
            warnings += summary.get("warnings", 0)
            
            timing = report.get("timing", {})
            total_time += timing.get("elapsed_seconds", 0.0)
            
            if report.get("status") == "pass":
                passed += 1
        
        pass_rate = passed / len(reports) if reports else 0.0
        avg_findings = total_findings / len(reports) if reports else 0.0
        avg_time = total_time / len(reports) if reports else 0.0
        
        return ValidationFeatures(
            validation_runs_last_7d=len(reports),
            pass_rate_7d=pass_rate,
            avg_findings_per_run=avg_findings,
            hard_fails_7d=hard_fails,
            warnings_7d=warnings,
            avg_validation_time_seconds=avg_time,
        )


class GovernanceExtractor:
    """Extract features from governance files."""
    
    def __init__(self, repo_path: Optional[Path] = None):
        """
        Initialize governance extractor.
        
        Args:
            repo_path: Path to repository (default: current directory)
        """
        self.repo_path = repo_path or Path.cwd()
    
    def extract_governance_features(self, days: int = 30) -> GovernanceFeatures:
        """
        Extract governance features for the last N days.
        
        Args:
            days: Number of days to analyze
            
        Returns:
            GovernanceFeatures object
        """
        # TODO: Implement actual governance file parsing
        # For now, return defaults
        # This would need to:
        # - Parse RULE_IDS.md to count rules added/removed
        # - Parse CONTEXT_BUDGET.md to get utilization
        # - Check reset trigger activation history
        
        return GovernanceFeatures(
            rules_added_30d=0,
            rules_removed_30d=0,
            context_budget_utilization=0.0,
            reset_triggers_activated_30d=0,
        )


class FeatureExtractor:
    """Main feature extractor combining all sources."""
    
    def __init__(
        self,
        repo_path: Optional[Path] = None,
        reports_dir: Optional[Path] = None
    ):
        """
        Initialize feature extractor.
        
        Args:
            repo_path: Path to git repository
            reports_dir: Directory containing validation reports
        """
        self.git_extractor = GitExtractor(repo_path)
        self.report_extractor = ReportExtractor(reports_dir)
        self.gov_extractor = GovernanceExtractor(repo_path)
    
    def extract_features(self) -> FeatureSet:
        """
        Extract complete feature set for current state.
        
        Returns:
            FeatureSet object
        """
        git_features = self.git_extractor.extract_git_features(days=30)
        validation_features = self.report_extractor.extract_validation_features(days=7)
        governance_features = self.gov_extractor.extract_governance_features(days=30)
        
        return FeatureSet(
            timestamp=datetime.utcnow().isoformat() + "Z",
            git_features=git_features,
            validation_features=validation_features,
            governance_features=governance_features,
        )
