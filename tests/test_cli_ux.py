#!/usr/bin/env python3
"""Tests for CLI UX components."""

import pytest
from lil_os.cli_ux import RichPanel, RichTable, InteractivePrompt, is_rich_available


def test_rich_panel():
    """Test RichPanel creation."""
    panel = RichPanel(
        title="Test Panel",
        content=["Line 1", "Line 2"]
    )
    assert panel.title == "Test Panel"
    assert len(panel.content) == 2


def test_rich_table():
    """Test RichTable creation."""
    table = RichTable(
        title="Test Table",
        columns=["Col1", "Col2"],
        rows=[["A", "B"], ["C", "D"]]
    )
    assert table.title == "Test Table"
    assert len(table.columns) == 2
    assert len(table.rows) == 2


def test_is_rich_available():
    """Test Rich availability check."""
    # Should not raise
    result = is_rich_available()
    assert isinstance(result, bool)
