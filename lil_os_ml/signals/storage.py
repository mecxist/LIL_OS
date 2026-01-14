#!/usr/bin/env python3
"""
Signal Storage - SQLite-based storage for signals.
"""

from __future__ import annotations

import sqlite3
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from .collector import Signal


class SignalStorage:
    """SQLite storage for signals."""
    
    SCHEMA_VERSION = 1
    
    def __init__(self, db_path: Path):
        """
        Initialize signal storage.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create signals table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS signals (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                source TEXT NOT NULL,
                signal_type TEXT NOT NULL,
                data TEXT NOT NULL,
                metadata TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Create indexes
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp ON signals(timestamp)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_source ON signals(source)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_signal_type ON signals(signal_type)
        """)
        
        # Create schema version table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # Check schema version
        cursor.execute("SELECT version FROM schema_version ORDER BY version DESC LIMIT 1")
        result = cursor.fetchone()
        if result is None:
            cursor.execute("INSERT INTO schema_version (version) VALUES (?)", (self.SCHEMA_VERSION,))
        
        conn.commit()
        conn.close()
    
    def save_signal(self, signal: Signal) -> int:
        """
        Save a signal to the database.
        
        Args:
            signal: Signal object to save
            
        Returns:
            ID of the saved signal
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO signals (timestamp, source, signal_type, data, metadata)
            VALUES (?, ?, ?, ?, ?)
        """, (
            signal.timestamp,
            signal.source,
            signal.signal_type,
            json.dumps(signal.data),
            json.dumps(signal.metadata) if signal.metadata else None
        ))
        
        signal_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return signal_id
    
    def save_signals(self, signals: List[Signal]) -> List[int]:
        """
        Save multiple signals to the database.
        
        Args:
            signals: List of Signal objects to save
            
        Returns:
            List of signal IDs
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        ids = []
        for signal in signals:
            cursor.execute("""
                INSERT INTO signals (timestamp, source, signal_type, data, metadata)
                VALUES (?, ?, ?, ?, ?)
            """, (
                signal.timestamp,
                signal.source,
                signal.signal_type,
                json.dumps(signal.data),
                json.dumps(signal.metadata) if signal.metadata else None
            ))
            ids.append(cursor.lastrowid)
        
        conn.commit()
        conn.close()
        
        return ids
    
    def get_signals(
        self,
        source: Optional[str] = None,
        signal_type: Optional[str] = None,
        limit: Optional[int] = None,
        since: Optional[str] = None
    ) -> List[Signal]:
        """
        Get signals from the database.
        
        Args:
            source: Filter by source name
            signal_type: Filter by signal type
            limit: Maximum number of signals to return
            since: ISO timestamp to filter signals after
            
        Returns:
            List of Signal objects
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT timestamp, source, signal_type, data, metadata FROM signals WHERE 1=1"
        params = []
        
        if source:
            query += " AND source = ?"
            params.append(source)
        
        if signal_type:
            query += " AND signal_type = ?"
            params.append(signal_type)
        
        if since:
            query += " AND timestamp >= ?"
            params.append(since)
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()
        
        signals = []
        for row in rows:
            signals.append(Signal(
                timestamp=row[0],
                source=row[1],
                signal_type=row[2],
                data=json.loads(row[3]),
                metadata=json.loads(row[4]) if row[4] else None
            ))
        
        return signals
    
    def get_signal_count(self, source: Optional[str] = None, signal_type: Optional[str] = None) -> int:
        """
        Get count of signals.
        
        Args:
            source: Filter by source name
            signal_type: Filter by signal type
            
        Returns:
            Number of signals
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        query = "SELECT COUNT(*) FROM signals WHERE 1=1"
        params = []
        
        if source:
            query += " AND source = ?"
            params.append(source)
        
        if signal_type:
            query += " AND signal_type = ?"
            params.append(signal_type)
        
        cursor.execute(query, params)
        count = cursor.fetchone()[0]
        conn.close()
        
        return count
