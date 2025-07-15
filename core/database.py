"""
Database module for Neuro_Sync, providing an interface to interact with the underlying data storage.
This module defines the core data structures and enums used throughout the application.
"""
import json
from dataclasses import dataclass, field # This import is neccessary for tasks and other structure definitions
from datetime import datetime, timedelta
from enum import Enum
import sqlite3
from typing import Optional, List, Dict, Any
import uuid
from pathlib import Path
from contextlib import contextmanager # This import is important in managing database connections

from ..config.database_config import (
    DatabaseConfig,
    get_raw_connection,
    Tables,
    QueryConfig,
    SchemaConfig,
)
from .models import Task, Habit, User, FinanceRecord, Achievement, XPEntry

#DATABASE SCHEMA
SCHEMA_SQL = """
--Users table
CREATE TABLE IF NOT EXISTS users (
    id TEST PRIMARY KEY,
    name TEST NOT NULL,
    email TEXT
    timezone TEXT NOT NULL,
    created_at TEXT NOT NULL,
    lat_active TEXT NOT NULL,
    );   
    
--Tasks table 
CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY, 
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    due_date TEXT,
    status TEST NOT NULL DEFAULT 'pending'
    priority TEXT NOT NULL DEFAULT 'medium'
    due_dat TEXT,
    created_at TEXT NOT NULL,
    estimated_duration INTEGER,
    actual_duration INTEGER,
    complete_at TEXT,
    );

--Habits table
CREATE TABLE IF NOT EXISTS habits (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    frequency TEXT NOT NULL,
    start_date TEXT NOT NULL,
    end_date TEXT,
    target_streak INTEGER NOT NULL DEFAULT 0, 
    current_streak INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
    last_completed TEXT,
);

-- Finance table
CREATE TABLE IF NOT EXISTS finance_entries (
    id TEXT PRIMARY KEY,
    user_id TEXT_NOT NULL,
    amount REAL NOT NULL,
    category TEXT NOT NULL,
    transaction_date TEXT NOT NULL,
    description TEXT,
    source TEXT NOT NULL DEFAULT '',
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    note TEXT DEFAULT ''
    is_recurring BOOLEAN NOT NULL DEFAULT FALSE
    tags TEXT DEFAULT '[]'  
);

-- XP Entried table (
CREATE TABLE IF NOT EXISTS xp_entries (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    amount INTEGER NOT NULL,
    source TEXT NOT NULL,
    points INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);

--Achievements table 
CREATE TABLE IF NOT EXISTS achievements(
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    points INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    unlocked BOOLEAN NOT NULL DEFAULT FALSE
);

-- App state table (for system settings and configurations)
CREATE TABLE IF NOT EXISTS app_state (
    key TEXT PRIMARY KEY,
    value TEXT,
    applied_at TEXT NOT NULL
);

-- Schema version table
CREATE TABLE IF NOT EXISTS schema_version (
    verison INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);

--AI cache table (for caching AI responses
CREATE TABLE IF NOT EXISTS ai_cache (
    id TEXT PRIMARY KEY,
    cache_key TEXT NOT NULL UNIQUE,
    response_data TEXT NOT NULL,
    created_at TEXT NOT NULL,
    expires_at TEXT NOT NULL

);
"""

#DATABASE CONNECTION MANAGEMENT
class Database:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DatabaseConfig.DATABASE_PATH
        self.ensure_database_exists()

    def ensure_database_exists(self):
        # Create database and tables if they do not exist
        if not self.db_path.parent.exists():
            self.db_path.parent.mkdir(parents=True, exist_ok=True)

        with self.get_connection() as conn:
            # Create all tables
            conn.executescript(SCHEMA_SQL)

            #Create indexes for performance
            for index_sql in QueryConfig.INDEXES:
                conn.execute(index_sql)

            #Set schema version
            self._set_schema_version(conn, SchemaConfig.CURRENT_VERSION)

            conn.commit()
    
    @contextmanager
    def get_connection(self):
        """ Get databse connection with proper cleanup"""
        conn = get_raw_connection()
        try:
            yield conn
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()