#!/usr/bin/env python3
"""
Report Signal Collector

Collects signals from validation reports in .lil_os/reports/
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any, Optional

from .collector import SignalCollector, Signal


class ReportSignalCollector(SignalCollector):
    """Collects signals from validation reports."""
    
    def __init__(self, reports_dir: Optional[Path] = None):
        """
        Initialize report signal collector.
        
        Args:
            reports_dir: Path to reports directory (default: .lil_os/reports/)
        """
        super().__init__("reports")
        self.reports_dir = reports_dir or Path(".lil_os/reports")
    
    def collect(self, limit: Optional[int] = None, **kwargs) -> List[Signal]:
        """
        Collect signals from validation reports.
        
        Args:
            limit: Maximum number of reports to process
            **kwargs: Additional arguments (ignored)
            
        Returns:
            List of report signals
        """
        if not self.reports_dir.exists():
            return []
        
        signals = []
        report_files = sorted(
            self.reports_dir.glob("*_report.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        if limit:
            report_files = report_files[:limit]
        
        for report_file in report_files:
            try:
                with open(report_file, "r", encoding="utf-8") as f:
                    report_data = json.load(f)
                
                signal_data = {
                    "check_name": report_data.get("check_name", "unknown"),
                    "status": report_data.get("status", "unknown"),
                    "summary": report_data.get("summary", {}),
                    "findings_count": len(report_data.get("findings", [])),
                    "timing": report_data.get("timing", {}),
                    "git_commit": report_data.get("git_commit"),
                }
                
                metadata = {
                    "report_file": str(report_file),
                    "timestamp": report_data.get("timestamp"),
                }
                
                signals.append(self._create_signal(
                    "validation_report",
                    signal_data,
                    metadata=metadata
                ))
            except Exception:
                # Skip corrupted files
                continue
        
        return signals
