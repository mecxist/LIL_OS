#!/usr/bin/env python3
"""Tests for signal collectors."""

import tempfile
from pathlib import Path
from lil_os_ml.signals import GitSignalCollector, ReportSignalCollector, SignalStorage


def test_git_signal_collector():
    """Test GitSignalCollector."""
    collector = GitSignalCollector()
    # Should not raise even if not in git repo
    signals = collector.collect(limit=10)
    assert isinstance(signals, list)


def test_report_signal_collector():
    """Test ReportSignalCollector."""
    with tempfile.TemporaryDirectory() as tmpdir:
        reports_dir = Path(tmpdir) / "reports"
        reports_dir.mkdir()
        
        collector = ReportSignalCollector(reports_dir)
        signals = collector.collect()
        assert isinstance(signals, list)


def test_signal_storage():
    """Test SignalStorage."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = Path(tmpdir) / "signals.db"
        storage = SignalStorage(db_path)
        
        from lil_os_ml.signals.collector import Signal
        from datetime import datetime
        
        signal = Signal(
            timestamp=datetime.utcnow().isoformat() + "Z",
            source="test",
            signal_type="test",
            data={"key": "value"}
        )
        
        signal_id = storage.save_signal(signal)
        assert signal_id > 0
        
        signals = storage.get_signals(source="test")
        assert len(signals) == 1
        assert signals[0].data["key"] == "value"
